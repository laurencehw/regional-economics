"""Shared infrastructure for manuscript figures.

Provides style constants, projection lookups, Natural Earth boundary loading,
city/corridor annotation, source notes, and a reusable plotnine base theme.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# ------------------------------------------------------------------ #
#  Style constants
# ------------------------------------------------------------------ #

FIGURE_WIDTH = 6        # inches (single column)
DPI = 300
OUTPUT_FORMATS = ("png", "pdf")

FIGSIZE_MAP = (FIGURE_WIDTH, 5)
FIGSIZE_THEMATIC = (FIGURE_WIDTH, 4)
FIGSIZE_CONCEPT = (FIGURE_WIDTH, 4.5)
FIGSIZE_WIDE = (8, 5)

# Per-region color palette (matches generate_regional_dashboard.py)
REGION_COLORS = {
    "americas":   "#1b9e77",
    "east_asia":  "#d95f02",
    "south_asia": "#7570b3",
    "europe":     "#e7298a",
    "mena":       "#66a61e",
    "africa":     "#e6ab02",
    "global":     "#666666",
}

# Qualitative palette for multi-series charts
QUAL_PALETTE = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3",
    "#ff7f00", "#a65628", "#f781bf", "#999999",
]

# Neutral tones for map backgrounds
LAND_COLOR = "#f0f0f0"
WATER_COLOR = "#d4e6f1"
BORDER_COLOR = "#888888"
HIGHLIGHT_COLOR = "#ffeda0"

# ------------------------------------------------------------------ #
#  Projection lookup (EPSG/ESRI codes per region)
# ------------------------------------------------------------------ #

PROJECTIONS = {
    "americas":       "ESRI:102003",    # Albers Equal-Area Conic (NA)
    "latin_america":  "ESRI:102033",    # South America Albers
    "east_asia":      "ESRI:102012",    # Asia Lambert Conformal Conic
    "south_asia":     "ESRI:102029",    # Asia South Lambert Conformal Conic
    "europe":         "EPSG:3035",      # ETRS89 LAEA Europe
    "mena":           "EPSG:32637",     # WGS 84 / UTM zone 37N
    "africa":         "ESRI:102022",    # Africa Albers Equal-Area Conic
    "global":         "EPSG:4326",      # WGS84 (for Robinson use geopandas)
}


# ------------------------------------------------------------------ #
#  Natural Earth boundary loader
# ------------------------------------------------------------------ #

NE_BASE_URL = "https://naturalearth.s3.amazonaws.com"

NE_DATASETS = {
    "admin_0_countries":      f"{NE_BASE_URL}/50m_cultural/ne_50m_admin_0_countries.zip",
    "admin_1_states":         f"{NE_BASE_URL}/50m_cultural/ne_50m_admin_1_states_provinces.zip",
    "populated_places":       f"{NE_BASE_URL}/50m_cultural/ne_50m_populated_places_simple.zip",
    "lakes":                  f"{NE_BASE_URL}/50m_physical/ne_50m_lakes.zip",
    "admin_0_countries_110m": f"{NE_BASE_URL}/110m_cultural/ne_110m_admin_0_countries.zip",
}

GEODATA_DIR = Path(__file__).resolve().parent.parent / "data" / "geodata"


def load_boundaries(dataset: str = "admin_0_countries", cache_dir: Path | None = None):
    """Download and cache a Natural Earth dataset, return a GeoDataFrame.

    Parameters
    ----------
    dataset : str
        Key into NE_DATASETS.
    cache_dir : Path, optional
        Override default cache directory.
    """
    import geopandas as gpd

    url = NE_DATASETS[dataset]
    dest = (cache_dir or GEODATA_DIR) / dataset
    dest.mkdir(parents=True, exist_ok=True)

    shapefile = list(dest.glob("*.shp"))
    if shapefile:
        return gpd.read_file(shapefile[0])

    # Download from URL (geopandas handles zip)
    gdf = gpd.read_file(url)
    # Cache locally
    gdf.to_file(dest / f"{dataset}.shp")
    return gdf


def get_country_boundaries(iso3_list: List[str] | None = None,
                           dataset: str = "admin_0_countries"):
    """Return country boundaries GeoDataFrame, optionally filtered to iso3 codes."""
    gdf = load_boundaries(dataset)
    # Normalize ISO column
    iso_col = "ISO_A3" if "ISO_A3" in gdf.columns else "ADM0_A3"
    gdf = gdf.rename(columns={iso_col: "iso3"})
    if iso3_list is not None:
        gdf = gdf[gdf["iso3"].isin(iso3_list)].copy()
    return gdf


def get_admin1_boundaries(country_iso3: str | List[str]):
    """Return admin-1 boundaries for one or more countries."""
    gdf = load_boundaries("admin_1_states")
    iso_col = "iso_a2" if "iso_a2" in gdf.columns else "adm0_a3"
    if isinstance(country_iso3, str):
        country_iso3 = [country_iso3]
    # Try matching on adm0_a3 first
    if "adm0_a3" in gdf.columns:
        return gdf[gdf["adm0_a3"].isin(country_iso3)].copy()
    return gdf


# ------------------------------------------------------------------ #
#  Region ISO3 sets
# ------------------------------------------------------------------ #

ISO3_SETS = {
    "north_america": ["USA", "CAN", "MEX"],
    "latin_america": [
        "BRA", "ARG", "CHL", "COL", "PER", "VEN", "ECU", "BOL",
        "PRY", "URY", "GUY", "SUR", "MEX", "GTM", "HND", "SLV",
        "NIC", "CRI", "PAN", "CUB", "DOM", "HTI", "JAM", "TTO",
    ],
    "americas": [
        "USA", "CAN", "MEX", "BRA", "ARG", "CHL", "COL", "PER",
        "VEN", "ECU", "BOL", "PRY", "URY", "GUY", "SUR", "GTM",
        "HND", "SLV", "NIC", "CRI", "PAN", "CUB", "DOM", "HTI",
        "JAM", "TTO",
    ],
    "east_asia": [
        "CHN", "JPN", "KOR", "TWN", "SGP", "IDN", "MYS", "THA",
        "VNM", "PHL", "MMR", "KHM", "LAO", "BRN",
    ],
    "south_asia": [
        "IND", "PAK", "BGD", "LKA", "NPL", "BTN", "MDV", "AFG",
    ],
    "europe": [
        "GBR", "FRA", "DEU", "ITA", "ESP", "PRT", "NLD", "BEL",
        "AUT", "CHE", "POL", "CZE", "SVK", "HUN", "ROU", "BGR",
        "HRV", "SVN", "GRC", "IRL", "DNK", "SWE", "NOR", "FIN",
        "EST", "LVA", "LTU", "LUX", "MLT", "CYP",
    ],
    "mena": [
        "SAU", "ARE", "QAT", "KWT", "BHR", "OMN", "IRQ", "IRN",
        "SYR", "JOR", "LBN", "ISR", "PSE", "YEM", "EGY", "LBY",
        "TUN", "DZA", "MAR",
    ],
    "gcc": ["SAU", "ARE", "QAT", "KWT", "BHR", "OMN"],
    "ssa": [
        "NGA", "ZAF", "KEN", "ETH", "GHA", "TZA", "UGA", "SEN",
        "CIV", "CMR", "AGO", "MOZ", "MDG", "ZMB", "ZWE", "BWA",
        "NAM", "RWA", "BDI", "MLI", "BFA", "NER", "TCD", "CAF",
        "COD", "COG", "GAB", "GNQ", "SLE", "LBR", "GIN", "GMB",
        "GNB", "TGO", "BEN", "MWI", "LSO", "SWZ", "DJI", "ERI",
        "SOM", "SSD", "MRT", "SDN",
    ],
}


# ------------------------------------------------------------------ #
#  City/corridor annotator
# ------------------------------------------------------------------ #

ANNOTATIONS_PATH = Path(__file__).resolve().parent / "annotations.json"


def load_annotations(chapter: str | None = None) -> Dict[str, Any]:
    """Load annotation data from annotations.json.

    Parameters
    ----------
    chapter : str, optional
        If provided, return only annotations for that chapter key.
    """
    if not ANNOTATIONS_PATH.exists():
        return {}
    data = json.loads(ANNOTATIONS_PATH.read_text(encoding="utf-8"))
    if chapter:
        return data.get(chapter, {})
    return data


def _project_point(lon: float, lat: float, crs) -> Tuple[float, float]:
    """Transform a single lon/lat point to the target CRS."""
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    return transformer.transform(lon, lat)


def project_cities(cities: List[Dict], crs) -> List[Dict]:
    """Return a copy of city dicts with lon/lat projected to target CRS."""
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    out = []
    for city in cities:
        c = dict(city)
        c["lon"], c["lat"] = transformer.transform(city["lon"], city["lat"])
        out.append(c)
    return out


def project_corridors(corridors: List[Dict], crs) -> List[Dict]:
    """Return a copy of corridor dicts with waypoints projected to target CRS."""
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    out = []
    for corr in corridors:
        c = dict(corr)
        projected = []
        for lon, lat in corr["waypoints"]:
            px, py = transformer.transform(lon, lat)
            projected.append([px, py])
        c["waypoints"] = projected
        out.append(c)
    return out


def project_arrows(arrows: List[Dict], crs) -> List[Dict]:
    """Return a copy of arrow dicts with start/end projected to target CRS."""
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    out = []
    for arrow in arrows:
        a = dict(arrow)
        sx, sy = transformer.transform(arrow["start"][0], arrow["start"][1])
        ex, ey = transformer.transform(arrow["end"][0], arrow["end"][1])
        a["start"] = [sx, sy]
        a["end"] = [ex, ey]
        out.append(a)
    return out


def annotate_cities(ax, cities: List[Dict], transform=None):
    """Plot city markers and labels on a matplotlib axis.

    Each city dict: {name, lat, lon, label_offset: [dx, dy], style: str}
    Cities should already be projected to the map CRS via project_cities().
    """
    for city in cities:
        x, y = city["lon"], city["lat"]
        dx, dy = city.get("label_offset", [0.5, 0.5])
        style = city.get("style", "major")
        marker = "o" if style == "major" else "s"
        size = 30 if style == "major" else 15
        color = "#333333" if style == "major" else "#666666"
        fontsize = 7 if style == "major" else 6

        ax.scatter(x, y, s=size, c=color, marker=marker, zorder=5)
        ax.annotate(
            city["name"], (x, y), xytext=(dx, dy),
            textcoords="offset points", fontsize=fontsize,
            ha="left", va="bottom", zorder=6,
        )


def annotate_corridors(ax, corridors: List[Dict], transform=None):
    """Draw corridor route lines on a matplotlib axis.

    Each corridor dict: {name, waypoints: [[x,y],...], style: str}
    Waypoints should already be projected to the map CRS via project_corridors().
    """
    for corridor in corridors:
        pts = np.array(corridor["waypoints"])
        style = corridor.get("style", "trade")
        color = "#e41a1c" if style == "trade" else "#377eb8"
        ls = "--" if style == "trade" else "-."
        lw = 1.5

        ax.plot(pts[:, 0], pts[:, 1], color=color, linestyle=ls,
                linewidth=lw, zorder=4, alpha=0.7)

        # Label at midpoint
        mid = len(pts) // 2
        ax.annotate(
            corridor["name"],
            (pts[mid, 0], pts[mid, 1]),
            fontsize=5, color=color, ha="center", va="bottom",
            fontstyle="italic", zorder=6,
        )


def annotate_arrows(ax, arrows: List[Dict], transform=None):
    """Draw directional flow arrows on a matplotlib axis.

    Each arrow dict: {label, start: [x,y], end: [x,y], style: str}
    Points should already be projected to the map CRS via project_arrows().
    """
    for arrow in arrows:
        x0, y0 = arrow["start"]
        x1, y1 = arrow["end"]
        color = arrow.get("color", "#e41a1c")
        ax.annotate(
            "", xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(
                arrowstyle="->,head_width=0.2,head_length=0.15",
                lw=1.5, color=color, alpha=0.7,
            ),
            zorder=4,
        )
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        if "label" in arrow:
            ax.text(mx, my, arrow["label"], fontsize=5, color=color,
                    ha="center", va="bottom", fontstyle="italic", zorder=6)


# ------------------------------------------------------------------ #
#  Source note helper
# ------------------------------------------------------------------ #

def add_source_note(ax, text: str, fontsize: float = 6):
    """Place a source attribution note at the bottom of a figure."""
    ax.annotate(
        f"Source: {text}",
        xy=(0.0, -0.08), xycoords="axes fraction",
        fontsize=fontsize, color="#808080", ha="left", va="top",
    )


def add_figure_source(fig, text: str, fontsize: float = 6):
    """Place source note at figure bottom (outside axes)."""
    fig.text(0.02, 0.01, f"Source: {text}",
             fontsize=fontsize, color="#808080", ha="left", va="bottom")


# ------------------------------------------------------------------ #
#  Base plotnine theme
# ------------------------------------------------------------------ #

def get_base_theme():
    """Return a plotnine theme: hrbrthemes if available, else theme_minimal."""
    try:
        from hrbrthemes import theme_ipsum
        return theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        return theme_minimal()


# ------------------------------------------------------------------ #
#  Map helpers
# ------------------------------------------------------------------ #

def setup_map_ax(ax, title: str = "", bbox: Tuple[float, ...] | None = None):
    """Configure a matplotlib axes for map display."""
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", pad=8)
    if bbox:
        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])


def shade_countries(ax, gdf, column: str | None = None,
                    color: str = HIGHLIGHT_COLOR,
                    cmap: str = "YlOrRd",
                    edgecolor: str = BORDER_COLOR,
                    linewidth: float = 0.5,
                    legend: bool = False):
    """Plot countries with optional choropleth shading."""
    if column and column in gdf.columns:
        gdf.plot(ax=ax, column=column, cmap=cmap, edgecolor=edgecolor,
                 linewidth=linewidth, legend=legend)
    else:
        gdf.plot(ax=ax, color=color, edgecolor=edgecolor, linewidth=linewidth)


def save_figure(fig, output_dir: Path, filename_stem: str,
                formats: Tuple[str, ...] = OUTPUT_FORMATS):
    """Save a figure in multiple formats and return the paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for fmt in formats:
        path = output_dir / f"{filename_stem}.{fmt}"
        fig.savefig(str(path), dpi=DPI, bbox_inches="tight",
                    facecolor="white", edgecolor="none")
        paths[fmt] = str(path)
        print(f"  Saved: {path}")
    return paths


def save_summary(output_dir: Path, filename_stem: str, summary: Dict):
    """Write a JSON summary alongside the figure."""
    path = output_dir / f"{filename_stem}_summary.json"
    path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(f"  Summary: {path}")
    return str(path)


# ------------------------------------------------------------------ #
#  Smoke-test / CLI helpers
# ------------------------------------------------------------------ #

def default_output_dir() -> Path:
    return Path(__file__).resolve().parent


def add_common_args(parser):
    """Add standard --run-smoke-test, --output-dir, --seed args to an argparse parser."""
    parser.add_argument("--run-smoke-test", action="store_true",
                        help="Generate with synthetic data (no external files needed)")
    parser.add_argument("--output-dir", type=str, default=None,
                        help=f"Output directory (default: figures/output/)")
    parser.add_argument("--seed", type=int, default=42)
    return parser


def get_output_dir(args) -> Path:
    """Resolve output directory from args."""
    if args.output_dir:
        return Path(args.output_dir)
    return default_output_dir()
