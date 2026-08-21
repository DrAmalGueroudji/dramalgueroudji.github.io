#!/usr/bin/env python3
"""One-time/rerunnable generator: parses the curated BibTeX files of the CV
and emits HTML fragments (stdout) to paste into index.html.

Zero dependencies — a small state-machine BibTeX reader tuned to this corpus.
Usage: .venv/bin/python tools/generate_publications.py
"""

import re
from pathlib import Path

BIB_DIR = Path(__file__).resolve().parent.parent / (
    "CV_2026_08_Gueroudji_Amal/gueroudji-vita-2025/bibtex"
)

# (file, section-id, heading) — gueroudji_additions.bib deliberately excluded.
SOURCES = [
    ("gueroudji_journal-book.bib", "journal", "Journal Articles"),
    ("gueroudji_proceedings.bib", "proceedings", "Refereed Proceedings"),
    ("gueroudji_techreports.bib", "reports", "Technical Reports"),
    ("gueroudji_invited.bib", "invited", "Invited Talks"),
    ("gueroudji_presentations.bib", "seminars", "Presentations &amp; Seminars"),
    ("gueroudji_tutorials.bib", "tutorials", "Tutorials"),
]

# Entries whose bib author field is malformed (commas instead of "and").
AUTHOR_OVERRIDES = {
    "gueroudji:hpcdsl": (
        '<span class="self">A. Gueroudji</span>, R. Baghdadi, '
        "K. Benatchba, and S. Amarasinghe"
    ),
}

# Extra links per bib key: web pages that don't belong in the CV bib files
# (event programs, talk videos, profiles). label -> shown on the pill.
# Local files: files/papers/<bib-key>.<ext> -> "PDF" pill,
# files/slides/<bib-key>.<ext> -> "Slides" pill (see files/README.md).
LOCAL_DIRS = [("files/papers", "PDF"), ("files/slides", "Slides")]

