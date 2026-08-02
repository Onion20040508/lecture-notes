#!/usr/bin/env python3
"""Assemble the four standalone lecture-note documents into one volume.

Design constraints:
  * The standalone .tex sources are never modified; bodies are extracted,
    label-namespaced, and lightly rewritten into build/<prefix>_body.tex.
  * Displayed numbering inside each Part matches the standalone document
    exactly (sections, equations, figures, theorem environments all reset
    at each \\part), so the plain-text cross-document citation registers
    ("[Mech. \\S3.2]", "[Fld. Remark 2.7]") remain literally accurate.
  * Adding a future course (QFT, GR) = one PARTS entry.

Usage:  python3 build_volume.py            # extract + write master
        (then pdflatex master; see build.sh)
"""

import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # /home/claude/qm

# ---- registry: add future parts (QFT, GR) here -------------------------
PARTS = [
    # prefix, source tex,                                  volume part title
    ("osc",  ROOT / "osc/ho_reference.tex",
     "Oscillators: From One Spring to the Wave Equation"),
    ("mech", ROOT / "mech/variational_mechanics_course.tex",
     "Variational and Hamiltonian Mechanics"),
    ("fld",  ROOT / "fld/relativity_field_theory.tex",
     "Special Relativity and Classical Field Theory"),
    ("qm",   ROOT / "qm/quantum_mechanics.tex",
     "Quantum Mechanics"),
]

FIG_DIRS = [ROOT / "osc", ROOT / "mech", ROOT / "fld", ROOT / "qm"]

BUILD = HERE / "build"


def extract(src_path: Path, prefix: str):
    """Return (title_block, abstract, body) with labels namespaced."""
    src = src_path.read_text()

    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", src, re.S)
    body = m.group(1)

    # capture and strip abstract
    am = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, re.S)
    abstract = am.group(1).strip() if am else ""
    if am:
        body = body[:am.start()] + body[am.end():]

    # capture original title/subtitle from the preamble for the part page
    tm = re.search(r"\\title\{(.*?)\}\s*\n\\author", src, re.S)
    title_block = tm.group(1).strip() if tm else ""

    # strip standalone front matter
    body = re.sub(r"\\maketitle", "", body)
    body = re.sub(r"\\(clearpage|newpage)\s*\\tableofcontents\s*\\(clearpage|newpage)", "", body)
    body = re.sub(r"\\tableofcontents", "", body)

    # namespace every label and every internal reference to it
    body = re.sub(r"\\label\s*\{([^}]*)\}", rf"\\label{{{prefix}:\1}}", body)
    body = re.sub(r"\\(ref|eqref|pageref)\s*\{([^}]*)\}", rf"\\\1{{{prefix}:\2}}", body)

    # demote internal \part -> \InnerPart (keeps per-document Part I/II/... numbering)
    body = re.sub(r"\\part\{([^}]*)\}", r"\\InnerPart{\1}", body)

    # per-part appendix switch
    body = body.replace("\\appendix", "\\PartAppendix")

    return title_block, abstract, body


def main():
    BUILD.mkdir(exist_ok=True)

    part_inputs = []
    for prefix, tex, part_title in PARTS:
        title_block, abstract, body = extract(tex, prefix)
        (BUILD / f"{prefix}_body.tex").write_text(body)
        part_inputs.append(
            "\\StartPart{%s}{%s}{%s}\n\\input{%s_body}\n"
            % (part_title, title_block, abstract, prefix)
        )

    master = MASTER_TEMPLATE.replace("%%PARTS%%", "\n".join(part_inputs))
    (BUILD / "master.tex").write_text(master)

    # collect figures (names verified collision-free by the audit)
    for d in FIG_DIRS:
        if d.is_dir():
            for f in list(d.glob("fig_*.pdf")) + list(d.glob("fig_*.png")):
                shutil.copy(f, BUILD / f.name)

    print("wrote", BUILD / "master.tex", "and", len(PARTS), "part bodies")


