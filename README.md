# Thinh Tran — ePortfolio

The ePortfolio for LE/COOP 2100 (York University, Lassonde School of Engineering, Fall 2026).
A plain static site: the words live in `content/`, one Markdown file per page, and `build.py`
turns them into the HTML in `docs/`, which GitHub Pages serves.

## Update the site

```bash
python3 build.py     # content/*.md -> docs/*.html, and docs/resume.pdf from the Career page
python3 check.py     # must say PASS before anything is pushed
git add -A && git commit -m "Week N: <what changed>" && git push
```

`build.py` stamps every page's footer with today's date ("Last updated"), which the course
manual requires. `resume.pdf` is the Career page printed through its print stylesheet, so
the web resume and the PDF can never disagree.

## What `check.py` guards

1. Nothing private is published: phone number, home address and postal code are looked up
   from a private record outside this repository and searched for in every page and the PDF.
2. Every internal link and `#anchor` resolves, and every external link answers.
3. Every page carries the full navigation and the footer (name, email, last updated).
4. Words the system dictionary doesn't know are listed for a human read.

## Page structure (matches the course manual)

| File | Section |
|---|---|
| `content/index.md` | Home: purpose statement + table of contents |
| `content/about.md` | A — About Me |
| `content/career.md` | B — Career: education, experience, skills, resume |
| `content/goals.md` | C — Goals and Portfolios (Discover Myself) |
| `content/reflections.md` | D — Reflections (Retell, Relate, Reflect) |
| `content/projects.md` | E — Projects, each tagged with Lassonde competencies |

Each content file starts with a short header (`title`, `nav`, `eyebrow`, `description`) and a
`---` line; everything below it is Markdown.
