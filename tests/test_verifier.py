"""Comprehensive unit, canonical, forgery, and AST zero-float tests for Paper 88."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import pytest

from src.xc_nonadd_verifier import SCHEMA, verify_certificate, verify_file

REPO_ROOT = Path(__file__).resolve().parent.parent
CERT_DIR = REPO_ROOT / "certificates"
CERT_FILES = sorted(CERT_DIR.glob("*.json"))


def test_sixteen_canonical_certificates_exist() -> None:
    assert len(CERT_FILES) == 16


@pytest.mark.parametrize("cert_path", CERT_FILES, ids=[p.stem for p in CERT_FILES])
def test_canonical_certificate_passes(cert_path: Path) -> None:
    res = verify_file(cert_path)
    assert res["file"] == cert_path.name


def test_zero_float_ast_audit() -> None:
    src_path = REPO_ROOT / "src" / "xc_nonadd_verifier.py"
    tree = ast.parse(src_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            pytest.fail(f"float literal found: {node.value}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
            pytest.fail("float() call found")
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name not in ("math", "cmath", "numpy", "scipy")
        if isinstance(node, ast.ImportFrom):
            assert node.module not in ("math", "cmath", "numpy", "scipy")


def test_reject_wrong_schema() -> None:
    c = json.loads((CERT_DIR / "C01_six_cycle_S_L1e6_full_1prod.json").read_text(encoding="utf-8"))
    c["schema"] = "WRONG"
    with pytest.raises(ValueError, match="schema"):
        verify_certificate(c)


def test_reject_forged_ordinary_rank() -> None:
    c = json.loads((CERT_DIR / "C02_six_cycle_S_L2e6.json").read_text(encoding="utf-8"))
    c["claimed_ordinary_rank_S"] = 14
    with pytest.raises(ValueError):
        verify_certificate(c)


def test_reject_prop9_d3_out_of_range() -> None:
    c = json.loads((CERT_DIR / "C06_prop9_d2_L1e6_canonical.json").read_text(encoding="utf-8"))
    c["power_d"] = 3
    with pytest.raises(ValueError, match="d in \\{1, 2\\}"):
        verify_certificate(c)


def test_reject_forged_prop9_claim3() -> None:
    c = json.loads((CERT_DIR / "C06_prop9_d2_L1e6_canonical.json").read_text(encoding="utf-8"))
    c["claim3_alternating_bound"] = [1, 2]
    with pytest.raises(ValueError, match="Claim 3"):
        verify_certificate(c)


def test_reject_prop9_too_small_L() -> None:
    c = json.loads((CERT_DIR / "C06_prop9_d2_L1e6_canonical.json").read_text(encoding="utf-8"))
    c["scale_L"] = 100
    with pytest.raises(ValueError):
        verify_certificate(c)


def test_reject_non_reduced_rational() -> None:
    c = json.loads((CERT_DIR / "C06_prop9_d2_L1e6_canonical.json").read_text(encoding="utf-8"))
    c["beta"] = [2, 400]
    with pytest.raises(ValueError, match="lowest terms"):
        verify_certificate(c)


def test_reject_forged_polytope_xc() -> None:
    c = json.loads((CERT_DIR / "C09_polytope_P_L1e6_cor15_k1.json").read_text(encoding="utf-8"))
    c["claimed_xc_PP"] = 80
    with pytest.raises(ValueError):
        verify_certificate(c)


def test_reject_forged_polytope_vertices() -> None:
    c = json.loads((CERT_DIR / "C09_polytope_P_L1e6_cor15_k1.json").read_text(encoding="utf-8"))
    c["claimed_vertices"] = 149
    with pytest.raises(ValueError):
        verify_certificate(c)


def test_reject_polytope_small_scale_L() -> None:
    c = json.loads((CERT_DIR / "C09_polytope_P_L1e6_cor15_k1.json").read_text(encoding="utf-8"))
    c["scale_L"] = 10
    with pytest.raises(ValueError, match="scale_L"):
        verify_certificate(c)


def test_reject_polytope_nonpositive_simplex_k() -> None:
    c = json.loads((CERT_DIR / "C09_polytope_P_L1e6_cor15_k1.json").read_text(encoding="utf-8"))
    c["simplex_k_cor15"] = 0
    with pytest.raises(ValueError, match="simplex_k_cor15"):
        verify_certificate(c)


def test_reject_forged_prop11_deficit() -> None:
    c = json.loads((CERT_DIR / "C13_thm2_linear_n6_sharp.json").read_text(encoding="utf-8"))
    c["claimed_deficit_lb"] = 3
    with pytest.raises(ValueError, match="mismatch"):
        verify_certificate(c)


def test_reject_forged_prop11_rank_M3() -> None:
    c = json.loads((CERT_DIR / "C14_thm2_linear_n27.json").read_text(encoding="utf-8"))
    c["claimed_rank_M3n_lb"] = 1977
    with pytest.raises(ValueError, match="mismatch"):
        verify_certificate(c)


def test_reject_forged_Rt_sequence() -> None:
    c = json.loads((CERT_DIR / "C15_thm2_square_R3.json").read_text(encoding="utf-8"))
    c["claimed_j_sequence"] = [2, 4, 10]
    with pytest.raises(ValueError, match="Rt mismatch"):
        verify_certificate(c)


def test_reject_forged_Rt_deficit() -> None:
    c = json.loads((CERT_DIR / "C16_thm2_square_R5.json").read_text(encoding="utf-8"))
    c["claimed_square_deficit_lb"] = 6
    with pytest.raises(ValueError, match="Rt mismatch"):
        verify_certificate(c)


def test_reject_bool_as_int_injection() -> None:
    c = json.loads((CERT_DIR / "C13_thm2_linear_n6_sharp.json").read_text(encoding="utf-8"))
    c["num_blocks_n"] = True
    with pytest.raises(ValueError, match="exact int"):
        verify_certificate(c)


def test_reject_int_as_bool_injection() -> None:
    c = json.loads((CERT_DIR / "C01_six_cycle_S_L1e6_full_1prod.json").read_text(encoding="utf-8"))
    c["verify_one_product_27"] = 1
    with pytest.raises(ValueError, match="bool"):
        verify_certificate(c)
