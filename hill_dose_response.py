"""
hill_dose_response.py
=====================
Hill dose-response model for illustrative chemical-agent exposure analysis.

Reproduces Table IV from:
  Regmi, R. "Artificial Intelligence for WMD Threat Prevention:
  A Technical Assessment Framework." 2026.

⚠ DISCLAIMER ─────────────────────────────────────────────────────────────
The EC₅₀ = 50 ppm and Hill coefficient n = 2 used here are PURELY
ILLUSTRATIVE NOMINAL values.  They do NOT correspond to any specific
chemical agent and MUST NOT be used for operational hazard assessment.
See paper §IV.C and Table IV caption.
────────────────────────────────────────────────────────────────────────────

Model
-----
Hill dose-response function:

    ψ(C) = Cⁿ / (EC₅₀ⁿ + Cⁿ)

where
    C     = agent concentration (ppm)
    EC₅₀  = 50 ppm  (nominal; purely illustrative)
    n     = 2       (Hill coefficient)

Population exposure estimate:

    Affected = ψ(C) × ρ_pop × A

where
    ρ_pop = 1 000 persons/km²
    A     = 0.5 km²  (affected area)

Usage:
    python hill_dose_response.py

    To display the figure:
        pip install matplotlib
        python hill_dose_response.py --plot

Author: Raman Regmi (ramanregmi@proton.me)
Repo:   https://github.com/ramanregmi/nbc-ai-dalm-2026
"""

import argparse
import numpy as np

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
EC50  = 50.0   # ppm (nominal, illustrative only)
n     = 2.0    # Hill coefficient
RHO   = 1000.0 # persons / km²
AREA  = 0.5    # km²

# Concentration points in Table IV (ppm)
CONCENTRATIONS = [5.0, 10.0, 25.0, 50.0, 75.0, 100.0]


# ---------------------------------------------------------------------------
# Hill function
# ---------------------------------------------------------------------------

def hill(C, ec50=EC50, n_hill=n):
    """Return response fraction ψ ∈ [0, 1]."""
    Cn = C ** n_hill
    return Cn / (ec50 ** n_hill + Cn)


def affected(C):
    """Return estimated affected population."""
    return hill(C) * RHO * AREA


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(plot=False):
    print("=" * 60)
    print("Hill Dose-Response Model (illustrative, EC₅₀ = 50 ppm)")
    print("=" * 60)
    print("\n⚠  Nominal parameters only — not specific to any agent.\n")
    print(f"{'C (ppm)':<12} {'ψ(C)':>8} {'Affected persons':>18}")
    print("-" * 42)

    for C in CONCENTRATIONS:
        psi = hill(C)
        aff = affected(C)
        print(f"{C:<12.1f} {psi:>8.4f} {aff:>18.0f}")

    # Spot-check EC50 point
    psi_ec50 = hill(EC50)
    assert abs(psi_ec50 - 0.5) < 1e-9, f"ψ(EC₅₀) should be 0.5, got {psi_ec50}"
    aff_ec50 = affected(EC50)
    print(f"\nAt C = EC₅₀ = {EC50} ppm:  ψ = {psi_ec50:.4f},  affected ≈ {aff_ec50:.0f}")
    print(f"  (ψ = 0.5 at EC₅₀ by definition ✓)")
    print(f"\n✓ Hill dose-response table reproduced.")

    if plot:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("\nmatplotlib not installed — skipping plot.")
            return

        C_range = np.linspace(0, 200, 400)
        psi_range = hill(C_range)

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(C_range, psi_range * 100, "b-", linewidth=2)
        ax.axhline(50, color="gray", linestyle="--", alpha=0.6)
        ax.axvline(EC50, color="red", linestyle="--", alpha=0.6, label=f"EC₅₀ = {EC50} ppm")
        for C in CONCENTRATIONS:
            ax.scatter([C], [hill(C) * 100], color="black", zorder=5, s=40)
        ax.set_xlabel("Concentration (ppm)")
        ax.set_ylabel("Response ψ(C) (%)")
        ax.set_title(f"Hill dose-response  (EC₅₀={EC50} ppm, n={n})\n"
                     "⚠ Illustrative nominal values only")
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig("hill_dose_response.png", dpi=150)
        print("\nFigure saved to hill_dose_response.png")
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hill dose-response table")
    parser.add_argument("--plot", action="store_true", help="Save and display figure")
    args = parser.parse_args()
    main(plot=args.plot)
