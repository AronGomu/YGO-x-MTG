# YGO × MTG Showcase Website — Checked Implementation Plan

## NOTE : For all design related implementation. Use Impeccable skills and use DESIGN.md.

## Validation audit — 2026-07-19

- **Result: not complete.** Every checkbox was reviewed under a proof-required rule.
- Unchecked boxes remain unchecked where code, test, commit-history, external-setting, deployment, rights, or visual-approval evidence is missing.
- Full evidence matrix: [`website_validation_report.md`](website_validation_report.md).

## Plan status

- [x] Planning only. No application code built in this phase.
- [x] User overrides supersede conflicting recommendations.
- [x] Non-conflicting recommendations become implementation defaults.
- [x] Independent code/security/contract/accessibility reviews completed against this plan.
- [x] Review findings incorporated below.
- [x] Initial public catalog target: ten English MSE projects — six non-archetype sections plus four defined archetypes; publish unique cards after ownership resolution.
- [x] Defined archetypes only: Burning Abyss, Nekroz, Shaddoll, Spellbook.
- [x] Non-archetype sections: Creatures, Fusions, Synchro, Xyz, Link, Non-creature from `03`, `05`, `06`, `07`, `08`, `09` MSE projects.
- [ ] User authorizes implementation before Commit 01 begins.

## Locked product and stack

- [x] Use static Astro app under `website/`.
- [x] Use Svelte islands for header search, filters, sidebar/drawer, interactive galleries, and presentation mode.
- [x] Keep Astro responsible for static routes, HTML, metadata, and build-time source loading.
- [x] Use npm, Node 24, strict TypeScript, scoped CSS, and CSS custom-property theme tokens.
- [x] Use no backend, database, account system, CMS, analytics, CSS framework, or full UI kit.
- [x] Keep website read-only. MSE remains card editor and source of truth.
- [x] Read card text/metadata from included `.mse-set` card files.
- [x] Read final card visuals from canonical `.mse-set/render/*.png` files.
- [x] Use MSE card `image:` artwork for section menu illustrations.
- [x] Build Nekroz as first complete vertical slice, then enable remaining catalog sections without component copies.
- [x] Ship English-only routes, interface copy, metadata, authored content, and card content for MVP.
- [x] Use unprefixed English routes rooted at `/`; do not add `/en`, `/fr`, locale switches, translation placeholders, or `hreflang` in MVP.
- [x] Use global stable card routes at `/cards/<stable-id>/` through one route builder.
- [x] Defer localization architecture and non-English content until after MVP.
- [x] Use homepage feed for both newly added and meaningfully updated cards, with visible status badge.
- [x] Use latest 12 feed items; full feed lives at global `/updates/` route.
- [x] Use card-name-only fuzzy search in header and `Ctrl/Cmd+K` palette.
- [x] Use persistent/collapsible desktop catalog sidebar and modal mobile drawer.
- [x] Left nav order: collapsible Non-Archetype parent first with six child sections (Creatures, Fusions, Synchro, Xyz, Link, Non-creature), then defined archetypes in alphabetical order.
- [x] A card belongs to a defined-archetype gallery only when its owning MSE project is one of the four registered archetypes; every other published card lives under Non-Archetype even if the original Yu-Gi-Oh! card had archetype flavor.
- [x] Use card detail layout: render left, parsed text right, optional authored explanation below.
- [x] Use optional original-YGO comparison in presentation mode.
- [x] Use immutable snapshots scoped by catalog section.
- [x] Vendor approved MSE mana-symbol assets; public build never reads local `F:` path.

## Global commit protocol

- [ ] Before each commit, run `git status --short` and preserve unrelated user files.
- [ ] Before each commit, stage explicit paths only.
- [ ] Before each commit, run `git diff --cached --check`.
- [ ] Before each commit, run all checks listed for that commit.
- [ ] Before each commit, remove temporary exports, caches, traces, screenshots, coverage, and build output not intentionally tracked.
- [ ] Never commit `.env`, machine paths, secrets, `node_modules/`, `.astro/`, `dist/`, Playwright output, or temporary generated assets.
- [ ] Never commit with red required checks.
- [ ] Record each commit hash below.

---

# Commit 01 — Add reusable render export and source validation

- [ ] **Goal:** Establish deterministic MSE render producer before website consumers.
- [ ] Add reusable Python CLI `.script/export_mse_renders.py` using `MSEConfig.load()` only.
- [ ] Support one `.mse-set` input, explicit output, canonical-update mode, and `--dry-run`.
- [ ] Make dry run list manifest cards, exact names, created/modified dates, missing/stale renders, unresolved artwork, and planned output paths.
- [ ] Export to temporary directory outside active `.mse-set`.
- [ ] Require direct MSE CLI exit code `0` and exact manifest PNG count.
- [ ] Decode every export and reject oversized/decompression-bomb images.
- [ ] Rename exports to exact card `name:` values using manifest order.
- [ ] Generate tracked per-project render provenance manifest with schema version, source card hash, referenced artwork hash, render hash, export timestamp, and MSE/style identifiers.
- [ ] Define render-freshness source hash over all effective visual inputs, including manifest order/automatic numbering and `card_code_text*`; exclude only notes, timestamps, BOM, and line-ending noise.
- [ ] Keep semantic-date fingerprint separate so numbering-only changes can invalidate render freshness without advancing card change date.
- [ ] Prove batch-export ordinal mapping with distinct integration fixture compared pixel-for-pixel against isolated one-card exports; otherwise export every card through isolated temporary project.
- [ ] Refuse duplicate display names among manifest-included cards only, missing included cards, unresolved art, path escapes, or stale extra canonical renders; ignore non-included legacy duplicates.
- [ ] Add hash-locked root `requirements-dev.lock` containing full Python dependency closure.
- [ ] Require `pip install --require-hashes -r requirements-dev.lock` locally and in CI.
- [ ] Add Python tests for dry run, naming, source hashing, provenance schema, missing art, duplicates, and temp cleanup.
- [ ] Load paths through canonical `realpath` resolver; reject symlinks/junctions, UNC paths, drive-relative paths, absolute MSE paths, and targets outside approved project root.
- [ ] Add exact resource limits: set/card source bytes, card count, image bytes, dimensions, and decoded pixels.
- [ ] Document chosen limits in CLI help and tests.
- [ ] Run CLI dry run for all ten first-release MSE projects: non-archetype Creatures/Fusions/Synchro/Xyz/Link/Non-creature plus Burning Abyss, Shaddoll, Nekroz, and Spellbook.
- [ ] Run `python -m unittest discover -s tests`.
- [ ] Run `git diff --check`.
- [ ] Commit message: `feat(mse): add canonical render export workflow`.
- [ ] Commit hash: `TODO`.