MASTER_TEMPLATE = r"""\documentclass[11pt]{article}
\PassOptionsToPackage{dvipsnames}{xcolor}

% ---- union of the four documents' preambles ---------------------------
\usepackage[margin=1in]{geometry}
\usepackage{amsmath, amssymb, amsthm}
\usepackage{mathtools}
\usepackage{slashed}
\usepackage{simpler-wick}
\usepackage{empheq}
\usepackage{xcolor}
\usepackage{enumitem}
\newcommand{\contr}[2]{\overbracket[0.5pt][2pt]{#1\,#2}}
\newcommand{\ud}{\mathrm{d}}
\newcommand{\pp}{\partial}
\newcommand{\abs}[1]{\left|#1\right|}
\newcommand{\half}{\tfrac{1}{2}}
\newcommand{\diag}{\operatorname{diag}}
\newcommand{\Tr}{\operatorname{Tr}}
\newcommand{\order}[1]{\mathcal{O}(#1)}
\newcommand{\Lag}{\mathcal{L}}
\newcommand{\Ham}{\mathcal{H}}
\newcommand{\lrpd}{\overset{\leftrightarrow}{\pp}}
\newcommand{\dal}{\Box}
\newcommand{\unit}[1]{\,\mathrm{#1}}
\newcommand{\bbone}{\mathord{1\mskip-4.5mu\mathrm{l}}}
\newcommand{\ketbra}[2]{\lvert #1 \rangle\langle #2 \rvert}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tikz}
\usetikzlibrary{decorations.pathmorphing, decorations.markings, patterns, arrows.meta, calc}
\usepackage{mathrsfs}
\usepackage[colorlinks=true, linkcolor=blue!50!black, urlcolor=blue!50!black]{hyperref}
\usepackage[expansion=false]{microtype}

% one shared per-section counter, exactly the scheme of all four sources,
% so every theorem-environment number matches its standalone document
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{convention}[theorem]{Convention}
\newtheorem{postulate}[theorem]{Postulate}
\newtheorem{example}[theorem]{Example}
\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{keypoint}[theorem]{Key point}
\newtheorem{note}[theorem]{Note}

% ---- macros (union; no name conflicts across the four sources) --------
\newcommand{\dd}{\mathrm{d}}
\newcommand{\ee}{\mathrm{e}}
\newcommand{\ii}{\mathrm{i}}
\newcommand{\pd}[2]{\frac{\partial #1}{\partial #2}}
\newcommand{\tot}[2]{\frac{\dd #1}{\dd #2}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\Rre}{\operatorname{Re}}
\newcommand{\Iim}{\operatorname{Im}}
\newcommand{\vx}{\vec{x}}
\newcommand{\vv}{\vec{v}}
\newcommand{\ve}{\vec{e}}
\newcommand{\vp}{\vec{p}}
\newcommand{\vq}{\vec{q}}
\newcommand{\vr}{\vec{r}}
\newcommand{\vth}{\vec{\theta}}
\newcommand{\vQ}{\vec{Q}}
\newcommand{\vP}{\vec{P}}
\newcommand{\vE}{\vec{E}}
\newcommand{\vB}{\vec{B}}
\newcommand{\mA}{\mathsf{A}}
\newcommand{\mM}{\mathsf{M}}
\newcommand{\mK}{\mathsf{K}}
\newcommand{\op}[1]{\hat{#1}}
\newcommand{\idop}{\mathbf{1}}
\newcommand{\ket}[1]{\lvert #1 \rangle}
\newcommand{\bra}[1]{\langle #1 \rvert}
\newcommand{\braket}[2]{\langle #1 | #2 \rangle}
\newcommand{\planned}[1]{\begin{quote}\small\itshape [Planned --- #1]\end{quote}}

\tikzset{
  spring/.style={thick, decorate, decoration={coil, aspect=0.5,
      segment length=2.2mm, amplitude=2mm, pre length=2mm, post length=2mm}},
  damper/.style={thick},
  ground/.style={fill, pattern=north east lines, draw=none, minimum width=0.6cm, minimum height=0.25cm},
  mass/.style={draw, thick, fill=gray!15, minimum width=0.9cm, minimum height=0.9cm},
}

% ---- part machinery ----------------------------------------------------
% Each \StartPart resets section/equation/figure/table/footnote counters so
% that displayed numbering inside a Part reproduces the standalone document,
% and prefixes hyperref anchors with the part number to keep them unique.
\makeatletter
\newcounter{innerpart}
\renewcommand{\theHsection}{\thepart.\arabic{section}}
\renewcommand{\theHequation}{\thepart.\arabic{equation}}
\renewcommand{\theHfigure}{\thepart.\arabic{figure}}
\renewcommand{\theHtable}{\thepart.\arabic{table}}
\renewcommand{\theHtheorem}{\thepart.\arabic{section}.\arabic{theorem}}

\newcommand{\StartPart}[3]{%
  \clearpage
  \part{#1}
  \setcounter{section}{0}\setcounter{equation}{0}%
  \setcounter{figure}{0}\setcounter{table}{0}\setcounter{footnote}{0}%
  \setcounter{innerpart}{0}%
  \renewcommand{\thesection}{\arabic{section}}%
  \renewcommand{\theHsection}{\thepart.\arabic{section}}%
  \renewcommand{\theHtheorem}{\thepart.\arabic{section}.\arabic{theorem}}%
  \begin{center}\itshape #2\end{center}
  \medskip
  \begin{quote}\small #3\end{quote}
  \clearpage
}

\newcommand{\InnerPart}[1]{%
  \stepcounter{innerpart}%
  \clearpage
  \begin{center}\Large\bfseries Part \Roman{innerpart}\\[4pt]#1\end{center}
  \addcontentsline{toc}{subsection}{Part \Roman{innerpart}: #1}%
  \medskip
}

\newcommand{\PartAppendix}{%
  \setcounter{section}{0}%
  \renewcommand{\thesection}{\Alph{section}}%
  \renewcommand{\theHsection}{\thepart.app.\arabic{section}}%
  \renewcommand{\theHtheorem}{\thepart.app.\arabic{section}.\arabic{theorem}}%
}
\makeatother

\title{\bfseries Lecture Notes in Physics, Volumes I--IV\\[4pt]
\large Oscillators \(\cdot\) Variational Mechanics \(\cdot\)
Spacetime and Fields \(\cdot\) Quantum Mechanics}
\author{Technical reference for lecture slides}
\date{\today}

\begin{document}
\maketitle

\begin{quote}\small
This volume binds the four standalone documents of the series. Each Part
reproduces its source verbatim, with its own internal numbering, so the
plain-text cross-references between Parts --- written as
[Osc.\ \S$n$], [Mech.\ \S$n$], [Fld.\ \S$n$] --- read exactly as in the
standalone documents. Conventions are stated per Part and occasionally
break at Part boundaries by design (notably: the summation convention is
introduced only in Part III). Future courses (quantum field theory,
general relativity) are intended to join as further Parts.
\end{quote}

\clearpage
\setcounter{tocdepth}{2}
\tableofcontents

%%PARTS%%

\end{document}
"""

if __name__ == "__main__":
    main()
