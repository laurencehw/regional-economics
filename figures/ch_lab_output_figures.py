"""Additional figures for Data in Depth boxes and lab output visualizations.

Generates 19 publication-quality figures using synthetic data that mirrors
the patterns described in each chapter's analytical narrative.

All figures use plotnine + hrbrthemes where suitable, falling back to
matplotlib for specialized layouts (coefficient plots, tables, stacked bars).
"""

from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

from plotnine import (
    ggplot, aes, geom_point, geom_line, geom_smooth, geom_bar,
    geom_col, geom_hline, geom_vline, geom_text, geom_label,
    geom_errorbarh, geom_rect, geom_segment, geom_histogram,
    geom_ribbon, geom_abline, geom_area,
    labs, scale_x_continuous, scale_x_log10, scale_y_continuous,
    scale_y_log10, scale_color_manual, scale_fill_manual,
    coord_flip, facet_wrap, theme, element_text, element_blank,
    element_rect, element_line, annotate,
    position_dodge, position_stack,
)

from figure_utils import (
    FIGSIZE_CONCEPT, FIGSIZE_THEMATIC, DPI, FIGURE_WIDTH,
    QUAL_PALETTE, REGION_COLORS, add_figure_source,
    save_figure, save_summary, add_common_args, get_output_dir,
    get_base_theme,
)

warnings.filterwarnings("ignore", category=FutureWarning)

# Consistent sizing
W = FIGURE_WIDTH  # 6 inches
H_THEMATIC = 4
H_CONCEPT = 4.5


# ================================================================== #
#  Helpers
# ================================================================== #