# Commit 02 — Generate and verify 19 canonical Nekroz renders

- [ ] **Goal:** Complete Nekroz visual source for pilot without website code.
- [ ] Record 2026-07-19 user publication approval and per-asset hashes before staging any binary.
- [ ] Export Nekroz through Commit 01 CLI.
- [ ] Require exactly 19 decodable PNGs.
- [ ] Update `MSE_projects/12_YGO_Necroz.mse-set/render/` only after full export succeeds.
- [ ] Commit matching Nekroz render provenance manifest.
- [ ] Confirm canonical render names equal 19 manifest card names exactly.
- [ ] Re-export remaining first-release projects to temporary directories after ownership mapping exists.
- [ ] Compare decoded pixels of every re-export against existing canonical render.
- [ ] Backfill provenance only when re-export pixels match exactly; replace canonical render only through explicit reviewed regeneration when they differ.
- [ ] Decode all first-release renders across ten MSE projects.
- [ ] Strip unsafe PNG ancillary metadata only in future public derivatives; preserve canonical MSE originals inside source project.
- [ ] Visually inspect named samples: Nekroz — Trishula, Burning Abyss — Dante, Pilgrim, El Shaddoll — Construct, High Priestess of Prophecy, plus one card from each non-archetype section.
- [ ] Check sample art, symbols, text overflow, frame integrity, and readability.
- [ ] Delete temporary exports.
- [ ] Run `python -m unittest discover -s tests`.
- [ ] Run `git diff --check`.
- [ ] Stage only canonical renders/provenance directly belonging to this step.
- [ ] Commit message: `chore(showcase): add canonical Nekroz renders`.
- [ ] Commit hash: `TODO`.

# Commit 03 — Enforce meaningful MSE modification timestamps

- [ ] **Goal:** Ensure website dates represent visible/mechanical card changes, not maintenance churn.
- [ ] Inventory every repository script/skill that writes MSE card files.
- [ ] Define semantic card fingerprint fields: display name, cost, type/subtype, rarity, rules, flavor, P/T, and other visible non-art face fields; exclude source artwork bytes.
- [ ] Exclude notes, timestamps, collection numbering, path-only normalization, BOM, and line-ending changes from semantic fingerprint.
- [ ] Count artwork change only when final rendered pixels change; equivalent source path/metadata/encoding changes do not count.
- [ ] Add shared Python helper that updates `time_modified` when non-art semantic fingerprint changes.
- [ ] Make canonical render export/reconciliation sole artwork-date producer: advance `time_modified` only after normalized final render pixels change.
- [ ] Update active MSE-writing scripts to use shared helper without rewriting unrelated metadata.
- [ ] Validate MSE GUI saves for semantic change, no-op save, numbering-only change, and artwork-only visible/no-visible change.
- [ ] Add pre-publication reconciliation comparing committed semantic/render fingerprints with current GUI output.
- [ ] Reject timestamp-only GUI churn; provide explicit normalization command that restores prior timestamp without altering card content.
- [ ] Define timestamp grammar `YYYY-MM-DD HH:MM:SS` as timezone-free local time.
- [ ] Add tests proving rules/stats/art/name changes advance timestamp.
- [ ] Add tests proving numbering/notes/path-normalization-only changes do not advance timestamp.
- [ ] Add tests proving unchanged reruns are idempotent.
- [ ] Update relevant project skills/docs so future writers preserve timestamp contract.
- [ ] Run `python -m unittest discover -s tests`.
- [ ] Run `git diff --check`.
- [ ] Commit message: `fix(mse): preserve meaningful card modification dates`.
- [ ] Commit hash: `TODO`.

# Commit 04 — Scaffold Astro, Svelte, and baseline test harnesses

- [ ] **Goal:** Create minimal static site that builds and runs tests without card content.
- [ ] Create `website/package.json` and committed `package-lock.json`.
- [ ] Pin Node 24 in `website/.nvmrc` and `package.json#engines`.
- [ ] Add Astro static output and `@astrojs/svelte`.
- [ ] Add strict Astro/TypeScript configuration.
- [ ] Add environment-validated single source for `SITE_URL` and `BASE_PATH`.
- [ ] Configure production source maps off.
- [ ] Add CSS tokens for layout, typography, color, contrast, elevation, focus, motion, and catalog-section accents.
- [ ] Add dark semantic smoke layout and page.
- [ ] Add `prefers-reduced-motion` baseline with no automatic motion loop over five seconds and no flashing.
- [ ] Add Vitest.
- [ ] Add Playwright now, before any later commit claims browser tests.
- [ ] Add one production-preview Playwright smoke test.
- [ ] Add exact command for installing pinned Chromium, Firefox, WebKit, and required system dependencies.
- [ ] Add exact package scripts: `dev`, `build`, `preview`, `check`, `lint`, `format`, `format:check`, `test`, `test:e2e`, `content:check`, `links:check`.
- [ ] Add ESLint Astro/Svelte support and Prettier Astro/Svelte support.
- [ ] Update root `.gitignore` for website dependencies/build/test residue.
- [ ] Verify both base modes: `/YGO-x-MTG/` and `/`.
- [ ] Run `npm ci`.
- [ ] Run `npm run format:check`.
- [ ] Run `npm run lint`.
- [ ] Run `npm run check`.
- [ ] Run `npm run test`.
- [ ] Run `npm run build` in both base modes.
- [ ] Run `npm run test:e2e`.
- [ ] Commit message: `feat(showcase): scaffold Astro and Svelte site`.
- [ ] Commit hash: `TODO`.

# Commit 05 — Parse MSE into allowlisted public data

