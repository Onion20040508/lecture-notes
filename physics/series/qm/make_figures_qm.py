"""
Figures for "From Brackets to Amplitudes".
Every element drawn from the exact formulas stated in the text.

fig_bloch.pdf : the Bloch sphere; poles = S_z eigenstates, equator
                point = |+x>, one general state at (theta, phi) with
                the exact parametrization
                |psi> = cos(theta/2)|+> + e^{i phi} sin(theta/2)|->.
"""
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 11, "font.family": "serif", "mathtext.fontset": "cm",
})

fig = plt.figure(figsize=(5.4, 5.4))
ax = fig.add_subplot(111, projection="3d")

# wireframe sphere
u = np.linspace(0, 2*np.pi, 60)
v = np.linspace(0, np.pi, 30)
xs = np.outer(np.cos(u), np.sin(v))
ys = np.outer(np.sin(u), np.sin(v))
zs = np.outer(np.ones_like(u), np.cos(v))
ax.plot_wireframe(xs, ys, zs, color="0.88", linewidth=0.35,
                  rstride=4, cstride=4)
# equator and a meridian, solid
ax.plot(np.cos(u), np.sin(u), 0*u, color="0.55", lw=0.9)
ax.plot(np.cos(u), 0*u, np.sin(u), color="0.85", lw=0.6)

# axes through the sphere: label poles |+>, |->, equator |+>_x, |+>_y
axis_len = 1.32
for vec, lab, off, ha in (
        ((0,0,axis_len),  r"$|{+}\rangle$", ( 0.00, 0.00, 0.10), "center"),
        ((0,0,-axis_len), r"$|{-}\rangle$", ( 0.00, 0.00,-0.17), "center"),
        ((axis_len,0,0),  r"$|{+}\rangle_x$", ( 0.28, 0.00,-0.02), "left"),
        ((0,axis_len,0),  r"$|{+}\rangle_y$", ( 0.02, 0.24, 0.00), "left")):
    ax.quiver(0,0,0,*vec, color="0.35", arrow_length_ratio=0.055, lw=1.0)
    ax.text(vec[0]+off[0], vec[1]+off[1], vec[2]+off[2], lab,
            fontsize=12, ha=ha, va="center")

# a general state at (theta, phi) -- exact Bloch map
theta, phi = 0.35*np.pi, 0.30*np.pi
n = np.array([np.sin(theta)*np.cos(phi),
              np.sin(theta)*np.sin(phi),
              np.cos(theta)])
ax.quiver(0,0,0,*n, color="C3", arrow_length_ratio=0.09, lw=2.2)
ax.text(n[0]+0.03, n[1]+0.10, n[2]+0.17,
        r"$|\theta,\varphi\rangle$", color="C3", fontsize=13, ha="left")

# dashed guides: polar-angle arc (red) and azimuth arc (blue)
t = np.linspace(0, theta, 40)
r_arc = 0.38
ax.plot(r_arc*np.sin(t)*np.cos(phi), r_arc*np.sin(t)*np.sin(phi),
        r_arc*np.cos(t), color="C3", lw=1.0, ls="--")
tm = 0.55*theta
ax.text(0.50*np.sin(tm)*np.cos(phi)-0.05, 0.50*np.sin(tm)*np.sin(phi),
        0.52*np.cos(tm)+0.05, r"$\theta$", color="C3", fontsize=12)
p = np.linspace(0, phi, 40)
r_eq = 0.55
ax.plot(r_eq*np.cos(p), r_eq*np.sin(p), 0*p, color="C0", lw=1.0, ls="--")
ax.text(0.72*np.cos(phi/2), 0.72*np.sin(phi/2), -0.16,
        r"$\varphi$", color="C0", fontsize=12, ha="center")
# projection guides
ax.plot([n[0], n[0]], [n[1], n[1]], [0, n[2]], color="0.6", lw=0.7, ls=":")
ax.plot([0, n[0]], [0, n[1]], [0, 0], color="0.6", lw=0.7, ls=":")

ax.set_box_aspect((1,1,0.95))
ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25); ax.set_zlim(-1.25, 1.25)
ax.set_axis_off()
ax.view_init(elev=18, azim=38)
fig.tight_layout()
fig.savefig("fig_bloch.pdf", bbox_inches="tight", pad_inches=0.25)
plt.close(fig)
print("bloch written")

