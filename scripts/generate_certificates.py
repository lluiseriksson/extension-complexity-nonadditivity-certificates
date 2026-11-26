"""Generate all 16 canonical certificates for Paper 88 (XC-NONADD-CERT-1.0)."""

from __future__ import annotations

import json
from pathlib import Path
from src.xc_nonadd_verifier import SCHEMA, verify_certificate


def main() -> None:
    out = Path("certificates")
    out.mkdir(parents=True, exist_ok=True)
    certs = [
        # Mode 1: 6-cycle matrix S (24x39), rank-14 & rank-27 (1521 cols!) factorizations, D functional
        {
            "schema": SCHEMA,
            "id": "C01_six_cycle_S_L1e6_full_1prod",
            "mode": "six_cycle_matrix_factorizations",
            "scale_L": 1000000,
            "verify_one_product_27": True,
            "claimed_ordinary_rank_S": 12,
            "claimed_nonneg_rank_S": 14,
            "claimed_nonneg_rank_S_prod": 27,
        },
        {
            "schema": SCHEMA,
            "id": "C02_six_cycle_S_L2e6",
            "mode": "six_cycle_matrix_factorizations",
            "scale_L": 2000000,
            "verify_one_product_27": False,
            "claimed_ordinary_rank_S": 12,
            "claimed_nonneg_rank_S": 14,
            "claimed_nonneg_rank_S_prod": 27,
        },
        {
            "schema": SCHEMA,
            "id": "C03_six_cycle_S_L1e7",
            "mode": "six_cycle_matrix_factorizations",
            "scale_L": 10000000,
            "verify_one_product_27": False,
            "claimed_ordinary_rank_S": 12,
            "claimed_nonneg_rank_S": 14,
            "claimed_nonneg_rank_S_prod": 27,
        },
        {
            "schema": SCHEMA,
            "id": "C04_six_cycle_S_L5e5",
            "mode": "six_cycle_matrix_factorizations",
            "scale_L": 500000,
            "verify_one_product_27": False,
            "claimed_ordinary_rank_S": 12,
            "claimed_nonneg_rank_S": 14,
            "claimed_nonneg_rank_S_prod": 27,
        },
        # Mode 2: Proposition 9 Claims 1-4 exact rational lower bounds for d=1 and d=2
        {
            "schema": SCHEMA,
            "id": "C05_prop9_d1_L1e6",
            "mode": "lower_bound_proposition9",
            "power_d": 1,
            "scale_L": 1000000,
            "tau": [1, 5000],
            "beta": [1, 200],
            "eps": [2601, 1000000],
            "claim2_probe_bound": [663, 5000],
            "claim3_alternating_bound": [39, 100],
        },
        {
            "schema": SCHEMA,
            "id": "C06_prop9_d2_L1e6_canonical",
            "mode": "lower_bound_proposition9",
            "power_d": 2,
            "scale_L": 1000000,
            "tau": [1, 5000],
            "beta": [1, 200],
            "eps": [5201, 1000000],
            "claim2_probe_bound": [663, 2500],
            "claim3_alternating_bound": [62412, 76523],
        },
        {
            "schema": SCHEMA,
            "id": "C07_prop9_d2_L2e6_tighter",
            "mode": "lower_bound_proposition9",
            "power_d": 2,
            "scale_L": 2000000,
            "tau": [1, 10000],
            "beta": [1, 200],
            "eps": [5201, 2000000],
            "claim2_probe_bound": [1313, 5000],
            "claim3_alternating_bound": [39, 50],
        },
        {
            "schema": SCHEMA,
            "id": "C08_prop9_d1_L5e5",
            "mode": "lower_bound_proposition9",
            "power_d": 1,
            "scale_L": 500000,
            "tau": [1, 2500],
            "beta": [1, 200],
            "eps": [2601, 500000],
            "claim2_probe_bound": [338, 2500],  # wait: 13*(1/2500 + 1/100) = 13*26/2500 = 338/2500 = 169/1250!
            "claim3_alternating_bound": [202878, 497399],
        },
        # Mode 3: Explicit 24D 50-facet 150-vertex polytope P (Eq. 5.3), Thm. 1, Cor. 15, Sec. 7.2
        {
            "schema": SCHEMA,
            "id": "C09_polytope_P_L1e6_cor15_k1",
            "mode": "polytope_p_and_transfer",
            "scale_L": 1000000,
            "claimed_dim": 24,
            "claimed_facets": 50,
            "claimed_vertices": 150,
            "claimed_xc_P": 40,
            "claimed_xc_PP": 79,
            "simplex_k_cor15": 1,
        },
        {
            "schema": SCHEMA,
            "id": "C10_polytope_P_L1e6_cor15_k10",
            "mode": "polytope_p_and_transfer",
            "scale_L": 1000000,
            "claimed_dim": 24,
            "claimed_facets": 50,
            "claimed_vertices": 150,
            "claimed_xc_P": 40,
            "claimed_xc_PP": 79,
            "simplex_k_cor15": 10,
        },
        {
            "schema": SCHEMA,
            "id": "C11_polytope_P_L1e6_channel_k48",
            "mode": "polytope_p_and_transfer",
            "scale_L": 1000000,
            "claimed_dim": 24,
            "claimed_facets": 50,
            "claimed_vertices": 150,
            "claimed_xc_P": 40,
            "claimed_xc_PP": 79,
            "simplex_k_cor15": 48,
        },
        {
            "schema": SCHEMA,
            "id": "C12_polytope_P_L2e6_cor15_k100",
            "mode": "polytope_p_and_transfer",
            "scale_L": 2000000,
            "claimed_dim": 24,
            "claimed_facets": 50,
            "claimed_vertices": 150,
            "claimed_xc_P": 40,
            "claimed_xc_PP": 79,
            "simplex_k_cor15": 100,
        },
        # Mode 4: Theorem 2 unbounded linear deficit ceil(5n/27) and identical square R_t
        {
            "schema": SCHEMA,
            "id": "C13_thm2_linear_n6_sharp",
            "mode": "unbounded_and_square_deficits",
            "submode": "linear_deficit_prop11",
            "num_blocks_n": 6,
            "claimed_rank_M2n": 450,
            "claimed_rank_M3n_lb": 440,
            "claimed_rank_prod_ub": 888,
            "claimed_deficit_lb": 2,
        },
        {
            "schema": SCHEMA,
            "id": "C14_thm2_linear_n27",
            "mode": "unbounded_and_square_deficits",
            "submode": "linear_deficit_prop11",
            "num_blocks_n": 27,
            "claimed_rank_M2n": 2025,
            "claimed_rank_M3n_lb": 1976,
            "claimed_rank_prod_ub": 3996,
            "claimed_deficit_lb": 5,
        },
        {
            "schema": SCHEMA,
            "id": "C15_thm2_square_R3",
            "mode": "unbounded_and_square_deficits",
            "submode": "identical_square_Rt",
            "num_blocks_t": 3,
            "claimed_j_sequence": [2, 4, 12],
            "claimed_cover_Ct": 18,
            "claimed_square_deficit_lb": 3,
        },
        {
            "schema": SCHEMA,
            "id": "C16_thm2_square_R5",
            "mode": "unbounded_and_square_deficits",
            "submode": "identical_square_Rt",
            "num_blocks_t": 5,
            "claimed_j_sequence": [2, 4, 12, 36, 108],
            "claimed_cover_Ct": 162,
            "claimed_square_deficit_lb": 5,
        },
    ]
    # Reduce lowest terms for C08 automatically
    certs[7]["claim2_probe_bound"] = [169, 1250]
    for c in certs:
        verify_certificate(c)
        (out / f"{c['id']}.json").write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")
    print(f"Generated and verified {len(certs)} certificates in {out}")


if __name__ == "__main__":
    main()