- [ ] **Goal:** Build safe, typed, read-only MSE ingestion boundary.
- [ ] Define raw MSE field model separately from public parsed-card DTO.
- [ ] Map exact keys: `super_type`, `sub_type`, `rule_text`, `flavor_text`, `card_code_text`, and repeated face/number fields.
- [ ] Define optionality per card type; require P/T as pair only for creature types.
- [ ] Validate repeated `card_code_text*` values agree where present.
- [ ] Parse UTF-8 with/without BOM, tab indentation, blank fields, and multiline values.
- [ ] Preserve source path/line only in diagnostics; never expose it in public DTO.
- [ ] Preserve unknown fields internally only; never serialize them publicly.
- [ ] Parse included manifest entries in order and ignore non-included legacy files.
- [ ] Parse timezone-free timestamps into local calendar/date-time objects without UTC conversion.
- [ ] Require valid `time_modified` for publication; reserve Git fallback for local diagnostics only.
- [ ] Define stable ordering tie-break: modified descending, manifest index ascending, stable ID ascending.
- [ ] Define one strict English publication predicate accepting canonical source tokens `EN` and `English`; reject unknown, conflicting, or non-English language values.
- [ ] Validate `set_language` + `card_language` through that English-only publication predicate.
- [ ] Implement canonical `realpath` containment for manifest/card/image/render paths; reject symlinks/junctions and Windows path variants escaping approved roots.
- [ ] Enforce source byte, field length, card count, token count, and nesting-depth limits.
- [ ] Define escaped public DTO containing only website-required fields.
- [ ] Use framework-safe JSON serialization for hydrated Svelte props and search data.
- [ ] Add malicious fixtures in every public string field: names, aliases, types, metadata, rules, flavor, and routes.
- [ ] Add synthetic fixtures for BOM, multiline, malformed indentation, duplicate keys, optional fields, repeated fields, and limits.
- [ ] Add live contract tests for ten English first-release projects and exact unique published total after ownership resolution.
- [ ] Assert Nekroz publishes 19 manifest cards despite legacy duplicates.
- [ ] Add read-only test proving source bytes never change.
- [ ] Run `npm run content:check`.
- [ ] Run `npm run test`.
- [ ] Run `npm run check`.
- [ ] Commit message: `feat(showcase): parse MSE card projects safely`.
- [ ] Commit hash: `TODO`.

# Commit 06 — Define catalog registry, publication graph, and stable IDs

- [ ] **Goal:** Centralize every route, search, nav, and publication decision.
- [ ] Create typed registry for ten catalog sections: six non-archetype sections plus four defined archetypes.
- [ ] Non-archetype sections map 1:1 to MSE projects `03`, `05`, `06`, `07`, `08`, `09` with fixed labels Creatures, Fusions, Synchro, Xyz, Link, Non-creature.
- [ ] Defined archetypes map to MSE projects `10`, `11`, `12`, `13` with labels Burning Abyss, Shaddoll, Nekroz, Spellbook.
- [ ] Register all ten but set Nekroz as only initially published section for the vertical slice.
- [ ] Record English source, English label, section kind (`non-archetype` | `archetype`), doc-derived intro source, optional authored override, theme tokens, order, iconic ID, and support-role IDs where applicable.
- [ ] Treat doc-derived intros/overrides as plain text or pass them through same raw-HTML-disabled, safe-URL-allowlisted Markdown pipeline as card explanations.
- [ ] Ownership rule: a card publishes under a defined archetype only when its owning MSE project is one of the four registered archetypes; every other published card lives under Non-Archetype even if the original Yu-Gi-Oh! card had archetype flavor.
- [ ] When the same display name appears in both a defined-archetype project and a non-archetype/staple project, defined-archetype ownership wins; the staple copy is not published as a second public card.
- [ ] Known first-release ownership collisions: `Herald of the Arc Light` → Nekroz; `Downerd Magician` and `Leviair the Sea Dragon` → Burning Abyss.
- [ ] Mark four Nekroz support cards that live inside the Nekroz MSE project but are not Nekroz-named cards; they still publish under Nekroz because that project is a defined archetype package.
- [ ] Record iconic defaults for archetypes: Dante, Construct, Trishula, High Priestess; record one iconic default per non-archetype section.
- [ ] Record optional original-YGO comparison image mapping.
- [ ] Define explicit stable card IDs and mappings for every published English source filename after ownership resolution.
- [ ] Track former source filenames, searchable former display names, and route aliases as separate concepts.
- [ ] Keep stable ID unchanged when source filename/display name changes.
- [ ] Define retired identity/tombstone shape retained for historical snapshots.
- [ ] Define shared English publication graph used by routes, search, sitemap, homepage, sidebar, and snapshots.
- [ ] Keep localization and translation-equivalence modeling out of MVP.
- [ ] Add publication-level withdrawal status that removes affected live/snapshot routes and assets from public output without rewriting immutable source history.
- [ ] Document withdrawal as website-output control only, not erasure from public Git history/clones/artifacts.
- [ ] Validate all registered MSE sources declare `set_language: EN` and `card_language: English`; test live headers plus invalid/non-English fixtures.
- [ ] Reject duplicate IDs, missing manifest mappings, duplicate active public names after ownership resolution, missing iconic IDs, and invalid aliases.
- [ ] Define one route builder with exact English templates, base path handling, and trailing-slash policy.
- [ ] Use global card routes so section reassignment does not change canonical card URL.
- [ ] Left-nav model: collapsible Non-Archetype parent first; child order Creatures → Fusions → Synchro → Xyz → Link → Non-creature; then defined archetypes alphabetical (Burning Abyss, Nekroz, Shaddoll, Spellbook).
- [ ] Section routes: `/sections/non-archetype/<slug>/` for non-archetype children and `/archetypes/<slug>/` for defined archetypes, or one shared `/sections/<slug>/` builder if that keeps one template without losing nav labels.
- [ ] Add tests for ownership resolution, collision winners, retired identities, rename preservation, route output, English-only publication, nav order, support roles, and iconic resolution.
- [ ] Run `npm run content:check`.
- [ ] Run `npm run test`.
- [ ] Commit message: `feat(showcase): register catalog sections and card identities`.
- [ ] Commit hash: `TODO`.


# Commit 07 — Convert MSE markup into safe semantic content

