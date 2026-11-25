from pathlib import Path
from wenmode import Wenmode, MarkdownRenderer
from wenmode.nodes import Root, Heading

wen = Wenmode()

for s in sections(Path("./trash/en.md").read_text(encoding="utf-8")):
    print(s["level"], s["title"])
    print(s["text"])