# ----------------------------------------------------------------------
# fig_wavepacket.pdf : the minimum-uncertainty Gaussian in both
# representations; exact formulas, reciprocal widths, product = hbar/2.
# Units: hbar = 1, Delta x = 1.
# ----------------------------------------------------------------------
fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.2, 3.4))
sx = 1.0                       # Delta x
sp = 0.5/sx                    # Delta p = hbar/(2 Delta x), hbar = 1
x = np.linspace(-4, 4, 500)
p = np.linspace(-2, 2, 500)
rho_x = np.exp(-x**2/(2*sx**2))/np.sqrt(2*np.pi*sx**2)
rho_p = np.exp(-p**2/(2*sp**2))/np.sqrt(2*np.pi*sp**2)

axL.plot(x, rho_x, color="C0", lw=1.8)
axL.fill_between(x, rho_x, alpha=0.12, color="C0")
axL.set_xlabel(r"$x$  [units of $\Delta x$]")
axL.set_ylabel(r"$|\psi(x)|^2$")
axL.annotate("", xy=(sx, 0.242), xytext=(-sx, 0.242),
             arrowprops=dict(arrowstyle="<->", color="C0", lw=1.0))
axL.text(0, 0.255, r"$2\,\Delta x$", ha="center", color="C0", fontsize=10)

axR.plot(p, rho_p, color="C3", lw=1.8)
axR.fill_between(p, rho_p, alpha=0.12, color="C3")
axR.set_xlabel(r"$p$  [units of $\hbar/\Delta x$]")
axR.set_ylabel(r"$|\varphi(p)|^2$")
axR.annotate("", xy=(sp, 0.484), xytext=(-sp, 0.484),
             arrowprops=dict(arrowstyle="<->", color="C3", lw=1.0))
axR.text(0, 0.51, r"$2\,\Delta p = \hbar/\Delta x$",
         ha="center", color="C3", fontsize=10)

for ax_ in (axL, axR):
    ax_.spines[["top","right"]].set_visible(False)
    ax_.set_ylim(bottom=0)
fig.suptitle(r"The Gaussian pair:  $\Delta x\,\Delta p = \hbar/2$, exactly",
             fontsize=11, y=1.02)
fig.tight_layout()
fig.savefig("fig_wavepacket.pdf", bbox_inches="tight")
plt.close(fig)
print("wavepacket written")

# ----------------------------------------------------------------------
# fig_well_tunnel.pdf : (L) infinite-well eigenstates at their energies;
# (R) exact barrier transmission T(E/V0), tunneling + resonances.
# ----------------------------------------------------------------------
fig, (aL, aR) = plt.subplots(1, 2, figsize=(9.6, 3.6))

# Left: box states. Units L=1, E_n = n^2 (in units of E_1).
xw = np.linspace(0, 1, 400)
for n in (1, 2, 3):
    En = n**2
    psi = np.sqrt(2)*np.sin(n*np.pi*xw)
    aL.plot(xw, En + 0.85*psi, color=f"C{n-1}", lw=1.6)
    aL.axhline(En, color=f"C{n-1}", lw=0.6, ls=":")
    aL.text(1.02, En, rf"$n={n}$", va="center", fontsize=10, color=f"C{n-1}")
for xwall in (0, 1):
    aL.axvline(xwall, color="0.2", lw=2.0)
aL.set_xlim(-0.06, 1.14); aL.set_ylim(-0.6, 11.0)
aL.set_xlabel(r"$x/L$")
aL.set_ylabel(r"$E_n/E_1$  (waves offset to their levels)")
aL.set_title(r"Infinite well: $\psi_n \propto \sin(n\pi x/L)$, $E_n = n^2 E_1$",
             fontsize=10)
aL.spines[["top","right"]].set_visible(False)

# Right: exact T(E) for a rectangular barrier, z0 = sqrt(2 m V0) a / hbar = 7
z0 = 7.0
eps = np.linspace(0.01, 3.0, 1200)   # E/V0
T = np.empty_like(eps)
for i, e in enumerate(eps):
    if e < 1.0:
        ka = z0*np.sqrt(1.0 - e)
        T[i] = 1.0/(1.0 + np.sinh(ka)**2/(4*e*(1.0 - e)))
    elif e > 1.0:
        ka = z0*np.sqrt(e - 1.0)
        T[i] = 1.0/(1.0 + np.sin(ka)**2/(4*e*(e - 1.0)))
    else:
        T[i] = 1.0/(1.0 + z0**2/4)
aR.semilogy(eps, T, color="C3", lw=1.6)
aR.axvline(1.0, color="0.5", lw=0.8, ls="--")
aR.text(1.03, 3e-5, r"$E = V_0$", fontsize=9, color="0.4")
aR.set_xlabel(r"$E/V_0$")
aR.set_ylabel(r"$T$")
aR.set_title(r"Barrier transmission, $\sqrt{2mV_0}\,a/\hbar = 7$", fontsize=10)
aR.spines[["top","right"]].set_visible(False)
aR.set_ylim(1e-6, 2)