- [ ] **Goal:** Render faithful searchable card text without raw HTML injection.
- [ ] Define rich-text AST for text, paragraphs, line breaks, bold, italic, auto labels, word-list values, separators, and mana symbols.
- [ ] Parse every markup form used by all first-release published cards.
- [ ] Reject unknown/unbalanced markup with card path and line context.
- [ ] Preserve punctuation, quotes, accents, and intentional line breaks.
- [ ] Never use unsanitized raw HTML rendering.
- [ ] Render accessible mana symbols with visible PNG plus hidden English label.
- [ ] Render casting costs with greedy token parser.
- [ ] Keep normalized plain text alongside AST for search/accessibility.
- [ ] Test XSS-like payloads across text nodes, attributes, metadata, JSON hydration, and search serialization.
- [ ] Add fixtures for every active MSE tag and cost pattern.
- [ ] Add structural assertions rather than snapshot-only tests.
- [ ] Run `npm run test`.
- [ ] Run `npm run check`.
- [ ] Commit message: `feat(showcase): render MSE card text safely`.
- [ ] Commit hash: `TODO`.

# Commit 08 — Bundle, sanitize, and validate public images

- [ ] **Goal:** Publish pixel-faithful derivatives without leaking metadata or local paths.
- [ ] Resolve final render by exact card name inside owning project render folder.
- [ ] Resolve iconic/original comparison art only through canonical contained path resolver.
- [ ] Verify render provenance source hash matches current visual source hash.
- [ ] Require every render, iconic image, original-comparison image, derivative, and OG image hash to resolve to active rights/attribution/approval evidence.
- [ ] Apply withdrawal status before asset import so revoked assets never enter public output.
- [ ] Reject missing, stale, extra, duplicate, undecodable, oversized, or path-escaping assets.
- [ ] Generate metadata-stripped public PNG derivatives; retain canonical MSE originals outside public artifact.
- [ ] Generate WebP/AVIF gallery variants.
- [ ] Record dimensions/aspect ratios and never crop card renders.
- [ ] Emit hashed asset filenames.
- [ ] Eager-load first visible content; lazy-load rest.
- [ ] Ensure build contains no `F:`, repository root, home path, UNC path, `file:` URL, EXIF/XMP/text chunks, or tool-local metadata.
- [ ] Add tests mapping every published unique card to one valid render and every published section iconic card to one valid illustration.
- [ ] Add tests for malicious image paths, symlinks/junctions, decompression bombs, and unsafe metadata.
- [ ] Run `npm run content:check`.
- [ ] Run `npm run test`.
- [ ] Run `npm run build`.
- [ ] Commit message: `feat(showcase): bundle safe canonical card assets`.
- [ ] Commit hash: `TODO`.

# Commit 09 — Build English shell and accessible navigation

- [ ] **Goal:** Create shared English chrome before card experiences.
- [ ] Keep MVP interface copy in English without an i18n dependency or locale dictionary layer.
- [ ] Set `<html lang="en">` on every page.
- [ ] Serve homepage and all MVP routes without locale prefixes.
- [ ] Do not render language links, translation placeholders, locale redirects, or `hreflang` in MVP.
- [ ] Build labeled desktop catalog navigation with collapsible Non-Archetype parent first, six child sections, then alphabetical defined archetypes; expose collapse with `aria-expanded`/`aria-controls`.
- [ ] Give every icon-rail destination visible tooltip and accessible name.
- [ ] Build named modal mobile drawer with initial focus, inert background, focus trap, Escape close, and focus restoration; preserve Non-Archetype parent/child structure on mobile.
- [ ] Add header search slot.
- [ ] Add skip link, landmarks, heading hierarchy, current-route text/shape cue, and persistent `:focus-visible`.
- [ ] Add Astro View Transitions only when motion allowed.
- [ ] Disable transitions, smooth scrolling, parallax, tilt, sweep, reveal movement, and ambient movement under reduced motion.
- [ ] Use no auto-moving decorative loop over five seconds and no flashing.
- [ ] Support forced-colors mode and WCAG AA text/UI contrast; focus indicator at least 3:1.
- [ ] Add responsive checks at 320, 375, 768, 1280, and 1920 CSS pixels.
- [ ] Add 200% text zoom and 400% reflow checks.
- [ ] Ensure portrait/landscape support, no zoom suppression, virtual-keyboard-safe focus, and WCAG 2.2 target sizing.
- [ ] Run unit and Playwright tests in Chromium, Firefox, and WebKit for shell/navigation.
- [ ] Run `npm run test:e2e`.
- [ ] Commit message: `feat(showcase): add English navigation shell`.
- [ ] Commit hash: `TODO`.

# Commit 10 — Deliver complete 19-card Nekroz vertical slice

- [ ] **Goal:** Prove reusable catalog-section page with Nekroz before enabling others.
- [ ] Create one English catalog-section route template reused by non-archetype and archetype sections.
- [ ] Publish `/archetypes/nekroz/` with exactly 19 English manifest cards.
- [ ] Generate no locale availability or translation-placeholder routes.
- [ ] Render hero, doc-derived identity, iconic illustration, count, and latest update.
- [ ] Render responsive linked card grid with meaningful alt/decorative handling.
- [ ] Group by local calendar day newest first; keep manifest order inside day.
- [ ] Define shared filter query schema: `on`, inclusive `since`, inclusive `until`, `wave=latest`, type, rarity, card-name query, and normalized parsed-card-text query.
- [ ] Keep section parsed-text filtering separate from header global search, which remains card-name-only.
- [ ] Define invalid-value behavior, canonical query ordering, and round-trip serializer.
- [ ] Add labeled native controls; use fieldset/legend where grouped.
- [ ] Add keyboard-operable clear action and preserve focus after filtering.
- [ ] Announce result counts/no-results through polite live region.
- [ ] Persist filters in URL and use same parsed order for presentation mode later.
- [ ] Add support-card text badge/non-color cue for four support cards.
- [ ] Add user-triggered hover/focus tilt, foil, and glow with equivalent non-motion focus affordance.
- [ ] Use accessible link names independent of artwork.
- [ ] Test filters, boundaries, latest wave, URL round trip, invalid params, tie ordering, empty state, keyboard flow, and reduced motion.
- [ ] Capture named QA evidence for Nekroz — Trishula at 375×812, 1280×720, 1920×1080, 200% zoom, 400% reflow, reduced motion, and forced colors; include Non-Archetype nav collapse evidence.
- [ ] Run `npm run test`.
- [ ] Run `npm run test:e2e`.
- [ ] Run `npm run build`.
- [ ] Commit message: `feat(showcase): publish Nekroz catalog gallery`.
- [ ] Commit hash: `TODO`.

