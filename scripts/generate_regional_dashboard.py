"""Regional Diagnostics Dashboard — standardized 1-page visual summary per Part.

Generates a 5-panel composite figure plus GIS placeholder for each of the
book's six regions.  Panels:
  A: Convergence (β, half-life, σ direction)
  B: Spatial inequality (Gini)
  C: Activity ranking (top/bottom 5 units)
  D: Lab headline result (region-specific)
  E: Services profile (top 5 export categories)
  GIS: Placeholder for future map

Supports two modes:
  1. --run-smoke-test: calibrated synthetic data (no external files needed)
  2. Real mode: reads lab JSON summaries + services CSV
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

# ------------------------------------------------------------------ #
#  Region configuration
# ------------------------------------------------------------------ #

REGIONS: Dict[str, Dict[str, Any]] = {
    "americas": {
        "label": "The Americas",
        "lab": 1,
        "color": "#1b9e77",
        "projection": "Albers Equal-Area Conic",
        "convergence": {
            "beta": -0.025, "se_beta": 0.009,
            "half_life_years": 27.7, "sigma_direction": "declining",
            "sigma_start": 0.50, "sigma_end": 0.38,
        },
        "gini": 0.48,
        "top5": [
            ("United States", 63544), ("Canada", 52144),
            ("Chile", 25155), ("Uruguay", 22800), ("Panama", 18789),
        ],
        "bottom5": [
            ("Haiti", 1815), ("Honduras", 5628),
            ("Nicaragua", 5683), ("Bolivia", 8554), ("Guatemala", 8848),
        ],
        "metric": "GDP per capita (PPP, 2020 USD)",
        "headline": {
            "type": "sar_rho",
            "sar_rho": 0.32, "se_rho": 0.07, "p_value": 0.001,
            "label": "SAR spatial autocorrelation (rho)",
        },
        "services": [
            ("Transport", 132.5), ("Travel", 211.8),
            ("Financial", 165.3), ("ICT", 142.0), ("Business", 118.7),
        ],
    },
    "east_asia": {
        "label": "East Asia and ASEAN",
        "lab": 2,
        "color": "#d95f02",
        "projection": "Lambert Conformal Conic",
        "convergence": {
            "beta": -0.048, "se_beta": 0.015,
            "half_life_years": 14.4, "sigma_direction": "declining",
            "sigma_start": 0.55, "sigma_end": 0.40,
        },
        "gini": 0.42,
        "top5": [
            ("Singapore", 65233), ("Japan", 42248),
            ("South Korea", 44292), ("Brunei", 31086), ("Malaysia", 28364),
        ],
        "bottom5": [
            ("Myanmar", 4792), ("Cambodia", 4246),
            ("Laos", 7829), ("Vietnam", 10583), ("Philippines", 9061),
        ],
        "metric": "GDP per capita (PPP, 2020 USD)",
        "headline": {
            "type": "convergence_scatter",
            "beta": -0.048, "se_beta": 0.015,
            "half_life_years": 14.4,
            "label": "Beta-convergence (electronics GVC corridor)",
        },
        "services": [
            ("Transport", 245.3), ("Travel", 190.7),
            ("ICT", 158.4), ("Financial", 112.6), ("Business", 135.2),
        ],
    },
    "south_asia": {
        "label": "South Asia",
        "lab": 3,
        "color": "#7570b3",
        "projection": "Asia South Lambert Conformal Conic",
        "convergence": {
            "beta": -0.012, "se_beta": 0.008,
            "half_life_years": 57.8, "sigma_direction": "flat",
            "sigma_start": 0.48, "sigma_end": 0.47,
        },
        "gini": 0.52,
        "top5": [
            ("Maldives", 19531), ("Sri Lanka", 13827),
            ("India", 7333), ("Bhutan", 12612), ("Bangladesh", 5733),
        ],
        "bottom5": [
            ("Afghanistan", 2065), ("Nepal", 3877),
            ("Pakistan", 5839), ("Bangladesh", 5733), ("Myanmar", 4792),
        ],
        "metric": "GDP per capita (PPP, 2020 USD)",
        "headline": {
            "type": "hhi_lq",
            "hhi": 0.18, "top_lqs": [
                ("IT Services", 3.2), ("Textiles", 2.8),
                ("Pharmaceuticals", 2.1), ("Gems", 1.9), ("Tea", 1.7),
            ],
            "label": "Industrial concentration (HHI) + top LQs",
        },
        "services": [
            ("ICT", 198.5), ("Business", 87.3),
            ("Transport", 45.2), ("Travel", 38.9), ("Financial", 22.1),
        ],
    },
    "europe": {
        "label": "Europe",
        "lab": 4,
        "color": "#e7298a",
        "projection": "ETRS89 Lambert Azimuthal Equal-Area",
        "convergence": {
            "beta": -0.020, "se_beta": 0.006,
            "half_life_years": 34.7, "sigma_direction": "declining",
            "sigma_start": 0.42, "sigma_end": 0.33,
        },
        "gini": 0.32,
        "top5": [
            ("Luxembourg", 118001), ("Ireland", 99239),
            ("Switzerland", 72874), ("Norway", 67294), ("Denmark", 60908),
        ],
        "bottom5": [
            ("Moldova", 13664), ("Ukraine", 12376),
            ("Albania", 14948), ("North Macedonia", 16253),
            ("Bosnia", 15732),
        ],
        "metric": "GDP per capita (PPP, 2020 USD)",
        "headline": {
            "type": "rdd_tau",
            "tau": 1850, "se_tau": 420, "bandwidth_km": 75,
            "p_value": 0.001,
            "label": "RDD treatment effect at EU border (€/cap)",
        },
        "services": [
            ("Financial", 412.8), ("Transport", 389.1),
            ("Business", 345.6), ("Travel", 298.4), ("ICT", 267.3),
        ],
    },
    "mena": {
        "label": "Middle East and North Africa",
        "lab": 5,
        "color": "#66a61e",
        "projection": "WGS 84 / UTM zone 37N",
        "convergence": {
            "beta": -0.008, "se_beta": 0.011,
            "half_life_years": 86.6, "sigma_direction": "rising",
            "sigma_start": 0.52, "sigma_end": 0.58,
        },
        "gini": 0.55,
        "top5": [
            ("Qatar", 96491), ("UAE", 69901),
            ("Kuwait", 49901), ("Bahrain", 49005), ("Saudi Arabia", 46811),
        ],
        "bottom5": [
            ("Yemen", 2284), ("Syria", 4600),
            ("Sudan", 4120), ("Mauritania", 5834), ("Djibouti", 5689),
        ],
        "metric": "GDP per capita (PPP, 2020 USD)",
        "headline": {
            "type": "scm_gap",
            "mean_post_gap": -4.8, "pre_rmspe": 0.42,
            "treated_unit": "YEM", "intervention_year": 2015,
            "years": list(range(2005, 2023)),
            "gap_values": [
                0.2, -0.1, 0.3, -0.2, 0.1, 0.0, -0.3, 0.2, -0.1, 0.1,
                -4.2, -5.1, -4.8, -5.3, -4.5, -4.9, -5.0, -4.6,
            ],
            "label": "SCM mean post-treatment gap (YEM 2015)",
        },
        "services": [
            ("Transport", 78.9), ("Travel", 62.3),
            ("Financial", 45.1), ("Business", 33.8), ("ICT", 28.4),
        ],
    },
    "africa": {
        "label": "Sub-Saharan Africa",
        "lab": 6,
        "color": "#e6ab02",
        "projection": "Africa Albers Equal-Area Conic",
        "convergence": {
            "beta": -0.005, "se_beta": 0.010,
            "half_life_years": 138.6, "sigma_direction": "rising",
            "sigma_start": 0.58, "sigma_end": 0.63,
        },
        "gini": 0.62,
        "top5": [
            ("Seychelles", 30486), ("Mauritius", 22032),
            ("Botswana", 18113), ("Gabon", 16562), ("South Africa", 14740),
        ],
        "bottom5": [
            ("Burundi", 771), ("Somalia", 1322),
            ("Central African Rep.", 993), ("Mozambique", 1295),
            ("Malawi", 1577),
        ],
        "metric": "GDP per capita (PPP, 2020 USD)",
        "headline": {
            "type": "moran_i",
            "moran_i": 0.34, "p_value": 0.001, "n_units": 48,
            "hh_count": 8, "ll_count": 14, "hl_count": 6, "lh_count": 5,
            "label": "Moran's I (night-lights spatial autocorrelation)",
        },
        "services": [
            ("Transport", 42.1), ("Travel", 35.8),
            ("ICT", 18.3), ("Financial", 14.7), ("Business", 11.2),
        ],
    },
}

VALID_REGIONS = list(REGIONS.keys())


# ------------------------------------------------------------------ #
#  CLI
# ------------------------------------------------------------------ #

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a regional diagnostics dashboard (5 panels + GIS placeholder)"
    )
    parser.add_argument(
        "--region", type=str, required=True,
        choices=VALID_REGIONS,
        help="Region key",
    )
    parser.add_argument("--lab-summary-dir", type=str, default=None,
                        help="Directory containing lab JSON summaries (real mode)")
    parser.add_argument("--services-csv", type=str, default=None,
                        help="CSV with services export data (real mode)")
    parser.add_argument("--output-dir", type=str, default="output/dashboards")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


# ------------------------------------------------------------------ #
#  Synthetic dashboard generation (calibrated per region)
# ------------------------------------------------------------------ #

def synthetic_dashboard(region: str, seed: int = 42) -> Dict[str, Any]:
    """Return a complete dashboard dict from calibrated synthetic values."""
    rng = np.random.default_rng(seed)
    cfg = REGIONS[region]

    conv = cfg["convergence"]
    convergence = {
        "beta": conv["beta"],
        "se_beta": conv["se_beta"],
        "half_life_years": conv["half_life_years"],
        "convergence_detected": conv["beta"] < 0,
        "sigma_start": conv["sigma_start"],
        "sigma_end": conv["sigma_end"],
        "sigma_direction": conv["sigma_direction"],
    }

    top5 = [{"unit": u, "value": v + int(rng.normal(0, 50))}
            for u, v in cfg["top5"]]
    bottom5 = [{"unit": u, "value": v + int(rng.normal(0, 50))}
               for u, v in cfg["bottom5"]]

    inequality = {
        "spatial_gini": cfg["gini"],
        "n_units": len(cfg["top5"]) + len(cfg["bottom5"]),
        "top_unit": cfg["top5"][0][0],
        "bottom_unit": cfg["bottom5"][0][0],
    }

    activity = {
        "metric": cfg["metric"],
        "top_5": top5,
        "bottom_5": bottom5,
    }

    services = [{"category": cat, "value_bn": round(val + float(rng.normal(0, 1)), 1)}
                for cat, val in cfg["services"]]

    return {
        "convergence": convergence,
        "inequality": inequality,
        "activity_ranking": activity,
        "headline": cfg["headline"],
        "services_top5": services,
    }


# ------------------------------------------------------------------ #
#  Real-data loader (reads lab JSON summaries)
# ------------------------------------------------------------------ #

def load_dashboard(region: str, lab_dir: str, services_csv: str | None) -> Dict[str, Any]:
    """Load dashboard panels from real lab JSON outputs + services CSV."""
    import pandas as pd

    lab_path = Path(lab_dir)
    cfg = REGIONS[region]

    # Attempt to load from standardized summary files
    panels = synthetic_dashboard(region)  # start with defaults as fallback

    # Override with real data where available
    for json_file in lab_path.glob("*summary*.json"):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            # Detect convergence results
            if "beta" in data or "convergence" in data:
                conv_src = data.get("convergence", data)
                if "beta" in conv_src:
                    panels["convergence"]["beta"] = conv_src["beta"]
                if "se_beta" in conv_src:
                    panels["convergence"]["se_beta"] = conv_src["se_beta"]
        except (json.JSONDecodeError, KeyError):
            continue

    if services_csv:
        svc_df = pd.read_csv(services_csv)
        if "category" in svc_df.columns and "value_bn" in svc_df.columns:
            top = svc_df.nlargest(5, "value_bn")
            panels["services_top5"] = top[["category", "value_bn"]].to_dict(orient="records")

    return panels


# ------------------------------------------------------------------ #
#  JSON summary builder
# ------------------------------------------------------------------ #

def build_summary(region: str, panels: Dict[str, Any], smoke_test: bool) -> Dict[str, Any]:
    """Assemble the full JSON summary for a region dashboard."""
    cfg = REGIONS[region]
    return {
        "method": "Regional_Diagnostics_Dashboard",
        "region": region,
        "region_label": cfg["label"],
        "lab_number": cfg["lab"],
        "smoke_test": smoke_test,
        **panels,
    }


# ------------------------------------------------------------------ #
#  Matplotlib composite figure
# ------------------------------------------------------------------ #

def plot_dashboard(panels: Dict[str, Any], region: str,
                   output_path: Path) -> None:
    """Render 2×3 matplotlib composite: 5 panels + GIS placeholder."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed — skipping figure generation")
        return

    cfg = REGIONS[region]
    fig, axes = plt.subplots(2, 3, figsize=(10, 6.5))
    fig.suptitle(f"Regional Diagnostics: {cfg['label']}", fontsize=13,
                 fontweight="bold", y=0.98)

    color = cfg["color"]

    # --- Panel A: Convergence dot + whisker ---
    ax = axes[0, 0]
    conv = panels["convergence"]
    beta = conv["beta"]
    se = conv["se_beta"]
    ax.errorbar(0, beta, yerr=1.96 * se, fmt="o", color=color,
                capsize=5, markersize=8, linewidth=2)
    ax.axhline(0, color="#808080", linestyle="--", linewidth=0.7)
    ax.set_xlim(-0.5, 0.5)
    ax.set_xticks([])
    ax.set_ylabel("beta coefficient")
    hl = conv["half_life_years"]
    sigma_dir = conv["sigma_direction"]
    ax.set_title(f"A: Convergence\nbeta={beta:.3f}, t1/2={hl:.0f}y, sigma {sigma_dir}",
                 fontsize=9)

    # --- Panel B: Spatial Gini bar ---
    ax = axes[0, 1]
    gini = panels["inequality"]["spatial_gini"]
    ax.barh(["Spatial\nGini"], [gini], color=color, height=0.4)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Gini coefficient")
    ax.text(gini + 0.02, 0, f"{gini:.2f}", va="center", fontsize=10,
            fontweight="bold")
    ax.set_title("B: Spatial Inequality", fontsize=9)

    # --- Panel C: Activity lollipop ---
    ax = axes[0, 2]
    top5 = panels["activity_ranking"]["top_5"]
    bot5 = panels["activity_ranking"]["bottom_5"]
    names = [d["unit"] for d in reversed(bot5 + top5)]
    values = [d["value"] for d in reversed(bot5 + top5)]
    colors = ["#d62728" if i < 5 else color for i in range(10)]
    ax.barh(range(10), values, color=colors, height=0.6)
    ax.set_yticks(range(10))
    ax.set_yticklabels(names, fontsize=7)
    ax.set_xlabel(panels["activity_ranking"]["metric"], fontsize=7)
    ax.set_title("C: Activity Ranking", fontsize=9)

    # --- Panel D: Lab headline (varies by region) ---
    ax = axes[1, 0]
    hl_data = panels["headline"]
    hl_type = hl_data["type"]

    if hl_type == "sar_rho":
        rho = hl_data["sar_rho"]
        se_r = hl_data["se_rho"]
        ax.errorbar(0, rho, yerr=1.96 * se_r, fmt="s", color=color,
                    capsize=5, markersize=8, linewidth=2)
        ax.axhline(0, color="#808080", linestyle="--", linewidth=0.7)
        ax.set_xlim(-0.5, 0.5)
        ax.set_xticks([])
        ax.set_ylabel("rho")

    elif hl_type == "convergence_scatter":
        rng = np.random.default_rng(99)
        x = rng.uniform(7, 11, 10)
        y = hl_data["beta"] * x + rng.normal(0, 0.5, 10)
        ax.scatter(x, y, color=color, s=30, alpha=0.7)
        xfit = np.linspace(7, 11, 50)
        ax.plot(xfit, hl_data["beta"] * xfit, color=color, linewidth=1.5)
        ax.set_xlabel("ln(initial GDP pc)", fontsize=8)
        ax.set_ylabel("Growth rate", fontsize=8)

    elif hl_type == "hhi_lq":
        lqs = hl_data["top_lqs"]
        names_lq = [lq[0] for lq in reversed(lqs)]
        vals_lq = [lq[1] for lq in reversed(lqs)]
        ax.barh(range(len(lqs)), vals_lq, color=color, height=0.5)
        ax.set_yticks(range(len(lqs)))
        ax.set_yticklabels(names_lq, fontsize=7)
        ax.axvline(1.0, color="#808080", linestyle="--", linewidth=0.7)
        ax.set_xlabel("Location Quotient", fontsize=8)

    elif hl_type == "rdd_tau":
        tau = hl_data["tau"]
        se_t = hl_data["se_tau"]
        ax.errorbar(0, tau, yerr=1.96 * se_t, fmt="D", color=color,
                    capsize=5, markersize=8, linewidth=2)
        ax.axhline(0, color="#808080", linestyle="--", linewidth=0.7)
        ax.set_xlim(-0.5, 0.5)
        ax.set_xticks([])
        ax.set_ylabel("tau (EUR/cap)")

    elif hl_type == "scm_gap":
        years = hl_data["years"]
        gaps = hl_data["gap_values"]
        interv = hl_data["intervention_year"]
        ax.plot(years, gaps, color=color, linewidth=1.5)
        ax.axhline(0, color="#808080", linestyle="--", linewidth=0.7)
        ax.axvline(interv, color="#666666", linestyle=":", linewidth=0.8)
        ax.set_xlabel("Year", fontsize=8)
        ax.set_ylabel("Gap (pp)", fontsize=8)

    elif hl_type == "moran_i":
        rng = np.random.default_rng(77)
        n = hl_data["n_units"]
        x = rng.normal(0, 1, n)
        y = hl_data["moran_i"] * x + rng.normal(0, 0.6, n)
        ax.scatter(x, y, color=color, s=20, alpha=0.6)
        ax.axhline(0, color="#808080", linestyle="--", linewidth=0.5)
        ax.axvline(0, color="#808080", linestyle="--", linewidth=0.5)
        xfit = np.linspace(x.min(), x.max(), 50)
        ax.plot(xfit, hl_data["moran_i"] * xfit, color=color, linewidth=1.2)
        ax.set_xlabel("z (unit value)", fontsize=8)
        ax.set_ylabel("Wz (spatial lag)", fontsize=8)

    ax.set_title(f"D: {hl_data['label']}", fontsize=8)

    # --- Panel E: Services bar ---
    ax = axes[1, 1]
    svc = panels["services_top5"]
    svc_names = [s["category"] for s in reversed(svc)]
    svc_vals = [s["value_bn"] for s in reversed(svc)]
    ax.barh(range(5), svc_vals, color=color, height=0.5)
    ax.set_yticks(range(5))
    ax.set_yticklabels(svc_names, fontsize=8)
    ax.set_xlabel("Exports ($B)", fontsize=8)
    ax.set_title("E: Top 5 Service Exports", fontsize=9)

    # --- Panel F: GIS placeholder ---
    ax = axes[1, 2]
    ax.set_facecolor("#f0f0f0")
    ax.text(0.5, 0.5, f"GIS Map Placeholder\n{cfg['projection']}",
            ha="center", va="center", fontsize=9, color="#808080",
            transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("F: Sub-national Map", fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(str(output_path), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Dashboard figure saved: {output_path}")


# ------------------------------------------------------------------ #
#  Main
# ------------------------------------------------------------------ #

def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    region = args.region

    if args.run_smoke_test:
        panels = synthetic_dashboard(region, seed=args.seed)
        smoke = True
    else:
        if not args.lab_summary_dir:
            raise ValueError("Provide --lab-summary-dir or use --run-smoke-test")
        panels = load_dashboard(region, args.lab_summary_dir, args.services_csv)
        smoke = False

    summary = build_summary(region, panels, smoke_test=smoke)

    # Write JSON
    json_path = output_dir / "dashboard_summary.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Summary JSON: {json_path}")

    # Write figure
    try:
        fig_path = output_dir / f"dashboard_{region}.pdf"
        plot_dashboard(panels, region, fig_path)
    except ImportError:
        print("matplotlib not installed — skipping figure generation")

    # Print key stats
    conv = panels["convergence"]
    print(f"Region: {REGIONS[region]['label']}")
    print(f"  beta={conv['beta']:.3f}, half-life={conv['half_life_years']:.0f}y, "
          f"sigma {conv['sigma_direction']}")
    print(f"  Spatial Gini: {panels['inequality']['spatial_gini']:.2f}")
    print(f"  Headline: {panels['headline']['label']}")


if __name__ == "__main__":
    main()
