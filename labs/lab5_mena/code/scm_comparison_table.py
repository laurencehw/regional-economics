"""Cross-spec SCM comparison: booktabs LaTeX table + grouped bar chart.

Smoke-test mode generates 3 synthetic summary dicts.
Real mode reads multiple SCM summary JSONs from run_lab5_scm_baseline.py.
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SCM cross-spec comparison table")
    parser.add_argument("--summaries", type=str, nargs="+", default=None,
                        help="SCM summary JSON paths (or glob pattern)")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def synthetic_summaries(seed: int = 42) -> List[Dict]:
    """Generate 3 synthetic SCM summaries with different validity levels."""
    rng = np.random.default_rng(seed)
    specs = [
        {
            "treated_iso3": "YEM", "intervention_year": 2015,
            "donor_count": 9, "pre_year_count": 15, "post_year_count": 10,
            "pre_rmspe": 5.66, "post_rmspe": 17.88,
            "post_pre_rmspe_ratio": 3.16, "mean_post_gap": -14.83,
        },
        {
            "treated_iso3": "SYR", "intervention_year": 2018,
            "donor_count": 9, "pre_year_count": 18, "post_year_count": 7,
            "pre_rmspe": 4.20, "post_rmspe": 6.30,
            "post_pre_rmspe_ratio": 1.50, "mean_post_gap": -3.21,
        },
        {
            "treated_iso3": "LBY", "intervention_year": 2014,
            "donor_count": 9, "pre_year_count": 14, "post_year_count": 11,
            "pre_rmspe": 8.50, "post_rmspe": 5.10,
            "post_pre_rmspe_ratio": 0.60, "mean_post_gap": 2.50,
        },
    ]
    return specs


def resolve_summary_paths(patterns: List[str]) -> List[Path]:
    """Resolve glob patterns to actual JSON paths."""
    paths = []
    for pat in patterns:
        expanded = glob.glob(pat, recursive=True)
        if expanded:
            paths.extend(Path(p) for p in expanded)
        else:
            p = Path(pat)
            if p.exists():
                paths.append(p)
    return sorted(set(paths))


def format_latex_table(specs: List[Dict]) -> str:
    """Format SCM comparison into booktabs LaTeX table."""
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{SCM Baseline Specifications: MENA Conflict Economies}",
        r"\label{tab:scm_comparison}",
        r"\begin{tabular}{lccccccl}",
        r"\toprule",
        (r"Treated & Int.\ Year & Donors & Pre Yrs & "
         r"Pre RMSPE & Post RMSPE & Ratio & Validity \\"),
        r"\midrule",
    ]
    for s in specs:
        ratio = s.get("post_pre_rmspe_ratio")
        if ratio is not None and ratio > 2.0:
            validity = "Strong"
        elif ratio is not None and ratio > 1.0:
            validity = "Moderate"
        else:
            validity = "Weak"

        pre_r = s.get("pre_rmspe", 0)
        post_r = s.get("post_rmspe", 0)
        ratio_str = f"{ratio:.2f}" if ratio is not None else "---"
        lines.append(
            f"{s['treated_iso3']} & {s['intervention_year']} & "
            f"{s['donor_count']} & {s.get('pre_year_count', '---')} & "
            f"{pre_r:.2f} & {post_r:.2f} & {ratio_str} & {validity} \\\\"
        )

    lines += [
        r"\bottomrule",
        (r"\multicolumn{8}{l}{\footnotesize RMSPE = root mean squared prediction error. "
         r"Ratio $>$ 2 indicates strong treatment effect.} \\"),
        r"\end{tabular}",
        r"\end{table}",
    ]
    return "\n".join(lines)


def plot_comparison(specs: List[Dict], output_path: Path) -> None:
    """Grouped bar chart of pre/post RMSPE and ratio by spec."""
    from plotnine import (
        aes, geom_col, geom_hline, geom_text, ggplot, labs,
        position_dodge, scale_fill_manual, theme, element_text,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    rows = []
    for s in specs:
        label = f"{s['treated_iso3']} ({s['intervention_year']})"
        rows.append({"spec": label, "metric": "Pre RMSPE",
                     "value": s.get("pre_rmspe", 0)})
        rows.append({"spec": label, "metric": "Post RMSPE",
                     "value": s.get("post_rmspe", 0)})
    df = pd.DataFrame(rows)

    p = (
        ggplot(df, aes(x="spec", y="value", fill="metric"))
        + geom_col(position=position_dodge(width=0.7), width=0.6)
        + scale_fill_manual(values={"Pre RMSPE": "#377eb8", "Post RMSPE": "#e41a1c"})
        + labs(x="", y="RMSPE", title="SCM Fit: Pre vs. Post RMSPE", fill="")
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
        specs = synthetic_summaries(seed=args.seed)
    else:
        if not args.summaries:
            raise ValueError("Provide --summaries or use --run-smoke-test")
        paths = resolve_summary_paths(args.summaries)
        if not paths:
            raise FileNotFoundError(f"No summary JSONs found for: {args.summaries}")
        specs = []
        for p in paths:
            specs.append(json.loads(p.read_text(encoding="utf-8")))

    # LaTeX table
    tex = format_latex_table(specs)
    tex_path = out_dir / "scm_comparison_table.tex"
    tex_path.write_text(tex, encoding="utf-8")
    print(f"LaTeX table: {tex_path}")

    # Summary JSON
    valid_specs = [
        s for s in specs
        if s.get("post_pre_rmspe_ratio") is not None
        and s["post_pre_rmspe_ratio"] > 2.0
    ]
    summary = {
        "method": "SCM_Comparison",
        "n_specs": len(specs),
        "specs": [
            {
                "treated_iso3": s["treated_iso3"],
                "intervention_year": s["intervention_year"],
                "post_pre_rmspe_ratio": s.get("post_pre_rmspe_ratio"),
                "mean_post_gap": s.get("mean_post_gap"),
            }
            for s in specs
        ],
        "valid_specs": len(valid_specs),
        "smoke_test": args.run_smoke_test,
    }
    summary_path = out_dir / "comparison_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Summary: {summary_path}")

    # Figure (optional — requires plotnine)
    try:
        plot_comparison(specs, out_dir / "scm_comparison.pdf")
    except ImportError:
        print("plotnine not installed — skipping figure generation")


if __name__ == "__main__":
    main()