# Commit 11 — Add stable card detail pages and authored explanations

- [ ] **Goal:** Make each published card readable and directly shareable.
- [ ] Generate global stable-ID card routes from one route builder.
- [ ] Use desktop render-left/text-right layout and accessible mobile DOM order.
- [ ] Render heading, cost, type/subtype, rarity, rules, flavor, P/T when valid, collection number, and English-formatted modified date.
- [ ] Avoid duplicating full parsed text in image alt; use concise alt plus adjacent semantic transcription.
- [ ] Add named zoom trigger and native modal `<dialog>` opened with `showModal()`, with initial focus, focus trap, Escape, close control, inert background, and focus restoration.
- [ ] Add English Markdown collection keyed by stable ID.
- [ ] Disable MDX/components and raw HTML.
- [ ] Allowlist Markdown elements/attributes.
- [ ] Allow safe link schemes only; reject `javascript:`, unsafe `data:`, `file:`, remote images, and tracking pixels.
- [ ] Require same-origin approved images.
- [ ] Omit explanation when file absent.
- [ ] Add previous/next manifest navigation and three deterministic same-section related cards.
- [ ] Add breadcrumb and canonical route data.
- [ ] Test valid/missing explanation, unknown ID, duplicate explanation file, malicious URLs, raw HTML, image zoom, focus flow, and direct load.
- [ ] Run `npm run test`.
- [ ] Run `npm run test:e2e`.
- [ ] Commit message: `feat(showcase): add card detail pages`.
- [ ] Commit hash: `TODO`.

# Commit 12 — Build immutable snapshot engine

- [ ] **Goal:** Add atomic, self-contained historical data model before routes/content.
- [ ] Define schema-versioned snapshot scoped by catalog section with required explicit parent or `--no-parent`.
- [ ] Reject cross-section parent IDs and lineage forks; maintain one explicit published head per catalog section.
- [ ] Define canonical UTF-8 serialization, deterministic key order, SHA-256, and exact hashed field set.
- [ ] Exclude notes, unknown editor fields, source paths, BOM, and line-ending noise from content hash.
- [ ] Store full lineage state for every active card ID/fingerprint, even when release selection contains only changed subset.
- [ ] Store selected release entries separately from full baseline state.
- [ ] Store self-contained public DTO and exact public image derivatives for selected historical entries.
- [ ] Retain removed cards through snapshot-contained identity rather than active registry validation.
- [ ] Validate active IDs when creating snapshot; allow retired/tombstoned IDs when reading history.
- [ ] Require CLI `--section`, `--parent` or `--no-parent`, plus optional `--on`, inclusive `--since`, inclusive `--until`, and explicit IDs.
- [ ] Refuse overwrite of existing snapshot ID.
- [ ] Classify `new`, `updated-text`, `updated-art`, `renamed`, and unchanged against full parent state.
- [ ] Add merge-base immutability checker rejecting modification/deletion/rename of pre-existing snapshot payloads/assets while verifying hashes.
- [ ] Add deterministic tests for lineage heads, fork rejection, partial selection/full baseline, removed cards, rename stability, hashes, schema version, overwrite refusal, and immutability guard.
- [ ] Do not add routes or snapshot content in this commit.
- [ ] Run `npm run test`.
- [ ] Commit message: `feat(showcase): add immutable snapshot engine`.
- [ ] Commit hash: `TODO`.

# Commit 13 — Add generic historical snapshot routes

- [ ] **Goal:** Render any valid snapshot without adding production snapshot data.
- [ ] Add catalog-section snapshot route template through shared route builder.
- [ ] Render selected entries from self-contained snapshot DTO/assets, never current live cards.
- [ ] Add snapshot title, date, selected count, status classes, and previous/next lineage links.
- [ ] Respect publication withdrawal status so revoked assets/routes are omitted publicly without rewriting source snapshot.
- [ ] Add English unavailable/withdrawn states.
- [ ] Add tests with synthetic snapshots for historical independence, removed cards, lineage links, and withdrawal.
- [ ] Run `npm run test`.
- [ ] Run `npm run build`.
- [ ] Commit message: `feat(showcase): add historical showcase routes`.
- [ ] Commit hash: `TODO`.

# Commit 14 — Publish initial Nekroz showcase snapshot

- [ ] **Goal:** Add accepted first dated showcase as data-only commit.
- [ ] Generate snapshot ID `001-2026-07-17` for English Nekroz lineage with `--no-parent`.
- [ ] Store full baseline state for all 19 active Nekroz cards.
- [ ] Select exactly 15 cards whose MSE `time_modified` local date is `2026-07-17` as visible release entries.
- [ ] Record explicit selected stable IDs and source/render hashes.
- [ ] Confirm four cards dated `2026-07-12` remain in baseline but not visible release entries.
- [ ] Confirm omitted four cards cannot later be misclassified as newly added.
- [ ] Add no route/component code in this commit.
- [ ] Add tests for exact 15 selected IDs, 19-card baseline, immutability, and historical independence.
- [ ] Run `npm run test`.
- [ ] Run `npm run build`.
- [ ] Commit message: `content(showcase): publish first Nekroz showcase`.
- [ ] Commit hash: `TODO`.

# Commit 15 — Add global updates feed and release aggregation

- [ ] **Goal:** Give homepage and “View all” one canonical new/updated source.
- [ ] Aggregate latest snapshot lineage per catalog section.
- [ ] For sections without snapshot, define current published cards as initial `new` entries.
- [ ] Include both newly added and meaningfully updated cards.
- [ ] Sort by modified timestamp descending, manifest index ascending, stable ID ascending.
- [ ] Generate global `/updates/` route.
- [ ] Add filters for status, section, `on`, inclusive `since`, inclusive `until`, and latest wave.
- [ ] Reuse shared query parser/serializer from section pages.
- [ ] Add no-change/empty states and stable pagination or bounded full list.
- [ ] Add tests for per-section lineage, no-snapshot baseline, partial snapshots, new/updated badges, ordering, and URL round trips.
- [ ] Run `npm run test`.
- [ ] Run `npm run build`.
- [ ] Commit message: `feat(showcase): add global card updates feed`.
- [ ] Commit hash: `TODO`.

