"""Figures for the harmonic oscillator technical reference.

All curves are computed from the exact formulas derived in the document.
Output: PDF figures in the current directory.
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "lines.linewidth": 1.4,
    "figure.dpi": 150,
    "text.usetex": False,
    "mathtext.fontset": "cm",
    "font.family": "serif",
})

C0, C1, C2, C3 = "#1f4e79", "#b03a2e", "#1e8449", "#7d3c98"


# ----------------------------------------------------------------------
# Fig 1: damped oscillator, three regimes, same initial condition
# ----------------------------------------------------------------------
def fig_damped():
    w0 = 1.0
    t = np.linspace(0, 12, 2000)

    # underdamped beta = 0.2, x(0)=1, v(0)=0
    b = 0.2
    wd = np.sqrt(w0**2 - b**2)
    x_u = np.exp(-b*t) * (np.cos(wd*t) + (b/wd)*np.sin(wd*t))

    # critical beta = 1
    x_c = np.exp(-w0*t) * (1 + w0*t)

    # overdamped beta = 2
    b = 2.0
    l1 = -b + np.sqrt(b**2 - w0**2)
    l2 = -b - np.sqrt(b**2 - w0**2)
    x_o = (l2*np.exp(l1*t) - l1*np.exp(l2*t)) / (l2 - l1)

    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.plot(t, x_u, color=C0, label=r"underdamped $(\beta = 0.2\,\omega_0)$")
    ax.plot(t, x_c, color=C1, label=r"critical $(\beta = \omega_0)$")
    ax.plot(t, x_o, color=C2, label=r"overdamped $(\beta = 2\,\omega_0)$")
    ax.plot(t, np.exp(-0.2*t)/np.cos(np.arctan(0.2/np.sqrt(1-0.04))), color=C0,
            lw=0.8, ls="--", alpha=0.6)
    ax.plot(t, -np.exp(-0.2*t)/np.cos(np.arctan(0.2/np.sqrt(1-0.04))), color=C0,
            lw=0.8, ls="--", alpha=0.6)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel(r"$\omega_0 t$")
    ax.set_ylabel(r"$x(t)/x_0$")
    ax.set_xlim(0, 12)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig("fig_damped_cases.pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 2: beats (undamped, driven off resonance, starting from rest)
# ----------------------------------------------------------------------
def fig_beats():
    w0, w, f0 = 1.0, 0.9, 1.0
    t = np.linspace(0, 140, 6000)
    x = f0/(w0**2 - w**2) * (np.cos(w*t) - np.cos(w0*t))
    env = np.abs(2*f0/(w0**2 - w**2) * np.sin((w0 - w)*t/2))

    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    ax.plot(t, x, color=C0, lw=0.9)
    ax.plot(t, env, color=C1, ls="--", lw=1.2, label="envelope")
    ax.plot(t, -env, color=C1, ls="--", lw=1.2)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel(r"$\omega_0 t$")
    ax.set_ylabel(r"$x(t)$")
    ax.set_xlim(0, 140)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig("fig_beats.pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 3: resonant growth, omega = omega_0, undamped
# ----------------------------------------------------------------------
def fig_growth():
    w0, f0 = 1.0, 1.0
    t = np.linspace(0, 60, 4000)
    x = f0/(2*w0) * t * np.sin(w0*t)

    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    ax.plot(t, x, color=C0, lw=0.9)
    ax.plot(t,  f0/(2*w0)*t, color=C1, ls="--", lw=1.2,
            label=r"envelope $\pm\, f_0 t/2\omega_0$")
    ax.plot(t, -f0/(2*w0)*t, color=C1, ls="--", lw=1.2)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel(r"$\omega_0 t$")
    ax.set_ylabel(r"$x(t)$")
    ax.set_xlim(0, 60)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig("fig_resonance_growth.pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 4: amplitude response family A(omega) for several beta
# ----------------------------------------------------------------------
def fig_amplitude():
    w0, f0 = 1.0, 1.0
    w = np.linspace(0.01, 2.2, 2000)
    betas = [0.05, 0.10, 0.20, 0.40, 1/np.sqrt(2)]
    labels = [r"$\beta/\omega_0=0.05$", r"$0.10$", r"$0.20$", r"$0.40$",
              r"$1/\sqrt{2}$"]
    colors = plt.cm.viridis(np.linspace(0.05, 0.85, len(betas)))

    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    for b, lab, c in zip(betas, labels, colors):
        A = f0/np.sqrt((w0**2 - w**2)**2 + 4*b**2*w**2)
        ax.plot(w, A, color=c, label=lab)

    # locus of peaks: omega_peak = sqrt(w0^2 - 2 b^2), A_max = f0/(2 b w_d)
    bb = np.linspace(0.02, 1/np.sqrt(2) - 1e-4, 300)
    wpk = np.sqrt(w0**2 - 2*bb**2)
    Apk = f0/(2*bb*np.sqrt(w0**2 - bb**2))
    ax.plot(wpk, Apk, color="k", ls=":", lw=1.1, label="locus of maxima")

    ax.axvline(w0, color="gray", lw=0.7, ls="--")
    ax.text(w0 + 0.02, 9.3, r"$\omega=\omega_0$", color="gray", fontsize=9)
    ax.set_xlabel(r"$\omega/\omega_0$")
    ax.set_ylabel(r"$A(\omega)\,/\,(f_0/\omega_0^2)$")
    ax.set_xlim(0, 2.2)
    ax.set_ylim(0, 10.5)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig("fig_amplitude_family.pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 5: phase lag delta(omega)
# ----------------------------------------------------------------------
def fig_phase():
    w0 = 1.0
    w = np.linspace(0.0, 2.2, 2000)
    betas = [0.05, 0.10, 0.20, 0.40, 1/np.sqrt(2)]
    labels = [r"$\beta/\omega_0=0.05$", r"$0.10$", r"$0.20$", r"$0.40$",
              r"$1/\sqrt{2}$"]
    colors = plt.cm.viridis(np.linspace(0.05, 0.85, len(betas)))

    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    for b, lab, c in zip(betas, labels, colors):
        delta = np.arctan2(2*b*w, w0**2 - w**2)
        ax.plot(w, delta, color=c, label=lab)
    ax.axhline(np.pi/2, color="gray", lw=0.7, ls="--")
    ax.axvline(w0, color="gray", lw=0.7, ls="--")
    ax.set_yticks([0, np.pi/2, np.pi])
    ax.set_yticklabels([r"$0$", r"$\pi/2$", r"$\pi$"])
    ax.set_xlabel(r"$\omega/\omega_0$")
    ax.set_ylabel(r"$\delta(\omega)$")
    ax.set_xlim(0, 2.2)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig("fig_phase_family.pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 6: coupled oscillators, energy exchange (beats), weak coupling
# ----------------------------------------------------------------------
def fig_coupled_beats():
    w0 = 1.0
    wc2 = 0.05
    w1 = w0
    w2 = np.sqrt(w0**2 + 2*wc2)
    t = np.linspace(0, 280, 8000)
    x1 = 0.5*(np.cos(w1*t) + np.cos(w2*t))
    x2 = 0.5*(np.cos(w1*t) - np.cos(w2*t))
    env = np.abs(np.cos((w2 - w1)*t/2))

    fig, axes = plt.subplots(2, 1, figsize=(5.8, 4.2), sharex=True)
    axes[0].plot(t, x1, color=C0, lw=0.8)
    axes[0].plot(t, env, color=C1, ls="--", lw=1.1)
    axes[0].plot(t, -env, color=C1, ls="--", lw=1.1)
    axes[0].set_ylabel(r"$x_1(t)/a$")
    axes[1].plot(t, x2, color=C2, lw=0.8)
    axes[1].plot(t, np.abs(np.sin((w2 - w1)*t/2)), color=C1, ls="--", lw=1.1)
    axes[1].plot(t, -np.abs(np.sin((w2 - w1)*t/2)), color=C1, ls="--", lw=1.1)
    axes[1].set_ylabel(r"$x_2(t)/a$")
    axes[1].set_xlabel(r"$\omega_0 t$")
    for ax in axes:
        ax.axhline(0, color="k", lw=0.5)
        ax.set_xlim(0, 280)
    fig.tight_layout()
    fig.savefig("fig_coupled_beats.pdf")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 7: forced coupled oscillators, steady-state amplitudes vs omega
#        undamped (exact) + small damping overlay (numerical)
# ----------------------------------------------------------------------
def fig_forced_coupled():
    w0, f0 = 1.0, 1.0
    wc2 = 0.5
    w1 = w0
    w2 = np.sqrt(w0**2 + 2*wc2)
    wa = np.sqrt(w0**2 + wc2)          # antiresonance
    w = np.linspace(0.01, 2.2, 4000)

    X1 = (f0/2)*(1/(w1**2 - w**2) + 1/(w2**2 - w**2))
    X2 = (f0/2)*(1/(w1**2 - w**2) - 1/(w2**2 - w**2))

    # small damping: solve (A - w^2 I + 2 i beta w I) X = f0 e1
    b = 0.04
    A = np.array([[w0**2 + wc2, -wc2], [-wc2, w0**2 + wc2]])
    X1d = np.empty_like(w)
    X2d = np.empty_like(w)
    for i, wi in enumerate(w):
        M = A - wi**2*np.eye(2) + 2j*b*wi*np.eye(2)
        sol = np.linalg.solve(M, np.array([f0, 0.0]))
        X1d[i], X2d[i] = np.abs(sol[0]), np.abs(sol[1])

    fig, axes = plt.subplots(2, 1, figsize=(5.8, 5.2), sharex=True)

    for ax, X, Xd, name, col, loc in [
        (axes[0], X1, X1d, r"$|X_1(\omega)|$ (driven mass)", C0, "upper left"),
        (axes[1], X2, X2d, r"$|X_2(\omega)|$", C2, "upper right"),
    ]:
        Xa = np.abs(X).copy()
        Xa[Xa > 12] = np.nan
        ax.plot(w, Xa, color=col, label="undamped (exact)")
        ax.plot(w, Xd, color=C1, lw=1.0, ls="--",
                label=r"small damping $(\beta=0.04\,\omega_0)$")
        ax.axvline(w1, color="gray", lw=0.7, ls=":")
        ax.axvline(w2, color="gray", lw=0.7, ls=":")
        ax.set_ylim(0, 8)
        ax.set_ylabel(name)
        ax.legend(frameon=False, loc=loc)

    axes[0].axvline(wa, color=C3, lw=1.0, ls="-.")
    axes[0].annotate("antiresonance\n" + r"$\omega_a=\sqrt{\omega_0^2+\omega_c^2}$",
                     xy=(wa, 0.30), xytext=(1.60, 3.6),
                     color=C3, fontsize=9,
                     arrowprops=dict(arrowstyle="->", color=C3, lw=0.9))
    # mode-frequency labels above the top axes, clear of all plot content
    axes[0].text(w1, 8.25, r"$\omega_1$", color="gray", ha="center")
    axes[0].text(w2, 8.25, r"$\omega_2$", color="gray", ha="center")
    axes[1].set_xlabel(r"$\omega/\omega_0$")
    axes[1].set_xlim(0, 2.2)
    fig.tight_layout()
    fig.savefig("fig_forced_coupled.pdf")
    plt.close(fig)




# ----------------------------------------------------------------------
# Fig 8: normal-mode shapes of the N=5 chain
# ----------------------------------------------------------------------
def fig_chain_modes():
    N = 5
    xs = np.linspace(0, N + 1, 400)
    js = np.arange(0, N + 2)

    fig, axes = plt.subplots(N, 1, figsize=(5.6, 6.2), sharex=True)
    for n in range(1, N + 1):
        ax = axes[n - 1]
        env = np.sin(n*np.pi*xs/(N + 1))
        vj = np.sin(n*np.pi*js/(N + 1))
        ax.plot(xs, env, color="gray", lw=0.8, alpha=0.6)
        ax.stem(js, vj, linefmt="C0-", markerfmt="C0o", basefmt="k-")
        wn = 2*np.sin(n*np.pi/(2*(N + 1)))
        ax.set_ylim(-1.35, 1.35)
        ax.set_ylabel(rf"$n={n}$")
        ax.text(1.01, 0.5, rf"$\omega_{{{n}}}={wn:.3f}\,\omega_0$",
                transform=ax.transAxes, fontsize=9, va="center")
        ax.set_yticks([])
    axes[-1].set_xlabel(r"site index $j$   (sites $0$ and $N+1$ are the walls)")
    axes[-1].set_xticks(range(0, N + 2))
    fig.tight_layout()
    fig.savefig("fig_chain_modes.pdf", bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 9: dispersion relation of the chain
# ----------------------------------------------------------------------
def fig_dispersion():
    th = np.linspace(0, np.pi, 400)
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.plot(th, 2*np.sin(th/2), color=C0, label=r"$\omega=2\omega_0\sin(\theta/2)$")
    ax.plot(th, th, color=C1, ls="--", lw=1.1,
            label=r"long-wavelength limit $\omega=\omega_0\theta$")
    for N, ms, lab in [(5, 7, r"$N=5$ modes"), (20, 3.5, r"$N=20$ modes")]:
        tn = np.arange(1, N + 1)*np.pi/(N + 1)
        ax.plot(tn, 2*np.sin(tn/2), "o", ms=ms, mfc="white" if N == 5 else C2,
                mec=C2, color=C2, lw=0, label=lab)
    ax.axhline(2, color="gray", lw=0.7, ls=":")
    ax.text(0.06, 2.04, r"zone-boundary maximum $2\omega_0$", color="gray",
            fontsize=8.5, va="bottom")
    ax.set_xticks([0, np.pi/2, np.pi])
    ax.set_xticklabels([r"$0$", r"$\pi/2$", r"$\pi$"])
    ax.set_xlim(0, np.pi)
    ax.set_ylim(0, 2.35)
    ax.set_xlabel(r"$\theta_n = n\pi/(N+1)$")
    ax.set_ylabel(r"$\omega_n/\omega_0$")
    ax.legend(frameon=False, loc="lower right", fontsize=8.5)
    fig.tight_layout()
    fig.savefig("fig_dispersion.pdf")
    plt.close(fig)




# ----------------------------------------------------------------------
# Fig 10: modes of a square membrane, rendered as 3D surfaces
# ----------------------------------------------------------------------
def fig_membrane_modes():
    x = np.linspace(0, 1, 120)
    X, Y = np.meshgrid(x, x)
    modes = [(1, 1), (2, 1), (1, 2), (2, 2)]

    fig = plt.figure(figsize=(6.4, 5.8))
    for idx, (n, m) in enumerate(modes, 1):
        ax = fig.add_subplot(2, 2, idx, projection="3d")
        Z = np.sin(n*np.pi*X)*np.sin(m*np.pi*Y)
        ax.plot_surface(X, Y, Z, cmap="RdBu_r", vmin=-1, vmax=1,
                        rcount=80, ccount=80, linewidth=0, antialiased=True)
        # nodal lines: the surface crosses zero along straight lines
        for kk in range(1, n):
            ax.plot([kk/n, kk/n], [0, 1], [0, 0], color="k", ls="--", lw=1.2)
        for kk in range(1, m):
            ax.plot([0, 1], [kk/m, kk/m], [0, 0], color="k", ls="--", lw=1.2)
        w = np.sqrt(n**2 + m**2)/np.sqrt(2)
        ax.set_title(rf"$(n,m)=({n},{m})$:  $\omega={w:.3f}\,\omega_{{11}}$",
                     fontsize=9, pad=0)
        ax.set_zlim(-1.4, 1.4)
        ax.set_box_aspect((1, 1, 0.55))
        ax.view_init(elev=26, azim=-58)
        ax.set_axis_off()
    fig.subplots_adjust(left=0.0, right=1.0, top=0.94, bottom=0.0,
                        wspace=-0.1, hspace=0.02)
    fig.savefig("fig_membrane_modes.png", dpi=220)
    plt.close(fig)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    fig_damped()
    fig_beats()
    fig_growth()
    fig_amplitude()
    fig_phase()
    fig_coupled_beats()
    fig_forced_coupled()
    fig_chain_modes()
    fig_dispersion()
    fig_membrane_modes()
    print("all figures written")
