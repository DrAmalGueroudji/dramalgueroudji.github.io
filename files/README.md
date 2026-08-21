# Local files (papers & slides)

Drop files here to have them linked automatically from the website:

- `files/papers/<bib-key>.pdf` → adds a **PDF** button on that publication
- `files/slides/<bib-key>.pdf` → adds a **Slides** button on that publication or talk

`<bib-key>` is the BibTeX entry key from the CV bib files, e.g.

- `files/papers/gueroudji2021deisa.pdf` (the DEISA HiPC'21 paper)
- `files/slides/gueroudji-talk-multicore-2025.pdf` (the Multicore World 2025 talk)

To list all keys:

    grep -h '^@' CV_2026_08_Gueroudji_Amal/gueroudji-vita-2025/bibtex/*.bib

After adding files, regenerate the pages:

    .venv/bin/python tools/generate_publications.py

A local file is added *in addition to* any external DOI/arXiv/Video links.
Anything other than `.pdf` works too (`.pptx`, `.key`, `.html`) — the link
uses whatever extension the file has.
