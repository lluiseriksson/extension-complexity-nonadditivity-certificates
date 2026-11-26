# Formal Certification of Non-Additivity of Polytope Extension Complexity Under Cartesian Products (`XC-NONADD-CERT-1.0`)

**Author:** Lluis Eriksson  
**License:** `MIT` (code, Lean 4 proofs, certificates, tests); `CC-BY-4.0` (manuscript, figures)  
**Target Preprint:** Minhao Liu, *"Extension complexity is not additive under Cartesian products"*, `arXiv:2611.33631v1` (25 November 2026), disproving Conjecture 1.2 of Grande–Padrol–Sanyal.

## Verification Summary
- **Constructive Lean 4.35.0 kernel** (`lean/ExtensionComplexityNonaddCert.lean`): 18/18 theorems (`0 sorry`, `0` custom axioms, `0 Classical.choice`, `0` warnings).
- **Zero-float exact rational Python verifier** (`src/xc_nonadd_verifier.py`): AST-audited zero-float implementation across 4 modes (exact rank-14 factorization of the $24\times 39$ six-cycle matrix $S$ and rank-27 factorization on all 1,521 columns of $S \otimes_1 S$, Proposition 9 Claims 1–4 exact rational lower-bound contraction budgets, explicit 24D 50-facet 150-vertex rational polytope $P$ with $\operatorname{xc}(P)=40$ and $\operatorname{xc}(P\times P)=79$ + zero-error 7-bit channel saving, and Theorem 2 unbounded linear $\lceil 5n/27\rceil$ and identical-square $\delta(R_t, R_t)\ge t$ deficits).
- **Certificates & Tests:** 16/16 canonical JSON certificates (`certificates/C01`–`C16`), 34/34 pytest unit + forgery + AST checks.

## Replay Commands
```bash
(cd lean && lake build)
python -m src.xc_nonadd_verifier certificates
pytest -q
```
