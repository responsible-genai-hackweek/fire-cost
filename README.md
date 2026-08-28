# fire-cost

**Fire moves fast. Recovery doesn't.**

A wildfire can consume a neighborhood in hours. What comes after — mapping the
damage, tracking what's rebuilt, what's abandoned — takes years. This archive
follows both timescales: the Palisades & Eaton fires, mapped from satellite data in
the days after they burned, and Lahaina, still being counted building by building
two years on.

Wildfire damage and recovery analysis — fire perimeters, satellite burn-severity
analysis, and building-detection results for recent US and Canadian wildfires.

> [!TIP]
> ## 🌐 [**View the live site**](https://responsible-genai-hackweek.github.io/fire-cost/)
>
> Two interactive, browser-only pages — no install, no build step:
> - **Lahaina Wildfire Recovery** — post-fire (Aug 2023) vs. 2025 aerial imagery of
>   Lahaina, Maui, with a draggable swipe divider and building detections on each side.
> - **Palisades & Eaton Fires** — satellite dNBR burn-severity slideshow for the
>   January 2025 Los Angeles fires.

---

## What's in this repo

| Path | Contents |
| --- | --- |
| [`docs/`](docs) | The site published at the link above (GitHub Pages source). Plain HTML/JS, no build step. |
| [`fire_perimeters/`](fire_perimeters) | Fire perimeter boundaries (GeoJSON, EPSG:4326) for 9 wildfires. |
| [`download_perimeters.py`](download_perimeters.py) | Script that fetches the perimeters above from public agency APIs. |

## The site

[`docs/index.html`](docs/index.html) is the landing page, linking to:

- **[`lahaina_wildfire_2023.html`](docs/lahaina_wildfire_2023.html)** — side-by-side
  building-footprint comparison map, built with Leaflet and leaflet-side-by-side.

  ![Lahaina Building Recovery map — left side shows red-outlined buildings still standing 11 days after the Aug 2023 fire, right side shows teal-outlined buildings standing in 2025 (survivors plus rebuilds), with a draggable swipe divider and a confidence-threshold control panel](example.png)

  Drag the divider to compare **left: buildings still standing 11 days after the
  fire** against **right: buildings standing in 2025** (survivors and rebuilds
  combined). A confidence-threshold slider (default 0.6) filters both layers live
  and updates the detection counts shown in the panel; click any footprint for its
  individual confidence score.
  - **Post-fire imagery** — NOAA-hosted (Maxar/WaldoAir), 7.5 cm, Aug 14 2023
  - **Recovery imagery** — Eagleview/Pictometry via Maui County, 3 in, 2025
  - **Detections** — SAM3 building footprints: 848 post-fire, 952 recovery
  - Confidence-threshold slider (default 0.6), live counts, per-layer toggles
  - Detections are in
    [`docs/lahaina_postfire_buildings_2023-08-14.geojson`](docs/lahaina_postfire_buildings_2023-08-14.geojson)
    and
    [`docs/lahaina_recovery_buildings_2025.geojson`](docs/lahaina_recovery_buildings_2025.geojson)
    (WGS84; each feature carries `label` and `confidence_score`).
- **[`palisades_eaton_fires_2025.html`](docs/palisades_eaton_fires_2025.html)** —
  self-contained satellite dNBR burn-severity slideshow for the Palisades and Eaton
  fires (Jan 2025, Los Angeles). No external data files needed.

### Running the site locally

Because the Lahaina map fetches its GeoJSON over HTTP, it has to be served rather
than opened from `file://`:

```sh
cd docs
python3 -m http.server 8000
# then open http://localhost:8000/
```

The Palisades & Eaton page has no external dependencies and will open fine directly
from `file://`.

## Fire perimeters

[`download_perimeters.py`](download_perimeters.py) pulls perimeters for eight US fires
from the WFIGS Interagency Perimeters FeatureServer (NIFC/ArcGIS Online), plus the 2024
Jasper fire in Alberta from NRCan's National Burned Area Composite. One GeoJSON per fire
(EPSG:4326) is committed in [`fire_perimeters/`](fire_perimeters):

Lahaina 2023 · LA 2025 (Palisades, Eaton, Hughes, Hurst) · Spokane 2026 (Old Trails,
Autumn Lane, Fairview) · Jasper AB 2024

Requires `geopandas` and `shapely`:

```sh
pip install geopandas shapely
python3 download_perimeters.py
```

## Attribution and licensing

Post-fire imagery: NOAA-hosted (Maxar/WaldoAir), Aug 14 2023 — CC BY-NC &nbsp;·&nbsp;
2025 imagery: Eagleview/Pictometry via Maui County

Sources:
[NOAA NGS — Maui Hawaii Fire Imagery](https://storms.ngs.noaa.gov/storms/2023_hawaii/index.html) ·
[Maui County GIS — 2025 Pictometry imagery](https://mauicounty.maps.arcgis.com/home/item.html?id=b90c3b88980448d8be4262ce132c816e) ·
[tile service endpoint](https://tiles.arcgis.com/tiles/fsrDo0QMPlK9CkZD/arcgis/rest/services/PictometryLahainaKula_2025/MapServer)

> [!NOTE]
> Detections are model estimates; counts are noisy below ~0.6 confidence. Imagery
> licensing: 2025 Pictometry (Eagleview) — contact Maui County before public use;
> post-fire — CC BY-NC.

## Repo notes

- `lahaina/` and `Presentation/` are earlier, now-superseded copies of the site kept
  around from before it moved to `docs/` (the actual GitHub Pages source). Treat
  `docs/` as canonical; the other two are not actively maintained.

---

Produced by [Element 84's Agentic Queryable Earth](https://element84.com/geospatial/introducing-the-new-agentic-queryable-earth-conversational-composable-and-traceable/).