EXTRA_LINKS = {
    # "bib-key": [("Video", "https://..."), ("Program", "https://...")],
    "nguyen2026streamguard": [("PDF", "https://arxiv.org/pdf/2606.30848")],
    "ockerman2026more": [("PDF", "https://arxiv.org/pdf/2606.08950")],
    "yang_2025_gets": [("PDF", "https://arxiv.org/pdf/2511.10687")],
    "lahiry_2025_distributed": [("PDF", "https://arxiv.org/pdf/2510.18300")],
    "lahiry2025scalable": [("PDF", "https://arxiv.org/pdf/2506.20674")],
    "da2024workflows": [("PDF", "https://arxiv.org/pdf/2410.14943")],
    "gueroudji2023dask": [("PDF", "https://hal.science/hal-04409157/document")],
    "gueroudji2021deisa": [("PDF", "https://hal.science/hal-03509198/document")],
    "grandgirard2022new": [("Slides", "https://cea.hal.science/cea-03740685/document")],
    "kumar2022efficient": [("SSRN", "https://ssrn.com/abstract=4288211")],
    "rao2025throughput": [("PDF", "https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=11514121")],
    "dorier2025toward": [("PDF", "https://www.frontiersin.org/journals/high-performance-computing/articles/10.3389/fhpcp.2025.1638203/pdf")],
    "yildis2023": [("PDF", "https://web.cels.anl.gov/~tpeterka/papers/2024/yildiz-fgcs24-paper.pdf")],
    "gueroudji_2026_federated": [("PDF", "https://hal.science/hal-05533387v1/file/Beyond%20Centralized%20Labs%20-%20Federating%20the%20Co-Scientist.pdf")],
    "sirvent_2025_reroducibility": [("PDF", "https://dl.acm.org/doi/pdf/10.1145/3736731.3746141")],
    "souza_2025_llm": [("PDF", "https://arxiv.org/pdf/2509.13978")],
    "ockerman_2025_exploring": [("PDF", "https://arxiv.org/pdf/2509.12384")],
    "souza_prov_2025": [("PDF", "https://arxiv.org/pdf/2508.02866")],
    "gueroudji_controla_2025": [("PDF", "https://rafaelsilva.com/files/publications/gueroudji2025ai4sc.pdf")],
    "ockerman_pgt_2025": [("PDF", "https://arxiv.org/pdf/2507.11683")],
    "carns_roofline_2025": [
        ("PDF", "https://cug.org/proceedings/cug2025_proceedings/includes/files/pap137s2-file1.pdf"),
        ("Slides", "https://cug.org/proceedings/cug2025_proceedings/includes/files/pap137s2-file2.pdf"),
    ],
    "Ockerman2025Efficient": [("Poster", "https://drive.google.com/file/d/1NRgnsOTjKSANJsTQjLM3KAx415V3UqRR/view")],
    "nicolae2024diaspora": [("PDF", "https://web.cels.anl.gov/~woz/papers/Diaspora_2024.pdf")],
    "gueroudji:perf": [("PDF", "https://www.osti.gov/servlets/purl/2588773")],
    "dorier:extending": [("PDF", "https://www.pdl.cmu.edu/ftp/HECStorage/ext-mochi_essa24.pdf")],
    "amal:dask-talk-2023": [("Video", "https://www.youtube.com/watch?v=dTsTkRD6rbY")],
    "amal:jlesc-talk-2023": [("Program", "https://events.hifis.net/event/617/timetable/?view=indico_weeks_view")],
    "gueroudji-talk-dask": [("Program", "https://sc23.conference-program.com/presentation/?id=ws_ipdrm101&sess=sess428")],
    "gueroudji-talk-compass": [("Program", "https://2021.compas-conference.fr/programme/")],
    "gueroudji-talk-hpcda": [("Event", "https://hpcda.github.io/author/amal-gueroudji/")],
    "amal:per3s-talk-2022": [("Program", "https://per3s.github.io/per3s.2022/")],
    "gueroudji-talk-mcs-2025": [("Event", "https://www.anl.gov/event/stability-in-motion-performance-characterization-resilience-and-trustworthy-contemporary-workflows")],
    "gueroudji-talk-resilio": [("Program", "https://workflows.community/workshops/works-2025/")],
    "gueroudji-talk-controla": [("Event", "https://www.escience-conference.org/2025/")],
    "gueroudji-talk-multicore-2025": [("Video", "https://www.youtube.com/watch?v=RdLJEGVcExw")],
    "amal:mcore-talk-2025": [("Video", "https://www.youtube.com/watch?v=RdLJEGVcExw")],
    "gueroudji-talk-perf": [("Program", "https://works-workshop.org/2024/")],
    "tut:escience:prov": [("Program", "https://www.escience-conference.org/2025/tutorials")],
    "amal:IEEE-talk-2026": [("Program", "https://wieils.ieee.org/2026-usa/program/speakers/")],
    "amal:mcore-talk-2026": [("Event", "https://multicore.world/multicore-world-2026/")],
    "gueroudji-talk-APS-2026": [("Program", "https://www.aps.anl.gov/APS-Seminars-Training-Schools-Etc/APS-Scientific-Computation-Seminar-Series/2026")],
    "gueroudji-talk-jlesc-2026": [("Event", "https://jlesc.github.io/events/18th-jlesc-workshop/")],
    "gueroudji-talk-multicore-2026": [("Program", "https://multicore.world/speakers-2026/amal-gueroudji/")],
    "gueroudji-talk-HPCA-2026": [("Program", "https://acx-2026.cels.anl.gov/schedule/")],
}

MONTHS = {
    "jan": "Jan", "feb": "Feb", "mar": "Mar", "apr": "Apr", "may": "May",
    "jun": "Jun", "jul": "Jul", "aug": "Aug", "sep": "Sep", "oct": "Oct",
    "nov": "Nov", "dec": "Dec",
}

