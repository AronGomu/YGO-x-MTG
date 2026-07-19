# YGO × MTG showcase

Static Astro + Svelte presentation of English canonical MSE card projects. MSE remains editor and source of truth; website code never writes source projects.

## Requirements

- Node 24 (`.nvmrc`)
- npm 11+
- Python 3.13 + `python -m pip install --require-hashes -r ../requirements-dev.lock`
- Configured MSE install only when exporting canonical renders (`python ../setup_mse.py`)

## Local commands

```bash
npm ci
npm run dev
npm run format:check
npm run lint
npm run check
npm run content:check
npm run test
npm run build
npm run links:check
npm run test:e2e
```

Install pinned browser engines once:

```bash
npx playwright install --with-deps chromium firefox webkit
```

Root deployment mode uses `SITE_URL=https://example.com BASE_PATH=/ npm run build`. GitHub Pages mode uses `BASE_PATH=/YGO-x-MTG/`. `BASE_PATH` must start and end with `/`.

## Content boundary

`scripts/build-content.mjs` reads only manifest-included cards from ten registered English projects. It validates source limits, language headers, paths, fields, markup, dates, ownership, identities, renders, and image dimensions. Public DTOs omit editor notes, unknown fields, and source paths. Generated files under `public/generated/` and `src/generated/` are build residue.

Currently incomplete Link source records are withheld fail-closed and listed in generated `publicationDiagnostics`; finish those MSE cards through normal card/rule workflows before publication. Do not weaken parser requirements.

## Catalog and identities

`build-content.mjs` owns section registry and fixed nav order: Non-Archetype children (Creatures, Fusions, Synchro, Xyz, Link, Non-creature), then Burning Abyss, Nekroz, Shaddoll, Spellbook. Defined-archetype project ownership wins known duplicate names. Card routes are global: `/cards/<stable-id>/`.

When renaming a source/display name, preserve old stable ID through explicit identity mapping before merging. Keep former display names (search aliases), former filenames, route aliases, retired identities, and withdrawal state separate. Never derive a new ID silently for an already-published card.

MVP is English only. Do not add locale prefixes, language switches, translation placeholders, or `hreflang`.

## MSE render workflow

Dry-run all validation without writing:

```bash
python ../.script/export_mse_renders.py ../MSE_projects/12_YGO_Necroz.mse-set --dry-run
```

Export outside active project:

```bash
python ../.script/export_mse_renders.py ../MSE_projects/12_YGO_Necroz.mse-set --output ../tmp/nekroz-renders
```

Attest existing canonical pixels against a fresh MSE export without replacing renders:

```bash
python ../.script/export_mse_renders.py ../MSE_projects/12_YGO_Necroz.mse-set --attest-canonical
```

Canonical update is atomic with `render-provenance.json`:

```bash
python ../.script/export_mse_renders.py ../MSE_projects/12_YGO_Necroz.mse-set --canonical
```

Exporter converts MSE's opaque RGB output to RGBA and makes only pure-white outer corner pixels transparent; enclosed white card content remains opaque. This versioned transform marks legacy opaque-render provenance stale. Export rejects linked/escaping paths, unresolved art, duplicate included names, stale extra renders, decode-limit violations, nonzero MSE exit, wrong counts, wrong filenames, and corners that remain opaque. Canonical originals remain untouched by website derivative stripping.

## Meaningful dates

`.script/mse_content.py` defines semantic fingerprints and `update_time_modified_if_semantic_changed`. Rules, stats, names, costs, types, rarity, and visible non-art face fields advance `time_modified`. Notes, timestamps, numbering, path-only normalization, BOM, and line endings do not. Artwork dates advance only after final normalized render pixels differ. Timestamp grammar is timezone-free local `YYYY-MM-DD HH:MM:SS`.

## Markup, authored content, symbols

MSE markup is allowlisted and escaped before semantic HTML mapping. Unknown/unbalanced tags fail builds. Explanations live under `content/explanations/<stable-id>.md`; raw HTML, MDX components, remote images, and unsafe URL schemes remain forbidden. Mana symbols must be vendored with rights evidence before use; public output never reads machine-local paths.

## Snapshots and updates

Snapshot `001-2026-07-17` records Nekroz's 19-card baseline and 15 selected release entries. Snapshots use self-contained public card DTOs and render hashes. Never edit, delete, or rename a published snapshot payload; add a child snapshot. Global updates use local timestamps, then manifest index, then stable ID.

## Presentation controls

Gallery presentation uses Previous/Next buttons plus Left/Right, Space, Home/End, Escape, Fullscreen, and Clean mode. Filtered gallery order is preserved. Reduced motion disables card lift and choreographed movement.

## Security, dependencies, deployment

- `npm run audit:deps` blocks high npm advisories, forbidden/unknown production licenses, and unreviewed install-script packages. CI installs with `--ignore-scripts`, then rebuilds reviewed `esbuild`/`sharp` only; review records live in `trusted-install-scripts.json`.
- `python ../.script/audit_python_dependencies.py` checks hash-locked Python packages against OSV.
- Exceptions require owner, rationale, issue, and expiry in `security-exceptions.json`.
- `npm run rights:check` blocks public artifacts until owner approval and per-asset hashes exist in `content/asset-rights.json`.
- Verification CI has `contents: read`, protects snapshot/identity history, builds and browser-checks root/repository base modes, enforces payload budgets/scanners, then emits SHA-bound artifact.
- Pages deployment downloads exact verified run artifact, checks source/digest, runs no checkout/install/build, and requires protected `github-pages` environment reviewers.

Rollback: revert bad source commit, let verification produce new trusted artifact, redeploy it. Never force-push deployment history.

## Rights revocation

Set affected asset/card withdrawal state, rebuild, stop current Pages deployment if needed, and ship verified removal. This controls future website output only; it cannot erase public Git history, clones, caches, or prior downloaded artifacts. Escalate takedown requests to repository owner.

## Troubleshooting

- Missing/stale render → exporter `--dry-run`, then reviewed canonical export.
- Malformed MSE → fix source field/tag; never relax validator.
- Missing symbol → vendor approved asset; never reference local MSE install.
- Duplicate ID/name → resolve ownership or add explicit identity mapping.
- Non-English source → correct source headers/content; no fallback publication.
- Unsafe Markdown → remove raw HTML/remote or unsafe URL.
- Base-path 404 → rebuild with matching slash-delimited `BASE_PATH`, then `npm run links:check`.
