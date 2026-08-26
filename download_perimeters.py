#!/usr/bin/env python3
"""Download fire perimeters for four incidents.

US fires come from the WFIGS Interagency Perimeters FeatureServer (NIFC/ArcGIS
Online), which covers 2016-present but is US-only. The 2024 Jasper fire is in
Jasper National Park, Alberta, so it comes from NRCan's National Burned Area
Composite (NBAC) instead.

Outputs one GeoJSON per fire in data/ (EPSG:4326).
"""

import io
import json
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

WFIGS = (
    "https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services"
    "/WFIGS_Interagency_Perimeters/FeatureServer/0/query"
)
NBAC_2024 = "https://cwfis.cfs.nrcan.gc.ca/downloads/nbac/NBAC_2024_20260513.zip"

# attr_UniqueFireIdentifier is the stable IRWIN-side key: <year>-<unit>-<local id>.
US_FIRES = {
    "la_2025_palisades": "2025-CALFD-000738",
    "la_2025_eaton": "2025-CALAC-009087",
    "la_2025_hughes": "2025-CAANF-250270",
    "la_2025_hurst": "2025-CALFD-0003294",
    "spokane_2026_old_trails": "2026-WANES-001845",
    "spokane_2026_autumn_lane": "2026-WANES-001857",
    "spokane_2026_fairview": "2026-WANES-001852",
    "lahaina_2023": "2023-HIMAUX-000775",
}

# NBAC carries no fire names, only NFIREID. 451 is the Jasper Wildfire Complex:
# ADMIN_NAME=PC (Parks Canada), ADMIN_DIV=JA, 31,645 ha, 2024-07-22 to 2024-09-07.
JASPER_NFIREID = 451

OUT = Path(__file__).parent / "data"


def repair(gdf):
    """Fix self-intersecting rings.

    Several published perimeters have overlapping rings, which makes any area
    computed from them too large (Palisades reads 24,054 ac raw vs 23,448 ac
    published). make_valid + buffer(0) dissolves the overlap and brings the
    computed area back in line with the reported acreage.
    """
    from shapely import make_valid

    bad = ~gdf.geometry.is_valid
    if bad.any():
        gdf = gdf.copy()
        gdf.geometry = gdf.geometry.apply(make_valid).buffer(0)
    return gdf


def fetch_wfigs(uid: str):
    import geopandas as gpd

    params = {
        "where": f"attr_UniqueFireIdentifier='{uid}'",
        "outFields": "*",
        "outSR": "4326",
        "f": "geojson",
    }
    url = f"{WFIGS}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=120) as r:
        fc = json.load(r)
    if "error" in fc:
        raise RuntimeError(f"{uid}: {fc['error']}")
    if not fc.get("features"):
        raise RuntimeError(f"{uid}: no features returned")
    return repair(gpd.GeoDataFrame.from_features(fc["features"], crs="EPSG:4326"))


def fetch_jasper():
    import geopandas as gpd

    raw = OUT / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    shp_dir = raw / "nbac2024"
    if not any(shp_dir.glob("*.shp")):
        print(f"  downloading NBAC 2024 (~74 MB) ...")
        with urllib.request.urlopen(NBAC_2024, timeout=600) as r:
            blob = r.read()
        zipfile.ZipFile(io.BytesIO(blob)).extractall(shp_dir)
    shp = next(shp_dir.glob("*.shp"))
    gdf = gpd.read_file(shp)
    fire = gdf[gdf["NFIREID"] == JASPER_NFIREID]
    if fire.empty:
        raise RuntimeError(f"NFIREID {JASPER_NFIREID} not found in {shp.name}")
    return repair(fire.to_crs("EPSG:4326"))


def acres(gdf) -> float:
    """Area in acres, computed on an equal-area projection (EPSG:6933)."""
    return gdf.to_crs(6933).area.sum() / 4046.86


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    for name, uid in US_FIRES.items():
        gdf = fetch_wfigs(uid)
        path = OUT / f"{name}.geojson"
        gdf.to_file(path, driver="GeoJSON")
        print(f"{name:<26} {uid:<20} {len(gdf)} feat  {acres(gdf):>9,.0f} ac "
              f"(published {gdf.iloc[0]['poly_GISAcres']:,.0f})")

    fire = fetch_jasper()
    path = OUT / "jasper_ab_2024.geojson"
    fire.to_file(path, driver="GeoJSON")
    ha = float(fire.iloc[0]["POLY_HA"])
    print(f"{'jasper_ab_2024':<26} {'NBAC NFIREID 451':<20} 1 feat  "
          f"{acres(fire):>9,.0f} ac (published {ha:,.0f} ha)")


if __name__ == "__main__":
    main()