LATEX_REPL = [
    ("\\&", "&amp;"), ("\\'{e}", "é"), ("\\'e", "é"), ('\\"{e}', "ë"),
    ("\\`{e}", "è"), ("\\`e", "è"), ("\\'{a}", "á"), ("\\`{a}", "à"),
    ("\\`a", "à"), ("\\^{o}", "ô"), ("\\c{c}", "ç"), ('\\"{u}', "ü"),
    ('\\"u', "ü"), ('\\"{o}', "ö"), ('\\"o', "ö"), ("\\'{i}", "í"),
    ("\\'{\\i}", "í"), ("\\l{}", "ł"), ("\\l ", "ł"), ("\\l", "ł"),
    ("\\k{a}", "ą"), ("\\'{c}", "ć"), ("\\'c", "ć"), ("\\'{o}", "ó"),
    ("\\'o", "ó"), ("~", " "), ("---", "—"), ("--", "–"),
    ("\\emph", ""), ("\\textit", ""), ("\\textbf", ""), ("\\it ", ""),
    ("\\ ", " "), ("$", ""),
]


def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("\\url", "")
    for a, b in LATEX_REPL:
        s = s.replace(a, b)
    s = s.replace("{", "").replace("}", "")
    s = s.strip().rstrip(",")
    # known typo in gueroudji_presentations.bib
    if s.startswith("he 1st Annual"):
        s = "T" + s
    return s.strip()