# Commit 16 — Add accessible global card-name search

- [ ] **Goal:** Find one specific card from every route.
- [ ] Build typed search documents with explicit `matchNames` separate from metadata.
- [ ] Match English current/former card names only; exclude rules, explanations, IDs, and section prose from scorer.
- [ ] Normalize case, punctuation, apostrophes, and spacing.
- [ ] Rank exact, prefix, then bounded fuzzy score; tie-break manifest order, stable ID.
- [ ] Build labeled Svelte combobox inside native modal `<dialog>` opened with `showModal()`, with `aria-expanded`, `aria-controls`, `aria-autocomplete`, listbox/options, stable active-descendant IDs, initial focus, focus trap, inert background, and focus restoration.
- [ ] Add `Ctrl/Cmd+K`, arrows, Enter, and Escape.
- [ ] Add polite result-count/no-results announcement.
- [ ] Link each result to global stable card route.
- [ ] Ensure hydrated search JSON uses safe framework serialization.
- [ ] Add unit tests for normalization, ranking, ties, English-only scope, and security.
- [ ] Add Chromium/Firefox/WebKit keyboard and screen-reader-semantics browser tests.
- [ ] Run `npm run test`.
- [ ] Run `npm run test:e2e`.
- [ ] Commit message: `feat(showcase): add global card search`.
- [ ] Commit hash: `TODO`.

# Commit 17 — Build animated homepage

- [ ] **Goal:** Surface newest changes and provide iconic catalog-section menu.
- [ ] Show latest 12 global feed entries with `New`/`Updated` status text and non-color cues.
- [ ] Link “View all” to `/updates/` while preserving feed semantics.
- [ ] Render large semantic links for currently published catalog sections; pilot shows Nekroz only, and same component automatically expands after remaining sections publish.
- [ ] Show section name, identity, count, and latest update; Non-Archetype may appear as one parent entry or six child entries, but nav order still places Non-Archetype before alphabetical archetypes.
- [ ] Add user-triggered hover/focus tilt, glow, parallax, and reveal under five seconds.
- [ ] Ensure focus styling exposes same information as hover without requiring motion.
- [ ] Disable movement under reduced motion/coarse pointer; never flash.
- [ ] Use meaningful link names independent of artwork; use decorative alt where text already names tile.
- [ ] Reserve image dimensions; lazy-load below fold.
- [ ] Add initial/no-update/error states.
- [ ] Test latest-12 status/order, View all route, no-update state, iconic resolution, keyboard focus, reduced motion, and English labels.
- [ ] Capture QA evidence at 375×812, 1280×720, 1920×1080, 200% zoom, 400% reflow, reduced motion, and forced colors.
- [ ] Run `npm run test`.
- [ ] Run `npm run test:e2e`.
- [ ] Commit message: `feat(showcase): add animated cube homepage`.
- [ ] Commit hash: `TODO`.

# Commit 18 — Add fullscreen presentation and original comparison

- [ ] **Goal:** Preserve recording workflow inside public website.
- [ ] Use named native dialog enhanced with Fullscreen API and fixed-overlay fallback.
- [ ] Layout large card left and English name/date/optional public presenter note right.
- [ ] Source presenter note only from sanitized authored website content; explicitly forbid MSE `notes` field.
- [ ] Add optional original-YGO image comparison toggle where mapping exists.
- [ ] Give original comparison image meaningful English alt text; use empty alt only when adjacent content fully conveys its purpose.
- [ ] Add explicit clean-mode toggle plus inactivity auto-hide.
- [ ] Never hide a focused control; reveal controls on keyboard focus/movement.
- [ ] Add named previous/next/close/fullscreen/clean/comparison controls.
- [ ] Add Left/Right, Space, Home/End, Escape.
- [ ] Set initial focus, trap focus, inert background, and restore trigger focus.
- [ ] Announce current card and position through polite live region.
- [ ] Preserve filtered gallery order.
- [ ] Prefetch adjacent images after open only.
- [ ] Pause/hide decorative motion while open.
- [ ] Disable transitions under reduced motion.
- [ ] Test open/navigation/position announcement/clean mode/focus/fullscreen denial/comparison/Escape.
- [ ] Verify 1920×1080 and 1080×1920 recording layouts.
- [ ] Run `npm run test:e2e`.
- [ ] Commit message: `feat(showcase): add card presentation mode`.
- [ ] Commit hash: `TODO`.

# Commit 19 — Enable remaining first-release catalog sections

- [ ] **Goal:** Complete first generation only after full Nekroz gallery/detail/snapshot/feed/search/home/presentation vertical slice works.
- [ ] Switch remaining nine first-release section publication flags on: Creatures, Fusions, Synchro, Xyz, Link, Non-creature, Burning Abyss, Shaddoll, Spellbook.
- [ ] Add no section-specific page component copies.
- [ ] Publish ten English catalog sections with unique cards after ownership resolution.
- [ ] Generate no non-English or translation-placeholder routes in MVP.
- [ ] Apply section accents only through registry tokens.
- [ ] Resolve every fail-closed source audit issue before publication, including missing required creature P/T and malformed/unbalanced MSE markup; use existing card/rule workflows rather than silently weakening parser validation.
- [ ] Verify support roles, iconic art, rights evidence, render provenance, ownership collisions, and withdrawal status for each section.
- [ ] Confirm left nav shows Non-Archetype parent first, six children in fixed order, then archetypes alphabetical, without component copies.
- [ ] Confirm homepage automatically expands from one to all published section tiles without component edits.
- [ ] Confirm global feed/search automatically include newly published sections.
- [ ] Capture QA evidence for Burning Abyss — Dante, Pilgrim; El Shaddoll — Construct; High Priestess of Prophecy; and one card from each non-archetype section at desktop/mobile/reduced-motion.
- [ ] Test route counts, unique published counts, filters, detail routes, ownership winners, English-only publication, homepage, feed, search, presentation, nav order, and no duplicated page logic.
- [ ] Run `npm run test`.
- [ ] Run `npm run test:e2e`.
- [ ] Run `npm run build`.
- [ ] Commit message: `feat(showcase): publish first cube catalog`.
- [ ] Commit hash: `TODO`.

