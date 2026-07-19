# Website implementation validation

**Audit date:** 2026-07-19  
**Scope:** every checkbox in `website_implementation_plan.md`, `website/`, root MSE tooling/tests, GitHub workflow files, local git history  
**Rule:** `[x]` requires direct code, test, history, runtime, or external-setting proof. Partial impl does not count.

## Verdict

**NOT COMPLETE.** Plan has 563 checkboxes: 32 pre-checked planning/decision boxes, 531 unchecked implementation/protocol/completion boxes. Audit found strong partial implementation, but release blockers plus missing explicit features prevent validating all boxes. No unchecked plan box was promoted without full proof.

Main blockers:

1. Public asset rights remain pending; `npm run rights:check` fails.
2. Planned 25-commit sequence does not exist. Entire website/tooling/workflow implementation remains untracked at `HEAD` (`7af3ac5`). Commit hashes cannot be filled.
3. 26 Link source cards remain withheld fail-closed; Commit 19 requires resolving all source audit issues.
4. Snapshot engine is hardcoded to one Nekroz snapshot, not generic section-scoped lineage/CLI.
5. Updates filters, original-YGO comparison, presenter notes, mana-symbol PNG rendering, rich-text AST, several QA/a11y/perf gates are absent.
6. GitHub branch protection, required environment reviewers, successful verification/deploy runs, deployed smoke checks, visual approval remain externally unverified.

## Executed gates

| Gate | Result | Evidence |
|---|---|---|
| `python -m unittest discover -s tests` | PASS | 77 tests |
| `python .script/audit_python_dependencies.py` | PASS | 1 locked package clean |
| Exporter dry run, all 10 first-release projects | PASS | 10/10 |
| `npm run format:check` | PASS | Prettier clean |
| `npm run lint` | PASS | ESLint clean |
| `npm run check` | PASS | Astro 0 errors; 1 deprecation hint |
| `npm run content:check` | PASS with publication diagnostics | 10 sections, 155 unique cards, snapshot `001-2026-07-17`; 26 cards withheld |
| `npm run test` after content generation | PASS | 17 tests |
| `npm run test` from missing generated DTO state | FAIL | `Cannot find module '../generated/catalog.json'`; clean-checkout test contract broken |
| Root-base `npm run build` | PASS | 170 pages; leak scan clean |
| Repo-base `/YGO-x-MTG/` build | PASS | 170 pages; leak scan clean |
| Root/repo link checks | PASS | 170 pages clean in each mode |
| `npm run budgets:check` | PASS | 7 JS, 170 HTML, 520 images |
| `npm audit --audit-level=high` | PASS | 0 vulnerabilities |
| `npm run licenses:check` | PASS | 169 production packages allowed |
| `npm run test:e2e` | PASS with planned coverage gaps | 20 passed, 4 intentionally skipped |
| Repo-base browser smoke | NOT RUN | Existing user Astro dev server occupies fixed port 4321 |
| `npm run rights:check` | **FAIL / RELEASE BLOCKER** | `publicationStatus: pending-owner-approval`; no approved asset hashes |
| `git diff --check` | PASS | No whitespace errors |
| Commit/history checks | **FAIL** | No Commit 01–25 hashes; website is untracked |

## Commit-by-commit checkbox verdict

