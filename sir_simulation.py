"""
sir_simulation.py
=================
SIR epidemic simulation for AI-accelerated biological threat response.

Reproduces Figure 2 and the 55.3 % harm-reduction result from:
  Regmi, R. "Artificial Intelligence for WMD Threat Prevention:
  A Technical Assessment Framework." 2026.

Model
-----
Standard SIR with time-varying transmission β(t):

    dS/dt = -β(t) · S(t) · I(t) / N
    dI/dt =  β(t) · S(t) · I(t) / N  -  γ · I(t)
    dR/dt =  γ · I(t)

After intervention at day t_int:
    β(t) = ε · β₀      (ε = 0.20, i.e., 80 % reduction)

Parameters
----------
R₀       = 2.5   (basic reproduction number)
Tg       = 5 d   (generation time → γ = 1/Tg, β₀ = R₀/Tg)
N        = 100 000
I₀       = 10    (initial infected)
ε        = 0.20  (post-intervention transmission fraction)
t_int_baseline = 5.0 d
t_int_ai       = 2.5 d

Usage:
    python sir_simulation.py

    To display the figure:
        pip install matplotlib
        python sir_simulation.py --plot

Author: Raman Regmi (ramanregmi@proton.me)
Repo:   https://github.com/ramanregmi/nbc-ai-dalm-2026
"""

import argparse
import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
R0  = 2.5
Tg  = 5.0          # days
gamma = 1.0 / Tg
beta0 = R0 * gamma  # = R0 / Tg = 0.5 /day
eps   = 0.20        # post-intervention β multiplier
N     = 100_000
I0    = 10
S0    = N - I0
R_init = 0

T_END = 30.0        # days to simulate
DT    = 0.01        # solver output step (days)


# ---------------------------------------------------------------------------
# ODE right-hand side
# ---------------------------------------------------------------------------

def sir_rhs(t, y, t_int):
    S, I, R = y
    beta = beta0 * (eps if t >= t_int else 1.0)
    dS = -beta * S * I / N
    dI =  beta * S * I / N - gamma * I
    dR =  gamma * I
    return [dS, dI, dR]


# ---------------------------------------------------------------------------
# Run simulation
# ---------------------------------------------------------------------------

def run(t_int, label):
    t_span = (0, T_END)
    t_eval = np.arange(0, T_END + DT, DT)
    sol = solve_ivp(
        sir_rhs,
        t_span,
        [S0, I0, R_init],
        args=(t_int,),
        t_eval=t_eval,
        max_step=0.05,
        method="RK45",
        dense_output=False,
    )
    return sol.t, sol.y[0], sol.y[1], sol.y[2]   # t, S, I, R


def cumulative_infected(S_arr):
    """Total infections = N - S(T_END)  (since S starts at N-I0 ≈ N)."""
    return N - S_arr[-1]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(plot=False):
    t_b, S_b, I_b, R_b = run(t_int=5.0, label="Baseline (day 5)")
    t_a, S_a, I_a, R_a = run(t_int=2.5, label="AI-assisted (day 2.5)")

    cum_base = cumulative_infected(S_b)
    cum_ai   = cumulative_infected(S_a)
    harm_red = (cum_base - cum_ai) / cum_base * 100

    # Peak infected
    peak_base = I_b.max()
    peak_ai   = I_a.max()

    print("=" * 60)
    print("SIR Epidemic Simulation — AI-Accelerated Response")
    print("=" * 60)
    print(f"\nParameters:")
    print(f"  R₀ = {R0},  Tg = {Tg} d,  γ = {gamma:.4f} /d,  β₀ = {beta0:.4f} /d")
    print(f"  ε (post-intervention) = {eps}")
    print(f"  N = {N:,},  I₀ = {I0}")
    print(f"\nResults at t = {T_END:.0f} days:")
    print(f"{'Scenario':<28} {'Cum. infected':>14} {'Peak I(t)':>10}")
    print("-" * 55)
    print(f"{'Baseline (t_int = 5.0 d)':<28} {cum_base:>14,.0f} {peak_base:>10,.0f}")
    print(f"{'AI-assisted (t_int = 2.5 d)':<28} {cum_ai:>14,.0f} {peak_ai:>10,.0f}")
    print("-" * 55)
    print(f"\nHarm reduction (cumulative): {harm_red:.1f} %")
    print(f"Expected (paper):            55.3 %")
    assert abs(harm_red - 55.3) < 1.0, f"Harm reduction mismatch: {harm_red:.1f}%"
    print("\n✓ SIR result matches paper (55.3 % harm reduction).")

    if plot:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("\nmatplotlib not installed — skipping plot.")
            return

        fig, axes = plt.subplots(1, 2, figsize=(11, 4))

        ax = axes[0]
        ax.plot(t_b, I_b, "b-",  label=f"Baseline (t_int=5 d)")
        ax.plot(t_a, I_a, "r--", label=f"AI-assisted (t_int=2.5 d)")
        ax.axvline(5.0, color="blue",  linestyle=":", alpha=0.6, label="Baseline intervention")
        ax.axvline(2.5, color="red",   linestyle=":", alpha=0.6, label="AI intervention")
        ax.set_xlabel("Days")
        ax.set_ylabel("Active infections I(t)")
        ax.set_title("Active infections over time")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

        ax = axes[1]
        cum_b_arr = N - S_b
        cum_a_arr = N - S_a
        ax.plot(t_b, cum_b_arr, "b-",  label="Baseline")
        ax.plot(t_a, cum_a_arr, "r--", label="AI-assisted")
        ax.set_xlabel("Days")
        ax.set_ylabel("Cumulative infected")
        ax.set_title(f"Cumulative infections (harm reduction: {harm_red:.1f} %)")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig("sir_simulation.png", dpi=150)
        print("\nFigure saved to sir_simulation.png")
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SIR epidemic simulation")
    parser.add_argument("--plot", action="store_true", help="Save and display figure")
    args = parser.parse_args()
    main(plot=args.plot)
