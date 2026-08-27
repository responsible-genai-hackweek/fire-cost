# fire-cost

Wildfire damage and recovery analysis — fire perimeters and building-detection
results for recent US and Canadian wildfires.

> [!TIP]
> ## 🗺️ [**Open the live map — Lahaina Building Recovery**](https://responsible-genai-hackweek.github.io/fire-cost/lahaina/)
>
> Post-fire (Aug 2023) vs. 2025 aerial imagery of Lahaina, Maui, with a draggable
> swipe divider and building detections on each side. Runs in the browser — nothing
> to install.

---

## The map

[`lahaina/index.html`](lahaina/index.html) — a single static page (plain HTML + JS, no
build step), using Leaflet and leaflet-side-by-side from CDN.

- **Post-fire imagery** — NOAA-hosted (Maxar/WaldoAir), 7.5 cm, Aug 14 2023
- **Recovery imagery** — Eagleview/Pictometry via Maui County, 3 in, 2025
- **Detections** — SAM3 building footprints: 848 post-fire, 952 recovery
- Confidence-threshold slider (default 0.6), live counts, and per-layer toggles

Detections are in
[`lahaina/lahaina_postfire_buildings_2023-08-14.geojson`](lahaina/lahaina_postfire_buildings_2023-08-14.geojson)
and
[`lahaina/lahaina_recovery_buildings_2025.geojson`](lahaina/lahaina_recovery_buildings_2025.geojson)
(WGS84; each feature carries `label` and `confidence_score`).

### Running it locally

The page fetches its GeoJSON over HTTP, so it has to be served rather than opened
from `file://`:

```sh
cd lahaina
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Fire perimeters

[`download_perimeters.py`](download_perimeters.py) pulls perimeters for eight US fires
from the WFIGS Interagency Perimeters FeatureServer (NIFC/ArcGIS Online), plus the 2024
Jasper fire in Alberta from NRCan's National Burned Area Composite. One GeoJSON per fire
(EPSG:4326) is committed in [`fire_perimeters/`](fire_perimeters/):

Lahaina 2023 · LA 2025 (Palisades, Eaton, Hughes, Hurst) · Spokane 2026 (Old Trails,
Autumn Lane, Fairview) · Jasper AB 2024

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

---

Produced by [Element 84's Agentic Queryable Earth](https://element84.com/geospatial/introducing-the-new-agentic-queryable-earth-conversational-composable-and-traceable/).
