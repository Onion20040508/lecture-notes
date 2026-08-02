"""
Figures for "From Spacetime to Fields", Part I (Special Relativity).
Every curve is drawn from the exact formula stated in the text -- no sketches.

Outputs (PDF, vector):
  fig_lightcone_simultaneity.pdf   light cone + boosted axes and tilted
                                   simultaneity slices (beta = 0.5)
  fig_interval_hyperbolae.pdf      calibration hyperbolae c^2 t^2 - x^2 = const,
                                   with the unit ticks of a boosted frame
  fig_rapidity_addition.pdf        composing N equal boosts: naive Galilean sum
                                   vs exact tanh(N * arctanh(beta))
  fig_muon_survival.pdf            muon survival fraction vs traversed depth,
                                   with and without time dilation (exact
                                   exponential laws)
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 11,
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "axes.linewidth": 0.8,
})

# ----------------------------------------------------------------------
# 1. Light cone with boosted simultaneity slices
# ----------------------------------------------------------------------
beta = 0.5
gamma = 1.0 / np.sqrt(1.0 - beta**2)

fig, ax = plt.subplots(figsize=(5.2, 5.2))

L = 3.0
# light cone: ct = +/- x
xx = np.linspace(-L, L, 2)
ax.plot(xx, xx, color="0.55", lw=1.2)
ax.plot(xx, -xx, color="0.55", lw=1.2)
ax.fill_between(np.linspace(-L, L, 100),
                np.abs(np.linspace(-L, L, 100)), L,
                color="0.92", zorder=0)
ax.fill_between(np.linspace(-L, L, 100),
                -L, -np.abs(np.linspace(-L, L, 100)),
                color="0.92", zorder=0)
ax.text(0.12, 2.55, "future", fontsize=10, color="0.35")
ax.text(0.12, -2.75, "past", fontsize=10, color="0.35")
ax.text(2.0, 2.12, r"$ct = x$", fontsize=10, color="0.35", rotation=45)

# unprimed axes
ax.axhline(0, color="k", lw=1.0)
ax.axvline(0, color="k", lw=1.0)
ax.annotate("", xy=(L, 0), xytext=(L - 0.001, 0),
            arrowprops=dict(arrowstyle="-|>", color="k"))
ax.annotate("", xy=(0, L), xytext=(0, L - 0.001),
            arrowprops=dict(arrowstyle="-|>", color="k"))
ax.text(L - 0.15, -0.32, r"$x$", fontsize=13)
ax.text(-0.38, L - 0.15, r"$ct$", fontsize=13)

# primed axes: ct' axis is worldline x = beta ct  (line ct = x/beta);
# x' axis is the simultaneity line ct = beta x.
tt = np.linspace(-L, L, 2)
ax.plot(beta * tt, tt, color="C0", lw=1.6)                # ct' axis
ax.plot(tt, beta * tt, color="C0", lw=1.6)                # x'  axis
ax.text(beta * 2.55 + 0.10, 2.55, r"$ct'$", fontsize=13, color="C0")
ax.text(2.55, beta * 2.55 - 0.38, r"$x'$", fontsize=13, color="C0")

# lines of simultaneity in S' : ct = beta x + const (parallel to x' axis)
for c0 in (-1.5, -0.75, 0.75, 1.5, 2.25):
    ax.plot(tt, beta * tt + c0, color="C0", lw=0.8, ls="--", alpha=0.8)
ax.text(-2.9, beta * (-2.9) + 2.25 + 0.10,
        r"$t' = \mathrm{const}$", fontsize=10, color="C0")

ax.set_xlim(-L, L)
ax.set_ylim(-L, L)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title(r"Boosted axes and simultaneity slices, $\beta = 0.5$",
             fontsize=11)
fig.tight_layout()
fig.savefig("fig_lightcone_simultaneity.pdf")
plt.close(fig)

# ----------------------------------------------------------------------
# 2. Calibration hyperbolae
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.2, 5.2))
L = 3.0

# light cone
xx = np.linspace(-L, L, 2)
ax.plot(xx, xx, color="0.55", lw=1.0)
ax.plot(xx, -xx, color="0.55", lw=1.0)

# timelike hyperbolae  (ct)^2 - x^2 = s^2 > 0 : ct = +/- sqrt(s^2 + x^2)
xs = np.linspace(-L, L, 400)
for s2, lw in ((1.0, 1.6), (4.0, 1.0)):
    ax.plot(xs, np.sqrt(s2 + xs**2), color="C3", lw=lw)
    ax.plot(xs, -np.sqrt(s2 + xs**2), color="C3", lw=lw, alpha=0.45)
# spacelike hyperbolae  (ct)^2 - x^2 = -s^2 < 0 : x = +/- sqrt(s^2 + (ct)^2)
ts = np.linspace(-L, L, 400)
for s2, lw in ((1.0, 1.6), (4.0, 1.0)):
    ax.plot(np.sqrt(s2 + ts**2), ts, color="C2", lw=lw)
    ax.plot(-np.sqrt(s2 + ts**2), ts, color="C2", lw=lw, alpha=0.45)

ax.text(0.06, 1.02, r"$s^2 = +1$", fontsize=10, color="C3")
ax.text(0.06, 2.06, r"$s^2 = +4$", fontsize=10, color="C3")
ax.text(1.04, -0.30, r"$s^2 = -1$", fontsize=10, color="C2")
ax.text(2.06, -0.30, r"$s^2 = -4$", fontsize=10, color="C2")

# axes
ax.axhline(0, color="k", lw=1.0)
ax.axvline(0, color="k", lw=1.0)
ax.text(L - 0.15, -0.32, r"$x$", fontsize=13)
ax.text(-0.42, L - 0.15, r"$ct$", fontsize=13)

# boosted frame unit ticks: images of (ct,x)=(1,0) and (0,1) under the
# inverse boost, i.e. the events (gamma, gamma beta) and (gamma beta, gamma)
beta = 0.5
gamma = 1.0 / np.sqrt(1 - beta**2)
ax.plot([gamma * beta], [gamma], marker="o", color="C0", ms=6, zorder=5)
ax.plot([gamma], [gamma * beta], marker="o", color="C0", ms=6, zorder=5)
ax.plot([0], [1], marker="o", color="k", ms=5, zorder=5)
ax.plot([1], [0], marker="o", color="k", ms=5, zorder=5)
tt = np.linspace(-L, L, 2)
ax.plot(beta * tt, tt, color="C0", lw=1.1)
ax.plot(tt, beta * tt, color="C0", lw=1.1)
ax.text(gamma * beta + 0.10, gamma + 0.05,
        r"$(ct',x')=(1,0)$", fontsize=9, color="C0")
ax.text(gamma + 0.10, gamma * beta - 0.28,
        r"$(ct',x')=(0,1)$", fontsize=9, color="C0")

ax.set_xlim(-L, L)
ax.set_ylim(-L, L)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title(r"Hyperbolae of constant interval calibrate every frame",
             fontsize=11)
fig.tight_layout()
fig.savefig("fig_interval_hyperbolae.pdf")
plt.close(fig)

# ----------------------------------------------------------------------
# 3. Rapidity addition: composing N equal boosts of beta_1 = 0.5
# ----------------------------------------------------------------------
beta1 = 0.5
phi1 = np.arctanh(beta1)
N = np.arange(0, 9)

naive = N * beta1                       # Galilean guess
exact = np.tanh(N * phi1)               # rapidities add: phi_N = N phi_1

fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.axhline(1.0, color="0.55", lw=1.0, ls=":")
ax.text(0.15, 1.03, r"$\beta = 1$ (light)", fontsize=10, color="0.35")
ax.plot(N, naive, "s--", color="0.5", lw=1.2, ms=5,
        label=r"Galilean sum $N\beta_1$")
ax.plot(N, exact, "o-", color="C0", lw=1.6, ms=5,
        label=r"exact $\tanh(N\phi_1)$, $\phi_1=\mathrm{artanh}\,\beta_1$")
ax.set_xlabel(r"number of composed boosts $N$ (each $\beta_1 = 0.5$)")
ax.set_ylabel(r"resulting velocity $\beta$")
ax.set_ylim(0, 2.1)
ax.set_xlim(-0.2, 8.2)
ax.legend(frameon=False, loc="upper left", fontsize=10)
ax.set_title("Velocities saturate; rapidities add", fontsize=11)
fig.tight_layout()
fig.savefig("fig_rapidity_addition.pdf")
plt.close(fig)

# ----------------------------------------------------------------------
# 4. Muon survival: exact exponential laws with and without dilation
# ----------------------------------------------------------------------
tau = 2.197e-6          # s, muon proper lifetime
c = 2.998e8             # m/s
beta = 0.995
gamma = 1.0 / np.sqrt(1 - beta**2)

d = np.linspace(0, 15e3, 400)                    # depth traversed, m
f_naive = np.exp(-d / (beta * c * tau))          # no dilation
f_exact = np.exp(-d / (gamma * beta * c * tau))  # lab lifetime gamma*tau

fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.semilogy(d / 1e3, f_naive, "--", color="0.5", lw=1.4,
            label=r"no dilation: $\exp[-d/(\beta c\,\tau)]$")
ax.semilogy(d / 1e3, f_exact, "-", color="C0", lw=1.8,
            label=r"with dilation: $\exp[-d/(\gamma\beta c\,\tau)]$")
ax.axvline(15.0, color="0.7", lw=0.9, ls=":")
ax.text(14.7, 3e-9, "production altitude", rotation=90,
        fontsize=9, color="0.35", va="bottom")
# annotate the two survival fractions at 15 km
ax.plot([15], [np.exp(-15e3 / (beta * c * tau))], "s", color="0.4", ms=5)
ax.plot([15], [np.exp(-15e3 / (gamma * beta * c * tau))], "o",
        color="C0", ms=5)
ax.set_xlabel(r"depth traversed $d$ [km]")
ax.set_ylabel(r"surviving fraction")
ax.set_ylim(1e-11, 2)
ax.set_xlim(0, 15.5)
ax.legend(frameon=False, loc="lower left", fontsize=10)
ax.set_title(r"Cosmic-ray muons, $\beta = 0.995$ $(\gamma \approx 10)$",
             fontsize=11)
fig.tight_layout()
fig.savefig("fig_muon_survival.pdf")
plt.close(fig)

print("figures written")

# ----------------------------------------------------------------------
# 5. Proper time along two worldlines between the same events (twin remark)
# ----------------------------------------------------------------------
beta = 0.6
gamma = 1.0 / np.sqrt(1 - beta**2)

fig, ax = plt.subplots(figsize=(4.6, 5.4))

# events A=(0,0), B=(ct=2, x=0); kinked worldline out to (1, beta) and back
ax.plot([0, 0], [0, 2], color="C0", lw=1.8, zorder=3)
ax.plot([0, beta, 0], [0, 1, 2], color="C3", lw=1.8, zorder=3)

# proper-time ticks: straight line, dtau = dt; kinked, dtau = dt/gamma
dtau = 0.4
for k in range(1, 5):
    ax.plot([-0.03, 0.03], [k * dtau, k * dtau], color="C0", lw=1.4, zorder=4)
# kinked: each leg has total proper time 1/gamma = 0.8 -> 2 ticks per leg
for k in (1, 2):
    t = k * dtau * gamma            # coordinate time when proper time = k*dtau
    x = beta * t
    ax.plot([x - 0.03, x + 0.03], [t - 0.018, t + 0.018],
            color="C3", lw=1.4, zorder=4)
    ax.plot([x - 0.03, x + 0.03], [2 - t + 0.018, 2 - t - 0.018],
            color="C3", lw=1.4, zorder=4)

# events
for (x, t, name, dx) in ((0, 0, "A", -0.10), (0, 2, "B", -0.10),
                          (beta, 1, "turnaround", 0.06)):
    ax.plot([x], [t], "ko", ms=5, zorder=5)
    ax.text(x + dx, t, name, fontsize=11,
            ha="right" if dx < 0 else "left", va="center")

ax.text(-0.09, 1.0, r"$c\tau = 2\,cT$", fontsize=11, color="C0",
        ha="right", rotation=90)
ax.text(0.36, 0.42, r"$c\tau = 2\,cT/\gamma = 1.6\,cT$",
        fontsize=11, color="C3", rotation=59)

ax.set_xlim(-0.55, 1.05)
ax.set_ylim(-0.15, 2.2)
ax.set_xlabel(r"$x$  [units of $cT$]")
ax.set_ylabel(r"$ct$  [units of $cT$]")
ax.set_xticks([0, 0.6])
ax.set_yticks([0, 1, 2])
ax.set_title(r"Straight maximizes proper time ($\beta = 0.6$, $\gamma = 1.25$)",
             fontsize=11)
fig.tight_layout()
fig.savefig("fig_twin_proper_time.pdf")
plt.close(fig)

print("twin figure written")

# ----------------------------------------------------------------------
# 6. The mass shell: E = sqrt(p^2 + m^2), with the massless asymptote
# ----------------------------------------------------------------------
p = np.linspace(-3, 3, 400)
m = 1.0
E_massive = np.sqrt(p**2 + m**2)
E_massless = np.abs(p)

fig, ax = plt.subplots(figsize=(5.6, 4.2))
ax.plot(p, E_massive, color="C0", lw=1.8,
        label=r"$E = \sqrt{p^2 + m^2}$  ($m = 1$)")
ax.plot(p, E_massless, color="0.5", lw=1.2, ls="--",
        label=r"$E = |p|$  ($m = 0$, light cone)")

# rest energy gap
ax.annotate("", xy=(0, 1), xytext=(0, 0),
            arrowprops=dict(arrowstyle="<->", color="C3", lw=1.2))
ax.text(0.08, 0.46, r"rest energy $m$", fontsize=10, color="C3")

# nonrelativistic parabola for comparison: E = m + p^2/2m
pn = np.linspace(-1.6, 1.6, 200)
ax.plot(pn, m + pn**2 / (2 * m), color="C2", lw=1.0, ls=":",
        label=r"$E = m + p^2/2m$  (NR expansion)")

ax.set_xlabel(r"$p$  [units of $m$]")
ax.set_ylabel(r"$E$  [units of $m$]")
ax.set_xlim(-3, 3)
ax.set_ylim(0, 3.3)
ax.legend(frameon=False, loc="upper center", fontsize=9)
ax.set_title(r"The mass shell $E^2 - p^2 = m^2$", fontsize=11)
fig.tight_layout()
fig.savefig("fig_mass_shell.pdf")
plt.close(fig)

print("mass shell figure written")

# ----------------------------------------------------------------------
# 7. Chain to field: discrete displacements sampling a smooth profile
# ----------------------------------------------------------------------
L = 1.0
prof = lambda x: 0.8*np.sin(np.pi*x/L) + 0.35*np.sin(3*np.pi*x/L)

fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.0), sharey=True)
for ax, N in zip(axes, (8, 32)):
    a = L/(N+1)
    xj = a*np.arange(1, N+1)
    xs = np.linspace(0, L, 400)
    ax.plot(xs, prof(xs), color="C0", lw=1.2, alpha=0.85)
    ax.stem(xj, prof(xj), linefmt="0.6", markerfmt="ko", basefmt="k-")
    ax.plot(xj, prof(xj), "ko", ms=3.5)
    ax.set_xlabel(r"$x$")
    ax.set_title(rf"$N = {N}$,  $a = L/{N+1}$", fontsize=10)
    ax.set_xlim(0, L)
axes[0].set_ylabel(r"$y_j$  /  $\phi(x,t)$")
for ax in axes:
    for s in ("top","right"): ax.spines[s].set_visible(False)
fig.suptitle(r"$y_j(t) = \phi(x_j, t)$: the label $j$ becomes the label $x$",
             fontsize=11)
fig.tight_layout()
fig.savefig("fig_chain_to_field.pdf")
plt.close(fig)
print("chain-to-field figure written")

# ----------------------------------------------------------------------
# 8. Three dispersion relations: chain, string, Klein-Gordon
#    units: c_s = 1 (string/chain), c = 1 (KG), lattice spacing a = 1
# ----------------------------------------------------------------------
k = np.linspace(0, np.pi, 400)
m_kg = 0.5

w_chain = 2*np.sin(k/2)            # omega_0 = c_s/a = 1
w_string = k
w_kg = np.sqrt(k**2 + m_kg**2)

fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.plot(k, w_string, color="0.45", lw=1.2, ls="--",
        label=r"string / massless:  $\omega = k$")
ax.plot(k, w_chain, color="C0", lw=1.8,
        label=r"chain:  $\omega = 2\sin(ka/2)/a$")
ax.plot(k, w_kg, color="C3", lw=1.8,
        label=r"Klein--Gordon:  $\omega = \sqrt{k^2 + m^2}$")

# mark the two departure scales
ax.axvline(m_kg, color="C3", lw=0.8, ls=":", alpha=0.7)
ax.text(m_kg + 0.04, 2.9, r"$k \sim m$", fontsize=10, color="C3")
ax.axvline(2.0, color="C0", lw=0.8, ls=":", alpha=0.7)
ax.text(2.04, 2.9, r"$k \sim 1/a$", fontsize=10, color="C0")

# mass gap annotation
ax.annotate("", xy=(0, m_kg), xytext=(0, 0),
            arrowprops=dict(arrowstyle="<->", color="C3", lw=1.1))
ax.text(0.05, 0.18, r"$m$", fontsize=11, color="C3")

ax.set_xlabel(r"$k$  [units of $1/a$]")
ax.set_ylabel(r"$\omega$  [units of $c_s/a$ resp. $c/a$]")
ax.set_xlim(0, np.pi)
ax.set_ylim(0, 3.4)
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.set_title("Two ways to leave the light line", fontsize=11)
fig.tight_layout()
fig.savefig("fig_dispersion_trio.pdf")
plt.close(fig)
print("dispersion trio written")
