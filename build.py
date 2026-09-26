"""Build the ePortfolio: content/*.md -> docs/*.html with one shared template.

Each content file starts with a small header block:
    title: About Me
    nav: About
    eyebrow: A — About Me
    description: One line for search/social previews.
    ---
followed by Markdown. Run:  python3 build.py
"""
import datetime
import pathlib
import shutil
import subprocess

import markdown

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "docs"

# (file stem, output name) in navigation order
PAGES = [
    ("index", "index.html"),
    ("about", "about.html"),
    ("career", "career.html"),
    ("goals", "goals.html"),
    ("reflections", "reflections.html"),
    ("projects", "projects.html"),
]

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

NAME = "Thinh Tran"
EMAIL = "thinhvt99@gmail.com"

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body class="page-{stem}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="wordmark" href="index.html">Thinh Tran<span class="wordmark-sub">ePortfolio</span></a>
    <nav aria-label="Main">
      <ul class="nav">
{nav}
      </ul>
    </nav>
  </div>
</header>
<main id="main" class="wrap">
{eyebrow}
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-row">
    <p><strong>{name}</strong> · <a href="mailto:{email}">{email}</a></p>
    <p class="updated">Last updated {updated}</p>
    <p><a class="home-link" href="index.html">&larr; Home</a></p>
  </div>
</footer>
</body>
</html>
"""


def parse(path):
    """Split a content file into its header fields and Markdown body."""
    head, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = {}
    for line in head.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def build():
    updated = datetime.date.today().strftime("%B %-d, %Y")
    pages = [(stem, out, *parse(CONTENT / f"{stem}.md")) for stem, out in PAGES]

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    for stem, out, meta, body in pages:
        nav_items = []
        for _, o, m, _ in pages:
            current = ' aria-current="page"' if o == out else ""
            nav_items.append(f'        <li><a href="{o}"{current}>{m["nav"]}</a></li>')
        nav = "\n".join(nav_items)
        html_body = markdown.markdown(body, extensions=["tables", "attr_list", "md_in_html", "toc"])
        eyebrow = f'<p class="eyebrow">{meta["eyebrow"]}</p>' if meta.get("eyebrow") else ""
        title = NAME + " — ePortfolio" if stem == "index" else f'{meta["title"]} — {NAME}'
        (OUT / out).write_text(TEMPLATE.format(
            title=title, description=meta["description"], stem=stem, nav=nav,
            eyebrow=eyebrow, body=html_body, name=NAME, email=EMAIL, updated=updated,
        ), encoding="utf-8")

    shutil.copy(ROOT / "style.css", OUT / "style.css")
    (OUT / ".nojekyll").write_text("")  # serve files as-is on GitHub Pages

    # The PDF resume is the Career page printed with its print stylesheet, so the two never drift.
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=5000",
         f"--print-to-pdf={OUT / 'resume.pdf'}", (OUT / "career.html").as_uri()],
        check=True, capture_output=True,
    )
    print(f"built {len(pages)} pages -> {OUT} (last updated {updated})")


if __name__ == "__main__":
    build()