| Commit | Verdict | Validated evidence | Unvalidated / failed requirements |
|---|---|---|---|
| 01 render export | PARTIAL | CLI, `MSEConfig.load()`, dry-run, temp export, limits, containment, provenance, hash lock, 10-project dry run | No batch-vs-isolated pixel fixture; sparse exporter tests; root-link containment flaw; no commit/hash |
| 02 Nekroz renders | BLOCKED | 19-card manifest/renders/provenance; all decode through content build | Rights approval absent; full fresh re-export pixel attestation and named visual QA absent; no commit/hash |
| 03 meaningful timestamps | PARTIAL | Shared semantic helper; numbering/notes/timestamp exclusions; tests | Writer inventory/integration incomplete; GUI scenarios, reconciliation command, churn normalization absent; no commit/hash |
| 04 Astro scaffold | PARTIAL | Astro/Svelte static app, Node 24, strict TS, tokens, Vitest/Playwright, scripts, both base builds | `npm run test` fails from clean generated state; repo-base smoke blocked locally; no commit/hash |
| 05 safe MSE parser | PARTIAL | Manifest-only parsing, UTF-8/BOM, containment, limits, English headers, public DTO omission, 155-card graph | No separate typed raw model/runtime schema; creature P/T can both be missing; token/nesting limits and malicious fixture matrix absent; no read-only byte test |
| 06 registry/IDs | PARTIAL | 10-section order, ownership collisions, explicit identities, aliases/withdrawal, global routes | Retired identities still enter live graph; no historical staged publication proof; test matrix incomplete |
| 07 semantic MSE content | **FAIL** | Allowlisted escaping; unknown/unbalanced tags rejected | No rich-text AST, mana PNG assets, greedy cost parser, full tag/cost/XSS fixture matrix |
| 08 public images | BLOCKED | PNG/WebP/AVIF derivatives, metadata scan, dimensions, provenance checks, hashed Astro assets | Rights inventory unapproved; malicious image fixtures incomplete; no dedicated OG derivative generation proof |
| 09 shell/nav | PARTIAL | English shell, nav order, native dialogs, skip link, focus styles, reduced motion, forced colors | Desktop collapse not persistent; no View Transitions; mobile current cue/skip focus/contrast issues; responsive/zoom/target-size QA incomplete |
| 10 Nekroz vertical slice | PARTIAL | Reused section template, exact 19 cards, filters/query round-trip, grouping, support labels, empty state | Named QA captures absent; date controls lack fieldset; coverage incomplete; no commit/hash |
| 11 card details | PARTIAL | Stable global routes, render/text layout, optional safe Markdown, zoom dialog, prev/next/related | Breadcrumb semantics missing; security/focus/direct-load test matrix incomplete |
| 12 snapshot engine | **FAIL** | One hash-checked snapshot shape exists | No generic creation CLI, parent/head/fork logic, overwrite refusal, change classes, generic immutability semantics/tests |
| 13 snapshot routes | **FAIL** | One historical Nekroz route renders snapshot DTO/assets | Route/discovery hardcoded to archetype Nekroz; no generic section route, lineage links, unavailable states, synthetic tests |
| 14 initial snapshot | PASS (data only) | ID/date, 19 baseline, 15 selected, snapshot-contained renders/hash | Commit/history and full independence proof absent |
| 15 global updates | **FAIL** | `/updates/` aggregation/order/status list exists | No filters, shared query controls, empty/no-change state, pagination/bound, lineage tests |
| 16 global search | PARTIAL | Name-only docs, current/former names, normalization/ranking, stable routes, keyboard basics | Focus-trap/semantics/security/browser test matrix incomplete |
| 17 homepage | PARTIAL | Latest 12, status cues, View all, 10 section tiles, responsive imagery/reduced motion | No no-update/error states, QA captures, richer interaction requirements/tests |
| 18 presentation | **FAIL** | Native dialog/fullscreen fallback, prev/next/clean/close, live position, filtered order | Original comparison absent; presenter note absent; adjacent prefetch absent; keyboard handler rejects shortcuts while control focused |
| 19 all sections | **FAIL** | 10 section routes; 155 unique cards; shared templates/nav/home/feed/search expand from registry | 26 Link cards withheld; fail-closed issues unresolved; named cross-section QA/tests absent |
| 20 SEO/security | PARTIAL | Metadata, sitemap, robots, 404, legal, hashed CSP, link/leak scan, no sourcemaps | Secret scanner misses common token classes; OG generation/metadata attack tests incomplete |
| 21 browser/a11y/perf | **FAIL** | Playwright 3-browser smoke; axe on selected routes; forced colors; broad artifact budget | Interactive-state axe matrix, 320/400%/200%, virtual keyboard, target sizes, per-route 50 KiB JS, Lighthouse, QA artifacts absent |
| 22 supply chain | PARTIAL | npm/Python advisory scripts, licenses, exceptions file, Dependabot, reviewed install scripts | Policy failure-fixture tests and full exception/maintenance proof incomplete |
| 23 verification CI | BLOCKED | SHA-pinned actions, read-only perms, Node/Python, two base builds, browser matrix, artifact digest flow | Workflow untracked/unrun; rights gate fails; branch protection/CODEOWNER enforcement unverified |
| 24 Pages deploy | BLOCKED | Separate artifact-only deploy workflow; no checkout/install/build in privileged job | Workflow untracked/unrun; current-main SHA not revalidated after delayed approval; protected environment and deployed smoke unverified |
| 25 docs | PARTIAL | Root/website README covers core local/content/security/ops flows | Clean-install proof, temporary registry-only onboarding proof, full green gates absent |
| Final gate | **FAIL** | Core local static app builds and major flows run | Commit history, rights, source completeness, missing features/QA, CI/deploy proof, user visual approval absent |