fig.tight_layout()
fig.savefig("fig_well_tunnel.pdf", bbox_inches="tight")
plt.close(fig)
print("well/tunnel written")

# ----------------------------------------------------------------------
# fig_sho.pdf : (L) SHO eigenfunctions n=0..3 at their levels in the
# parabola; (R) |u_20|^2 vs the classical density -- correspondence.
# Units hbar = m = omega = 1.
# ----------------------------------------------------------------------
from numpy.polynomial.hermite import hermval
from math import factorial

def u_n(n, x):
    c = np.zeros(n+1); c[n] = 1.0
    return hermval(x, c)*np.exp(-x**2/2)/np.sqrt(2.0**n*factorial(n)*np.sqrt(np.pi))

fig, (aL, aR) = plt.subplots(1, 2, figsize=(9.6, 3.7),
                             gridspec_kw={"width_ratios":[1,1.15]})
xs = np.linspace(-4.6, 4.6, 600)
aL.plot(xs, 0.5*xs**2, color="0.35", lw=1.4)
for n in range(4):
    En = n + 0.5
    aL.plot(xs, En + 0.42*u_n(n, xs), color=f"C{n}", lw=1.5)
    aL.axhline(En, color=f"C{n}", lw=0.5, ls=":", alpha=0.8)
    aL.text(4.75, En, rf"$n={n}$", va="center", fontsize=9, color=f"C{n}")
aL.set_xlim(-4.6, 5.9); aL.set_ylim(0, 4.6)
aL.set_xlabel(r"$x\ \ [\sqrt{\hbar/m\omega}\,]$")
aL.set_ylabel(r"$E/\hbar\omega$")
aL.set_title(r"$u_n$ at their levels in $V=\frac{1}{2} m\omega^2x^2$", fontsize=10)
aL.spines[["top","right"]].set_visible(False)

n_big = 20
xb = np.linspace(-7.5, 7.5, 1200)
aR.plot(xb, u_n(n_big, xb)**2, color="C0", lw=1.0,
        label=r"$|u_{20}(x)|^2$")
A = np.sqrt(2*(n_big + 0.5))
xc = np.linspace(-A*0.9995, A*0.9995, 800)
aR.plot(xc, 1/(np.pi*np.sqrt(A**2 - xc**2)), color="C3", lw=1.8, ls="--",
        label=r"classical $\ \frac{1}{\pi\sqrt{A^2-x^2}}$")
aR.set_xlabel(r"$x\ \ [\sqrt{\hbar/m\omega}\,]$")
aR.set_ylabel("probability density")
aR.set_ylim(0, 0.34)
aR.legend(frameon=False, fontsize=9, loc="upper center")
aR.set_title(r"$n=20$: quantum ripples on the classical density", fontsize=10)
aR.spines[["top","right"]].set_visible(False)

fig.tight_layout()
fig.savefig("fig_sho.pdf", bbox_inches="tight")
plt.close(fig)
print("sho written")

# ----------------------------------------------------------------------
# fig_paths.pdf : the sum over paths -- many contributing paths from
# (x_a,0) to (x_b,T); classical (stationary-S) path highlighted.
# ----------------------------------------------------------------------
rng = np.random.default_rng(7)
fig, ax = plt.subplots(figsize=(6.4, 4.0))
T = 1.0; xa, xb = 0.0, 1.0
ts = np.linspace(0, T, 200)

for k in range(14):
    # smooth Brownian-bridge-like wiggle: random Fourier sine series
    wig = np.zeros_like(ts)
    for n in range(1, 7):
        wig += rng.normal(0, 0.16/n) * np.sin(n*np.pi*ts/T)
    ax.plot(ts, xa + (xb-xa)*ts/T + wig, color="C0", lw=0.8, alpha=0.45)

ax.plot(ts, xa + (xb-xa)*ts/T, color="C3", lw=2.4,
        label=r"classical path: $\delta S = 0$")
ax.plot([0, T], [xa, xb], "o", color="0.15", ms=6, zorder=5)
ax.text(-0.02, xa-0.06, r"$(x_a,\,0)$", ha="right", fontsize=11)
ax.text(T+0.02, xb+0.03, r"$(x_b,\,T)$", ha="left", fontsize=11)
ax.text(0.52, 0.28, r"each path: weight $\mathrm{e}^{\mathrm{i}S[x]/\hbar}$",
        color="C0", fontsize=10)
