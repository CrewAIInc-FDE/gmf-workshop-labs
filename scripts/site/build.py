#!/usr/bin/env python3
"""Deterministic builder for the workshop teaching site (slides + speaker notes).

  site/index.md                 -> _site/index.html
  site/<module>/slides.md       -> _site/<module>/index.html        (slides page)
                                -> _site/<module>/notes/index.html  (speaker notes; not linked, noindex)
  site/<module>/assets/*        -> _site/<module>/assets/*

Slide syntax is documented in scripts/site/README.md.

Run locally:
  uv run --with markdown --with pymdown-extensions --with pygments python scripts/site/build.py
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
import string
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

REPO = Path(__file__).resolve().parents[2]
SRC_DIR = REPO / "site"
OUT_DIR = REPO / "_site"
HERE = Path(__file__).parent
TEMPLATE = HERE / "template.html"
NOTES_TEMPLATE = HERE / "notes.html"
STYLE = HERE / "style.css"
ASSETS = HERE / "assets"

MD_EXTENSIONS = [
    "tables",
    "pymdownx.superfences",
    "pymdownx.highlight",
    "toc",
    "sane_lists",
    "md_in_html",
    "attr_list",
    "pymdownx.tasklist",
    "pymdownx.tilde",
]
MD_CONFIG = {
    "pymdownx.highlight": {"guess_lang": False, "css_class": "codehilite", "use_pygments": True, "pygments_lang_class": True},
    "toc": {"permalink": "¶", "permalink_class": "headerlink", "permalink_title": "Link to this section"},
    "pymdownx.tasklist": {"custom_checkbox": False},
}

DIRECTIVES = {"slide", "idea", "image", "source", "notes", "time"}
IMAGE_EXTS = {".svg", ".png", ".jpg", ".jpeg", ".webp"}
TIME_RE = re.compile(r"^([01]?\d|2[0-3]):[0-5]\d$")
MAX_BULLETS = 5


class BuildError(Exception):
    pass


@dataclass
class Slide:
    n: int = 0
    title: str = ""
    idea: str = ""
    image: str = ""
    alt: str = ""
    bullets: list[str] = field(default_factory=list)
    source: str = ""
    notes_md: str = ""
    time: str = ""
    line: int = 0


# --------------------------------------------------------------------------
# slides.md parsing
# --------------------------------------------------------------------------

def parse_slides(path: Path) -> tuple[str, str, list[Slide]]:
    """Return (module title, intro markdown, slides). Raises BuildError with file:line."""
    rel = path.relative_to(REPO)
    title = ""
    intro: list[str] = []
    slides: list[Slide] = []
    notes: list[str] = []
    cur: Slide | None = None
    state = "intro"  # intro | slide | notes
    fence = False

    def err(lineno: int, msg: str) -> BuildError:
        return BuildError(f"{rel}:{lineno}: {msg}")

    def finish() -> None:
        nonlocal notes
        if cur is not None:
            cur.notes_md = "\n".join(notes).strip("\n")
            notes = []

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        stripped = line.strip()

        if state in ("intro", "notes") and stripped.startswith(("```", "~~~")):
            fence = not fence
        if fence or (state in ("intro", "notes") and stripped.startswith(("```", "~~~"))):
            (notes if state == "notes" else intro).append(line)
            continue

        m = re.match(r"^@([A-Za-z-]+)\b\s*(.*)$", line)
        if m:
            name, arg = m.group(1).lower(), m.group(2).strip()
            if name not in DIRECTIVES:
                raise err(lineno, f"unknown directive @{name} (known: {', '.join('@' + d for d in sorted(DIRECTIVES))})")
            if name == "slide":
                finish()
                if not arg:
                    raise err(lineno, "@slide needs a title: '@slide Why agents need constraints'")
                cur = Slide(n=len(slides) + 1, title=arg, line=lineno)
                slides.append(cur)
                state = "slide"
                continue
            if cur is None:
                raise err(lineno, f"@{name} before the first @slide")
            if name == "notes":
                if state == "notes":
                    raise err(lineno, "second @notes in one slide")
                state = "notes"
                if arg:
                    notes.append(arg)
                continue
            if name == "time":
                if state != "notes":
                    raise err(lineno, "@time belongs inside the notes (after @notes)")
                if cur.time:
                    raise err(lineno, "second @time in one slide")
                if not TIME_RE.match(arg):
                    raise err(lineno, f"@time needs 24-hour H:MM, like '@time 9:42' or '@time 13:30' (got '{arg}')")
                cur.time = arg
                continue
            # slide-body directives
            if state == "notes":
                raise err(lineno, f"@{name} must come before @notes")
            if name == "idea":
                if cur.idea:
                    raise err(lineno, "one idea per slide: second @idea")
                if not arg:
                    raise err(lineno, "@idea is empty")
                cur.idea = arg
            elif name == "source":
                if cur.source:
                    raise err(lineno, "second @source")
                cur.source = arg
            elif name == "image":
                if cur.image:
                    raise err(lineno, "one image per slide: second @image")
                if "|" not in arg:
                    raise err(lineno, "@image needs alt text: '@image assets/diagram.svg | What the picture shows'")
                img, alt = (p.strip() for p in arg.split("|", 1))
                if not alt:
                    raise err(lineno, f"@image {img} has empty alt text. Alt text is required.")
                if Path(img).suffix.lower() not in IMAGE_EXTS:
                    raise err(lineno, f"@image {img}: use one of {', '.join(sorted(IMAGE_EXTS))}")
                target = (path.parent / img).resolve()
                if not str(target).startswith(str(path.parent.resolve())) or not target.is_file():
                    raise err(lineno, f"@image {img}: file not found under {path.parent.relative_to(REPO)}/ (put images in assets/)")
                cur.image, cur.alt = img, alt
            continue

        if state == "intro":
            m1 = re.match(r"^# (.+)$", line)
            if m1 and not title and not fence:
                title = re.sub(r"[*_`]", "", m1.group(1)).strip()
            else:
                intro.append(line)
        elif state == "notes":
            notes.append(line)
        else:  # slide body, before @notes
            if not stripped:
                continue
            b = re.match(r"^[-*]\s+(.+)$", stripped)
            if b:
                cur.bullets.append(b.group(1).strip())
                if len(cur.bullets) > MAX_BULLETS:
                    raise err(lineno, f"more than {MAX_BULLETS} bullets on one slide - split it, or move detail into the notes")
            else:
                raise err(lineno, "text on a slide must be an @idea, @image, @source, or a '- bullet'; put anything else under @notes")
    finish()
    if not title:
        raise BuildError(f"{rel}: missing '# Module title' line before the first @slide")
    return title, "\n".join(intro).strip("\n"), slides


def inline(text: str) -> str:
    """Inline markdown (code, bold, italics, links) with the wrapping <p> removed."""
    out = markdown.Markdown(extensions=[]).convert(text).strip()
    return re.sub(r"^<p>(.*)</p>$", r"\1", out, flags=re.S)


def slide_html(s: Slide, total: int, img_prefix: str, uid: str, tag: str = "h2") -> str:
    classes = ["slide"]
    if s.image:
        classes.append("has-image")
    if s.bullets:
        classes.append("has-bullets")
    parts = [f'<section class="{" ".join(classes)}" id="{uid}" aria-labelledby="{uid}-title" data-n="{s.n}">',
             '<div class="slide-inner">',
             f'<{tag} class="slide-title" id="{uid}-title">{inline(s.title)}</{tag}>']
    if s.idea:
        parts.append(f'<p class="slide-idea">{inline(s.idea)}</p>')
    if s.bullets or s.image:
        parts.append('<div class="slide-body">')
        if s.bullets:
            parts.append('<ul class="slide-bullets">' + "".join(f"<li>{inline(b)}</li>" for b in s.bullets) + "</ul>")
        if s.image:
            parts.append(f'<figure class="slide-media"><img src="{html.escape(img_prefix + s.image)}" '
                         f'alt="{html.escape(s.alt, quote=True)}"></figure>')
        parts.append("</div>")
    if s.source:
        parts.append(f'<p class="slide-source">Source: {inline(s.source)}</p>')
    parts.append("</div>")
    parts.append(f'<span class="slide-num" role="img" aria-label="Slide {s.n} of {total}">{s.n} / {total}</span>')
    parts.append("</section>")
    return "".join(parts)


def notes_cards(slides: list[Slide], img_prefix: str) -> str:
    total = len(slides)
    cards = []
    for s in slides:
        md = markdown.Markdown(extensions=["sane_lists", "pymdownx.superfences", "pymdownx.highlight"],
                               extension_configs={"pymdownx.highlight": {"guess_lang": False}})
        notes = md.convert(s.notes_md) if s.notes_md.strip() else '<p class="nnone">No notes for this slide.</p>'
        timing = (f'<p class="ntime">Should be here by {html.escape(s.time)}</p>' if s.time else "")
        preview = slide_html(s, total, img_prefix, f"p{s.n}", tag="div")
        cards.append(
            f'<article class="ncard" id="n-{s.n}" aria-labelledby="n-{s.n}-h">'
            f'<h2 id="n-{s.n}-h">Slide {s.n} of {total}: {inline(s.title)}</h2>'
            f'<div class="nrow"><div class="nmini" aria-hidden="true">{preview}</div>'
            f'<div class="nbody">{timing}{notes}</div></div></article>'
        )
    return "\n".join(cards)


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------

def collect_pages() -> dict[Path, Path]:
    pages: dict[Path, Path] = {Path("index.md"): Path("index.html")}
    for sl in sorted(SRC_DIR.glob("*/slides.md")):
        mod = sl.parent.name
        pages[Path(mod) / "slides.md"] = Path(mod) / "index.html"
    return pages


def rewrite_links(htm: str, src: Path, pages: dict[Path, Path]) -> str:
    def fix(match: re.Match) -> str:
        href = match.group(2)
        if re.match(r"^(https?:|mailto:|#|data:)", href):
            return match.group(0)
        target, _, frag = href.partition("#")
        frag = f"#{frag}" if frag else ""
        rel = Path(os.path.normpath(src.parent / target))
        if rel in pages:
            new = os.path.relpath(pages[rel], pages[src].parent)
            if new.endswith("index.html"):
                new = new[: -len("index.html")] or "./"
            return f"{match.group(1)}{new}{frag}{match.group(3)}"
        return match.group(0)

    return re.sub(r'(href=")([^"]+)(")', fix, htm)


def first_title(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return re.sub(r"[*_`]", "", line[2:]).strip()
    return "CrewAI Workshop"


def toc_html(md: "markdown.Markdown") -> str:
    tokens = getattr(md, "toc_tokens", [])
    if len(tokens) == 1 and tokens[0]["level"] == 1:
        tokens = tokens[0]["children"]
    if not tokens:
        return ""
    items = [f'<li><a href="#{tok["id"]}">{tok["name"]}</a></li>' for tok in tokens]
    return '<p class="toc-title">On this page</p>\n<ul>' + "".join(items) + "</ul>"


def json_script(obj) -> str:
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def main() -> int:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    template = string.Template(TEMPLATE.read_text(encoding="utf-8"))
    notes_template = string.Template(NOTES_TEMPLATE.read_text(encoding="utf-8"))
    cssver = hashlib.sha256(STYLE.read_bytes()).hexdigest()[:10]
    jsver = hashlib.sha256(b"".join((HERE / n).read_bytes() for n in ("deck.js", "notes.js"))).hexdigest()[:10]
    pages = collect_pages()

    try:
        commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True, check=True).stdout.strip()
        built = subprocess.run(["git", "-C", str(REPO), "show", "-s", "--format=%cs", "HEAD"],
                               capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit, built = "dev", "local"

    (OUT_DIR / "assets").mkdir()
    for f in ASSETS.iterdir():
        shutil.copy2(f, OUT_DIR / "assets" / f.name)
    shutil.copy2(STYLE, OUT_DIR / "style.css")
    shutil.copy2(HERE / "deck.js", OUT_DIR / "deck.js")
    shutil.copy2(HERE / "notes.js", OUT_DIR / "notes.js")
    (OUT_DIR / "pygments.css").write_text(
        ".codehilite { background: #161616; }\n" + HtmlFormatter(style="lightbulb").get_style_defs(".codehilite"),
        encoding="utf-8")

    # robots.txt is a hint only; the real control is <meta name="robots" content="noindex"> on every page.
    (OUT_DIR / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")

    # Module assets (images) and other non-md files
    for asset in SRC_DIR.rglob("*"):
        if not asset.is_file() or asset.suffix.lower() == ".md" or asset.name.startswith("."):
            continue
        dest = OUT_DIR / asset.relative_to(SRC_DIR)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(asset, dest)

    notes_count = 0
    for src, out in pages.items():
        depth = len(out.parent.parts)
        root = "/".join([".."] * depth) if depth else "."
        dest = OUT_DIR / out
        dest.parent.mkdir(parents=True, exist_ok=True)
        is_index = src == Path("index.md")
        crumb = "" if is_index else f'<p class="crumb"><a href="{root}/">&larr; The day</a></p>'
        common = dict(root=root, cssver=cssver, built=built, commit=commit, lang="en", crumb=crumb,
                      pagenav="", tocLabel="On this page", extra_scripts="", bodyclass="", layoutclass="")

        if is_index:
            md_text = (SRC_DIR / src).read_text(encoding="utf-8")
            md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
            body = rewrite_links(md.convert(md_text), src, pages)
            page = template.substitute(**{**common, "title": first_title(md_text), "content": body, "toc": ""})
            dest.write_text(page, encoding="utf-8")
            print(f"  site/{src} -> _site/{out}")
            continue

        title, intro_md, slides = parse_slides(SRC_DIR / src)
        total = len(slides)
        md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
        intro = rewrite_links(md.convert(intro_md), src, pages) if intro_md else ""
        content = f'<h1>{html.escape(title)}</h1>\n<div class="deck-intro">{intro}</div>'
        toc = ""
        extra = ""
        layoutclass = ""
        if total:
            cards = "\n".join(slide_html(s, total, "", f"slide-{s.n}") for s in slides)
            content += (
                '<div class="deck-bar">'
                '<button type="button" class="btn" id="present-btn">Present <kbd>P</kbd></button>'
                '<button type="button" class="btn alt" id="speaker-btn">Speaker view <kbd>S</kbd></button>'
                '<p class="deck-hint">Present mode: arrow keys, space, or PageUp/PageDown to move; type a number then Enter to jump; Esc to exit. '
                'Open the speaker view first, then present.</p></div>'
                f'<div class="deck" id="deck" data-module="{html.escape(out.parent.name)}" data-notes-url="notes/">\n{cards}\n</div>'
                '<div class="sr-only" id="live" aria-live="polite"></div>'
                '<div class="jump-hud" id="jump-hud" role="status" hidden></div>'
                '<button type="button" class="exit-present" id="exit-present">Exit (Esc)</button>'
            )
            items = "".join(
                f'<li><a href="#slide-{s.n}"><span class="slide-toc-n">{s.n}.</span>{inline(s.title)}</a></li>' for s in slides)
            toc = f'<p class="toc-title">Slides</p>\n<ul>{items}</ul>'
            extra = f'<script src="{root}/deck.js?v={jsver}"></script>'
            layoutclass = " wide"
        else:
            content += '<p><em>No slides in this module yet.</em></p>'

        page = template.substitute(**{**common, "title": title, "content": content, "toc": toc,
                                      "tocLabel": "Slides", "extra_scripts": extra, "layoutclass": layoutclass,
                                      "bodyclass": "page-deck"})
        dest.write_text(page, encoding="utf-8")
        print(f"  site/{src} -> _site/{out}  ({total} slides)")

        if total:
            nroot = f"{root}/.."
            data = {"module": out.parent.name, "title": title,
                    "slides": [{"n": s.n, "title": re.sub(r"[*_`]", "", s.title), "time": s.time or None} for s in slides]}
            npage = notes_template.substitute(
                title=html.escape(title), root=nroot, cssver=cssver, jsver=jsver, total=total,
                cards=notes_cards(slides, "../"), data=json_script(data))
            ndest = OUT_DIR / out.parent / "notes" / "index.html"
            ndest.parent.mkdir(parents=True, exist_ok=True)
            ndest.write_text(npage, encoding="utf-8")
            notes_count += 1
            print(f"  site/{src} -> _site/{out.parent}/notes/index.html")

    print(f"\nBuilt {len(pages)} pages and {notes_count} notes pages into {OUT_DIR.relative_to(REPO)}/")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as e:
        print(f"BUILD ERROR: {e}", file=sys.stderr)
        sys.exit(1)