## Independent review findings

### P0 — blocking

- **Rights approval absent** — `website/content/asset-rights.json:3-8`. Public artifact intentionally blocked.
- **Commit protocol impossible to validate** — `git log` contains none of planned 25 commits; `website/`, `.github/`, root tooling/provenance remain untracked.

### P1 — major

- **26 publication diagnostics** — `website/scripts/build-content.mjs:376`, emitted at `:867`; Commit 19 explicitly requires zero fail-closed source issues.
- **Generic snapshot contract missing** — hardcoded source at `website/scripts/build-content.mjs:722`; archetype-only route at `website/src/pages/archetypes/[slug]/snapshots/[snapshot].astro`.
- **Snapshot hash meaning drifts** — baseline canonical-render hashes differ from selected snapshot-derivative hashes under same `renderHash` field. Clarify schema before future lineage.
- **Updates requirements absent** — `website/src/pages/updates/index.astro:13-55` renders list only; no status/section/date/wave filters.
- **Presentation requirements absent/broken** — no original comparison/presenter-note data; keyboard exits on focused controls at `website/src/components/FilterGallery.svelte:169-176`.
- **Mana requirement absent** — `website/src/lib/mse-markup.ts:52-53` emits text span, not approved visible PNG + hidden English label.
- **Clean test command broken** — `website/package.json:17` does not generate ignored `src/generated/catalog.json` before Vitest.
- **Deploy can publish stale successful main run after delayed approval** — `.github/workflows/deploy-pages.yml:18-21` does not compare workflow SHA to current `main` after environment wait.
- **Source-root symlink checks occur after canonicalization** — containment evidence is weaker than plan in `website/scripts/build-content.mjs`, `.script/mse_content.py`, `.script/export_mse_renders.py`.

### P2 — accessibility/quality

- Form borders and selected search state likely miss 3:1 non-text contrast — `website/src/styles/global.css`.
- Mobile current route lacks normal-mode non-color cue — `website/src/components/Navigation.svelte` + `website/src/styles/global.css`.
- Skip target `<main>` is not explicitly focusable — `website/src/layouts/BaseLayout.astro:61`.
- Breadcrumbs use slash-delimited paragraphs, not breadcrumb nav semantics.
- Date controls lack `fieldset`/`legend` — `website/src/components/FilterGallery.svelte:239-249`.
- Axe coverage skips open search/filter/drawer/zoom/presentation states; full route scan runs Chromium only.

## Impeccable UI audit

| Dimension | Score | Finding |
|---|---:|---|
| Accessibility | 2/4 | Strong semantics baseline; interaction/contrast/QA gaps remain |
| Performance | 3/4 | Static output, optimized derivatives, bounded bundles; no per-route JS/Lighthouse proof |
| Responsive | 2/4 | Fluid CSS and mobile layouts exist; mandated zoom/reflow/device checks absent |
| Theming | 3/4 | Cohesive OKLCH token system matches `DESIGN.md`; some direct colors remain |
| Anti-patterns | 4/4 | No obvious AI-slop families; artifact-led blackfoil system is distinct |
| **Total** | **14/20** | **Good, not release-complete** |

## Positive evidence

- Architecture follows static Astro + selective Svelte islands.
- Content builder resolves ownership, validates provenance, strips private source fields, generates safe derivatives.
- English-only unprefixed routes, 10-section nav order, 155 unique active card IDs, exact 19-card Nekroz gallery work.
- Snapshot `001-2026-07-17` has 19 baseline IDs and 15 selected entries.
- CSP hardening, output leak scanning, link checks, dependency/license checks, SHA-pinned workflows show strong security intent.
- Visual system follows `DESIGN.md`: neutral blackfoil, artwork-led color, section accents, serif/sans split, limited motion, reduced-motion fallback.

## Required completion order

1. Resolve asset publication rights + record exact approved hashes.
2. Finish 26 withheld Link sources through card/rule workflow.
3. Implement missing snapshot engine/routes, updates filters, mana symbols, presentation comparison/notes/prefetch.
4. Fix clean test contract, presentation keyboard path, a11y contrast/semantics.
5. Expand browser/a11y/reflow/perf/QA evidence.
6. Harden deploy current-main binding + root-link checks.
7. Re-run all local gates, CI, protected Pages deploy/smoke.
8. Obtain final visual approval.
9. Only then mark matching checkboxes `[x]`; commit hashes require actual commit history.
