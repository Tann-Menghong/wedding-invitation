"""Render the dynamic Jinja2 template + content.json into the static docs/ site.

Keeps the GitHub Pages mirror (no backend) in sync with the live app's
content without hand-porting HTML/CSS/JS on every change.
"""
import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DOCS_DIR = BASE_DIR / "docs"

GITHUB_EDIT_URL = "https://github.com/tann-menghong/wedding-invitation/edit/main/data/content.json"

PATH_REWRITES = {
    "/static/uploads/": "./img/",
    "/static/css/": "./css/",
    "/static/js/": "./js/",
}


def load_json(path: Path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def build():
    content = load_json(DATA_DIR / "content.json") or {}
    gallery = load_json(DATA_DIR / "gallery.json") or []

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
    template = env.get_template("index.html")
    html = template.render(
        content=content,
        gallery=gallery,
        messages=[],
        guest_name=None,
        static_site=True,
        github_edit_url=GITHUB_EDIT_URL,
    )

    for old, new in PATH_REWRITES.items():
        html = html.replace(old, new)

    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")

    (DOCS_DIR / "css").mkdir(exist_ok=True)
    (DOCS_DIR / "js").mkdir(exist_ok=True)
    img_dir = DOCS_DIR / "img"
    img_dir.mkdir(exist_ok=True)

    shutil.copyfile(STATIC_DIR / "css" / "style.css", DOCS_DIR / "css" / "style.css")
    shutil.copyfile(STATIC_DIR / "js" / "main.js", DOCS_DIR / "js" / "main.js")

    uploads_dir = STATIC_DIR / "uploads"
    existing = {p.name for p in uploads_dir.iterdir()} if uploads_dir.exists() else set()
    for f in uploads_dir.iterdir() if uploads_dir.exists() else []:
        shutil.copyfile(f, img_dir / f.name)
    for stale in img_dir.iterdir():
        if stale.name not in existing:
            stale.unlink()


if __name__ == "__main__":
    build()
