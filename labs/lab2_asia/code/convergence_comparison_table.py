"""Publication-quality comparison of the 4 convergence specs.

Produces a scatter plot with regression lines by subgroup,
a booktabs LaTeX table, and a comparison summary JSON.

Smoke-test mode runs the convergence scaffold on synthetic data for 2 specs.
Real mode reads existing spec_results.csv and panel_mapped.csv.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

SUBGROUPS = {
    "NE Asia Core": ["CHN", "JPN", "KOR"],
    "ASEAN-6": ["IDN", "MYS", "PHL", "SGP", "THA", "VNM"],
    "South Asia": ["IND"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convergence comparison table + scatter")
    parser.add_argument("--spec-results", type=str, default=None,
                        help="Path to spec_results.csv from run_real_asia_specs")
    parser.add_argument("--panel", type=str, default=None,
                        help="Path to panel_mapped.csv for scatter plot")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def assign_subgroup(country: str) -> str:
    for group, members in SUBGROUPS.items():
        if country in members:
            return group
    return "Other"


def synthetic_specs(seed: int, output_dir: Path) -> pd.DataFrame:
    """Generate synthetic convergence results for 2 specs by running the scaffold."""
    scaffold = Path(__file__).parent / "lab2_asia_convergence_scaffold.py"
    specs = []
    for spec_id, countries in [("full_panel", None), ("asean_6", ["IDN", "MYS", "PHL", "SGP", "THA", "VNM"])]:
        spec_dir = output_dir / spec_id
        spec_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            sys.executable, str(scaffold),
            "--run-smoke-test",
            "--seed", str(seed),
            "--output-dir", str(spec_dir),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        summary_path = spec_dir / "model_summary.json"
        if summary_path.exists():
            s = json.loads(summary_path.read_text(encoding="utf-8"))
            specs.append({
                "spec_id": spec_id,
                "status": "ok",
                "n_obs": s.get("n_obs", 0),
                "n_countries": s.get("n_countries", 0),
                "beta": s.get("beta", np.nan),
                "se_beta": s.get("se_beta", np.nan),
                "p_value": s.get("p_value", np.nan),
                "convergence_detected": s.get("convergence_detected", False),
                "half_life_years": s.get("half_life_years", np.nan),
            })
    return pd.DataFrame(specs)


def synthetic_panel(seed: int) -> pd.DataFrame:
    """Synthetic panel for scatter plot."""
    rng = np.random.default_rng(seed)
    rows: List[Dict] = []
    for eco in ["CHN", "JPN", "KOR", "IDN", "MYS", "THA", "VNM", "PHL", "SGP", "IND"]:
        base = rng.uniform(10, 14)
        for yr in range(2001, 2020):
            growth = rng.normal(-2 * (base - 12), 3)
            rows.append({
                "country": eco, "year": yr,
                "dva_growth": growth,
                "log_dva_lag": base + rng.normal(0, 0.2),
            })
    return pd.DataFrame(rows)


def format_latex_table(specs_df: pd.DataFrame) -> str:
    """Format spec results into booktabs LaTeX table."""
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Beta-Convergence Estimates: Asian GVC Participation}",
        r"\label{tab:convergence_specs}",
        r"\begin{tabular}{lcccccc}",
        r"\toprule",
        r"Specification & $N$ & Countries & $\hat{\beta}$ & SE & $p$-value & Half-life \\",
        r"\midrule",
    ]
    for _, row in specs_df.iterrows():
        beta_str = f"{row['beta']:.3f}"
        se_str = f"({row['se_beta']:.3f})"
        p_str = f"{row['p_value']:.3f}"
        hl = row.get("half_life_years", np.nan)
        hl_str = f"{hl:.2f}" if pd.notna(hl) and np.isfinite(hl) and hl > 0 else "---"

        stars = ""
        if pd.notna(row["p_value"]):
            if row["p_value"] < 0.01:
                stars = "***"
            elif row["p_value"] < 0.05:
                stars = "**"
            elif row["p_value"] < 0.10:
                stars = "*"

        spec_label = row["spec_id"].replace("_", " ").title()
        lines.append(
            f"{spec_label} & {int(row['n_obs'])} & {int(row['n_countries'])} "
            f"& {beta_str}{stars} & {se_str} & {p_str} & {hl_str} \\\\"
        )
    lines += [
        r"\bottomrule",
        r"\multicolumn{7}{l}{\footnotesize OLS with HC1 robust SE. "
        r"* $p<0.10$, ** $p<0.05$, *** $p<0.01$.} \\",
        r"\end{tabular}",
        r"\end{table}",
    ]
    return "\n".join(lines)


def plot_scatter(panel: pd.DataFrame, output_path: Path) -> None:
    from plotnine import (
        aes, geom_point, geom_smooth, ggplot, labs,
        scale_color_manual, theme, element_text,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    panel = panel.copy()
    if "log_dva_lag" not in panel.columns and "dva_lag" in panel.columns:
        panel = panel[panel["dva_lag"] > 0].copy()
        panel["log_dva_lag"] = np.log(panel["dva_lag"])

    required = {"country", "dva_growth", "log_dva_lag"}
    if not required.issubset(panel.columns):
        print(f"Scatter skipped: missing columns {required - set(panel.columns)}")
        return

    panel["subgroup"] = panel["country"].apply(assign_subgroup)
    panel = panel.dropna(subset=["dva_growth", "log_dva_lag"])

    colors = {"NE Asia Core": "#e41a1c", "ASEAN-6": "#377eb8", "South Asia": "#4daf4a"}
    p = (
        ggplot(panel, aes(x="log_dva_lag", y="dva_growth", color="subgroup"))
        + geom_point(alpha=0.4, size=1.5)
        + geom_smooth(method="lm", se=False, size=1)
        + scale_color_manual(values=colors)
        + labs(
            x="log(DVA Lag)",
            y="DVA Growth (%)",
            title="Beta-Convergence in Asian GVC Participation",
            color="Subgroup",
        )
        + base_theme
        + theme(
            figure_size=(6, 4),
            legend_position="bottom",
            plot_title=element_text(size=11),
        )
    )
    p.save(str(output_path), dpi=300)
    print(f"Scatter saved: {output_path}")


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.run_smoke_test:
        specs_df = synthetic_specs(seed=args.seed, output_dir=out_dir / "_smoke_specs")
        panel = synthetic_panel(seed=args.seed)
    else:
        if not args.spec_results:
            raise ValueError("Provide --spec-results or use --run-smoke-test")
        specs_df = pd.read_csv(args.spec_results)
        panel = pd.read_csv(args.panel) if args.panel else None

    # LaTeX table
    tex = format_latex_table(specs_df)
    tex_path = out_dir / "convergence_table.tex"
    tex_path.write_text(tex, encoding="utf-8")
    print(f"LaTeX table: {tex_path}")

    # Scatter plot
    if panel is not None:
        try:
            plot_scatter(panel, out_dir / "convergence_scatter.pdf")
        except ImportError:
            print("plotnine not installed — skipping scatter plot")

    # Summary JSON
    summary = {
        "method": "Convergence_Comparison",
        "n_specs": int(len(specs_df)),
        "specs": specs_df.to_dict(orient="records"),
        "converging_specs": int(specs_df["convergence_detected"].sum())
        if "convergence_detected" in specs_df.columns else 0,
        "smoke_test": args.run_smoke_test,
    }
    summary_path = out_dir / "comparison_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
