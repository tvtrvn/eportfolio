"""Pre-publish checks for the built site. Run after build.py:  python3 check.py [docs_dir]

1. Do-not-publish: no phone number or home address anywhere in the HTML or the PDF resume.
   The forbidden values are read from the private career record at check time, so they are
   never written into this (public) repository.
2. Every internal link and #anchor resolves.
3. Every external link answers (LinkedIn blocks bots with 999 - listed for a manual check).
4. Every page has the full nav and the footer the course manual requires.
5. Spelling: words not in the system dictionary are listed for a human read.
Exits 1 if any of checks 1-4 fail.
"""
import html.parser
import pathlib
import re
import subprocess
import sys
import urllib.request

DOCS = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "docs")
PERSONAL = pathlib.Path.home() / "Desktop/WORKSPACE/JobSearch/career_truth/sections/01_personal.md"
PAGES = ["index.html", "about.html", "career.html", "goals.html", "reflections.html", "projects.html"]
ALLOWED_WORDS = set("""
thinh tran eportfolio york lassonde coop le bel groupe canada pho ginger gingercuisine aritzia
upnxxt riipen codesignal github linkedin netlify vercel mongodb prisma redis postgresql sqlite numpy
pandas fastapi playwright vitest pytest junit typescript javascript nextjs js expo tailwind css html
sql redux toolkit docker premiere adobe powerpoint sharepoint microsoft sku skus csrf pptx python
claude eecs peps swot sep dec jul jun mar apr tvtrvn vt sharpe tiingo api ai co ontario vietnamese
mississauga vaughan toronto thinhvt edtech workflow workflows onboarding sole storefront frameworks
gmail io md hmac lump dca www https com app ca org beta sim ui self serve portfoliosite sql
apps automation barcode database email endpoints online pdf screenshots startup walkthrough
weightlifting coursework multi honours centre gradle teammates didn
""".split())


class Collect(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.text, self._skip = [], set(), [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def forbidden_values():
    rows = PERSONAL.read_text(encoding="utf-8")
    phone = re.search(r"\| Phone \| ([^|]+) \|", rows).group(1).strip()
    address = re.search(r"\| Address \| ([^|]+) \|", rows).group(1).strip()
    street, postal = address.split(",")[0], address.split(",")[-1].split()[-2:]
    digits = re.sub(r"\D", "", phone)
    return {
        "phone": re.compile(r"\D{0,3}".join(digits)),          # "(647) 515-7345", "647.515.7345", ...
        "street address": re.compile(re.escape(street), re.I),
        "postal code": re.compile(r"\s?".join(map(re.escape, postal)), re.I),
    }


def main():
    failures, parsed = [], {}
    for name in PAGES:
        c = Collect()
        c.feed((DOCS / name).read_text(encoding="utf-8"))
        parsed[name] = c

    # 1. do-not-publish
    corpus = {name: (DOCS / name).read_text(encoding="utf-8") for name in PAGES}
    corpus["resume.pdf"] = subprocess.run(["pdftotext", str(DOCS / "resume.pdf"), "-"],
                                          capture_output=True, text=True, check=True).stdout
    for label, pattern in forbidden_values().items():
        for where, text in corpus.items():
            if pattern.search(text):
                failures.append(f"DO-NOT-PUBLISH: {label} found in {where}")

    # 2 + 3. links
    external = set()
    for name, c in parsed.items():
        for href in c.links:
            if href.startswith(("http://", "https://")):
                external.add(href)
            elif href.startswith("mailto:"):
                continue
            else:
                target, _, anchor = href.partition("#")
                target = target or name
                if not (DOCS / target).exists():
                    failures.append(f"BROKEN LINK: {name} -> {href}")
                elif anchor and target in parsed and anchor not in parsed[target].ids:
                    failures.append(f"BROKEN ANCHOR: {name} -> {href}")
    manual = []
    for url in sorted(external):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link check)"})
        try:
            code = urllib.request.urlopen(req, timeout=15).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:  # network error
            code = f"error: {e.__class__.__name__}"
        if code == 999:
            manual.append(url)
        elif code != 200:
            failures.append(f"EXTERNAL LINK {code}: {url}")

    # 4. structure the manual requires on every page
    for name, c in parsed.items():
        page = " ".join(c.text)
        for required in ("Thinh Tran", "thinhvt99@gmail.com", "Last updated"):
            if required not in page:
                failures.append(f"FOOTER: {name} is missing '{required}'")
        for target in PAGES:
            if target not in c.links:
                failures.append(f"NAV: {name} has no link to {target}")

    # 5. spelling candidates (advisory)
    dictionary = set(pathlib.Path("/usr/share/dict/words").read_text().lower().split())
    unknown = set()
    for c in parsed.values():
        for word in re.findall(r"[A-Za-z]+", " ".join(c.text)):
            w = word.lower()
            forms = {w, w[:-1], w[:-2], w[:-3], w[:-3] + "y", w[:-2] + "e", w[:-1] + "e", w[:-3] + "e"}
            forms |= {w[:-3] + "e" + "d"[:0], w[:-4]}  # -ing/-est on a doubled or silent-e stem
            if len(w) > 2 and w not in ALLOWED_WORDS and not (forms & dictionary):
                unknown.add(word)

    print(f"checked {len(PAGES)} pages + resume.pdf, {len(external)} external links")
    if manual:
        print("CHECK BY HAND (site blocks automated requests):", *manual, sep="\n  ")
    if unknown:
        print("SPELLING - not in dictionary, read these:", ", ".join(sorted(unknown, key=str.lower)))
    if failures:
        print("FAIL", *failures, sep="\n  ")
        sys.exit(1)
    print("PASS: nothing private published, all links resolve, every page has nav + footer")


if __name__ == "__main__":
    main()
