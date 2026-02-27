"""Fetch and process NOAA/EOG VIIRS annual nighttime lights composites for Africa.

Outputs
-------
``labs/lab6_africa/data/raw/viirs/viirs_africa_{year}.csv``
  Long-format panel with columns: iso3, year, avg_radiance
  Compatible with ``labs/lab6_africa/data/source_mappings.json``
  (region_col: "iso3", radiance_col: "avg_radiance").

Optionally writes an Africa country adjacency edge list:
``labs/lab6_africa/data/raw/adjacency/adjacency_africa.csv``
  Columns: iso3, neighbor_iso3, shared_border_km

DATA SOURCE
-----------
NOAA/CIRES/DOE Earth Observation Group (EOG), Payne Institute,
Colorado School of Mines.
Product: VNL (VIIRS Nighttime Lights) Version 2.1 Annual Composites
  - Band used: average_masked (annual mean radiance, lit areas only)
  - Format: GeoTIFF, WGS84, float32
URL: https://eogdata.mines.edu/nighttime_light/annual/v21/

DOWNLOAD INSTRUCTIONS
---------------------
1. Register at https://eogdata.mines.edu/ (free).
2. Navigate to Annual VNL v2.1 for the desired year.
3. Download the ``...average_masked.dat.tif.gz`` file.
4. Decompress: gunzip VNL_v21_npp_YYYY_global_vcm*.average_masked.dat.tif.gz
5. Pass the resulting .tif path to --local-tif.

Files are ~200-500 MB per year. The script clips to the Africa bounding box
before processing, so memory usage is manageable on a standard laptop.

Use --smoke-test to generate synthetic country-level data for CI/testing
without downloading any raster files.

DEPENDENCIES
------------
The raster processing path requires rasterio and geopandas, which are
installed in this environment. The --smoke-test path has no additional deps.

USAGE EXAMPLES
--------------
Smoke test (no raster needed):
  python scripts/fetch_viirs_africa.py --smoke-test --year 2022

Real raster (pre-downloaded):
  python scripts/fetch_viirs_africa.py \\
      --local-tif path/to/VNL_v21_npp_2022_global.average_masked.dat.tif \\
      --year 2022

Build adjacency edge list alongside radiance:
  python scripts/fetch_viirs_africa.py --smoke-test --year 2022 --write-adjacency

Multi-year (call once per year then concatenate):
  for YEAR in 2019 2020 2021 2022; do
    python scripts/fetch_viirs_africa.py --local-tif viirs_${YEAR}.tif --year $YEAR
  done
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# African country ISO3 codes (UN M.49 Sub-region 002)
# ---------------------------------------------------------------------------
AFRICA_ISO3: List[str] = [
    "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CMR", "CPV", "CAF", "TCD",
    "COM", "COD", "COG", "CIV", "DJI", "EGY", "GNQ", "ERI", "SWZ", "ETH",
    "GAB", "GMB", "GHA", "GIN", "GNB", "KEN", "LSO", "LBR", "LBY", "MDG",
    "MWI", "MLI", "MRT", "MUS", "MAR", "MOZ", "NAM", "NER", "NGA", "RWA",
    "STP", "SEN", "SLE", "SOM", "ZAF", "SDN", "SSD", "TZA", "TGO", "TUN",
    "UGA", "ESH", "ZMB", "ZWE",
]

# Natural Earth 110m admin-0 country boundaries — stable S3 CDN
NATURAL_EARTH_URL = (
    "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
)

# Africa bounding box: (west, south, east, north)
AFRICA_BBOX = (-25.5, -35.5, 52.5, 38.5)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch/process VIIRS nighttime lights for Africa (Lab 6)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--local-tif",
        default=None,
        help="Path to a pre-downloaded VIIRS VNL GeoTIFF (.tif or .tif.gz uncompressed).",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2022,
        help="Year label written into the output CSV (default: 2022).",
    )
    parser.add_argument(
        "--output-dir",
        default="labs/lab6_africa/data/raw/viirs",
        help="Directory for radiance output CSV (default: labs/lab6_africa/data/raw/viirs).",
    )
    parser.add_argument(
        "--write-adjacency",
        action="store_true",
        help=(
            "Also build and write an Africa adjacency edge list "
            "(iso3, neighbor_iso3, shared_border_km) using Natural Earth boundaries."
        ),
    )
    parser.add_argument(
        "--adjacency-output-dir",
        default="labs/lab6_africa/data/raw/adjacency",
        help="Directory for adjacency CSV (default: labs/lab6_africa/data/raw/adjacency).",
    )
    parser.add_argument(
        "--ne-url",
        default=NATURAL_EARTH_URL,
        help="Override the Natural Earth country boundaries URL.",
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help=(
            "Generate synthetic country-level radiance (no raster download). "
            "For CI and quick-start validation."
        ),
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Synthetic data (smoke-test mode)
# ---------------------------------------------------------------------------

def synthetic_radiance(year: int, africa_iso3: List[str]) -> pd.DataFrame:
    """Return plausible synthetic mean radiance values for African countries.

    Values are calibrated to approximate the order of magnitude of real VIIRS
    annual composites (nanoWatts/cm²/sr): coastal/urban countries trend higher;
    Saharan/small-island countries trend lower.
    """
    rng = np.random.default_rng(seed=year % 100 + 42)
    base = {
        "NGA": 18.7, "ZAF": 22.4, "EGY": 21.1, "MAR": 15.6, "KEN": 14.1,
        "GHA": 12.3, "TUN": 16.8, "DZA": 11.2, "TZA":  9.9, "UGA":  8.7,
        "CIV": 10.8, "SEN":  9.4, "CMR":  8.3, "ZMB":  7.6, "ZWE":  8.1,
        "MOZ":  6.5, "ETH":  6.2, "SDN":  7.4, "SSD":  3.1, "CAF":  2.8,
        "MDG":  5.3, "MLI":  4.9, "NER":  3.7, "TCD":  3.4, "MRT":  4.1,
        "BFA":  5.8, "BEN":  7.2, "GIN":  4.6, "SLE":  5.1, "LBR":  4.4,
        "TGO":  6.9, "GAB":  9.3, "COG":  6.8, "COD":  4.5, "AGO":  7.2,
        "BWA":  9.7, "NAM":  8.5, "LSO":  6.3, "SWZ":  7.8, "RWA": 11.2,
        "BDI":  6.4, "UGA":  8.7, "DJI": 14.2, "SOM":  3.5, "ERI":  4.8,
        "LBY": 12.7, "GNQ":  8.9, "STP":  6.1, "CPV": 10.4, "COM":  5.7,
        "MUS": 19.3, "GNB":  4.3, "GMB":  6.8, "ESH":  2.9, "MWI":  6.1,
    }
    rows = []
    for iso3 in africa_iso3:
        base_val = base.get(iso3, 5.0)
        noise = rng.normal(0.0, 0.8)
        rows.append({
            "iso3": iso3,
            "year": year,
            "avg_radiance": round(max(0.1, base_val + noise), 2),
        })
    return pd.DataFrame(rows).sort_values("iso3").reset_index(drop=True)


def synthetic_adjacency(africa_iso3: List[str]) -> pd.DataFrame:
    """Return a plausible Africa adjacency edge list with approximate border lengths.

    Uses a hand-coded list of confirmed land borders between African countries.
    Border lengths are approximate (km) from CIA World Factbook / CIESIN data.
    """
    borders = [
        # North Africa
        ("DZA", "LBY",  982), ("DZA", "MAR",  1900), ("DZA", "MRT",  460),
        ("DZA", "MLI", 1359), ("DZA", "NER",  951), ("DZA", "TUN",  965),
        ("DZA", "ESH",   42), ("EGY", "LBY", 1115), ("EGY", "SDN", 1276),
        ("LBY", "TUN",  461), ("LBY", "SDN",  382), ("LBY", "TCD", 1055),
        ("LBY", "NER",  354), ("MAR", "ESH",  443), ("MAR", "MRT",   47),
        ("TUN", "LBY",  461),
        # West Africa
        ("BEN", "BFA",  306), ("BEN", "NER", 277), ("BEN", "NGA", 773),
        ("BEN", "TGO",  651), ("BFA", "GHA",  549), ("BFA", "CIV", 545),
        ("BFA", "MLI", 1000), ("BFA", "NER",  622), ("BFA", "TGO",  126),
        ("CIV", "GHA",  668), ("CIV", "GIN",  610),
        ("CIV", "LBR",  778), ("CIV", "MLI",  532), ("GHA", "TGO",  877),
        ("GIN", "GNB",  421), ("GIN", "LBR",  563), ("GIN", "MLI",  858),
        ("GIN", "SLE",  794), ("GIN", "SEN",  363), ("GMB", "SEN",  749),
        ("LBR", "SLE",  306), ("MRT", "MLI",  2237), ("MRT", "SEN",  742),
        ("MRT", "ESH",  1564), ("MLI", "NER", 838), ("MLI", "SEN",  419),
        ("NER", "NGA",  1497), ("NER", "TCD", 1175), ("NGA", "CMR", 1975),
        ("SEN", "GNB",  338), ("SEN", "MLI", 419), ("SLE", "GIN", 794),
        ("TGO", "GHA",  877),
        # Central Africa
        ("CAF", "CMR",  901), ("CAF", "TCD", 1556), ("CAF", "COD", 1577),
        ("CAF", "COG",  467), ("CAF", "SDN",  174), ("CAF", "SSD",  990),
        ("CMR", "TCD", 1116), ("CMR", "COG", 523), ("CMR", "GAB",  298),
        ("CMR", "GNQ",  183), ("COD", "AGO", 2646), ("COD", "BDI",  236),
        ("COD", "CAF", 1577), ("COD", "COG", 1229), ("COD", "RWA",  221),
        ("COD", "SSD", 639), ("COD", "TZA",  479), ("COD", "UGA",  765),
        ("COD", "ZMB", 2332), ("COG", "GAB",  2567), ("GAB", "GNQ",  350),
        # East Africa
        ("BDI", "RWA",  315), ("BDI", "TZA",  451), ("DJI", "ERI",  109),
        ("DJI", "ETH",  342), ("DJI", "SOM",   58), ("ERI", "ETH", 1033),
        ("ERI", "SDN",  605), ("ETH", "KEN",  861), ("ETH", "SOM", 1600),
        ("ETH", "SDN", 1606), ("ETH", "SSD",  883), ("KEN", "SOM",  682),
        ("KEN", "SSD",  232), ("KEN", "TZA",  775), ("KEN", "UGA",  814),
        ("RWA", "TZA",  222), ("RWA", "UGA",  172), ("SOM", "ETH", 1600),
        ("SDN", "SSD", 2158), ("SDN", "TCD", 1403), ("SSD", "UGA",  475),
        ("TZA", "MOZ",  840), ("TZA", "UGA",  396),
        ("TZA", "ZMB",  338),
        # Southern Africa
        ("AGO", "NAM",  1427), ("AGO", "ZMB", 1065),
        ("BWA", "NAM", 1544), ("BWA", "ZAF", 1840), ("BWA", "ZMB",   360),
        ("BWA", "ZWE",  813), ("LSO", "ZAF",  909), ("MOZ", "MWI",  1569),
        ("MOZ", "ZAF",  496), ("MOZ", "SWZ",  105), ("MOZ", "TZA",  840),
        ("MOZ", "ZMB", 1853), ("MOZ", "ZWE", 1231), ("MWI", "TZA",  475),
        ("MWI", "ZMB", 1477), ("NAM", "ZAF",  967), ("NAM", "ZMB",  233),
        ("SWZ", "ZAF",  438), ("ZAF", "ZWE",  225), ("ZMB", "ZWE",  797),
    ]
    rows = []
    iso_set = set(africa_iso3)
    for a, b, km in borders:
        if a in iso_set and b in iso_set:
            rows.append({"iso3": a, "neighbor_iso3": b, "shared_border_km": km})
            rows.append({"iso3": b, "neighbor_iso3": a, "shared_border_km": km})
    return (
        pd.DataFrame(rows)
        .drop_duplicates(subset=["iso3", "neighbor_iso3"])
        .sort_values(["iso3", "neighbor_iso3"])
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------------
# Raster processing
# ---------------------------------------------------------------------------

def load_africa_boundaries(ne_url: str):
    """Download Natural Earth country boundaries and return Africa subset."""
    import geopandas as gpd
    gdf = gpd.read_file(ne_url)
    # Natural Earth uses ISO_A3 column; fall back to ADM0_A3 if missing
    iso_col = "ISO_A3" if "ISO_A3" in gdf.columns else "ADM0_A3"
    gdf = gdf.rename(columns={iso_col: "iso3"})
    africa = gdf[gdf["iso3"].isin(AFRICA_ISO3)][["iso3", "geometry"]].copy()
    africa = africa.reset_index(drop=True)
    return africa


def extract_country_radiance(
    tif_path: str,
    africa_gdf,
    year: int,
) -> pd.DataFrame:
    """Compute country-level mean VIIRS radiance from a GeoTIFF.

    Strategy
    --------
    1. Open raster and read its nodata value.
    2. For each country polygon, use rasterio.mask.mask to clip.
    3. Exclude nodata pixels and pixels with radiance < 0 (sea/cloud mask).
    4. Record mean of valid lit pixels (or NaN if all masked).

    Valid range for VNL v2.1 average_masked: radiance >= 0 nW/cm²/sr.
    Negative values and nodata indicate masked-out areas.
    """
    import rasterio
    from rasterio.mask import mask as rio_mask
    from rasterio.crs import CRS
    from shapely.geometry import mapping

    rows = []
    with rasterio.open(tif_path) as src:
        nodata = src.nodata
        raster_crs = src.crs

        # Reproject country boundaries to match raster CRS if needed
        if raster_crs and raster_crs != CRS.from_epsg(4326):
            africa_gdf = africa_gdf.to_crs(raster_crs)

        for _, row in africa_gdf.iterrows():
            iso3 = row["iso3"]
            geom = [mapping(row["geometry"])]
            try:
                out_image, _ = rio_mask(src, geom, crop=True, all_touched=False)
                data = out_image[0].astype(float)

                # Mask nodata values
                if nodata is not None:
                    data[data == nodata] = np.nan
                # Mask physically invalid (negative) values
                data[data < 0] = np.nan

                valid = data[~np.isnan(data)]
                mean_rad = float(np.mean(valid)) if len(valid) > 0 else np.nan
            except Exception:
                mean_rad = np.nan

            rows.append({"iso3": iso3, "year": year, "avg_radiance": mean_rad})

    return pd.DataFrame(rows).sort_values("iso3").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Adjacency from Natural Earth (real geometry)
# ---------------------------------------------------------------------------

def build_adjacency_from_boundaries(africa_gdf) -> pd.DataFrame:
    """Compute shared-border adjacency and approximate border length (km).

    Uses shapely .touches() to find shared borders, then computes the
    intersection geometry length in degrees (× 111.12 km/degree).
    """
    import warnings
    rows = []
    n = len(africa_gdf)
    for i in range(n):
        geom_i = africa_gdf.iloc[i]["geometry"]
        iso_i = africa_gdf.iloc[i]["iso3"]
        for j in range(i + 1, n):
            geom_j = africa_gdf.iloc[j]["geometry"]
            iso_j = africa_gdf.iloc[j]["iso3"]
            try:
                if geom_i.touches(geom_j) or geom_i.intersects(geom_j):
                    inter = geom_i.intersection(geom_j)
                    if inter.is_empty:
                        continue
                    # Approximate km: degree-length × 111.12
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        length_deg = inter.length
                    km = round(length_deg * 111.12, 1)
                    if km <= 0:
                        continue
                    rows.append({"iso3": iso_i, "neighbor_iso3": iso_j, "shared_border_km": km})
                    rows.append({"iso3": iso_j, "neighbor_iso3": iso_i, "shared_border_km": km})
            except Exception:
                continue

    return (
        pd.DataFrame(rows)
        .drop_duplicates(subset=["iso3", "neighbor_iso3"])
        .sort_values(["iso3", "neighbor_iso3"])
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.smoke_test:
        print("Running in smoke-test mode (synthetic data).")
        radiance_df = synthetic_radiance(args.year, AFRICA_ISO3)
        adjacency_df = synthetic_adjacency(AFRICA_ISO3) if args.write_adjacency else None
        africa_gdf = None
    else:
        if args.local_tif is None:
            raise SystemExit(
                "Provide --local-tif PATH (path to pre-downloaded VIIRS GeoTIFF).\n"
                "See module docstring for download instructions, "
                "or use --smoke-test for synthetic data."
            )
        print(f"Loading Natural Earth country boundaries from {args.ne_url}")
        africa_gdf = load_africa_boundaries(args.ne_url)
        print(f"  Found {len(africa_gdf)} African countries in Natural Earth data.")

        print(f"Extracting radiance from: {args.local_tif}")
        radiance_df = extract_country_radiance(args.local_tif, africa_gdf, args.year)
        n_valid = radiance_df["avg_radiance"].notna().sum()
        print(f"  Valid country means: {n_valid}/{len(radiance_df)}")

        if args.write_adjacency:
            print("Building adjacency edge list from Natural Earth geometry.")
            adjacency_df = build_adjacency_from_boundaries(africa_gdf)
        else:
            adjacency_df = None

    # Write radiance CSV
    out_path = output_dir / f"viirs_africa_{args.year}.csv"
    radiance_df.to_csv(out_path, index=False)
    print(f"Wrote radiance: {out_path}  ({len(radiance_df)} rows)")

    # Write adjacency CSV
    if adjacency_df is not None:
        adj_dir = Path(args.adjacency_output_dir)
        adj_dir.mkdir(parents=True, exist_ok=True)
        adj_path = adj_dir / "adjacency_africa.csv"
        adjacency_df.to_csv(adj_path, index=False)
        print(f"Wrote adjacency: {adj_path}  ({len(adjacency_df)} rows)")

    # Write a small metadata sidecar
    meta = {
        "year": args.year,
        "smoke_test": args.smoke_test,
        "source_tif": str(args.local_tif) if args.local_tif else None,
        "n_countries": int(len(radiance_df)),
        "n_valid_radiance": int(radiance_df["avg_radiance"].notna().sum()),
        "fetched_at_utc": fetched_at,
    }
    meta_path = output_dir / f"viirs_africa_{args.year}_meta.json"
    with meta_path.open("w", encoding="utf-8") as fp:
        json.dump(meta, fp, indent=2)
    print(f"Wrote metadata: {meta_path}")


if __name__ == "__main__":
    main()
