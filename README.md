# amal-gueroudji.github.io

Personal academic website of **Amal Gueroudji** — Assistant Computer Scientist,
Mathematics and Computer Science Division, Argonne National Laboratory.

Static HTML, no build step, no framework, no dependencies. Published with
GitHub Pages.

## Pages

| File | Contents |
| --- | --- |
| `index.html` | Landing page — hero, research summary, selected work, contact |
| `research.html` | Research directions and projects |
| `publications.html` | Full publication list, grouped by venue type |
| `talks.html` | Invited talks, presentations, tutorials |
| `about.html` | Biography, appointments, service, honors |

## Layout

```
assets/          favicon and images (photo, city shots)
css/style.css    the entire theme — single stylesheet
js/main.js       progressive enhancement only (see below)
files/           optional local PDFs linked from publications/talks
tools/           BibTeX → HTML generator for the publication lists
.nojekyll        tells GitHub Pages to serve the tree as-is
```

**Design:** dark editorial palette (`--bg: #0c1116`) with teal (`#3fbfb2`) and
gold (`#d4a95a`) accents; Fraunces for display type, Inter for text. All colour
and type tokens are CSS custom properties at the top of `css/style.css`.

**JavaScript is optional.** `js/main.js` (92 lines) adds the mobile nav toggle,
scroll-reveal animations, count-up stats, and year de-duplication in the
publication lists. Every page is fully readable with JS disabled.

## Local preview

No server is strictly required — opening `index.html` works. To match the
deployed paths:

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

## Regenerating the publication lists

The entries on `publications.html` and `talks.html` come from the curated
BibTeX files of the CV. The generator prints HTML fragments on stdout, which
are then pasted into the relevant page — it does not rewrite the pages itself:

```bash
python3 tools/generate_publications.py   # emits HTML fragments on stdout
```

The generator is zero-dependency (a small state-machine BibTeX reader). It
reads from `CV_2026_08_Gueroudji_Amal/gueroudji-vita-2025/bibtex/`, which is
**git-ignored** — the raw CV sources are kept out of the public repo, so the
generator only runs in a local checkout that has them.

To attach a local PDF to an entry, drop it at `files/papers/<bib-key>.pdf` or
`files/slides/<bib-key>.pdf` and re-run the generator; see `files/README.md`.

## Deploying

```bash
git add -A && git commit -m "..."
git push
```

GitHub Pages serves `main` from the repository root. Note that this repo is a
*project* page, so the site lives at
`https://DrAmalGueroudji.github.io/amal-gueroudji.github.io/`. All internal
links are relative, so the subpath works. Renaming the repository to
`DrAmalGueroudji.github.io` — an exact match for the account name — would make
it a user page served from the root URL, with no content changes needed.

## Previous version

An earlier Flask + Jinja2 implementation of this site is archived in `old/`
(git-ignored). It is no longer used.

## License

[MIT](LICENSE).
