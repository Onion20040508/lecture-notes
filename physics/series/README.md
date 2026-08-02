# Lecture Notes Series — Volumes I–IV

Self-contained lecture notes in theoretical physics, written as a single
progression: from the harmonic oscillator to quantum mechanics.

## Contents
- `lecture_notes_volumes_I-IV.pdf` — combined volume (221 pp), Parts I–IV with
  unified front matter; per-part numbering matches each standalone document exactly.
- `osc/`   Part I   — Oscillators: From One Spring to the Wave Equation (`ho_reference.tex/.pdf`, 40 pp)
- `mech/`  Part II  — Variational and Hamiltonian Mechanics (`variational_mechanics_course.tex/.pdf`, 54 pp)
- `fld/`   Part III — Special Relativity and Classical Field Theory (`relativity_field_theory.tex/.pdf`, 65 pp)
- `qm/`    Part IV  — Quantum Mechanics (`quantum_mechanics.tex/.pdf`, 63 pp)
- `volume/` build system: `bash build.sh` regenerates the combined volume
  (`build/master.pdf`) from the standalone sources without modifying them.

## Building
Each part compiles standalone with `pdflatex <file>.tex` (twice) in its own
directory. Figures (`fig_*.pdf`) sit alongside the sources with generator
scripts (`make_figures_*.py`) where applicable.

The combined volume namespaces all labels, preserves each Part's internal
numbering, and validates every cross-Part citation (`check_crossrefs.py`)
before building — see `volume/README_volume.md` for design notes.

Further Parts (quantum field theory, general relativity) are planned; the
build registry accepts a new Part as a single entry.
