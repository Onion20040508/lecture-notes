# Lecture Notes in Physics, Volumes I–IV

A self-contained lecture note series written as **one continuous argument**,
not four separate courses: normal modes of a mass chain become fields in the
continuum limit; Poisson brackets become commutators. Each seam between Parts
is built deliberately, and cross-Part references (`[Osc. §n]`, `[Mech. §n]`,
`[Fld. §n]`) are machine-checked against the sources.

**Read the combined volume:** [`lecture_notes_volumes_I-IV.pdf`](lecture_notes_volumes_I-IV.pdf) (221 pp)

| Part | Notes | Coverage |
|---|---|---|
| I — Oscillators: From One Spring to the Wave Equation (`osc/`) | 40 pp | Simple, damped, and forced harmonic motion; resonance; coupled oscillators and normal modes; the N-mass chain and its continuum limit into the wave equation |
| II — Variational and Hamiltonian Mechanics (`mech/`) | 54 pp | Calculus of variations; Lagrangian mechanics via the pendulum and double pendulum; Legendre transform and Hamilton's equations; Poisson brackets, phase space, canonical transformations, and Hamilton–Jacobi theory — with full proofs (fundamental lemma, covariance of Euler–Lagrange, Jacobi identity) in appendices |
| III — Special Relativity and Classical Field Theory (`fld/`) | 65 pp | The two postulates and Minkowski geometry; relativistic particles; from the mass chain to continuum fields; Klein–Gordon, Noether's theorem for fields, Hamiltonian field theory; the field tensor, the Maxwell Lagrangian, gauge freedom |
| IV — Quantum Mechanics (`qm/`) | 63 pp | Hilbert space and Dirac notation; measurement, uncertainty, and time evolution; the quantum harmonic oscillator; the propagator by two routes; angular momentum from the SU(2) algebra, hydrogen, addition of angular momenta, and Wigner–Eckart |

## Layout and building

Each Part compiles standalone (`pdflatex <file>.tex`, twice) in its own
directory; figures (`fig_*.pdf`) sit alongside the sources with the Python
scripts that generate them (`make_figures_*.py`).

`volume/` binds the four standalone documents into one PDF **without touching
their sources**: labels are namespaced, each Part keeps its internal numbering
exactly, and `check_crossrefs.py` validates every cross-Part citation against
the current numbering of its target — the build refuses to run on drift.
Regenerate with `bash volume/build.sh`. Design notes in
[`volume/README_volume.md`](volume/README_volume.md).

Further Parts (quantum field theory, general relativity) are planned; the
build registry accepts a new Part as a single entry.