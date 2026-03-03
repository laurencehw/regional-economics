"""Permutation inference plot: RMSPE ratio distribution across in-space placebos.

Smoke-test mode generates a synthetic 10-unit placebo set.
Real mode reads an in-space placebo JSON from run_lab5_scm_robustness.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot in-space placebo RMSPE distribution")
    parser.add_argument("--placebo-json", type=str, default=None,
                        help="In-space placebo JSON (list of dicts)")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def synthetic_placebos(seed: int = 42) -> List[Dict]:
    """Synthetic 10-unit in-space placebo with baseline ratio = 4.0 (rank 1/10)."""
    rng = np.random.default_rng(seed)
    units = ["YEM", "EGY", "JOR", "LBN", "MAR", "SAU", "SYR", "TUN", "IRQ", "LBY"]
    results = []
    for unit in units:
        if unit == "YEM":
            ratio = 4.0
        else:
            ratio = rng.uniform(0.5, 3.0)
        results.append({
            "treated_unit": unit,
            "post_pre_rmspe_ratio": round(ratio, 4),
            "pre_rmspe": round(rng.uniform(1.0, 6.0), 4),
            "post_rmspe": round(ratio * rng.uniform(1.0, 6.0), 4),
            "is_baseline": unit == "YEM",
        })
    return results


def compute_rank_p_value(placebos: List[Dict], baseline_unit: str) -> float | None:
    """Fraction of units with RMSPE ratio >= baseline ratio."""
    ratios = []
    baseline_ratio = None
    for p in placebos:
        r = p.get("post_pre_rmspe_ratio")
        if r is None:
            continue
        ratios.append(r)
        if p["treated_unit"] == baseline_unit:
            baseline_ratio = r
    if baseline_ratio is None or len(ratios) < 2:
        return None
    rank = sum(1 for r in ratios if r >= baseline_ratio)
    return rank / len(ratios)


def plot_distribution(placebos: List[Dict], baseline_unit: str,
                      rank_p: float | None, output_path: Path) -> None:
    from plotnine import (
        aes, geom_col, geom_text, ggplot, labs,
        scale_fill_manual, theme, element_text, coord_flip,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    # Build dataframe sorted by ratio
    rows = []
    for p in placebos:
        ratio = p.get("post_pre_rmspe_ratio")
        if ratio is None:
            continue
        rows.append({
            "unit": p["treated_unit"],
            "ratio": ratio,
            "is_baseline": p.get("is_baseline", p["treated_unit"] == baseline_unit),
        })
    df = pd.DataFrame(rows).sort_values("ratio", ascending=True)
    df["unit"] = pd.Categorical(df["unit"], categories=df["unit"].tolist(), ordered=True)
    df["fill"] = df["is_baseline"].map({True: "Baseline", False: "Placebo"})

    subtitle = f"Rank p-value = {rank_p:.2f}" if rank_p is not None else ""

    p = (
        ggplot(df, aes(x="unit", y="ratio", fill="fill"))
        + geom_col(width=0.7)
        + geom_text(aes(label="ratio"), ha="left", nudge_y=0.05, size=7, format_string="{:.2f}")
        + coord_flip()
        + scale_fill_manual(values={"Baseline": "#e41a1c", "Placebo": "#377eb8"})
        + labs(x="", y="Post/Pre RMSPE Ratio",
               title=f"In-Space Placebo Distribution: {baseline_unit}",
               subtitle=subtitle, fill="")
        + base_theme
        + theme(figure_size=(6, 4), legend_position="bottom",
                plot_title=element_text(size=11))
    )
    p.save(str(output_path), dpi=300)
    print(f"Figure saved: {output_path}")


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.run_smoke_test:
        placebos = synthetic_placebos(seed=args.seed)
    else:
        if not args.placebo_json:
            raise ValueError("Provide --placebo-json or use --run-smoke-test")
        placebos = json.loads(Path(args.placebo_json).read_text(encoding="utf-8"))

    # Identify baseline unit
    baseline_entry = next((p for p in placebos if p.get("is_baseline")), None)
    baseline_unit = baseline_entry["treated_unit"] if baseline_entry else placebos[0]["treated_unit"]
    baseline_ratio = baseline_entry["post_pre_rmspe_ratio"] if baseline_entry else None

    rank_p = compute_rank_p_value(placebos, baseline_unit)

    summary = {
        "method": "Placebo_Distribution",
        "n_placebos": len([p for p in placebos if p.get("post_pre_rmspe_ratio") is not None]),
        "baseline_unit": baseline_unit,
        "baseline_ratio": baseline_ratio,
        "rank_p_value": rank_p,
        "smoke_test": args.run_smoke_test,
    }

    summary_path = out_dir / "placebo_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    plot_distribution(placebos, baseline_unit, rank_p, out_dir / "placebo_distribution.pdf")

    print(f"Summary: {summary_path}")
    print(f"Rank p-value: {rank_p}")


if __name__ == "__main__":
    main()