# Commit 20 — Add SEO, legal notices, CSP, and artifact leak scanning

- [ ] **Goal:** Make public build indexable, shareable, constrained, and auditable.
- [ ] Generate English metadata for home, section, card, updates, and snapshot routes.
- [ ] Generate canonical URLs from the English publication graph; emit no `hreflang` in MVP.
- [ ] Generate sitemap from actual routes only.
- [ ] Generate `robots.txt` and branded English 404.
- [ ] Add card/iconic Open Graph images and Twitter metadata.
- [ ] Add fan-project, asset, and mana-symbol attribution/provenance notices.
- [ ] Add safe external-link rel attributes.
- [ ] Configure no inline production scripts/styles where practical.
- [ ] Add tested meta CSP: `default-src 'none'`; explicit self-only scripts/styles/images/fonts; restrictive `base-uri`, `object-src`, `form-action`, `connect-src`, and `frame-src`.
- [ ] Document that GitHub Pages meta CSP cannot enforce `frame-ancestors`; require header-capable host if anti-framing becomes mandatory.
- [ ] Build allowlisted public DTO/assets only.
- [ ] Scan every text-like `dist/` artifact—HTML, JS, JSON, CSS, XML, maps—for secrets, notes, repo roots, drive/UNC/home paths, and `file:` URLs.
- [ ] Reject unexpected files/symlinks in output.
- [ ] Confirm production source maps are absent.
- [ ] Test malicious values in metadata, attributes, JSON, routes, and search output.
- [ ] Run `npm run build` in `/YGO-x-MTG/` and `/` modes.
- [ ] Run `npm run links:check` in both modes.
- [ ] Commit message: `feat(showcase): harden public metadata and output`.
- [ ] Commit hash: `TODO`.

# Commit 21 — Add complete browser, accessibility, and performance gates

- [ ] **Goal:** Turn manual expectations into reproducible release checks.
- [ ] Add `@axe-core/playwright` checks for home, section, detail, search, filters, mobile drawer, Non-Archetype collapse, zoom, and presentation.
- [ ] Make Chromium, Firefox, and WebKit core smoke matrix mandatory.
- [ ] Test keyboard-only paths, focus traps, inert backgrounds, and focus restoration for every dialog/drawer.
- [ ] Test combobox/listbox semantics and live announcements.
- [ ] Test labels, fieldsets, result announcements, and retained focus after filtering.
- [ ] Test `<html lang="en">` and absence of locale-prefixed routes, language links, translation placeholders, and `hreflang`.
- [ ] Test WCAG AA text/UI contrast, 3:1 focus indicators, forced colors, and non-color status cues.
- [ ] Test 320 CSS-pixel/400% reflow, 200% text zoom, portrait/landscape, virtual keyboard, target size, and no zoom suppression.
- [ ] Test reduced motion disables all listed movement and no content flashes.
- [ ] Add internal route/asset checker.
- [ ] Add compressed first-load JS budget ≤50 KB per catalog-section route excluding images.
- [ ] Add image loading/size budget and adjacent-prefetch assertions.
- [ ] Add Lighthouse diagnostic target ≥90 for performance/accessibility/SEO; report, do not create flaky hard gate until baseline stable.
- [ ] Add visual baselines only after user visual approval.
- [ ] Store QA screenshots/reports as CI artifacts, not source, unless explicitly approved baseline.
- [ ] Add regression test for every bug found.
- [ ] Run format, lint, Astro check, unit, E2E, build, link, Python, and `git diff --check` gates.
- [ ] Commit message: `test(showcase): gate browser quality and accessibility`.
- [ ] Commit hash: `TODO`.

# Commit 22 — Add supply-chain and license policy

- [ ] **Goal:** Define blocking dependency policy before verification/deployment workflows.
- [ ] Add npm advisory check with explicit blocking severity threshold.
- [ ] Add Python advisory check against hash-locked dependency closure with same documented threshold.
- [ ] Add reviewed exception file requiring owner, rationale, issue URL, and expiry date.
- [ ] Fail checks for expired exceptions.
- [ ] Scan direct and transitive production dependency licenses.
- [ ] Reject forbidden/unknown licenses and generate required third-party notices for bundled code.
- [ ] Audit lifecycle install scripts, package maintenance, and package necessity.
- [ ] Add dependency-review configuration for lockfile pull requests.
- [ ] Add monthly grouped Dependabot npm updates.
- [ ] Keep GitHub Action SHA updates reviewed separately.
- [ ] Add exact local package scripts/commands used by CI.
- [ ] Test configuration and failure fixtures.
- [ ] Commit message: `chore(showcase): enforce dependency policy`.
- [ ] Commit hash: `TODO`.

# Commit 23 — Add unprivileged verification CI

- [ ] **Goal:** Verify pull requests/main and produce immutable deployment artifact without deployment privileges.
- [ ] Add GitHub Actions workflow for pull requests and `main` pushes.
- [ ] Never use `pull_request_target`.
- [ ] Pin every third-party action to full commit SHA.
- [ ] Give verification job `contents: read` only.
- [ ] Set up Python 3.13 and install with `pip --require-hashes -r requirements-dev.lock`.
- [ ] Set up Node 24 and npm cache.
- [ ] Run `npm ci` and blocking npm/Python advisory/license checks.
- [ ] Install pinned Playwright Chromium, Firefox, WebKit, and system dependencies.
- [ ] Run Python tests and snapshot merge-base immutability guard.
- [ ] Build repository-base output into isolated `dist-pages/`; run link/leak/E2E checks against it.
- [ ] Build root-base output into isolated `dist-root/`; run link/leak/E2E checks against it.
- [ ] Validate render provenance and all rights-evidence/withdrawal records; do not install/run MSE in CI.
- [ ] Produce explicitly named immutable deploy artifact from `dist-pages/` containing source SHA and artifact SHA-256.
- [ ] Upload preview/QA/deploy artifact only after rights-evidence checks pass.
- [ ] Add concurrency cancellation for stale verification runs.
- [ ] Add `CODEOWNERS` coverage for `.github/workflows/**`, dependency locks, asset-rights inventory, and deployment config.
- [ ] Require branch protection on `main`: pull requests, verification status checks, no direct pushes, and required code-owner review for protected paths.
- [ ] Validate workflow on branch/PR before deployment workflow exists.
- [ ] Commit message: `ci(showcase): verify static website builds`.
- [ ] Commit hash: `TODO`.

