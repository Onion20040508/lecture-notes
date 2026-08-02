#!/usr/bin/env python3
r"""Manifest generator + cross-document citation checker for the series.

Validates plain-text bracket citations ([Mech. \S3.2], [Osc. Conv. 1.1],
[Fld. \S2.4, Remark 2.7], [Mech. App. B], [Mech. Part II]) against the
CURRENT numbering of the cited document. Number-level checking only ---
it catches the drift class (renumbered sections, vanished subsections,
shifted theorem environments), not content mismatches.

Usage: python3 check_crossrefs.py          (from the volume/ directory)
Exit code 1 if any citation fails to resolve.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = {
    "Osc":  ROOT / "osc/ho_reference.tex",
    "Mech": ROOT / "mech/variational_mechanics_course.tex",
    "Fld":  ROOT / "fld/relativity_field_theory.tex",
    "QM":   ROOT / "qm/quantum_mechanics.tex",
}
ENVS = ("theorem","lemma","proposition","corollary","definition",
        "convention","postulate","example","remark")

def manifest(path):
    src = re.sub(r"(?<!\\)%.*", "", path.read_text())
    secs, envs, parts, apps = {}, {}, 0, set()
    s = ss = 0; env_n = 0; in_app = False
    tokens = re.finditer(
        r"\\(section|subsection)\*?\{([^}\n]*)|\\appendix|\\part\{([^}]*)\}"
        r"|\\begin\{(" + "|".join(ENVS) + r")\}",
        src)
    starred = re.compile(r"\\(section|subsection)\*")
    for m in tokens:
        t = m.group(0)
        if t == r"\appendix":
            in_app = True; s = 0; continue
        if m.group(3) is not None:
            parts += 1; continue
        if m.group(4):
            env_n += 1
            envs[(("App" if in_app else "S"), s, env_n)] = m.group(4)
            continue
        if starred.match(t):    # starred sections don't advance counters
            continue
        if m.group(1) == "section":
            s += 1; ss = 0; env_n = 0
            key = (("App", chr(64+s)) if in_app else ("S", str(s)))
            (apps.add(chr(64+s)) if in_app else secs.setdefault(str(s), m.group(2)))
        else:
            ss += 1
            if not in_app: secs.setdefault(f"{s}.{ss}", m.group(2))
    return secs, envs, apps, parts

def check():
    mans = {k: manifest(p) for k, p in DOCS.items()}
    fails = 0
    cite = re.compile(r"\[(Osc|Mech|Fld|QM)\.\\?\s*([^\]]*)\]")
    for name, path in DOCS.items():
        src = re.sub(r"(?<!\\)%.*", "", path.read_text())
        for m in cite.finditer(src):
            target, rest = m.group(1), m.group(2)
            secs, envs, apps, parts = mans[target]
            ok, why = True, ""
            for sm in re.finditer(r"\\S+\\?\s*(\d+(?:\.\d+)?)", rest):
                if sm.group(1) not in secs and sm.group(1).split(".")[0] not in secs:
                    ok, why = False, f"\\S{sm.group(1)} not found"
            for am in re.finditer(r"App\.?\\?\s+([A-Z])\b", rest):
                if am.group(1) not in apps:
                    ok, why = False, f"App {am.group(1)} not found"
            for em in re.finditer(r"(Remark|Conv|Convention|Theorem|Lemma|Prop(?:osition)?|Postulate|Example|Definition)\.?\s+(\d+)\.(\d+)", rest):
                kind = {"Conv":"convention","Prop":"proposition"}.get(em.group(1), em.group(1).lower())
                got = envs.get(("S", int(em.group(2)), int(em.group(3))))
                if got != kind:
                    ok, why = False, f"{em.group(1)} {em.group(2)}.{em.group(3)}: env there is {got!r}"
            pm = re.search(r"Part\s+([IVX]+)", rest)
            if pm and {"I":1,"II":2,"III":3}.get(pm.group(1), 99) > parts:
                ok, why = False, f"Part {pm.group(1)} not found"
            if not ok:
                fails += 1
                print(f"FAIL  {name}: [{target}. {rest}]  --  {why}")
    print("all citations resolve" if not fails else f"{fails} failures")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(check())
