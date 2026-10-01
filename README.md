# nbc-ai-dalm-2026
# nbc-ai-dalm-2026

Reproducibility code for:

> Regmi, R. "Artificial Intelligence for WMD Threat Prevention: A Technical Assessment Framework." *IEEE Transactions on Technology and Society* (submitted 2026).

---

## Scripts

| Script | Reproduces |
|--------|-----------|
| `ncmm_scoring.py` | Table I — NCMM domain averages (N/R=2.87, Bio=2.73, Chem=2.73) |
| `dalm_ala.py` | Tables II & III — ALA values and sensitivity analysis (mean 9.9×) |
| `sir_simulation.py` | Figure 2 — SIR epidemic model, 55.3 % harm reduction |
| `piad_risk_scorer.py` | Table V — PIAD dual-use risk scores (7H/8M/3L) |
| `hill_dose_response.py` | Table IV — Hill dose-response (illustrative, EC₅₀=50 ppm) |

---

## Requirements

```
numpy>=1.24
scipy>=1.10
matplotlib>=3.7   # optional, for --plot flags
```

Install:

```bash
pip install numpy scipy matplotlib
```

---

## Usage

```bash
# Run all scripts
python ncmm_scoring.py
python dalm_ala.py
python sir_simulation.py
python piad_risk_scorer.py
python hill_dose_response.py

# SIR and Hill with figures
python sir_simulation.py --plot
python hill_dose_response.py --plot
```

All scripts print expected vs. computed values and assert correctness.

---

## Disclaimer

The Hill dose-response parameters (EC₅₀ = 50 ppm, n = 2) are **purely
illustrative nominal values** and do not correspond to any specific chemical
agent. They must not be used for operational hazard assessment.

---

## Author

Raman Regmi — ramanregmi@proton.me  
Independent researcher

## License

MIT
