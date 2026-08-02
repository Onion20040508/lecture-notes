"""Figures for the analytical mechanics reference. Exact formulas throughout."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

plt.rcParams.update({
    "font.size": 10, "axes.labelsize": 10, "legend.fontsize": 9,
    "lines.linewidth": 1.5, "figure.dpi": 150,
    "mathtext.fontset": "cm", "font.family": "serif",
})
C0, C1, C2, C3 = "#1f4e79", "#b03a2e", "#1e8449", "#7d3c98"


# ----------------------------------------------------------------------
# Brachistochrone: three descent curves A=(0,0) -> B=(pi,2), g = 1,
# with numerically computed travel times.
# ----------------------------------------------------------------------
def fig_brachistochrone():
    xB, yB = np.pi, 2.0

    # travel time functional T = int sqrt((1+y'^2)/(2 y)) dx   (g=1)
    def travel_time(y, yp, a=0.0, b=xB):
        f = lambda x: np.sqrt((1.0 + yp(x)**2) / (2.0*y(x)))
        val, _ = quad(f, a, b, limit=300)
        return val

    # straight line
    m = yB/xB
    T_line = travel_time(lambda x: m*x, lambda x: m*np.ones_like(np.atleast_1d(x))[0]
                         if np.isscalar(x) else m*np.ones_like(x))

    # circular arc, vertical start: center (R,0), R = (pi^2+4)/(2 pi)
    R = (np.pi**2 + 4)/(2*np.pi)
    yc = lambda x: np.sqrt(R**2 - (x - R)**2)
    ycp = lambda x: (R - x)/np.sqrt(R**2 - (x - R)**2)
    T_circ = travel_time(yc, ycp, 1e-12, xB)

    # cycloid a=1 : exact T = pi  (dT = dtheta)
    T_cyc = np.pi

    th = np.linspace(0, np.pi, 400)
    xcyc, ycyc = th - np.sin(th), 1 - np.cos(th)
    x = np.linspace(0, xB, 400)

    fig, ax = plt.subplots(figsize=(5.9, 3.6))
    ax.plot(x, m*x, color=C2, ls="-.",
            label=rf"straight line:  $T = {T_line:.3f}$")
    ax.plot(x, yc(x), color=C3, ls="--",
            label=rf"circular arc:  $T = {T_circ:.3f}$")
    ax.plot(xcyc, ycyc, color=C1, lw=2.0,
            label=rf"cycloid:  $T = \pi \approx {T_cyc:.3f}$")
    ax.plot([0, xB], [0, yB], "o", color="k", ms=5)
    ax.text(-0.06, -0.09, r"$A$", ha="right")
    ax.text(xB + 0.06, yB + 0.02, r"$B$")
    ax.invert_yaxis()
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$ (downward)")
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(r"descent times, $g=1$, from rest at $A$", fontsize=10)
    fig.tight_layout()
    fig.savefig("fig_brachistochrone.pdf")
    plt.close(fig)
    print("times:", T_line, T_circ, T_cyc)


# ----------------------------------------------------------------------
# Catenary vs parabola through the same endpoints and vertex
# ----------------------------------------------------------------------
def fig_catenary():
    C = 0.6
    x = np.linspace(-1, 1, 400)
    ycat = C*np.cosh(x/C)
    ycat -= ycat.min()
    # parabola with the same endpoints and same vertex (0,0)
    ypar = ycat[-1]*x**2

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(x, ycat, color=C0, lw=2.0, label=r"catenary $\;y \propto \cosh(x/C)$")
    ax.plot(x, ypar, color=C1, ls="--", label="parabola, same endpoints and vertex")
    # chain beads
    xs = np.linspace(-1, 1, 21)
    ys = C*np.cosh(xs/C) - C*np.cosh(1/C) + ycat[-1]
    ys = C*np.cosh(xs/C); ys -= ys.min()
    ax.plot(xs, ys, "o", color=C0, ms=3.5)
    ax.plot([-1, 1], [ycat[-1], ycat[-1]], "s", color="k", ms=6)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"height")
    ax.legend(frameon=False, loc="upper center", fontsize=8.5)
    fig.tight_layout()
    fig.savefig("fig_catenary.pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# Phase portraits: harmonic oscillator and pendulum (separatrix)
# ----------------------------------------------------------------------
def fig_phase_portraits():
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.1))

    # SHO: h = p^2/2 + q^2/2
    q = np.linspace(-2.4, 2.4, 300)
    p = np.linspace(-2.4, 2.4, 300)
    Q, P = np.meshgrid(q, p)
    H = 0.5*P**2 + 0.5*Q**2
    axes[0].contour(Q, P, H, levels=[0.25, 0.72, 1.4, 2.3],
                    colors=[C0], linewidths=1.2)
    axes[0].set_title("harmonic oscillator", fontsize=10)
    axes[0].set_xlabel(r"$q$")
    axes[0].set_ylabel(r"$p$")

    # pendulum: h = p^2/2 - cos(theta)
    th = np.linspace(-2*np.pi, 2*np.pi, 600)
    p = np.linspace(-3, 3, 500)
    TH, P = np.meshgrid(th, p)
    H = 0.5*P**2 - np.cos(TH)
    axes[1].contour(TH, P, H, levels=[-0.6, 0.0, 0.6],
                    colors=[C0], linewidths=1.1)
    axes[1].contour(TH, P, H, levels=[1.6, 2.6],
                    colors=[C2], linewidths=1.1)
    axes[1].contour(TH, P, H, levels=[1.0],
                    colors=[C1], linewidths=2.0)
    axes[1].set_title("pendulum (red: separatrix)", fontsize=10)
    axes[1].set_xlabel(r"$\theta$")
    axes[1].set_xticks([-2*np.pi, 0, 2*np.pi])
    axes[1].set_xticklabels([r"$-2\pi$", r"$0$", r"$2\pi$"])
    axes[1].set_ylabel(r"$p$")
    fig.tight_layout()
    fig.savefig("fig_phase_portraits.pdf")
    plt.close(fig)


if __name__ == "__main__":
    fig_brachistochrone()
    fig_catenary()
    fig_phase_portraits()
    print("lagrangian figures written")


# ----------------------------------------------------------------------
# fig_hj_action: Hamilton's principal function as a field over endpoints
# Exact formulas (m = omega = 1, launch point (q0,t0) = (0,0)):
#   free particle: S(q,t) = q^2 / (2 t)
#   oscillator:    S(q,t) = (q^2 / 2) * cot(t)      (q0 = 0 case of
#                  S = (w/(2 sin wT)) * ((q^2+q0^2) cos wT - 2 q q0))
# Both are verified against the Hamilton-Jacobi equation symbolically
# below before anything is drawn.
# ----------------------------------------------------------------------

def verify_hj_symbolically():
    import sympy as sp
    q, q0, t, m, w = sp.symbols('q q0 t m omega', positive=True)
    # free particle, general q0: S = m (q-q0)^2 / (2 t)
    S_free = m*(q - q0)**2/(2*t)
    hj_free = sp.simplify(sp.diff(S_free, t) + sp.diff(S_free, q)**2/(2*m))
    assert hj_free == 0, f"free-particle HJ residual: {hj_free}"
    # oscillator, general q0: S = (m w / (2 sin wT)) ((q^2+q0^2) cos wT - 2 q q0)
    S_sho = m*w/(2*sp.sin(w*t))*((q**2 + q0**2)*sp.cos(w*t) - 2*q*q0)
    hj_sho = sp.simplify(sp.diff(S_sho, t)
                         + sp.diff(S_sho, q)**2/(2*m)
                         + m*w**2*q**2/2)
    assert hj_sho == 0, f"oscillator HJ residual: {hj_sho}"
    print("HJ verified symbolically for both principal functions")


def make_hj_action_figure():
    verify_hj_symbolically()
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.4))

    # --- left: free particle, S = q^2/(2t), trajectories q = v t
    ax = axes[0]
    t = np.linspace(0.08, 3.0, 400)
    q = np.linspace(-2.6, 2.6, 400)
    T, Q = np.meshgrid(t, q)
    S = Q**2/(2*T)
    levels = [0.05, 0.2, 0.5, 1.0, 2.0, 4.0, 8.0]
    ax.contour(T, Q, S, levels=levels, colors='0.55', linewidths=0.7)
    for v in [-2.0, -1.2, -0.6, 0.0, 0.6, 1.2, 2.0]:
        ax.plot(t, v*t, 'C0', lw=1.6)
    ax.set_xlim(0, 3.0); ax.set_ylim(-2.6, 2.6)
    ax.set_xlabel(r'$t$'); ax.set_ylabel(r'$q$')
    ax.set_title(r'free particle: $S = q^2/2t$')

    # --- right: oscillator, S = (q^2/2) cot(t), trajectories q = A sin t
    ax = axes[1]
    t = np.linspace(0.08, np.pi - 0.02, 500)
    q = np.linspace(-2.6, 2.6, 400)
    T, Q = np.meshgrid(t, q)
    S = 0.5*Q**2/np.tan(T)
    levels = [-4.0, -2.0, -1.0, -0.4, 0.4, 1.0, 2.0, 4.0]
    ax.contour(T, Q, S, levels=levels, colors='0.55', linewidths=0.7)
    for A in [-2.4, -1.6, -0.8, 0.8, 1.6, 2.4]:
        ax.plot(t, A*np.sin(t), 'C0', lw=1.6)
    ax.axvline(np.pi, color='C3', lw=1.2, ls='--')
    ax.annotate(r'$\omega t = \pi$: refocusing', xy=(np.pi, 0),
                xytext=(2.05, 2.15), color='C3', fontsize=9,
                arrowprops=dict(arrowstyle='->', color='C3', lw=0.9))
    ax.set_xlim(0, np.pi + 0.25); ax.set_ylim(-2.6, 2.6)
    ax.set_xlabel(r'$t$'); ax.set_ylabel(r'$q$')
    ax.set_title(r'oscillator: $S = (q^2/2)\cot t$')

    fig.tight_layout()
    fig.savefig('fig_hj_action.pdf')
    plt.close(fig)
    print("hj action figure written")


make_hj_action_figure()
