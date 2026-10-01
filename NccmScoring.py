"""
ncmm_scoring.py
================
NBC-AI Capability Maturity Matrix (NCMM) scorer.

Reproduces Table I and domain averages from:
  Regmi, R. "Artificial Intelligence for WMD Threat Prevention:
  A Technical Assessment Framework." 2026.

The NCMM scores 15 AI tasks across three NBC domains using a
5-point scale evaluated on 5 equal-weight pillars:
  P1 Demonstrated Capability
  P2 Deployment Readiness
  P3 Operational Reliability
  P4 Domain Expert Validation
  P5 Governance/Safety Integration

Score rule: lowest pillar level at which ALL 5 criteria are satisfied.

Usage:
    python ncmm_scoring.py

Author: Raman Regmi (ramanregmi@proton.me)
Repo:   https://github.com/ramanregmi/nbc-ai-dalm-2026
"""

import numpy as np

# ---------------------------------------------------------------------------
# Task definitions (15 tasks — exactly as in Table I)
# ---------------------------------------------------------------------------
TASKS = [
    # Intelligence & Warning
    "Satellite imagery",
    "OSINT / text analytics",
    "Supply chain monitoring",
    # Detection & Attribution
    "Physical sensor analysis",
    "Forensic attribution",
    "Facility cyber intrusion",
    # Response & Consequence
    "Countermeasure dev.",
    "Dispersion modelling",
    "Emergency response",
    "Medical triage",
    # Deterrence Support
    "Treaty verification",
    "Scenario wargaming",
    "Deception detection",
    "Force posture opt.",
    "Public communication",
]

# ---------------------------------------------------------------------------
# NCMM scores (Table I values — read directly from LaTeX source)
# Row order matches TASKS above.
# Columns: [N/R score, Bio score, Chem score]
# ---------------------------------------------------------------------------
SCORES = np.array([
    # N/R   Bio   Chem
    [4,     3,    3],   # Satellite imagery
    [3,     4,    3],   # OSINT / text analytics
    [3,     2,    3],   # Supply chain monitoring
    [4,     3,    3],   # Physical sensor analysis
    [3,     2,    2],   # Forensic attribution
    [3,     3,    3],   # Facility cyber intrusion
    [2,     4,    2],   # Countermeasure dev.
    [3,     3,    4],   # Dispersion modelling
    [3,     3,    3],   # Emergency response
    [2,     3,    3],   # Medical triage
    [3,     2,    3],   # Treaty verification
    [3,     2,    2],   # Scenario wargaming
    [2,     2,    2],   # Deception detection
    [3,     2,    2],   # Force posture opt.
    [2,     3,    3],   # Public communication
], dtype=float)

DOMAINS = ["N/R", "Bio", "Chem"]

# ---------------------------------------------------------------------------
# Compute and display
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("NBC-AI Capability Maturity Matrix (NCMM)")
    print("=" * 60)
    print(f"\n{'Task':<42} {'N/R':>4} {'Bio':>4} {'Chem':>5}")
    print("-" * 60)
    for i, task in enumerate(TASKS):
        row = SCORES[i]
        print(f"{task:<42} {row[0]:>4.0f} {row[1]:>4.0f} {row[2]:>5.0f}")

    print("-" * 60)
    domain_means = SCORES.mean(axis=0)
    print(f"\n{'Domain averages (mean over 15 tasks)':<42}", end="")
    for m in domain_means:
        print(f"  {m:.2f}", end="")
    print()

    print("\nExpected (paper Table I caption):")
    print("  N/R = 2.87,  Bio = 2.73,  Chem = 2.73")

    print("\nComputed:")
    for d, m in zip(DOMAINS, domain_means):
        print(f"  {d}  = {m:.4f}  ≈ {m:.2f}")

    assert abs(domain_means[0] - 2.8667) < 0.001, "N/R mean mismatch"
    assert abs(domain_means[1] - 2.7333) < 0.001, "Bio mean mismatch"
    assert abs(domain_means[2] - 2.7333) < 0.001, "Chem mean mismatch"
    print("\n✓ All domain averages match paper values.")

if __name__ == "__main__":
    main()
