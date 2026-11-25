from dataclasses import dataclass


@dataclass
class Section:
    level: int         # 0 = text before the first heading
    title: str
    path: list[str]    # parent headings, ending with this one
    text: str          # original Markdown, without HTML comments


@dataclass
class Article:
    path: str          # e.g. "Beatmap/Difficulty"
    title: str  # first level-1 heading
    meta: dict         # front matter: tags, stub, outdated, ...
    sections: list[Section]
