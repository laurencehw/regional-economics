"""Fetch selected WIOD 2016-release files from Dataverse.

Source dataset:
- DOI: 10.34894/PJ2M1C
- Dataverse API: https://dataverse.nl/api/datasets/:persistentId/
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import requests


DATASET_DOI = "doi:10.34894/PJ2M1C"
DATASET_META_URL = "https://dataverse.nl/api/datasets/:persistentId/"
DATAFILE_URL_TEMPLATE = "https://dataverse.nl/api/access/datafile/{file_id}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch selected WIOD 2016 Dataverse files")
    parser.add_argument("--doi", default=DATASET_DOI)
    parser.add_argument(
        "--file-ids",
        default="199099,199337,199097",
        help="Comma-separated Dataverse file ids to download",
    )
    parser.add_argument(
        "--output-dir",
        default="data/external/wiod/2016_release",
        help="Directory for downloaded files (recommended: external storage path)",
    )
    parser.add_argument(
        "--manifest-out",
        default="data/raw/metadata/wiod_2016_pull_manifest_2026-02-22.json",
        help="Path for pull manifest JSON",
    )
    parser.add_argument("--timeout", type=int, default=120)
    return parser.parse_args()


def parse_csv_list(raw: str) -> List[int]:
    out: List[int] = []
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        out.append(int(token))
    return out


def sha256_of_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        while True:
            chunk = fp.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def fetch_dataset_metadata(doi: str, timeout: int) -> Dict[str, object]:
    params = {"persistentId": doi}
    response = requests.get(DATASET_META_URL, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    status = payload.get("status")
    if status != "OK":
        raise RuntimeError(f"Unexpected Dataverse response status: {status}")
    return payload


def main() -> None:
    args = parse_args()
    fetched_at = datetime.now(timezone.utc).isoformat()
    wanted_ids = set(parse_csv_list(args.file_ids))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = Path(args.manifest_out)
    manifest_out.parent.mkdir(parents=True, exist_ok=True)

    meta = fetch_dataset_metadata(doi=args.doi, timeout=args.timeout)
    files = meta["data"]["latestVersion"]["files"]
    by_id = {int(item["dataFile"]["id"]): item["dataFile"] for item in files}

    missing_ids = sorted(wanted_ids - set(by_id.keys()))
    if missing_ids:
        raise ValueError(f"Requested file IDs not found in dataset: {missing_ids}")

    downloads: List[Dict[str, object]] = []
    for file_id in sorted(wanted_ids):
        item = by_id[file_id]
        filename = item["filename"]
        expected_size = int(item.get("filesize", 0))
        dst = output_dir / filename

        url = DATAFILE_URL_TEMPLATE.format(file_id=file_id)
        with requests.get(url, stream=True, timeout=args.timeout) as response:
            response.raise_for_status()
            with dst.open("wb") as fp:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        fp.write(chunk)

        actual_size = dst.stat().st_size
        downloads.append(
            {
                "file_id": file_id,
                "filename": filename,
                "expected_size_bytes": expected_size,
                "actual_size_bytes": actual_size,
                "sha256": sha256_of_file(dst),
                "download_path": str(dst),
                "download_url": url,
            }
        )

    manifest = {
        "dataset_doi": args.doi,
        "fetched_at_utc": fetched_at,
        "dataset_url": "https://dataverse.nl/dataset.xhtml?persistentId=doi:10.34894/PJ2M1C",
        "downloads": downloads,
    }
    manifest_out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Downloaded files: {len(downloads)}")
    for d in downloads:
        print(f"- {d['filename']} ({d['actual_size_bytes']} bytes)")
    print(f"Manifest: {manifest_out}")


if __name__ == "__main__":
    main()
