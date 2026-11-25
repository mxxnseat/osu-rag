"""Parse English osu! wiki articles into headings and the Markdown under them.

Requires: pip install wenmode pyyaml
Usage:    python osu_wiki.py path/to/osu-wiki [output.jsonl]
"""
import json
import re
import sys
from pathlib import Path

from fastapi_injectable import get_injected_obj
import yaml
from wenmode import Wenmode
from wenmode.nodes import Heading
from wenmode.presets import github

from app.dtos.faq import AddFaqBody
from app.services.faq import get_faq_service

from .objects import Article, Section

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)^---[ \t]*\n", re.S | re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

ANCHOR_RE = re.compile(r"\s*\{#[^}]*\}$")  # custom anchors: "Title {#id}"

WEN = Wenmode(github(), positions=True)

def text_of(node) -> str:
    """Plain text of a node, without formatting."""
    if hasattr(node, "value"):
        return node.value
    return "".join(text_of(c) for c in getattr(node, "children", []))


def parse_sections(body: str) -> list[Section]:
    headings = [n for n in WEN.parse(body).children if isinstance(n, Heading)]
    # character offsets of the lines each heading occupies
    spans = [(n.position.start, n.position.end) for n in headings]
    starts = [start for start, _ in spans] + [len(body)]

    def clean(chunk: str) -> str:
        return COMMENT_RE.sub("", chunk).strip()

    sections = []
    intro = clean(body[:starts[0]])
    if intro:
        sections.append(Section(0, "intro", [], intro))

    stack: list[tuple[int, str]] = []
    for node, (_, end), next_start in zip(headings, spans, starts[1:]):
        title = ANCHOR_RE.sub("", text_of(node).strip())
        while stack and stack[-1][0] >= node.depth:
            stack.pop()
        stack.append((node.depth, title))
        sections.append(Section(
            node.depth, title, [t for _, t in stack], clean(body[end:next_start])
        ))
    return sections


def parse_article(file: Path, wiki_dir: Path) -> Article:
    source = file.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    meta = {}
    if match := FRONTMATTER_RE.match(source):
        meta = yaml.safe_load(match[1]) or {}
        source = source[match.end():]

    sections = parse_sections(source)
    title = next((s.title for s in sections if s.level == 1), "???????????")
    return Article(file.parent.relative_to(wiki_dir).as_posix(), title, meta, sections)


def parse_wiki(repo: Path):
    wiki_dir = repo / "wiki"
    if not wiki_dir.is_dir():
        raise SystemExit(f"No 'wiki' folder in {repo}")
    for file in sorted(wiki_dir.rglob("en.md")):
        yield parse_article(file, wiki_dir)

def content_splitter(content: str, max_length: int = 1000, overlap: int = 100) -> list[str]:
    if not 0 <= overlap < max_length:
        raise ValueError("overlap must be >= 0 and smaller than max_length")

    chunks = []
    ind = 0

    while ind < len(content):
        end = ind + max_length

        # The rest fits into one chunk
        if end >= len(content):
            chunks.append(content[ind:])
            break

        # Prefer to cut at a paragraph, then a line, then a word
        for sep in ("\n\n", "\n", " "):
            # Searching from ind + overlap guarantees we always move forward
            pos = content.rfind(sep, ind + overlap, end)
            if pos != -1:
                end = pos + len(sep)
                break
        # If no separator is found, `end` stays as a hard cut by length

        chunks.append(content[ind:end])
        ind = end - overlap

    return chunks

def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    faq_service = get_injected_obj(get_faq_service)
    for article in parse_wiki(Path(sys.argv[1])):
        for section in article.sections:
            for chunk_ind, content in enumerate(content_splitter(section.text)):
                payload = AddFaqBody(
                    content=content,
                    title=section.title,
                    section="",
                    path=section.path,
                    chunk_index=chunk_ind
                )
                faq_service.add(payload)

if __name__ == "__main__":
    main()
