"""
piad_risk_scorer.py
===================
Dual-use risk scoring using the PIAD framework.

Reproduces Table V from:
  Regmi, R. "Artificial Intelligence for WMD Threat Prevention:
  A Technical Assessment Framework." 2026.

Model
-----
    R = P × I × A × D

where each factor is rated 1–3:
    P  Probability of misuse (1=Low, 2=Medium, 3=High)
    I  Impact severity      (1=Low, 2=Medium, 3=High)
    A  AI acceleration      (1=Low, 2=Medium, 3=High)
    D  Detectability (inverse, 1=Easy to detect, 3=Hard)

Tier boundaries:
    High   R ≥ 27
    Medium 9 ≤ R ≤ 26
    Low    R < 9

Usage:
    python piad_risk_scorer.py

Author: Raman Regmi (ramanregmi@proton.me)
Repo:   https://github.com/ramanregmi/nbc-ai-dalm-2026
"""

from dataclasses import dataclass
from typing import Literal

Tier = Literal["High", "Medium", "Low"]

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Category:
    name: str
    domain: str   # "Nuclear/Radiological", "Biological", or "Chemical"
    P: int        # 1–3
    I: int        # 1–3
    A: int        # 1–3
    D: int        # 1–3

    @property
    def R(self) -> int:
        return self.P * self.I * self.A * self.D

    @property
    def tier(self) -> Tier:
        r = self.R
        if r >= 27:
            return "High"
        elif r >= 9:
            return "Medium"
        else:
            return "Low"


# ---------------------------------------------------------------------------
# 18 AI-enabled dual-use categories (Table V / tab:piad values)
# ---------------------------------------------------------------------------
CATEGORIES = [
    # High Risk (7)
    Category("Protein structure prediction",         "Bio",  P=3, I=3, A=2, D=3),
    Category("Generative chemistry (novel agents)",  "Chem", P=3, I=3, A=2, D=3),
    Category("Genomic sequence analysis",            "Bio",  P=3, I=3, A=2, D=3),
    Category("LLM synthesis / protocol guidance",   "Multi", P=3, I=3, A=3, D=2),
    Category("Autonomous drone navigation",          "Multi", P=3, I=3, A=2, D=3),
    Category("Deepfake / disinformation generation","Multi", P=3, I=2, A=3, D=3),
    Category("De novo pathogen design",              "Bio",  P=3, I=3, A=2, D=3),   # A revised to 2 (2025-26 landscape)

    # Medium Risk (8)
    Category("Satellite imagery analysis",           "N/R",  P=2, I=2, A=3, D=2),
    Category("Spectral / sensor analysis",           "Chem", P=2, I=2, A=2, D=3),
    Category("Atmospheric dispersion modelling",     "Chem", P=2, I=3, A=2, D=2),
    Category("NLP open-source intelligence",         "Multi",P=2, I=2, A=3, D=2),
    Category("Supply-chain anomaly detection",       "Multi",P=2, I=2, A=3, D=2),
    Category("Graph neural networks (precursors)",   "Chem", P=2, I=2, A=2, D=3),
    Category("Reinforcement learning (simulation)",  "Multi",P=2, I=2, A=2, D=3),
    Category("Isotope / forensic classification",    "N/R",  P=1, I=3, A=2, D=3),

    # Low Risk (3)
    Category("Seismic event classification",         "N/R",  P=1, I=2, A=2, D=2),
    Category("Medical triage AI",                    "Bio",  P=1, I=1, A=3, D=2),
    Category("Medical countermeasure allocation",    "Bio",  P=1, I=1, A=3, D=1),
]

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
TIER_COLORS = {"High": "H", "Medium": "M", "Low": "L"}

def main():
    print("=" * 80)
    print("PIAD Dual-Use Risk Scorer — 18 AI-Enabled Categories")
    print("=" * 80)
    print(f"\n{'#':<3} {'Category':<45} {'Dom':<5} {'P':>2} {'I':>2} {'A':>2} {'D':>2} {'R':>4} {'Tier':>7}")
    print("-" * 80)

    tier_counts = {"High": 0, "Medium": 0, "Low": 0}

    for i, cat in enumerate(CATEGORIES, 1):
        print(
            f"{i:<3} {cat.name:<45} {cat.domain[:3]:<5} "
            f"{cat.P:>2} {cat.I:>2} {cat.A:>2} {cat.D:>2} "
            f"{cat.R:>4} {cat.tier:>7}"
        )
        tier_counts[cat.tier] += 1

    print("-" * 80)
    print(f"\nTier summary:  High={tier_counts['High']}  Medium={tier_counts['Medium']}  Low={tier_counts['Low']}")
    print("Expected (paper Table V): High=7, Medium=8, Low=3")

    # Special check: de novo pathogen design
    de_novo = next(c for c in CATEGORIES if "De novo" in c.name)
    print(f"\nDe novo pathogen design: R = {de_novo.P}×{de_novo.I}×{de_novo.A}×{de_novo.D} = {de_novo.R}  (tier: {de_novo.tier})")
    assert de_novo.R == 54, f"De novo R mismatch: {de_novo.R}"
    assert de_novo.tier == "High"

    # Tier boundary verification
    print("\nTier boundary check:")
    print(f"  R=27 → {classify_r(27)}   (expected High)")
    print(f"  R=26 → {classify_r(26)}   (expected Medium)")
    print(f"  R=9  → {classify_r(9)}    (expected Medium)")
    print(f"  R=8  → {classify_r(8)}    (expected Low)")

    assert tier_counts == {"High": 7, "Medium": 8, "Low": 3}, \
        f"Tier count mismatch: {tier_counts}"
    print("\n✓ All 18 PIAD scores match paper Table V.")


def classify_r(r: int) -> Tier:
    if r >= 27:
        return "High"
    elif r >= 9:
        return "Medium"
    return "Low"


if __name__ == "__main__":
    main()