def _save_plotnine(p, output_dir, stem, width=W, height=H_THEMATIC):
    """Save a plotnine plot as PNG, return paths dict."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{stem}.png"
    p.save(str(path), width=width, height=height, dpi=DPI, verbose=False)
    print(f"  Saved: {path}")
    return {"png": str(path)}


def _save_mpl(fig, output_dir, stem):
    """Save a matplotlib figure as PNG, return paths dict."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{stem}.png"
    fig.savefig(str(path), dpi=DPI, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print(f"  Saved: {path}")
    plt.close(fig)
    return {"png": str(path)}


# ================================================================== #
#  1. Moran Scatter Plot (Ch 3A)
# ================================================================== #

def fig_moran_scatter(output_dir, seed=42):
    """Moran scatter plot with four quadrants labeled HH, HL, LH, LL."""
    rng = np.random.default_rng(seed)

    n = 80
    # Generate spatially correlated data
    y = rng.normal(0, 1, n)
    # Spatial lag correlated with y (rho ~ 0.6)
    wy = 0.6 * y + rng.normal(0, 0.5, n)

    df = pd.DataFrame({"y": y, "wy": wy})

    base = get_base_theme()
    p = (
        ggplot(df, aes("y", "wy"))
        + geom_point(color="#6a9bc3", alpha=0.6, size=2)
        + geom_smooth(method="lm", color="#c44e52", se=False, linetype="solid", size=1)
        + geom_hline(yintercept=0, linetype="dashed", color="#808080", size=0.5)
        + geom_vline(xintercept=0, linetype="dashed", color="#808080", size=0.5)
        + annotate("text", x=2.2, y=2.0, label="HH", size=12, color="#808080", fontstyle="italic")
        + annotate("text", x=-2.2, y=-2.0, label="LL", size=12, color="#808080", fontstyle="italic")
        + annotate("text", x=2.2, y=-1.5, label="HL", size=12, color="#808080", fontstyle="italic")
        + annotate("text", x=-2.2, y=1.5, label="LH", size=12, color="#808080", fontstyle="italic")
        + labs(
            title="Moran Scatter Plot: Spatial Autocorrelation in Regional Output",
            x="Standardized value (y)",
            y="Spatially lagged value (Wy)",
            caption="Source: Synthetic data illustrating positive spatial autocorrelation (Moran's I ≈ 0.6)."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_ch03a_moran_scatter")


# ================================================================== #
#  2. SAR Coefficient Plot (Ch 3A)
# ================================================================== #

def fig_sar_coefficients(output_dir, seed=42):
    """Coefficient plot for SAR model with CIs."""
    coefs = pd.DataFrame({
        "variable": [
            "Spatial lag (ρ)", "ln(K/L)", "Human capital",
            "Trade openness", "Urbanization", "Institutions"
        ],
        "estimate": [0.35, 0.28, 0.19, 0.12, 0.08, 0.15],
        "se": [0.06, 0.05, 0.04, 0.05, 0.03, 0.04],
    })
    coefs["lo"] = coefs["estimate"] - 1.96 * coefs["se"]
    coefs["hi"] = coefs["estimate"] + 1.96 * coefs["se"]
    # Order
    coefs["variable"] = pd.Categorical(
        coefs["variable"], categories=coefs["variable"].tolist()[::-1], ordered=True
    )

    base = get_base_theme()
    p = (
        ggplot(coefs, aes(y="variable", x="estimate"))
        + geom_vline(xintercept=0, linetype="dashed", color="#808080", size=0.5)
        + geom_errorbarh(aes(xmin="lo", xmax="hi"), height=0.2, color="#6a9bc3", size=0.8)
        + geom_point(color="#c44e52", size=3)
        + labs(
            title="SAR Model Estimates: Regional Growth Determinants",
            x="Coefficient estimate (95% CI)",
            y="",
            caption="Source: Illustrative SAR estimates; N = 265 regions, pseudo-R² = 0.72."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_ch03a_sar_coefficients")


# ================================================================== #
#  3. Distance Decay / Gravity (Ch 3B)
# ================================================================== #

def fig_distance_decay(output_dir, seed=42):
    """Log-log trade vs distance scatter with gravity fit."""
    rng = np.random.default_rng(seed)
    n = 200
    ln_dist = rng.uniform(4, 10, n)  # ln(km)
    ln_trade = 18 - 1.1 * ln_dist + rng.normal(0, 1.2, n)
    # Some zeros removed (log scale)

    df = pd.DataFrame({"ln_distance": ln_dist, "ln_trade": ln_trade})

    base = get_base_theme()
    p = (
        ggplot(df, aes("ln_distance", "ln_trade"))
        + geom_point(color="#6a9bc3", alpha=0.4, size=1.5)
        + geom_smooth(method="lm", color="#c44e52", se=True, size=1, alpha=0.15)
        + labs(
            title="Distance Decay in Bilateral Trade Flows",
            x="ln(Distance, km)",
            y="ln(Trade flow, USD)",
            caption="Source: Synthetic bilateral trade data; slope ≈ −1.1 (gravity elasticity)."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_ch03b_distance_decay")


# ================================================================== #
#  4. PPML vs OLS Gravity Coefficients (Ch 3B)
# ================================================================== #

def fig_ppml_vs_ols(output_dir, seed=42):
    """Side-by-side coefficient comparison of PPML vs OLS gravity."""
    coefs = pd.DataFrame({
        "variable": ["ln(Distance)", "ln(GDP_i)", "ln(GDP_j)", "Contiguity", "Common lang."] * 2,
        "estimator": (["OLS (log-linear)"] * 5) + (["PPML"] * 5),
        "estimate": [
            -1.42, 0.95, 0.88, 0.52, 0.35,   # OLS
            -0.93, 0.78, 0.74, 0.41, 0.28,    # PPML
        ],
        "se": [
            0.08, 0.04, 0.04, 0.12, 0.10,
            0.06, 0.03, 0.03, 0.09, 0.08,
        ],
    })
    coefs["lo"] = coefs["estimate"] - 1.96 * coefs["se"]
    coefs["hi"] = coefs["estimate"] + 1.96 * coefs["se"]
    coefs["variable"] = pd.Categorical(
        coefs["variable"],
        categories=["Common lang.", "Contiguity", "ln(GDP_j)", "ln(GDP_i)", "ln(Distance)"],
        ordered=True,
    )

    base = get_base_theme()
    p = (
        ggplot(coefs, aes(y="variable", x="estimate", color="estimator"))
        + geom_vline(xintercept=0, linetype="dashed", color="#808080", size=0.5)
        + geom_errorbarh(
            aes(xmin="lo", xmax="hi"),
            height=0.25, size=0.7,
            position=position_dodge(width=0.5),
        )
        + geom_point(size=2.5, position=position_dodge(width=0.5))
        + scale_color_manual(values=["#c44e52", "#6a9bc3"])
        + labs(
            title="Gravity Estimates: OLS vs. PPML",
            x="Coefficient (95% CI)",
            y="",
            color="Estimator",
            caption="Source: Illustrative; PPML attenuates distance elasticity (Santos Silva & Tenreyro 2006)."
        )
        + base
        + theme(
            plot_title=element_text(size=10, face="bold"),
            legend_position="bottom",
        )
    )
    return _save_plotnine(p, output_dir, "fig_ch03b_ppml_vs_ols")


# ================================================================== #
#  5. Inverted-U Deindustrialization (Ch 5)
# ================================================================== #

def fig_inverted_u(output_dir, seed=42):
    """Manufacturing share vs GDP/capita with quadratic fit."""
    rng = np.random.default_rng(seed)
    n = 45
    ln_gdppc = rng.uniform(6.0, 11.5, n)
    # Inverted U peaking around ln(GDP/cap) ~ 8.8
    peak = 8.8
    mfg = 22 - 2.0 * (ln_gdppc - peak)**2 + rng.normal(0, 2.5, n)
    mfg = np.clip(mfg, 2, 35)

    labels = [
        "ETH", "BGD", "VNM", "IND", "IDN", "CHN", "THA", "MYS",
        "MEX", "BRA", "TUR", "POL", "KOR", "CZE", "DEU", "JPN",
        "USA", "GBR", "FRA", "ITA", "ESP", "AUS", "CAN", "NLD",
        "SGP", "HKG", "PHL", "PAK", "NGA", "KEN", "GHA", "ZAF",
        "COL", "PER", "CHL", "ARG", "SAU", "ARE", "EGY", "MAR",
        "ROU", "HUN", "SWE", "NOR", "FIN",
    ]

    df = pd.DataFrame({
        "ln_gdppc": ln_gdppc,
        "mfg_share": mfg,
        "label": labels[:n],
    })

    base = get_base_theme()
    p = (
        ggplot(df, aes("ln_gdppc", "mfg_share"))
        + geom_point(color="#6a9bc3", alpha=0.6, size=2)
        + geom_text(aes(label="label"), size=6, nudge_y=1.2, color="#808080")
        + geom_smooth(method="lm", formula="y ~ x + I(x**2)",
                      color="#c44e52", se=True, alpha=0.12, size=1)
        + labs(
            title="Premature Deindustrialization: The Inverted U",
            x="ln(GDP per capita, PPP USD)",
            y="Manufacturing share of GDP (%)",
            caption="Source: Synthetic cross-section; quadratic fit illustrates Rodrik (2016) pattern."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_ch05_inverted_u")


# ================================================================== #
#  6. DVA Decomposition Stacked Bar (Ch 6)
# ================================================================== #

def fig_dva_decomposition(output_dir, seed=42):
    """Stacked bar of domestic VA decomposition for East Asian economies."""
    countries = ["Japan", "Korea", "Taiwan", "China", "Vietnam"]
    dva = [82, 65, 55, 72, 48]
    fva = [10, 22, 30, 18, 38]
    dbl = [8, 13, 15, 10, 14]

    rows = []
    for i, c in enumerate(countries):
        rows.append({"country": c, "component": "Domestic VA", "share": dva[i]})
        rows.append({"country": c, "component": "Foreign VA", "share": fva[i]})
        rows.append({"country": c, "component": "Double-counted", "share": dbl[i]})

    df = pd.DataFrame(rows)
    df["country"] = pd.Categorical(df["country"], categories=countries, ordered=True)
    df["component"] = pd.Categorical(
        df["component"],
        categories=["Double-counted", "Foreign VA", "Domestic VA"],
        ordered=True,
    )

    base = get_base_theme()
    p = (
        ggplot(df, aes(x="country", y="share", fill="component"))
        + geom_col(position=position_stack(), width=0.65)
        + scale_fill_manual(values=["#808080", "#c44e52", "#6a9bc3"])
        + labs(
            title="Domestic Value-Added Decomposition: East Asian Electronics",
            x="",
            y="Share of gross exports (%)",
            fill="Component",
            caption="Source: Synthetic data based on TiVA/WIOD patterns; Koopman, Wang & Wei (2014)."
        )
        + base
        + theme(
            plot_title=element_text(size=10, face="bold"),
            legend_position="bottom",
        )
    )
    return _save_plotnine(p, output_dir, "fig_ch06_dva_decomposition")


# ================================================================== #
#  7. China Provincial Gini (Ch 7)
# ================================================================== #

def fig_provincial_gini(output_dir, seed=42):
    """Interprovincial Gini coefficient over time."""
    years = np.arange(1990, 2024)
    # Rise from ~0.35 to ~0.45 by 2005, then plateau/slight decline
    t = (years - 1990) / (2023 - 1990)
    gini = 0.34 + 0.12 * (1 - np.exp(-4 * t)) - 0.02 * np.maximum(t - 0.5, 0)
    rng = np.random.default_rng(seed)
    gini += rng.normal(0, 0.003, len(years))

    df = pd.DataFrame({"year": years, "gini": gini})

    base = get_base_theme()
    p = (
        ggplot(df, aes("year", "gini"))
        + geom_line(color="#c44e52", size=1.2)
        + geom_point(color="#c44e52", size=1.5, alpha=0.6)
        + labs(
            title="China's Interprovincial Inequality, 1990–2023",
            x="",
            y="Gini coefficient (provincial GDP per capita)",
            caption="Source: Synthetic trajectory based on NBS/Kanbur & Zhang (2005) patterns."
        )
        + scale_y_continuous(limits=[0.30, 0.50])
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_ch07_provincial_gini")


# ================================================================== #
#  8. EU Convergence Fan (Ch 9)
# ================================================================== #

def fig_convergence_fan(output_dir, seed=42):
    """GDP/capita relative to EU average for cohesion countries."""
    years = np.arange(1990, 2024)
    rng = np.random.default_rng(seed)
    t = years - 1990

    # Relative GDP per capita (EU avg = 100)
    ireland = 70 + 2.5 * t + 0.05 * t**1.3 + rng.normal(0, 2, len(t))
    spain = 78 + 0.5 * t - 0.005 * t**1.5 + rng.normal(0, 1.5, len(t))
    portugal = 65 + 0.3 * t - 0.003 * t**1.5 + rng.normal(0, 1.5, len(t))
    greece = 68 + 0.4 * t - 0.02 * t**1.5 + rng.normal(0, 2, len(t))

    rows = []
    for yr, ie, es, pt, gr in zip(years, ireland, spain, portugal, greece):
        rows.append({"year": yr, "country": "Ireland", "gdp_rel": ie})
        rows.append({"year": yr, "country": "Spain", "gdp_rel": es})
        rows.append({"year": yr, "country": "Portugal", "gdp_rel": pt})
        rows.append({"year": yr, "country": "Greece", "gdp_rel": gr})

    df = pd.DataFrame(rows)

    base = get_base_theme()
    p = (
        ggplot(df, aes("year", "gdp_rel", color="country"))
        + geom_line(size=1)
        + geom_hline(yintercept=100, linetype="dashed", color="#808080", size=0.5)
        + annotate("text", x=2020, y=102, label="EU average", size=7, color="#808080")
        + scale_color_manual(values=["#808080", "#6a9bc3", "#c44e52", "#7dab6e"])
        + labs(
            title="EU Cohesion Country Convergence, 1990–2023",
            x="",
            y="GDP per capita (EU avg = 100)",
            color="",
            caption="Source: Synthetic data based on Eurostat patterns; Ireland's Celtic Tiger divergence visible."
        )
        + base
        + theme(
            plot_title=element_text(size=10, face="bold"),
            legend_position="bottom",
        )
    )
    return _save_plotnine(p, output_dir, "fig_ch09_convergence_fan")


# ================================================================== #
#  9. Mezzogiorno Gap (Ch 10)
# ================================================================== #

def fig_mezzogiorno_gap(output_dir, seed=42):
    """Mezzogiorno GDP/capita as % of Centre-North, 1950-2023."""
    years = np.arange(1950, 2024)
    rng = np.random.default_rng(seed)
    t = (years - 1950) / (2023 - 1950)
    # Rise from ~45% to ~58% by 1975, then stagnate at ~55-60%
    ratio = 45 + 15 * (1 - np.exp(-3 * t)) - 2 * np.sin(2 * np.pi * t * 2)
    ratio += rng.normal(0, 0.8, len(years))

    df = pd.DataFrame({"year": years, "ratio": ratio})

    base = get_base_theme()
    p = (
        ggplot(df, aes("year", "ratio"))
        + geom_line(color="#c44e52", size=1)
        + geom_hline(yintercept=100, linetype="dotted", color="#808080", size=0.5)
        + annotate("text", x=1985, y=62, label="Parity = 100",
                   size=7, color="#808080")
        + annotate("rect", xmin=1950, xmax=1975, ymin=42, ymax=65,
                   alpha=0.06, fill="#6a9bc3")
        + annotate("text", x=1962, y=43, label="Cassa per il\nMezzogiorno era",
                   size=6, color="#6a9bc3")
        + labs(
            title="The Persistent Mezzogiorno Gap, 1950–2023",
            x="",
            y="Mezzogiorno GDP/capita as % of Centre-North",
            caption="Source: Synthetic trajectory based on ISTAT/Daniele & Malanima (2007) patterns."
        )
        + scale_y_continuous(limits=[40, 70])
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_ch10_mezzogiorno_gap")


# ================================================================== #
#  10. SCM Gap Plot (Ch 12)
# ================================================================== #

def fig_scm_gap(output_dir, seed=42):
    """Synthetic control method: actual vs synthetic GDP for conflict country."""
    years = np.arange(2005, 2024)
    rng = np.random.default_rng(seed)
    treatment_year = 2015

    # Pre-treatment: actual ≈ synthetic
    t = years - 2005
    baseline = 100 + 3 * t + rng.normal(0, 1.5, len(years))
    synthetic = 100 + 3 * t + rng.normal(0, 0.8, len(years))

    # Post-treatment: actual diverges down
    post = years >= treatment_year
    baseline[post] = baseline[post] - 15 * (1 - np.exp(-0.4 * (years[post] - treatment_year)))
    # Add some noise
    baseline[post] += rng.normal(0, 2, post.sum())

    df = pd.DataFrame({
        "year": np.tile(years, 2),
        "gdp_index": np.concatenate([baseline, synthetic]),
        "series": ["Actual (Yemen)"] * len(years) + ["Synthetic control"] * len(years),
    })

    base = get_base_theme()
    p = (
        ggplot(df, aes("year", "gdp_index", color="series", linetype="series"))
        + geom_line(size=1.1)
        + geom_vline(xintercept=treatment_year, linetype="dashed", color="#808080", size=0.7)
        + annotate("text", x=treatment_year + 0.5, y=145,
                   label="Conflict onset", size=7, color="#808080", ha="left")
        + scale_color_manual(values=["#c44e52", "#6a9bc3"])
        + labs(
            title="Synthetic Control Estimate: GDP Impact of Conflict",
            x="",
            y="GDP index (2005 = 100)",
            color="",
            linetype="",
            caption="Source: Illustrative SCM output; Abadie, Diamond & Hainmueller (2010) method."
        )
        + base
        + theme(
            plot_title=element_text(size=10, face="bold"),
            legend_position="bottom",
        )
    )
    return _save_plotnine(p, output_dir, "fig_ch12_scm_gap")


# ================================================================== #
#  11. Urbanization without Industrialization (Ch 13)
# ================================================================== #

def fig_urbanization_industry(output_dir, seed=42):
    """Scatter of urbanization vs manufacturing for African countries."""
    rng = np.random.default_rng(seed)
    n = 30

    # African countries: high urbanization, low manufacturing
    africa_urb = rng.uniform(25, 75, n)
    africa_mfg = 5 + 0.05 * africa_urb + rng.normal(0, 3, n)
    africa_mfg = np.clip(africa_mfg, 2, 20)

    # Comparators (East Asian path): higher mfg at similar urbanization
    n2 = 10
    asia_urb = rng.uniform(30, 80, n2)
    asia_mfg = 8 + 0.25 * asia_urb + rng.normal(0, 3, n2)
    asia_mfg = np.clip(asia_mfg, 5, 35)

    africa_labels = [
        "NGA", "KEN", "ETH", "GHA", "TZA", "UGA", "SEN", "CIV",
        "CMR", "AGO", "MOZ", "ZMB", "ZWE", "BWA", "NAM", "RWA",
        "MLI", "BFA", "NER", "TCD", "COD", "COG", "GAB", "SLE",
        "LBR", "GIN", "TGO", "BEN", "MWI", "ZAF",
    ]
    asia_labels = ["CHN", "VNM", "THA", "MYS", "IDN", "PHL", "KHM", "BGD", "IND", "KOR"]

    df = pd.DataFrame({
        "urbanization": np.concatenate([africa_urb, asia_urb]),
        "mfg_share": np.concatenate([africa_mfg, asia_mfg]),
        "region": ["Sub-Saharan Africa"] * n + ["East/South Asia"] * n2,
        "label": africa_labels + asia_labels,
    })

    base = get_base_theme()
    p = (
        ggplot(df, aes("urbanization", "mfg_share", color="region"))
        + geom_point(alpha=0.6, size=2)
        + geom_text(aes(label="label"), size=5.5, nudge_y=1, alpha=0.7)
        + geom_smooth(method="lm", se=False, size=0.8, linetype="dashed")
        + scale_color_manual(values=["#6a9bc3", "#d4b44a"])
        + labs(
            title="Urbanization Without Industrialization",
            x="Urbanization rate (%)",
            y="Manufacturing share of GDP (%)",
            color="",
            caption="Source: Synthetic cross-section illustrating Gollin, Jedwab & Vollrath (2016) pattern."
        )
        + base
        + theme(
            plot_title=element_text(size=10, face="bold"),
            legend_position="bottom",
        )
    )
    return _save_plotnine(p, output_dir, "fig_ch13_urbanization_industry")


# ================================================================== #
#  12. Intra-Regional Trade Shares (Ch 14)
# ================================================================== #

def fig_intra_regional_trade(output_dir, seed=42):
    """Grouped bar chart of intra-regional trade shares."""
    df = pd.DataFrame({
        "bloc": ["EU", "USMCA", "ASEAN", "Mercosur", "AfCFTA", "SAARC"],
        "share": [64, 40, 24, 14, 15, 5],
    })
    df["bloc"] = pd.Categorical(
        df["bloc"],
        categories=["EU", "USMCA", "ASEAN", "Mercosur", "AfCFTA", "SAARC"],
        ordered=True,
    )
    colors = ["#c76da3", "#5aad8a", "#d4885a", "#5aad8a", "#d4b44a", "#8a83b8"]

    base = get_base_theme()
    p = (
        ggplot(df, aes("bloc", "share", fill="bloc"))
        + geom_col(width=0.6, show_legend=False)
        + geom_text(aes(label="share"), nudge_y=2, size=8, color="#333333")
        + scale_fill_manual(values=colors)
        + labs(
            title="Intra-Regional Trade Shares by Bloc",
            x="",
            y="Intra-bloc trade as % of total (%)",
            caption="Source: Synthetic approximation of WTO/UNCTAD (2023) reported shares."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_ch14_intra_regional_trade")


# ================================================================== #
#  13. Stranded Asset Timeline (Ch 15) — matplotlib
# ================================================================== #

def fig_stranded_timeline(output_dir, seed=42):
    """Waterfall chart of projected stranded asset values by sector."""
    fig, ax = plt.subplots(figsize=(W, H_THEMATIC))

    sectors = ["Coal\npower", "Coal\nmining", "Oil\nupstream", "Oil\nrefining",
               "Gas\nupstream", "Gas\nLNG", "Total"]
    values = [1.8, 0.9, 3.2, 1.4, 1.1, 0.6, 9.0]
    colors = ["#333333", "#555555", "#c44e52", "#dd8452", "#6a9bc3", "#8c7bba", "#808080"]

    # Waterfall
    cumulative = 0
    for i, (s, v, c) in enumerate(zip(sectors[:-1], values[:-1], colors[:-1])):
        ax.bar(i, v, bottom=cumulative, color=c, width=0.55, edgecolor="white", linewidth=0.5)
        ax.text(i, cumulative + v / 2, f"${v}T", ha="center", va="center",
                fontsize=7, color="white", fontweight="bold")
        cumulative += v

    # Total bar from zero
    ax.bar(len(sectors) - 1, values[-1], color=colors[-1], width=0.55,
           edgecolor="white", linewidth=0.5)
    ax.text(len(sectors) - 1, values[-1] / 2, f"${values[-1]}T",
            ha="center", va="center", fontsize=8, color="white", fontweight="bold")

    ax.set_xticks(range(len(sectors)))
    ax.set_xticklabels(sectors, fontsize=7)
    ax.set_ylabel("Projected stranded assets (USD trillions)", fontsize=8)
    ax.set_title("Stranded Fossil-Fuel Assets Under Net-Zero by 2050",
                 fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 10.5)

    add_figure_source(fig, "Synthetic estimates based on Carbon Tracker (2023) and IEA NZE scenario.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    return _save_mpl(fig, output_dir, "fig_ch15_stranded_timeline")


# ================================================================== #
#  14. Services Gravity Residual Plot (Ch 16)
# ================================================================== #

def fig_services_gravity(output_dir, seed=42):
    """Gravity residual plot for services trade."""
    rng = np.random.default_rng(seed)
    n = 120

    predicted = rng.uniform(3, 12, n)
    residual = rng.normal(0, 1.5, n)
    actual = predicted + residual

    # Some outliers
    outlier_labels = ["UK-US", "SG-HK", "IN-US", "DE-FR", "JP-CN",
                      "NG-UK", "BR-AR"]
    outlier_idx = rng.choice(n, len(outlier_labels), replace=False)
    for i, idx in enumerate(outlier_idx):
        if i < 3:
            actual[idx] = predicted[idx] + rng.uniform(3, 5)
        else:
            actual[idx] = predicted[idx] - rng.uniform(2.5, 4)

    labels = [""] * n
    for i, idx in enumerate(outlier_idx):
        labels[idx] = outlier_labels[i]

    df = pd.DataFrame({
        "predicted": predicted,
        "actual": actual,
        "label": labels,
        "is_outlier": [l != "" for l in labels],
    })

    base = get_base_theme()
    p = (
        ggplot(df, aes("predicted", "actual"))
        + geom_abline(intercept=0, slope=1, linetype="dashed", color="#808080", size=0.5)
        + geom_point(aes(color="is_outlier"), alpha=0.5, size=1.5, show_legend=False)
        + geom_text(
            aes(label="label"),
            data=df[df["is_outlier"]],
            size=7, nudge_y=0.5, color="#c44e52",
        )
        + scale_color_manual(values=["#6a9bc3", "#c44e52"])
        + labs(
            title="Services Trade: Actual vs. Gravity-Predicted Flows",
            x="ln(Predicted trade flow)",
            y="ln(Actual trade flow)",
            caption="Source: Illustrative gravity residuals; outlier pairs labeled."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_ch16_services_gravity")


# ================================================================== #
#  15. SAR Results Table Figure (Lab 1) — matplotlib
# ================================================================== #

def fig_lab1_sar_results(output_dir, seed=42):
    """Clean regression table rendered as a figure."""
    fig, ax = plt.subplots(figsize=(W, 4.2))
    ax.axis("off")

    table_data = [
        ["", "(1) OLS", "(2) SAR"],
        ["ln(K/L)", "0.312***", "0.281***"],
        ["", "(0.048)", "(0.052)"],
        ["Human capital", "0.215***", "0.194***"],
        ["", "(0.039)", "(0.041)"],
        ["Trade openness", "0.098*", "0.118**"],
        ["", "(0.054)", "(0.053)"],
        ["Urbanization", "0.065", "0.078*"],
        ["", "(0.042)", "(0.038)"],
        ["Institutions", "0.182***", "0.148***"],
        ["", "(0.044)", "(0.042)"],
        ["Spatial lag (ρ)", "—", "0.351***"],
        ["", "", "(0.058)"],
        ["", "", ""],
        ["N", "265", "265"],
        ["R² / pseudo-R²", "0.68", "0.72"],
        ["AIC", "412.3", "389.7"],
    ]

    table = ax.table(
        cellText=table_data,
        loc="center",
        cellLoc="center",
        colWidths=[0.35, 0.25, 0.25],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.15)

    # Style header row
    for j in range(3):
        cell = table[0, j]
        cell.set_text_props(fontweight="bold")
        cell.set_facecolor("#e8e8e8")
        cell.set_edgecolor("#cccccc")

    # Style all cells
    for i in range(len(table_data)):
        for j in range(3):
            cell = table[i, j]
            cell.set_edgecolor("#cccccc")
            if i > 0 and i % 2 == 0:  # SE rows
                cell.set_text_props(color="#808080")

    # Separator lines for bottom stats
    for i in [13, 14, 15, 16]:
        for j in range(3):
            table[i, j].set_facecolor("#f8f8f8")

    ax.set_title("Table: SAR Model Results — Regional Growth Regression",
                 fontsize=10, fontweight="bold", pad=20)

    add_figure_source(fig, "Lab 1 output; *** p<0.01, ** p<0.05, * p<0.10.")
    fig.tight_layout(rect=[0, 0.04, 1, 0.93])
    return _save_mpl(fig, output_dir, "fig_lab1_sar_results")


# ================================================================== #
#  16. Beta-Convergence Scatter (Lab 2)
# ================================================================== #

def fig_lab2_convergence(output_dir, seed=42):
    """Beta-convergence scatter for East Asian economies."""
    rng = np.random.default_rng(seed)

    countries = ["JPN", "KOR", "TWN", "SGP", "HKG", "MYS", "THA",
                 "IDN", "PHL", "VNM", "CHN", "KHM", "LAO", "MMR"]
    # Initial GDP/cap (1990, log scale)
    initial = [10.2, 9.1, 9.3, 9.8, 10.0, 8.5, 7.8,
               7.2, 7.5, 6.5, 7.0, 6.2, 6.0, 5.8]
    # Growth 1990-2020 (annual avg %)
    growth = [1.0, 4.2, 3.8, 3.5, 2.5, 4.0, 3.2,
              3.5, 2.8, 5.5, 7.8, 5.0, 5.2, 6.0]
    # Add noise
    growth = [g + rng.normal(0, 0.3) for g in growth]

    df = pd.DataFrame({
        "initial_gdppc": initial,
        "growth_rate": growth,
        "label": countries,
    })

    base = get_base_theme()
    p = (
        ggplot(df, aes("initial_gdppc", "growth_rate"))
        + geom_point(color="#d4885a", size=3)
        + geom_text(aes(label="label"), size=7, nudge_y=0.35, color="#555555")
        + geom_smooth(method="lm", color="#c44e52", se=True, alpha=0.1, size=0.8)
        + labs(
            title="Beta-Convergence in East Asia, 1990–2020",
            x="ln(Initial GDP per capita, 1990)",
            y="Average annual growth rate (%)",
            caption="Source: Synthetic data; negative slope indicates conditional β-convergence."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_lab2_convergence_scatter")


# ================================================================== #
#  17. Placebo Distribution (Lab 5)
# ================================================================== #

def fig_lab5_placebo(output_dir, seed=42):
    """Placebo distribution histogram with treated unit marked."""
    rng = np.random.default_rng(seed)

    # Placebo RMSPE ratios (post/pre) for donor pool
    n_placebos = 18
    ratios = rng.exponential(1.5, n_placebos)
    ratios = np.clip(ratios, 0.3, 8)

    # Treated unit has high ratio
    treated_ratio = 6.2

    df = pd.DataFrame({"rmspe_ratio": ratios})

    base = get_base_theme()
    p = (
        ggplot(df, aes(x="rmspe_ratio"))
        + geom_histogram(bins=10, fill="#6a9bc3", color="white", alpha=0.7)
        + geom_vline(xintercept=treated_ratio, color="#c44e52", size=1.2, linetype="solid")
        + annotate("text", x=treated_ratio + 0.3, y=4.5,
                   label="Yemen\n(treated)", size=8, color="#c44e52", ha="left")
        + labs(
            title="Placebo Test: Post/Pre RMSPE Ratio Distribution",
            x="Post-treatment / Pre-treatment RMSPE ratio",
            y="Count (donor units)",
            caption="Source: Lab 5 SCM placebo output; p-value ≈ 1/19 ≈ 0.053."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_lab5_placebo")


# ================================================================== #
#  18. Moran Permutation Test (Lab 6)
# ================================================================== #

def fig_lab6_moran_permutation(output_dir, seed=42):
    """Permutation histogram for Moran's I with observed value."""
    rng = np.random.default_rng(seed)

    n_perms = 999
    perm_I = rng.normal(-0.01, 0.06, n_perms)
    observed_I = 0.32

    df = pd.DataFrame({"moran_I": perm_I})

    base = get_base_theme()
    p = (
        ggplot(df, aes(x="moran_I"))
        + geom_histogram(bins=35, fill="#6a9bc3", color="white", alpha=0.7)
        + geom_vline(xintercept=observed_I, color="#c44e52", size=1.2)
        + annotate("text", x=observed_I + 0.01, y=55,
                   label=f"Observed I = {observed_I:.2f}\np < 0.001",
                   size=8, color="#c44e52", ha="left")
        + labs(
            title="Permutation Test for Moran's I (Nighttime Luminosity)",
            x="Moran's I (permuted distribution)",
            y="Count",
            caption="Source: Lab 6 output; 999 permutations under spatial randomness."
        )
        + base
        + theme(plot_title=element_text(size=10, face="bold"))
    )
    return _save_plotnine(p, output_dir, "fig_lab6_moran_permutation")


# ================================================================== #
#  19. STRI Tariff-Equivalent Bar Chart (Lab 7)
# ================================================================== #

def fig_lab7_stri_tariff(output_dir, seed=42):
    """STRI tariff-equivalent bars by sector and country."""
    sectors = ["Financial", "Telecom", "Transport", "Professional"]
    countries = ["India", "China", "Brazil", "Indonesia", "OECD avg"]
    tariff_equiv = {
        "Financial":     [65, 52, 38, 48, 18],
        "Telecom":       [55, 60, 42, 50, 15],
        "Transport":     [40, 45, 35, 42, 12],
        "Professional":  [70, 48, 55, 58, 22],
    }

    rows = []
    for s in sectors:
        for i, c in enumerate(countries):
            rows.append({"sector": s, "country": c, "tariff_equiv": tariff_equiv[s][i]})

    df = pd.DataFrame(rows)
    df["country"] = pd.Categorical(df["country"], categories=countries, ordered=True)
    df["sector"] = pd.Categorical(df["sector"], categories=sectors, ordered=True)

    base = get_base_theme()
    p = (
        ggplot(df, aes(x="country", y="tariff_equiv", fill="sector"))
        + geom_col(position=position_dodge(width=0.75), width=0.7)
        + scale_fill_manual(values=["#c44e52", "#6a9bc3", "#7dab6e", "#8c7bba"])
        + labs(
            title="Services Trade Restrictiveness: Ad-Valorem Equivalents",
            x="",
            y="Tariff-equivalent (% ad valorem)",
            fill="Sector",
            caption="Source: Illustrative estimates based on OECD STRI methodology; Jafari & Tarr (2017)."
        )
        + base
        + theme(
            plot_title=element_text(size=10, face="bold"),
            legend_position="bottom",
            axis_text_x=element_text(size=7),
        )
    )
    return _save_plotnine(p, output_dir, "fig_lab7_stri_tariff", height=4.5)


# ================================================================== #
#  CLI
# ================================================================== #

ALL_FIGURES = [
    ("fig_ch03a_moran_scatter",        fig_moran_scatter),
    ("fig_ch03a_sar_coefficients",     fig_sar_coefficients),
    ("fig_ch03b_distance_decay",       fig_distance_decay),
    ("fig_ch03b_ppml_vs_ols",          fig_ppml_vs_ols),
    ("fig_ch05_inverted_u",            fig_inverted_u),
    ("fig_ch06_dva_decomposition",     fig_dva_decomposition),
    ("fig_ch07_provincial_gini",       fig_provincial_gini),
    ("fig_ch09_convergence_fan",       fig_convergence_fan),
    ("fig_ch10_mezzogiorno_gap",       fig_mezzogiorno_gap),
    ("fig_ch12_scm_gap",              fig_scm_gap),
    ("fig_ch13_urbanization_industry", fig_urbanization_industry),
    ("fig_ch14_intra_regional_trade",  fig_intra_regional_trade),
    ("fig_ch15_stranded_timeline",     fig_stranded_timeline),
    ("fig_ch16_services_gravity",      fig_services_gravity),
    ("fig_lab1_sar_results",           fig_lab1_sar_results),
    ("fig_lab2_convergence_scatter",   fig_lab2_convergence),
    ("fig_lab5_placebo",               fig_lab5_placebo),
    ("fig_lab6_moran_permutation",     fig_lab6_moran_permutation),
    ("fig_lab7_stri_tariff",           fig_lab7_stri_tariff),
]


def main():
    parser = argparse.ArgumentParser(description="Lab output & Data in Depth figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    print(f"Generating {len(ALL_FIGURES)} figures to {output_dir}")
    summaries = []
    for name, func in ALL_FIGURES:
        print(f"\n  [{ALL_FIGURES.index((name, func)) + 1}/{len(ALL_FIGURES)}] {name}")
        try:
            paths = func(output_dir, args.seed)
            summaries.append({"figure": name, "status": "ok", **paths})
        except Exception as e:
            print(f"    ERROR: {e}")
            summaries.append({"figure": name, "status": "error", "error": str(e)})

    save_summary(output_dir, "ch_lab_output_figures", {"figures": summaries})
    ok = sum(1 for s in summaries if s["status"] == "ok")
    print(f"\n{'='*60}")
    print(f"Complete: {ok}/{len(ALL_FIGURES)} figures generated successfully.")


if __name__ == "__main__":
    main()
