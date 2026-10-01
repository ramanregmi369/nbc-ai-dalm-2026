"""
dalm_ala.py
===========
Detection-Attribution Latency Model (DALM) — ALA calculator.

Reproduces Tables II and III and the sensitivity analysis from:
  Regmi, R. "Artificial Intelligence for WMD Threat Prevention:
  A Technical Assessment Framework." 2026.

Model
-----
ALA (Acceleration of Latency to Action) is defined as:

    ALA = (τ_D0 + τ_A0) / (τ_D_ai + τ_A_ai)

where
    τ_D0    baseline detection latency  (hours)
    τ_A0    baseline attribution latency (hours)
    τ_D_ai  AI-assisted detection latency (hours)
    τ_A_ai  AI-assisted attribution latency (hours, back-calculated)

All τ values are expert elicitations (labeled [E] in the paper).
ALA values are therefore [M] (model-derived from expert inputs).

Usage:
    python dalm_ala.py

Author: Raman Regmi (ramanregmi@proton.me)
Repo:   https://github.com/ramanregmi/nbc-ai-dalm-2026
"""

import numpy as np

# ---------------------------------------------------------------------------
# Scenario parameters (Table II)
# ---------------------------------------------------------------------------
# Each entry: (label, tau_D0, tau_A0, tau_D_ai, tau_A_ai)
# All times in hours.
SCENARIOS = [
    # Label                          τ_D0   τ_A0    τ_D_ai  τ_A_ai
    ("Nuclear (smuggling)",           8.0,   72.0,   0.3,    8.2),
    ("Radiological (RDD)",            2.0,  336.0,   0.1,   30.1),
    ("Biological (novel pathogen)",  72.0,  168.0,   6.0,   16.9),
    ("Chemical (nerve agent)",        0.3,   48.0,   0.05,   4.6),
    ("Chemical (industrial)",         0.5,   24.0,   0.1,    2.6),
    ("Biological (known pathogen)",  24.0,   48.0,   2.0,    6.8),
]

# ---------------------------------------------------------------------------
# Sensitivity analysis parameters (Table VI in paper)
# Uses a single representative scenario:
#   Baseline total (τ_D0 + τ_A0) = 432 h
#   τ_A_ai = 26 h held constant across all three rows
# Three AI detection assumptions vary τ_D_ai:
#   Conservative: 50% reduction from baseline τ_D0=96h → τ_D_ai=48h
#   Moderate:     81% reduction                        → τ_D_ai=18h
#   Optimistic:   90% reduction                        → τ_D_ai=10h
# ---------------------------------------------------------------------------
SENSITIVITY_BASELINE_TOTAL = 432.0   # hours (τ_D0 + τ_A0)
SENSITIVITY_TAU_A_AI       = 26.0    # hours (held constant)
SENSITIVITY_SCENARIOS = [
    ("Conservative (50% reduction)", 48.0),   # τ_D_ai
    ("Moderate (81% reduction)",     18.0),
    ("Optimistic (90% reduction)",   10.0),
]

# ---------------------------------------------------------------------------
# Compute ALA
# ---------------------------------------------------------------------------

def compute_ala(tau_D0, tau_A0, tau_D_ai, tau_A_ai):
    """Return ALA ratio."""
    return (tau_D0 + tau_A0) / (tau_D_ai + tau_A_ai)


def main():
    print("=" * 72)
    print("Detection-Attribution Latency Model (DALM)")
    print("=" * 72)

    # --- Table II / III reproduction ---
    print(f"\n{'Scenario':<32} {'τ_D0':>6} {'τ_A0':>7} {'τ_Dai':>6} {'τ_Aai':>6} {'ALA':>7}")
    print("-" * 72)

    alas = []
    for label, td0, ta0, tdai, taai in SCENARIOS:
        ala = compute_ala(td0, ta0, tdai, taai)
        alas.append(ala)
        base_total = td0 + ta0
        ai_total   = tdai + taai
        print(f"{label:<32} {td0:>5.1f}h {ta0:>6.1f}h {tdai:>5.2f}h {taai:>5.1f}h {ala:>6.1f}×")
        # Print row totals (Tab III)
        print(f"  → Baseline total: {base_total:.1f} h  |  AI total: {ai_total:.1f} h")

    mean_ala = np.mean(alas)
    print("-" * 72)
    print(f"\nMean ALA (all 6 scenarios): {mean_ala:.2f}×  (paper states 9.9×)")

    # --- Sensitivity analysis (Table VI) ---
    # Single representative scenario: baseline total = 432 h, τ_A_ai = 26 h fixed.
    print("\n\nSensitivity Analysis (Table VI)")
    print(f"  Baseline total (τ_D0+τ_A0) = {SENSITIVITY_BASELINE_TOTAL} h")
    print(f"  τ_A_ai held constant = {SENSITIVITY_TAU_A_AI} h")
    print("-" * 60)
    print(f"{'AI Detection Assumption':<32} {'τ_D_ai':>7} {'τ_total_ai':>11} {'ALA':>7}")
    print("-" * 60)

    for label, tdai in SENSITIVITY_SCENARIOS:
        tau_total_ai = tdai + SENSITIVITY_TAU_A_AI
        ala_s = SENSITIVITY_BASELINE_TOTAL / tau_total_ai
        print(f"{label:<32} {tdai:>6.0f}h {tau_total_ai:>10.0f}h {ala_s:>6.1f}×")

    print("-" * 60)
    print("\nExpected (paper Table VI):")
    print("  Conservative: 5.8×  |  Moderate: 9.8×  |  Optimistic: 12.0×")

    # Assertions
    assert abs(mean_ala - 9.9) < 0.15, f"Mean ALA out of range: {mean_ala:.2f}"
    ala_cons = SENSITIVITY_BASELINE_TOTAL / (48.0 + SENSITIVITY_TAU_A_AI)
    ala_opt  = SENSITIVITY_BASELINE_TOTAL / (10.0 + SENSITIVITY_TAU_A_AI)
    assert abs(ala_cons - 5.8) < 0.1, f"Conservative ALA mismatch: {ala_cons:.2f}"
    assert abs(ala_opt  - 12.0) < 0.1, f"Optimistic ALA mismatch: {ala_opt:.2f}"
    print("\n✓ ALA values match paper Tables II/III and sensitivity Table VI.")


if __name__ == "__main__":
    main()
