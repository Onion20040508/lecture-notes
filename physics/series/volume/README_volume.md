# Series Volume — build system

Binds the four standalone documents into one PDF **without touching their
sources**. Each Part reproduces its document's internal numbering exactly
(sections, equations, figures, theorem environments all reset per Part),
so the plain-text citation registers "[Mech. §3.2]", "[Fld. Remark 2.7]"
remain literally accurate inside the volume.

## Layout
- `build_volume.py` — extracts each document's body, namespaces its labels
  (`osc:`, `mech:`, `fld:`, `qm:`), demotes internal `\part` to numbered
  inner parts (so "[Mech. Part II]" still reads correctly), switches
  `\appendix` to a per-Part variant, and writes `build/master.tex`.
- `check_crossrefs.py` — manifest generator + citation checker. Validates
  every bracket citation against the *current* numbering of its target
  (sections, subsections, appendices, inner Parts, and theorem-environment
  numbers like "Remark 2.7" / "Conv. 1.1"). Run it after ANY change to a
  document's section structure; `build.sh` runs it automatically and
  refuses to build on drift.
- `build.sh` — check → assemble → pdflatex ×2.

## Adding QFT / GR later
One entry in `PARTS` in `build_volume.py` (prefix, tex path, part title),
plus its figure directory in `FIG_DIRS`, plus a citation prefix in
`check_crossrefs.py`'s `DOCS`. The standalone document needs the same
conventions as the others (per-section shared theorem counter); nothing
else.

## Known design decisions
- Convention breaks at Part boundaries are intentional and stated in the
  volume preface (e.g. the summation convention arrives only in Part III).
- Standalone docs continue to compile unchanged; the volume build is a
  pure derivation from them.