ax.set_xlabel(r"$t$"); ax.set_ylabel(r"$x$")
ax.set_xlim(-0.14, 1.18); ax.set_ylim(-0.35, 1.45)
ax.legend(frameon=False, loc="upper left", fontsize=10)
ax.spines[["top","right"]].set_visible(False)
fig.tight_layout()
fig.savefig("fig_paths.pdf", bbox_inches="tight")
plt.close(fig)
print("paths written")

# ----------------------------------------------------------------------
# fig_ylm.pdf : polar profiles r(theta) = |Y_lm(theta)|^2 for l<=2
# (phi-independent), exact closed forms, drawn in the x-z plane.
# ----------------------------------------------------------------------
th = np.linspace(0, 2*np.pi, 720)   # full plane cut
def Y2(l, m, t):
    c, s = np.cos(t), np.sin(t)
    if (l, m) == (0, 0): return np.full_like(t, 1/(4*np.pi))
    if (l, m) == (1, 0): return 3/(4*np.pi)*c**2
    if (l, abs(m)) == (1, 1): return 3/(8*np.pi)*s**2
    if (l, m) == (2, 0): return 5/(16*np.pi)*(3*c**2 - 1)**2
    if (l, abs(m)) == (2, 1): return 15/(8*np.pi)*(s*c)**2
    if (l, abs(m)) == (2, 2): return 15/(32*np.pi)*s**4

panels = [(0,0),(1,0),(1,1),(2,0),(2,1),(2,2)]
fig, axes = plt.subplots(2, 3, figsize=(9.0, 6.0),
                         subplot_kw={"projection":"polar"})
for ax_, (l, m) in zip(axes.flat, panels):
    r = Y2(l, m, th)
    ax_.plot(th, r, color="C0", lw=1.5)
    ax_.fill(th, r, color="C0", alpha=0.15)
    ax_.set_theta_zero_location("N")   # theta measured from +z
    ax_.set_theta_direction(-1)
    ax_.set_xticks([]); ax_.set_yticks([])
    lbl = rf"$|Y_{{{l}{m}}}|^2$" if m == 0 else rf"$|Y_{{{l},\pm{m}}}|^2$"
    ax_.set_title(lbl, fontsize=11, pad=8)
fig.suptitle(r"Angular shapes: $r(\theta)=|Y_{\ell m}(\theta,\varphi)|^2$"
             r"  ($\varphi$-independent), $z$ upward", fontsize=11)
fig.tight_layout()
fig.savefig("fig_ylm.pdf", bbox_inches="tight")
plt.close(fig)
print("ylm written")

# ----------------------------------------------------------------------
# fig_hydrogen.pdf : radial probability densities P_nl(r) = r^2 R_nl^2
# for n = 1..3, exact Laguerre closed forms (units a0 = 1), with a
# numeric normalization audit printed for each curve.
# ----------------------------------------------------------------------
def R_nl(n, l, r):
    if (n,l)==(1,0): return 2*np.exp(-r)
    if (n,l)==(2,0): return (1/(2*np.sqrt(2)))*(2-r)*np.exp(-r/2)
    if (n,l)==(2,1): return (1/(2*np.sqrt(6)))*r*np.exp(-r/2)
    if (n,l)==(3,0): return (2/(81*np.sqrt(3)))*(27-18*r+2*r**2)*np.exp(-r/3)
    if (n,l)==(3,1): return (4/(81*np.sqrt(6)))*(6-r)*r*np.exp(-r/3)
    if (n,l)==(3,2): return (4/(81*np.sqrt(30)))*r**2*np.exp(-r/3)

r = np.linspace(0, 40, 6000)
fig, ax = plt.subplots(figsize=(7.6, 4.2))
styles = {1:"-", 2:"-", 3:"-"}
for (n,l),col in zip([(1,0),(2,0),(2,1),(3,0),(3,1),(3,2)],
                     ["C0","C1","C2","C3","C4","C5"]):
    P = r**2*R_nl(n,l,r)**2
    norm = np.trapezoid(P, r)
    print(f"  norm check (n,l)=({n},{l}): {norm:.6f}")
    ax.plot(r, P, color=col, lw=1.5,
            label=rf"$({n},{l})$")
ax.set_xlabel(r"$r/a_0$")
ax.set_ylabel(r"$P_{n\ell}(r) = r^2\,|R_{n\ell}|^2$   $[a_0^{-1}]$")
ax.legend(frameon=False, fontsize=9, ncols=3, title=r"$(n,\ell)$",
          title_fontsize=9)
ax.spines[["top","right"]].set_visible(False)
ax.set_xlim(0, 30); ax.set_ylim(bottom=0)
fig.tight_layout()
fig.savefig("fig_hydrogen.pdf", bbox_inches="tight")
plt.close(fig)
print("hydrogen written")