def parse_bib(path):
    """Parse a .bib file into a list of dicts (entry type + fields)."""
    text = path.read_text(encoding="utf-8")
    # strip comment lines
    text = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("%"))
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{", text):
        etype = m.group(1).lower()
        if etype in ("comment", "string", "preamble"):
            continue
        # walk braces to find the entry body
        depth, i = 1, m.end()
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[m.end():i - 1]
        key, _, rest = body.partition(",")
        fields = {"_type": etype, "_key": key.strip()}
        # field = {value} | "value" | bareword
        j = 0
        while j < len(rest):
            fm = re.compile(r"(\w+)\s*=\s*", re.S).search(rest, j)
            if not fm:
                break
            name = fm.group(1).lower()
            k = fm.end()
            if k < len(rest) and rest[k] == "{":
                depth, k2 = 1, k + 1
                while k2 < len(rest) and depth:
                    if rest[k2] == "{":
                        depth += 1
                    elif rest[k2] == "}":
                        depth -= 1
                    k2 += 1
                val = rest[k + 1:k2 - 1]
                j = k2
            elif k < len(rest) and rest[k] == '"':
                k2 = rest.find('"', k + 1)
                val = rest[k + 1:k2]
                j = k2 + 1
            else:
                k2 = rest.find(",", k)
                if k2 == -1:
                    k2 = len(rest)
                val = rest[k:k2]
                j = k2
            fields[name] = clean(val)
        entries.append(fields)
    return entries


def initials(given):
    parts = re.split(r"[\s.]+", given.strip())
    return " ".join(p[0] + "." for p in parts if p)


def format_authors(raw):
    """'Last, First and ...' or 'First Last and ...' -> 'F. Last, F. Last, and F. Last'
    with Gueroudji emphasized."""
    if not raw:
        return ""
    names = re.split(r"\s+and\s+", raw)
    out = []
    for n in names:
        n = n.strip()
        if n.lower() == "others":
            out.append("et al.")
            continue
        if "," in n:
            last, _, given = n.partition(",")
            last, given = last.strip(), given.strip()
        else:
            bits = n.split()
            last, given = bits[-1], " ".join(bits[:-1])
        disp = (initials(given) + " " + last) if given else last
        if "gueroudji" in last.lower():
            disp = f'<span class="self">{disp}</span>'
        out.append(disp)
    if len(out) == 1:
        return out[0]
    if out[-1] == "et al.":
        return ", ".join(out[:-1]) + ", et al."
    return ", ".join(out[:-1]) + (", and " if len(out) > 2 else " and ") + out[-1]


def links_html(e):
    links = []
    doi = e.get("doi", "")
    url = e.get("url", "")
    if doi:
        d = doi if doi.startswith("http") else "https://doi.org/" + doi
        links.append(f'<a class="pub-link" href="{d}">DOI</a>')
    if url and (not doi or url not in (doi, "https://doi.org/" + doi)):
        label = "arXiv" if "arxiv" in url.lower() else ("PDF" if url.lower().endswith(".pdf") else "Link")
        links.append(f'<a class="pub-link" href="{url}">{label}</a>')
    for label, href in EXTRA_LINKS.get(e["_key"], []):
        links.append(f'<a class="pub-link" href="{href.replace("&", "&amp;")}">{label}</a>')
    root = Path(__file__).resolve().parent.parent
    for dirname, label in LOCAL_DIRS:
        for f in sorted((root / dirname).glob(e["_key"] + ".*")):
            links.append(f'<a class="pub-link" href="{dirname}/{f.name}">{label}</a>')
    return "".join(links)


def venue_of(e):
    for f in ("journal", "booktitle", "publisher", "howpublished", "institution", "note"):
        v = e.get(f)
        if v and v.lower() != "invited":
            return v
    return ""


def trim_authors(html_authors):
    """Cap very long author lists (consortium papers) at 8 names + et al.,
    keeping the highlighted self-name visible."""
    parts = html_authors.split(", ")
    if len(parts) <= 12:
        return html_authors
    kept = parts[:8]
    if not any("self" in p for p in kept):
        kept.append(next(p for p in parts if "self" in p))
    return ", ".join(kept) + ", et al."


def entry_html(e, kind):
    year = e.get("year", "")
    month = MONTHS.get(e.get("month", "").lower()[:3], "")
    date = f"{month} {year}" if month else year
    title = e.get("title", "")
    authors = AUTHOR_OVERRIDES.get(e["_key"]) or trim_authors(
        format_authors(e.get("author", ""))
    )
    venue = venue_of(e)
    extras = []
    if e.get("volume"):
        v = e["volume"]
        if e.get("number"):
            v += f"({e['number']})"
        if e.get("pages"):
            v += f":{e['pages']}"
        extras.append(v)
    elif e.get("pages"):
        extras.append("pp. " + e["pages"])
    if e.get("address"):
        extras.append(e["address"])
    extra = (", " + ", ".join(extras)) if extras else ""
    meta = f'<span class="pub-venue">{venue}</span>{extra}' if venue else extra.lstrip(", ")
    lines = [f'          <li class="pub" data-year="{year}">']
    if authors:
        lines.append(f'            <span class="pub-authors">{authors}</span>')
    lines.append(f'            <span class="pub-title">{title}</span>')
    if meta:
        lines.append(f'            <span class="pub-meta">{meta}, {date}.</span>')
    else:
        lines.append(f'            <span class="pub-meta">{date}.</span>')
    lk = links_html(e)
    if lk:
        lines.append(f'            <span class="pub-links">{lk}</span>')
    lines.append("          </li>")
    return "\n".join(lines)


def render_list(fname, sid):
    entries = parse_bib(BIB_DIR / fname)
    entries.sort(key=lambda e: (-int(e.get("year", "0") or 0)))
    lines = [f'<ol class="pub-list" reversed id="list-{sid}">']
    lines += [entry_html(e, sid) for e in entries]
    lines.append("</ol>")
    return "\n".join(lines), len(entries)


def main():
    """Regenerate every <!-- GEN:list-x START/END --> block found in the site pages."""
    root = Path(__file__).resolve().parent.parent
    blocks = {}
    for fname, sid, heading in SOURCES:
        html, n = render_list(fname, sid)
        blocks[f"list-{sid}"] = html
        print(f"{heading}: {n} entries ({fname})")

    for page in sorted(root.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        changed = False
        for name, html in blocks.items():
            pat = re.compile(
                rf"(<!-- GEN:{name} START -->).*?(<!-- GEN:{name} END -->)", re.S
            )
            if pat.search(text):
                text = pat.sub(rf"\g<1>\n{html}\n\g<2>", text)
                changed = True
        if changed:
            page.write_text(text, encoding="utf-8")
            print(f"updated {page.name}")


if __name__ == "__main__":
    main()