# Commit 24 — Add protected GitHub Pages deployment

- [ ] **Goal:** Deploy exact trusted artifact without executing repository/dependency code under Pages/OIDC privileges.
- [ ] Confirm hard blockers and publication approvals are resolved.
- [ ] Add separate deploy workflow triggered by successful verification of trusted `main` SHA.
- [ ] For manual dispatch, require verified workflow run ID and reject runs whose SHA/branch/conclusion do not match trusted `main`.
- [ ] Pin every action to full commit SHA.
- [ ] Grant `pages: write` and `id-token: write` only to deploy job.
- [ ] Protect Pages environment with mandatory required reviewers; do not enable deployment if repository/account settings cannot enforce this gate.
- [ ] Download immutable artifact from exact successful verification run.
- [ ] Verify artifact source SHA and SHA-256 before upload.
- [ ] Run no checkout, package install, build script, or repository code in privileged deploy job.
- [ ] Deploy repository-base artifact only.
- [ ] Add deployment concurrency.
- [ ] Smoke-test deployed home, all ten catalog sections, Non-Archetype collapse, one detail route, updates, snapshot, search, asset, and 404.
- [ ] Document rollback as revert + verified artifact redeploy; never force-push deployment branch.
- [ ] Commit message: `ci(showcase): deploy verified site to GitHub Pages`.
- [ ] Commit hash: `TODO`.

# Commit 25 — Document development, content, and operations

- [ ] **Goal:** Make future archetype/card work data-only and reproducible while recording localization as post-MVP scope.
- [ ] Add concise root README website section.
- [ ] Add detailed `website/README.md`.
- [ ] Document Node/Python prerequisites and every package script.
- [ ] Document MSE source boundaries and read-only website guarantee.
- [ ] Document reusable render dry run/export/provenance workflow.
- [ ] Document timestamp semantic policy, GUI reconciliation, and writer obligations.
- [ ] Document stable IDs, former source names, search aliases, route aliases, retired identities, and withdrawal status.
- [ ] Document catalog registry, Non-Archetype parent/children, alphabetical archetype order, ownership rule, support roles, iconic art, doc-derived intros, and theme tokens.
- [ ] Document mana discovery/copy workflow and rights evidence requirement.
- [ ] Document parser limits, supported markup, and failure diagnostics.
- [ ] Document English-only MVP routes/content and explicitly defer localization, locale dictionaries, alternate-language sources, and `hreflang`.
- [ ] Document optional English explanation/presenter-note Markdown policy.
- [ ] Document snapshot lineage, full baseline vs selected entries, creation, immutability guard, change classes, and global feed semantics.
- [ ] Document search scope as card names only and section parsed-text filter separately.
- [ ] Document presentation controls and comparison-image alt policy.
- [ ] Document dependency/advisory/license policy.
- [ ] Document GitHub Pages verification artifact, deploy, rollback, mandatory reviewers, branch protection, and CODEOWNERS.
- [ ] Document emergency rights-revocation distribution-stop runbook and limits of deleting already-cloned Git history.
- [ ] Add troubleshooting for missing/stale render, malformed MSE, missing symbol, duplicate ID, accidental non-English source, unsafe Markdown, and base-path 404.
- [ ] Verify all documented commands from clean installs.
- [ ] Prove temporary fixture section onboarding requires registry/data only and no component edit; remove fixture afterward.
- [ ] Run complete Python/website quality gates.
- [ ] Commit message: `docs(showcase): document website maintenance`.
- [ ] Commit hash: `TODO`.

---

# Final completion gate

- [ ] All 25 commits exist in order or justified reorder is recorded.
- [ ] Every commit hash field is filled.
- [ ] Unrelated user files remain untouched.
- [ ] Nekroz vertical slice shipped before remaining catalog sections were enabled.
- [ ] Ten English catalog sections publish unique active cards after ownership resolution.
- [ ] Left nav places collapsible Non-Archetype first with six child sections, then alphabetical defined archetypes.
- [ ] Every published card has one stable unprefixed global route and one provenance-valid canonical render.
- [ ] MVP exposes only English UI, metadata, authored content, card content, and accessibility text.
- [ ] MVP emits no locale-prefixed routes, language switcher, translation placeholders, or `hreflang`.
- [ ] Homepage shows latest 12 new/updated entries with status badges and links to full global feed.
- [ ] Header search matches English current/former card names only and opens specific global card routes.
- [ ] Sidebar/drawer navigates Non-Archetype and archetypes accessibly on desktop/mobile.
- [ ] Card pages show render left, safe parsed text right, optional authored explanation below.
- [ ] Presentation mode includes right panel, clean toggle, keyboard controls, and optional original comparison.
- [ ] Snapshot `001-2026-07-17` preserves 19-card baseline and exactly 15 selected Nekroz showcase entries.
- [ ] Maintenance-only MSE/GUI edits do not advance effective `time_modified`; pre-publication reconciliation rejects timestamp churn.
- [ ] Public derivatives contain no unsafe metadata.
- [ ] Build exposes no source paths, notes, unknown fields, secrets, unsafe URLs, raw HTML, source maps, or unexpected files.
- [ ] Chromium, Firefox, WebKit, accessibility, reflow, zoom, forced-colors, reduced-motion, unit, Python, link, type, lint, format, and build gates pass.
- [ ] Both `/YGO-x-MTG/` and `/` base builds pass.
- [ ] Verification CI deploy artifact is bound to trusted main SHA and digest.
- [ ] Privileged deploy job executes no repository/dependency code.
- [ ] Protected GitHub Pages smoke test passes.
- [ ] User approves final visual result.
- [ ] Implementation complete.
