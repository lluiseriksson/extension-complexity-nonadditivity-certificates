"""Generate 3 publication-quality figures for Paper 88 (XC-NONADD-CERT-1.0)."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    out = Path("paper/figures")
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.size": 9.5,
        "axes.labelsize": 10,
        "axes.titlesize": 10.5,
        "legend.fontsize": 8.5,
        "figure.dpi": 220,
    })

    # Fig 1: Separation of rank_Q, rect cover, rank_+ on S and S x_1 S, and xc(P), xc(P x P)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.3))
    cats = ["Ordinary\nrank", "Rect.\ncover", r"$\mathrm{rank}_+$" + "\n(exact)"]
    vS = [12, 12, 14]
    vS2 = [24, 24, 27]
    x = np.arange(len(cats))
    w = 0.35
    b1 = ax1.bar(x - w / 2, vS, width=w, color="#1f4e79", label=r"Single matrix $S$")
    b2 = ax1.bar(x + w / 2, vS2, width=w, color="#d95f02", label=r"1-product $S \otimes_1 S$")
    for bars in (b1, b2):
        for b in bars:
            h = b.get_height()
            ax1.text(b.get_x() + b.get_width() / 2, h + 0.5, f"{int(h)}", ha="center", va="bottom", fontsize=8.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cats)
    ax1.set_ylim(0, 32)
    ax1.set_ylabel("Rank / Cover Count")
    ax1.set_title("(a) Beyond Rank & Rectangle Bounds (Rem. 8)")
    ax1.grid(axis="y", alpha=0.25)
    ax1.legend(loc="upper left", frameon=True)

    p_labels = [
        r"$2\,\mathrm{xc}(P)$",
        r"$\mathrm{xc}(P^2)$",
        r"$\mathrm{xc}(P)+$" + "\n" + r"$\mathrm{xc}(P\Delta_{48})$",
        r"$\mathrm{xc}(P^2\Delta_{48})$",
    ]
    p_vals = [80, 79, 129, 128]
    p_cols = ["#7f8c8d", "#2e6b3e", "#7f8c8d", "#1f4e79"]
    bars = ax2.bar(p_labels, p_vals, color=p_cols, width=0.52, edgecolor="#222222")
    for b, v in zip(bars, p_vals):
        ax2.text(b.get_x() + b.get_width() / 2, v + 2.2, f"{v}", ha="center", va="bottom", fontsize=8.5)
    ax2.axhline(128, ls=":", color="#c0392b", lw=1.3, label=r"$2^7 = 128$ (7-bit threshold)")
    ax2.set_ylim(0, 148)
    ax2.set_ylabel("Extension Complexity / Messages")
    ax2.set_title("(b) Thm. 1 & Zero-Error Channel Saving")
    ax2.grid(axis="y", alpha=0.25)
    ax2.legend(loc="upper left", frameon=True)
    fig.tight_layout()
    fig.savefig(out / "fig1_rank_and_polytope_savings.png", dpi=220)
    plt.close(fig)

    # Fig 2: Proposition 9 quantitative threshold budgets vs scale L
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.3))
    Ls = np.logspace(5.2, 7.2, 200)
    # Fix beta = 1/200 => tau = 200 / L
    taus = 200.0 / Ls
    beta = 1.0 / 200.0
    eps_d2 = 1.0 / Ls + 26.0 * taus
    c2_d2 = 26.0 * (taus + 2.0 * beta)
    c3_d2 = 26.0 * np.maximum(6.0 * beta, 6.0 * eps_d2 / (1.0 - eps_d2))
    ax1.semilogx(Ls, c2_d2, lw=2.0, color="#1f4e79", label=r"Claim 2: $26(\tau + 2\beta)$")
    ax1.semilogx(Ls, c3_d2, lw=2.0, color="#c0392b", label=r"Claim 3: $26\max(6\beta, 6\varepsilon/(1-\varepsilon))$")
    ax1.axhline(1.0, ls="--", color="#222222", lw=1.2, label="Threshold $< 1$")
    ax1.scatter([1e6, 2e6], [663 / 2500, 1313 / 5000], color="#1f4e79", s=40, zorder=5)
    ax1.scatter([1e6, 2e6], [62412 / 76523, 39 / 50], color="#c0392b", s=40, zorder=5)
    ax1.set_xlabel(r"Probe scale $L$ (with $\beta = 1/200$)")
    ax1.set_ylabel("Contraction bound")
    ax1.set_title("(a) Prop. 9 Lower-Bound Budgets ($d=2$)")
    ax1.set_ylim(0.15, 1.15)
    ax1.grid(alpha=0.25, which="both")
    ax1.legend(loc="center right", fontsize=8.0, frameon=True)

    # Proposition 11 discrete kernel d * rho^(d-1) for rho=1/2 and rho=3/4
    ds = np.arange(1, 13)
    f_half = ds * (0.5 ** (ds - 1))
    f_3q = ds * (0.75 ** (ds - 1))
    ax2.plot(ds, f_3q, lw=2.0, marker="o", color="#2e6b3e", label=r"$\rho=3/4$: $\max = 27/16$ ($d=3,4$)")
    ax2.plot(ds, f_half, lw=2.0, marker="s", color="#1f4e79", label=r"$\rho=1/2$: $\max = 1$ ($d=1,2$)")
    ax2.axhline(27.0 / 16.0, ls=":", color="#2e6b3e", lw=1.2)
    ax2.set_ylim(-0.05, 2.08)
    ax2.set_xlabel(r"Profile arity $d = |J_z|$")
    ax2.set_ylabel(r"$d\,\rho^{d-1}$")
    ax2.set_title("(b) Prop. 11 Conditional Counting Maximum")
    ax2.grid(alpha=0.25)
    ax2.legend(loc="upper right", frameon=True)
    fig.tight_layout()
    fig.savefig(out / "fig2_prop9_and_counting_kernel.png", dpi=220)
    plt.close(fig)

    # Fig 3: Theorem 2 linear deficit ceil(5n/27) & identical square R_t alphabet growth
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.3))
    ns = np.arange(1, 61)
    defs = np.ceil(5.0 * ns / 27.0)
    ax1.step(ns, defs, where="mid", lw=2.0, color="#1f4e79", label=r"Lower bound $\lceil 5n/27 \rceil$")
    ax1.plot(ns, 5.0 * ns / 27.0, ls="--", color="#c0392b", lw=1.4, label=r"Linear slope $5n/27$")
    ax1.scatter([6, 27], [2, 5], color="#d95f02", s=50, zorder=6, label="Certified C13–C14")
    ax1.set_xlabel(r"Number of coordinate blocks $n$")
    ax1.set_ylabel(r"Guaranteed deficit $\delta(U_n, V_n)$")
    ax1.set_title("(a) Linear-Fraction Deficit (Thm. 2)")
    ax1.grid(alpha=0.25)
    ax1.legend(loc="upper left", frameon=True)

    ts = np.arange(1, 7)
    js = [2]
    for _ in range(1, len(ts)):
        js.append(2 * sum(js))
    cts = np.cumsum(js)
    ax2.semilogy(ts, js, lw=2.0, marker="o", color="#8e44ad", label=r"Hitting size $j_t$ ($j_1=2$, $4\cdot 3^{t-2}$)")
    ax2.semilogy(ts, cts, lw=2.0, marker="s", ls="--", color="#2e6b3e", label=r"Cover number $C_t = \sum j_i$")
    ax2.set_xlabel(r"Guaranteed square deficit $t \leq \delta(R_t, R_t)$")
    ax2.set_ylabel("Alphabet / Cover parameter")
    ax2.set_title(r"(b) Identical-Factor Square $R_t$ (Lem. 12–13)")
    ax2.grid(alpha=0.25, which="both")
    ax2.legend(loc="upper left", frameon=True)
    fig.tight_layout()
    fig.savefig(out / "fig3_unbounded_deficits.png", dpi=220)
    plt.close(fig)
    print("Generated 3 figures for Paper 88.")


if __name__ == "__main__":
    main()
