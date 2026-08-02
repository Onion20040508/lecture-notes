# Oscillators Notes — Package

## Documents
1. ho_reference.tex/.pdf (40pp) — "EVERYTHING You Need to Know About Oscillators"
   (technical reference: SHO -> damped -> forced -> resonance -> coupled ->
   antiresonance/TMD -> N-chain -> wave equation -> Fourier -> 2D/3D outlook)
2. ho_nutshell.tex/.pdf (20pp) — same story, "In a Nutshell" (no heavy machinery);
   sections parallel 1:1; epistemic tags [verified here]/[stated; companion §n]

## Figure scripts (exact formulas, matplotlib)
- make_figures.py          -> reference figures (incl. 3D membrane PNG, 220dpi)
- make_figures_nutshell.py -> nutshell extras (SHM anatomy, energy exchange)

## Build
pdflatex ×2 in a directory containing the fig_* files.
Environment gotchas: microtype needs [expansion=false]; tikz needs calc library;
\newtheorem{check} clashes with built-in \check.
