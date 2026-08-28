# Wildfire Analysis Archive

Satellite burn-severity and building-recovery analysis for two wildfire events:

- **Palisades & Eaton Fires (Jan 2025, Los Angeles)** — `palisades_eaton_fires_2025.html`
  Self-contained satellite dNBR burn-severity slideshow. No external data files needed.
- **Lahaina Wildfire (Aug 2023, Maui)** — `lahaina_wildfire_2023.html`
  Side-by-side building-footprint comparison map (2023 vs 2025), built with Leaflet.
  Depends on the two `.geojson` files in this folder — keep them alongside the HTML.

Start at `index.html`.

## Viewing locally

Because the Lahaina map fetches its GeoJSON over HTTP, opening `lahaina_wildfire_2023.html`
directly as a `file://` URL will fail in most browsers (CORS/fetch restrictions on local files).
Serve the folder instead:

```bash
cd wildfire-analysis-site
python3 -m http.server 8000
```

Then open `http://localhost:8000/` in your browser.

The Palisades & Eaton page has no external dependencies and will open fine directly from `file://`.

## Publishing to GitHub Pages

1. Create a new repository and push all the files in this folder to the `main` branch
   (the `.nojekyll` file is already included — it stops GitHub from ignoring files/folders
   that start with an underscore, which Jekyll does by default).
2. In the repo: **Settings → Pages** → under "Build and deployment", set
   **Source: Deploy from a branch**, **Branch: main**, folder **/ (root)** → **Save**.
3. GitHub will publish at `https://<your-username>.github.io/<repo-name>/`
   (first deploy can take a minute or two).

No build step, no server-side code — it's a fully static site.

## Data sources

- `lahaina_postfire_buildings_2023-08-14.geojson` — building detections, 11 days post-fire (848 features)
- `lahaina_recovery_buildings_2025.geojson` — building detections, 2025 recovery survey (952 features)
