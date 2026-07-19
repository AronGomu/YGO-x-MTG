# YGO × MTG Showcase Website — Technical Stack Review

**Status:** BASE STACK SETTLED — CUSTOM-BRANCH FOLLOW-UP OPEN  
**Resolution rule:** User accepted every recommendation except explicit overrides below. Existing `TODO` markers remain archived worksheet fields; they no longer mean those choices are unanswered. Newly unblocked choices live in `showcase_technical_followup_questions.md`.

## User overrides — 2026-07-18

- **T5:** Use Svelte islands with Astro so interactive architecture supports future evolution.
- **T22:** Website mana symbols must duplicate MSE symbol assets from `F:/Softwares/Magic-Set-Editor-Full` instead of text-only CSS tokens.
- **T54:** Homepage lists newly added/changed cards and serves as archetype menu. Archetype entries are large illustrated tiles using iconic monster art, strong hover effects, and animation. First release includes additional archetypes, not Nekroz alone.
- **T55:** Global card-name search lives in header. Search resolves specific cards only. Every result links to dedicated card route.
- **Card detail:** Desktop layout uses rendered card left, parsed card text right, then authored description/explanation below.
- **Navigation:** Persistent left catalog navbar. Collapsible Non-Archetype parent first with six child sections, then alphabetical defined archetypes.
- **T63:** MVP is English only. Use unprefixed routes, `<html lang="en">`, English source/content, and no i18n layer, locale switcher, translation placeholders, or `hreflang`; defer localization until after MVP.
- All other recommendations are accepted unless these overrides make them inapplicable.

## Verified constraints

- GitHub repository: `AronGomu/YGO-x-MTG`; current branch `main`.
- No existing website, package manifest, JS lockfile, CI workflow, hosting config, domain config, or site generator.
- Local tools: Python 3.13, Node 24, npm 11.
- Existing project automation and tests use Python.
- Website must consume extensionless MSE card files plus canonical MSE render PNGs.
- MSE source uses UTF-8, sometimes BOM, tab-indented fields, multiline values, and MSE-specific inline markup.
- Nekroz pilot has 19 manifest cards but no canonical `render/` folder yet.
- Website pages need one reusable implementation; archetypes supply data/theme only.
- Website must remain read-only. Card editing stays in MSE and existing repository workflows.

---

# Technical design tree

## Round 1 — Delivery architecture

### T1. Site execution model?

- **A.** Fully static generated site; no production server/database.
- **B.** Server-rendered app.
- **C.** Static pages plus serverless API.
- **Recommended:** A. MSE data changes at build time; no requested server feature needs runtime backend.
- **Your answer:** TODO

### T2. Initial host?

- **A.** GitHub Pages.
- **B.** Cloudflare Pages.
- **C.** Vercel.
- **D.** Netlify.
- **E.** No deployment yet; local only.
- **Recommended:** A. Repository already lives on GitHub; static site needs no paid/runtime platform.
- **Your answer:** TODO

### T3. Are pull-request preview URLs required?

- **A.** Yes.
- **B.** No; CI artifact/local preview is enough.
- **Recommended:** B initially. Choose Cloudflare Pages/Vercel instead of GitHub Pages if preview URLs are mandatory.
- **Your answer:** TODO

### T4. Site framework?

- **A.** Astro.
- **B.** Vite + React SPA.
- **C.** Next.js static export.
- **D.** Eleventy.
- **E.** Custom Python static generator.
- **F.** Plain handwritten HTML/CSS/JS.
- **Recommended:** A. Content-first static routes, build-time filesystem access, minimal client JS, reusable components, strong SEO.
- **Your answer:** TODO

### T5. Client component runtime?

- **A.** Astro components + vanilla TypeScript islands.
- **B.** React islands.
- **C.** Svelte islands.
- **D.** Vue islands.
- **Recommended:** A. Current interactions—filters, tilt, modal, keyboard navigation—do not require framework state machinery.
- **Your answer:** TODO

### T6. Website location in repository?

- **A.** `website/` subdirectory.
- **B.** Repository root.
- **C.** `showcase/` subdirectory.
- **Recommended:** A. Keeps Node app separate from Python/MSE project while preserving one repository.
- **Your answer:** TODO

### T7. Package manager?

- **A.** npm.
- **B.** pnpm.
- **C.** Yarn.
- **D.** Bun.
- **Recommended:** A. Already installed; no monorepo need justifies another tool.
- **Your answer:** TODO

### T8. Node version policy?

- **A.** Pin Node 24 via `.nvmrc` and `package.json#engines`.
- **B.** Support Node 22 and 24.
- **C.** Leave unpinned.
- **Recommended:** A. Reproducible local/CI builds.
- **Your answer:** TODO

### T9. TypeScript policy?

- **A.** Strict TypeScript everywhere.
- **B.** TypeScript with relaxed checks.
- **C.** JavaScript.
- **Recommended:** A.
- **Your answer:** TODO

### T10. Styling stack?

- **A.** Scoped Astro CSS + CSS custom-property design tokens.
- **B.** Tailwind CSS.
- **C.** CSS Modules.
- **D.** Sass.
- **E.** CSS-in-JS.
- **Recommended:** A. Bespoke visual design, zero styling dependency, clean archetype theming.
- **Your answer:** TODO

### T11. UI component library?

- **A.** None; build small semantic components.
- **B.** Headless library for modal/dialog only.
- **C.** Full UI kit.
- **Recommended:** A. Surface is focused; full kit would fight custom YGO × MTG art direction.
- **Your answer:** TODO

### T12. Supported browsers?

- **A.** Current Chrome/Edge only.
- **B.** Current Chrome, Edge, Firefox, Safari.
- **C.** Include older browsers.
- **Recommended:** B.
- **Your answer:** TODO

### T13. JavaScript-disabled baseline?

- **A.** Cards/content remain readable; animation, filtering, modal unavailable.
- **B.** JavaScript required for entire site.
- **Recommended:** A. Static HTML should preserve core showcase content.
- **Your answer:** TODO

---

## Round 2 — MSE ingestion boundary

> Depends on T1, T4, and T6.

### T14. Where should MSE parsing run?

- **A.** TypeScript directly inside Astro build/dev.
- **B.** Python prebuild emits JSON consumed by website.
- **C.** Python generates complete HTML.
- **Recommended:** A. One website pipeline, live dev reload, no generated JSON contract. Keep Python only for MSE render/export workflows.
- **Your answer:** TODO

### T15. How are website archetypes registered?

- **A.** Explicit typed registry listing allowed `.mse-set` projects.
- **B.** Automatically publish every `.mse-set` under `MSE_projects/`.
- **C.** Infer only directories matching archetype naming convention.
- **Recommended:** A. Prevent accidental publication of incomplete/staple projects; registry also stores title/theme/order.
- **Your answer:** TODO

### T16. Registry format?

- **A.** TypeScript data module.
- **B.** JSON.
- **C.** YAML.
- **D.** TOML.
- **Recommended:** A. Typed, no parser dependency, colocated with build code.
- **Your answer:** TODO

### T17. Should parser support only fields currently needed or general MSE syntax?

- **A.** Minimal set/card parser for known fields and multiline values.
- **B.** Full generic MSE parser.
- **Recommended:** A. Full format implementation is unnecessary; preserve unknown fields without interpreting them.
- **Your answer:** TODO

### T18. Encoding behavior?

- **A.** Accept UTF-8 with/without BOM; fail other encodings.
- **B.** Attempt encoding detection.
- **Recommended:** A. Matches repository files and avoids silent text corruption.
- **Your answer:** TODO

### T19. Which MSE fields become website data?

- **A.** Name, mana cost, image, type, subtype, rarity, rules, flavor, power/toughness, card number, created/modified dates.
- **B.** Every MSE field.
- **C.** Name, rules, render, modified date only.
- **Recommended:** A. Covers detail/search/filter/accessibility while excluding editor-only metadata.
- **Your answer:** TODO

### T20. MSE rich-text handling?

- **A.** Parse recognized markup into typed text tokens, then render semantic HTML.
- **B.** Regex-replace tags and inject HTML.
- **C.** Strip all markup to plain text.
- **Recommended:** A. Preserves bold/italic structure without unsafe raw HTML injection.
- **Your answer:** TODO

### T21. Unknown MSE markup?

- **A.** Fail build with card/path/line context.
- **B.** Strip unknown tag and retain text.
- **C.** Render tag literally.
- **Recommended:** A during development. Silent stripping can alter card meaning.
- **Your answer:** TODO

### T22. Mana symbols in parsed website text?

- **A.** Render accessible styled text tokens (`{U}`, `{2}`, etc.).
- **B.** Use symbol SVG/font assets.
- **C.** Keep raw text.
- **Recommended:** A initially. No new licensed/custom font asset required.
- **Your answer:** TODO

### T23. Runtime schema validation after parsing?

- **A.** Zod schema.
- **B.** Custom TypeScript assertions.
- **C.** Compile-time types only.
- **Recommended:** B. Data enters through owned parser; focused assertions avoid dependency for one boundary.
- **Your answer:** TODO

### T24. Generated intermediate JSON?

- **A.** None; parse source directly.
- **B.** Generate and gitignore it.
- **C.** Generate and commit it.
- **Recommended:** A if T14=A.
- **Your answer:** TODO

### T25. Development refresh after MSE edit?

- **A.** Astro dev server watches MSE files and reloads automatically.
- **B.** Manual restart/sync command.
- **Recommended:** A. Add watched source paths through integration/plugin only if normal watcher misses external files.
- **Your answer:** TODO

### T26. Website publication unit?

- **A.** Only `include_file:` entries from each registered project manifest.
- **B.** Every `card *` file in project directory.
- **Recommended:** A. Manifest is source of truth for active set membership.
- **Your answer:** TODO

### T27. Missing card file referenced by manifest?

- **A.** Fail build.
- **B.** Skip with warning.
- **Recommended:** A.
- **Your answer:** TODO

### T28. Incomplete required card field?

- **A.** Fail build.
- **B.** Publish partial detail.
- **C.** Skip card.
- **Recommended:** A for name/render/date; optional fields may remain empty when card type permits.
- **Your answer:** TODO

### T29. Source traceability in generated output?

- **A.** Keep source project/card path in internal build data and diagnostics only.
- **B.** Display repository source link publicly.
- **C.** Omit source paths entirely.
- **Recommended:** A.
- **Your answer:** TODO

---

## Round 3 — Render image pipeline

> Depends on T1, T4, T14, and T26.

### T30. Canonical website image input?

- **A.** Exact PNG under `.mse-set/render/`, matched to card `name:`.
- **B.** Source illustration (`imageN.png`).
- **C.** Website-specific manual export.
- **Recommended:** A, matching explicit product decision.
- **Your answer:** TODO

### T31. Missing render policy?

- **A.** Fail build with export instructions.
- **B.** Auto-run MSE CLI during website build.
- **C.** Show placeholder.
- **Recommended:** A. Hosted CI should not need local Windows MSE installation.
- **Your answer:** TODO

### T32. Should local helper export renders before building?

- **A.** Separate explicit command (`npm run render:mse` or Python command).
- **B.** Automatic part of `npm run build`.
- **C.** Manual MSE GUI only.
- **Recommended:** A. Build remains deterministic; rendering remains available when configured.
- **Your answer:** TODO

### T33. Render freshness check?

- **A.** Require render Git commit at or after card Git commit.
- **B.** Compare filesystem mtimes.
- **C.** Require existence/decodability only.
- **D.** Store content hash metadata when exporting.
- **Recommended:** D long-term; C for pilot. Git commit ordering can combine files and mtimes are unstable.
- **Your answer:** TODO

### T34. How should Astro include renders?

- **A.** Build-time Vite asset imports/glob; emit hashed assets.
- **B.** Copy renders into `website/public/` before build.
- **C.** Reference repository-relative paths directly.
- **Recommended:** A. No duplicated source tree; production cache busting comes free.
- **Your answer:** TODO

### T35. Image optimization?

- **A.** Preserve source PNG only.
- **B.** Emit WebP/AVIF variants plus PNG fallback/download.
- **C.** Convert all to WebP.
- **Recommended:** B. Faster gallery while preserving lossless original.
- **Your answer:** TODO

### T36. Optimization ownership?

- **A.** Astro image pipeline/Sharp.
- **B.** Custom Python Pillow preprocessing.
- **C.** No optimization.
- **Recommended:** A if compatible with external dynamic imports; otherwise B as deterministic prebuild.
- **Your answer:** TODO

### T37. Gallery image loading?

- **A.** First visible cards eager; rest lazy.
- **B.** All eager.
- **C.** All lazy.
- **Recommended:** A.
- **Your answer:** TODO

### T38. Card-image download?

- **A.** Offer original rendered PNG download.
- **B.** No download control.
- **Recommended:** B initially unless public proxy downloads are desired.
- **Your answer:** TODO

### T39. Image dimensions/aspect handling?

- **A.** Read dimensions at build; reserve exact aspect ratio; never crop card render.
- **B.** Force generic 5:7 crop.
- **Recommended:** A.
- **Your answer:** TODO

### T40. Broken/undecodable PNG?

- **A.** Fail build.
- **B.** Warn and publish placeholder.
- **Recommended:** A.
- **Your answer:** TODO

---

## Round 4 — Dates, “new” state, snapshots

> Depends on MSE ingestion and accepted product date recommendations.

### T41. Canonical last-change value in build data?

- **A.** Parse MSE `time_modified`; Git fallback when absent.
- **B.** Git only.
- **Recommended:** A, already accepted at product level.
- **Your answer:** TODO

### T42. How should build obtain Git fallback on hosted CI?

- **A.** GitHub checkout with full history (`fetch-depth: 0`).
- **B.** No fallback in CI; require every card timestamp.
- **Recommended:** B plus validation requiring timestamps. Full history slows build for fallback that should rarely run.
- **Your answer:** TODO

### T43. “New since” filter execution?

- **A.** Client-side over embedded card dates.
- **B.** Separate static route generated per date.
- **C.** Both.
- **Recommended:** C: living-page filter plus intentional snapshot routes.
- **Your answer:** TODO

### T44. Filter URL persistence?

- **A.** Query string (`?since=2026-07-17`).
- **B.** Browser state only.
- **C.** URL hash.
- **Recommended:** A. Shareable filtered views with static hosting.
- **Your answer:** TODO

### T45. Immutable snapshots need exact historical content. Storage strategy?

- **A.** Commit snapshot JSON plus copied exact renders when snapshot is created.
- **B.** Reconstruct historical MSE/render files from Git during every build.
- **C.** Snapshot stores selected card IDs but always shows current content.
- **D.** Remove immutable snapshots; use living filters only.
- **Recommended:** A. Honest recording history, simple builds; duplication occurs only for deliberate releases.
- **Your answer:** TODO

### T46. Snapshot metadata format?

- **A.** Typed JSON manifest.
- **B.** Markdown frontmatter.
- **C.** TypeScript module.
- **Recommended:** A. Machine-generated, easy validation, language-neutral.
- **Your answer:** TODO

### T47. Snapshot route?

- **A.** `/archetypes/nekroz/showcases/001-2026-07-17/`.
- **B.** `/showcases/nekroz/2026-07-17/`.
- **C.** Custom.
- **Recommended:** A. Keeps snapshots under owning archetype and preserves sequence.
- **Your answer:** TODO

### T48. Removed cards on living site?

- **A.** Absent from current archetype page; retained only in immutable snapshots.
- **B.** Retired section.
- **Recommended:** A.
- **Your answer:** TODO

### T49. Stable card identity?

- **A.** Slugified display name.
- **B.** MSE card filename.
- **C.** Collection number + project slug.
- **D.** Explicit stable ID added to registry/metadata.
- **Recommended:** D. Names and numbering can change; stable URLs/history should not.
- **Your answer:** TODO

### T50. Where should stable ID live?

- **A.** New field in MSE card.
- **B.** Website registry mapping source filename to ID.
- **C.** Derived permanently from initial source filename.
- **Recommended:** B. Do not mutate card-domain format solely for website routing.
- **Your answer:** TODO

### T51. Card rename redirect?

- **A.** Keep old slug aliases in registry.
- **B.** Old links may break.
- **C.** Stable ID route means display-name rename does not alter URL.
- **Recommended:** C.
- **Your answer:** TODO

---

## Round 5 — Routes and interaction architecture

> Depends on T1, T4, T5, T15, and T49.

### T52. Required first-class routes?

- **A.** Home + archetype pages only.
- **B.** Home + archetype + card detail pages.
- **C.** Single landing page.
- **Recommended:** B. Card detail routes enable sharing, search indexing, and accessible text.
- **Your answer:** TODO

### T53. Card focus behavior from gallery?

- **A.** Navigate to detail route.
- **B.** Open modal only.
- **C.** Modal with URL update/deep link; direct URL renders full detail page.
- **Recommended:** C, but complexity higher. B for pilot if deep links can wait.
- **Your answer:** TODO

### T54. Homepage scope for pilot?

- **A.** Nekroz feature hero plus one archetype tile.
- **B.** Redirect directly to Nekroz.
- **C.** Full future cube shell with placeholders.
- **Recommended:** A. Real homepage, no fake future content.
- **Your answer:** TODO

### T55. Global search?

- **A.** Client-side index over all published cards.
- **B.** No search until second archetype.
- **C.** Hosted search service.
- **Recommended:** B for pilot, then A. Do not add service/backend.
- **Your answer:** TODO

### T56. Archetype filters?

- **A.** Date, card type, rarity, text query.
- **B.** Date only.
- **C.** No filters.
- **Recommended:** A. Parsed MSE text makes these cheap and useful.
- **Your answer:** TODO

### T57. Filter state implementation?

- **A.** Small vanilla TypeScript controller + URLSearchParams.
- **B.** React state.
- **C.** Global state library.
- **Recommended:** A.
- **Your answer:** TODO

### T58. Fullscreen presentation implementation?

- **A.** Native `<dialog>` enhanced with Fullscreen API.
- **B.** Custom fixed overlay.
- **C.** Separate presentation route.
- **Recommended:** A with fallback when Fullscreen API is denied.
- **Your answer:** TODO

### T59. Pointer tilt implementation?

- **A.** Vanilla pointer events updating CSS variables via `requestAnimationFrame`.
- **B.** Animation library (GSAP/Framer Motion).
- **C.** CSS fixed hover only.
- **Recommended:** A. Small, performant, dependency-free.
- **Your answer:** TODO

### T60. Ambient effects implementation?

- **A.** CSS gradients/pseudo-elements only.
- **B.** Canvas particles.
- **C.** WebGL/Three.js.
- **Recommended:** A for shared shell; no GPU-heavy dependency.
- **Your answer:** TODO

### T61. Archetype theme architecture?

- **A.** Typed theme tokens in registry applied as CSS variables.
- **B.** Separate stylesheet per archetype.
- **C.** One identical color theme for all archetypes.
- **Recommended:** A. Layout/behavior identical; accent identity remains data-driven.
- **Your answer:** TODO

### T62. User theme preference?

- **A.** Dark theme only.
- **B.** Light/dark toggle.
- **C.** System theme.
- **Recommended:** A. Art direction is intentionally dark; accessibility handled through contrast, not alternate theme.
- **Your answer:** TODO

### T63. Site language architecture?

- **Decision:** English-only MVP.
- **Routes:** Unprefixed `/`, `/archetypes/...`, `/cards/...`, `/updates/...`, and snapshot routes.
- **Document language:** `<html lang="en">` on every page.
- **Excluded from MVP:** i18n dependency, locale dictionaries, locale-prefixed routes, language switcher, translation placeholders, and `hreflang`.
- **Deferred:** Localization as a separately planned post-MVP feature.

### T64. Favorites/deck builder/user accounts?

- **A.** None.
- **B.** Local favorites only.
- **C.** Accounts and persisted collections.
- **Recommended:** A. Outside showcase mission.
- **Your answer:** TODO

### T65. CMS/admin editing?

- **A.** None; MSE remains only source/editor.
- **B.** Website admin UI.
- **Recommended:** A, matching explicit source-of-truth rule.
- **Your answer:** TODO

### T66. PWA/offline installation?

- **A.** No.
- **B.** Add service worker/app manifest.
- **Recommended:** A initially. Static host/browser cache already supports repeat viewing.
- **Your answer:** TODO

---

## Round 6 — SEO, accessibility, and public metadata

> Depends on T2, T52, and T63.

### T67. Page rendering for SEO?

- **A.** Fully generated HTML per route.
- **B.** Client-rendered SPA.
- **Recommended:** A.
- **Your answer:** TODO

### T68. Metadata source?

- **A.** Registry for archetype descriptions; parsed card fields for card pages.
- **B.** Manually authored per route.
- **Recommended:** A with optional overrides.
- **Your answer:** TODO

### T69. Open Graph images?

- **A.** Use lead card render directly.
- **B.** Generate branded 1200×630 social images at build.
- **C.** No OG images.
- **Recommended:** A for pilot; B after visual system stabilizes.
- **Your answer:** TODO

### T70. Sitemap and robots?

- **A.** Generate both automatically.
- **B.** None.
- **Recommended:** A for public deployment.
- **Your answer:** TODO

### T71. Canonical URL when no custom domain exists?

- **A.** GitHub Pages project URL.
- **B.** Omit canonical until domain chosen.
- **Recommended:** A, configurable through site setting.
- **Your answer:** TODO

### T72. Accessibility text for card render?

- **A.** Concise alt text plus full parsed card transcription adjacent/on detail page.
- **B.** Put complete rules text in image alt.
- **C.** Image only.
- **Recommended:** A. Avoid enormous alt strings while preserving equivalent content.
- **Your answer:** TODO

### T73. Keyboard interaction standard?

- **A.** Native controls, visible focus, dialog focus trap, Escape, arrow navigation.
- **B.** Mouse-first only.
- **Recommended:** A.
- **Your answer:** TODO

### T74. Motion accessibility?

- **A.** Honor `prefers-reduced-motion`; expose manual motion toggle persisted locally.
- **B.** Media query only.
- **C.** Always animate.
- **Recommended:** B initially. Manual toggle adds UI/state not yet required.
- **Your answer:** TODO

### T75. Contrast target?

- **A.** WCAG AA for text/controls; decorative glow exempt.
- **B.** Visual judgment only.
- **Recommended:** A.
- **Your answer:** TODO

### T76. Analytics?

- **A.** None.
- **B.** Privacy-friendly analytics (Plausible/Cloudflare).
- **C.** Google Analytics.
- **Recommended:** A until a measurement question exists.
- **Your answer:** TODO

---

## Round 7 — Deployment and CI

> Depends on T2, T4, T6, T7, and T31.

### T77. GitHub Pages deployment source?

- **A.** GitHub Actions artifact from site build.
- **B.** Commit built `dist/` to branch.
- **Recommended:** A. Keep generated build output out of source history.
- **Your answer:** TODO

### T78. Deployment trigger?

- **A.** Every push to `main` after checks pass.
- **B.** Manual workflow dispatch.
- **C.** Tagged releases only.
- **Recommended:** A, plus manual dispatch for recovery.
- **Your answer:** TODO

### T79. GitHub Pages base path?

- **A.** Build for `/YGO-x-MTG/` project path.
- **B.** Assume root `/` for future custom domain.
- **C.** Configure from environment so both work.
- **Recommended:** C. Use repository path now; root when custom domain arrives.
- **Your answer:** TODO

### T80. Custom domain now?

- **A.** No.
- **B.** Yes; provide domain later.
- **Recommended:** A.
- **Your answer:** TODO

### T81. CI MSE availability?

- **A.** CI never runs MSE; canonical renders must already be committed.
- **B.** Install/run MSE under Wine/Windows runner.
- **Recommended:** A. Website build validates renders but does not generate them.
- **Your answer:** TODO

### T82. Required CI gates before deploy?

- **A.** Content validation, unit tests, typecheck, lint, format check, site build, internal-link/image check.
- **B.** Build only.
- **C.** Add browser E2E too.
- **Recommended:** A for every push; E2E on PR/main if selected in T87.
- **Your answer:** TODO

### T83. Dependency caching?

- **A.** npm cache through `actions/setup-node`.
- **B.** No cache.
- **Recommended:** A.
- **Your answer:** TODO

### T84. Build artifact retention?

- **A.** Pages artifact only.
- **B.** Also upload preview artifact for every PR.
- **Recommended:** B if PR previews are not hosted.
- **Your answer:** TODO

### T85. 404 handling on static host?

- **A.** Generate branded `404.html` with site navigation/search.
- **B.** Host default.
- **Recommended:** A.
- **Your answer:** TODO

### T86. Security headers/CSP?

- **A.** Strict CSP via meta tag where host headers unavailable; no inline scripts unless hashed/nonced.
- **B.** Basic static deployment without CSP.
- **Recommended:** A if architecture avoids inline scripts. GitHub Pages cannot set arbitrary response headers.
- **Your answer:** TODO

---

## Round 8 — Testing and developer tooling

> Depends on T4, T5, T9, and T20.

### T87. Browser E2E stack?

- **A.** Playwright.
- **B.** Cypress.
- **C.** None.
- **Recommended:** A. Cover page load, filters, keyboard presentation, dialog, and direct card URLs.
- **Your answer:** TODO

### T88. Unit test stack for website TypeScript?

- **A.** Vitest.
- **B.** Node built-in test runner.
- **C.** Jest.
- **Recommended:** A. Native Vite/Astro integration and fast parser tests.
- **Your answer:** TODO

### T89. Existing Python tests?

- **A.** Keep separate; CI runs both Python `unittest` and website tests.
- **B.** Migrate tests to TypeScript.
- **C.** Website CI ignores Python tests.
- **Recommended:** A. Website changes can expose stale repository contracts.
- **Your answer:** TODO

### T90. Visual regression tests?

- **A.** Playwright screenshots for homepage, archetype, detail, presentation.
- **B.** Manual visual QA only.
- **C.** External visual service.
- **Recommended:** B for pilot; add A after design approval to avoid locking unfinished visuals.
- **Your answer:** TODO

### T91. Automated accessibility test?

- **A.** `@axe-core/playwright` on core routes.
- **B.** Static/manual audit only.
- **Recommended:** A once Playwright exists.
- **Your answer:** TODO

### T92. Lint/format stack?

- **A.** ESLint + Astro plugin + Prettier + Astro plugin.
- **B.** Biome only.
- **C.** Prettier only.
- **Recommended:** A. Mature `.astro` support and clear correctness/format separation.
- **Your answer:** TODO

### T93. Astro type/content check?

- **A.** `astro check` required in CI.
- **B.** TypeScript compile only.
- **Recommended:** A.
- **Your answer:** TODO

### T94. Link validation?

- **A.** Build-time route/asset assertions plus post-build link checker.
- **B.** Manual only.
- **Recommended:** A.
- **Your answer:** TODO

### T95. Test fixtures for MSE parser?

- **A.** Small synthetic fixtures covering BOM, tabs, multiline rules, markup, malformed input.
- **B.** Test against live Nekroz files only.
- **C.** Both.
- **Recommended:** C. Fixtures isolate edge cases; live files catch contract drift.
- **Your answer:** TODO

### T96. Lockfile policy?

- **A.** Commit `package-lock.json`; CI uses `npm ci`.
- **B.** Do not commit lockfile.
- **Recommended:** A.
- **Your answer:** TODO

### T97. Dependency update automation?

- **A.** Dependabot monthly grouped updates.
- **B.** Manual only.
- **Recommended:** A after pilot stabilizes.
- **Your answer:** TODO

---

## Round 9 — Performance and asset budgets

> Depends on T35, T37, T54, and T55.

### T98. Initial page performance target?

- **A.** Lighthouse performance/accessibility/SEO ≥ 90 on production build.
- **B.** No numeric target.
- **Recommended:** A as diagnostic target, not brittle unit gate.
- **Your answer:** TODO

### T99. Initial JavaScript budget?

- **A.** Under 50 KB compressed first-load JS per archetype page.
- **B.** Under 150 KB.
- **C.** No budget.
- **Recommended:** A with Astro + vanilla islands.
- **Your answer:** TODO

### T100. Initial card-image loading budget?

- **A.** Load hero/first row only; lazy-load rest.
- **B.** Preload all 19 for instant presentation.
- **C.** Adaptive: lazy gallery, prefetch next/previous once presentation opens.
- **Recommended:** C.
- **Your answer:** TODO

### T101. Search index loading?

- **A.** Inline for pilot; split per archetype when catalog grows.
- **B.** Always global upfront.
- **C.** Server search.
- **Recommended:** A.
- **Your answer:** TODO

### T102. Font/icon dependency budget?

- **A.** No webfont/icon package; use system text and small inline project-owned SVGs.
- **B.** Add icon library.
- **C.** Add hosted fonts.
- **Recommended:** A.
- **Your answer:** TODO

---

## Round 10 — Repository workflow and scope

> Depends on all prior technical choices.

### T103. Standard commands?

- **A.** `npm run dev`, `build`, `preview`, `test`, `test:e2e`, `lint`, `format`, `check` from `website/`.
- **B.** Root wrapper commands too.
- **Recommended:** A initially; document exact working directory.
- **Your answer:** TODO

### T104. Should root Python tooling invoke website build?

- **A.** No; separate ecosystems.
- **B.** Add Python wrapper.
- **Recommended:** A.
- **Your answer:** TODO

### T105. Generated outputs committed?

- **A.** Commit source/config/snapshot source assets; ignore `dist/`, caches, optimized derivatives.
- **B.** Commit full built site.
- **Recommended:** A when deploying through Actions.
- **Your answer:** TODO

### T106. Website release model?

- **A.** Continuous deploy from `main`.
- **B.** Semantic versions/tags.
- **C.** Manual releases.
- **Recommended:** A; snapshots provide content milestones.
- **Your answer:** TODO

### T107. Pilot implementation boundary?

- **A.** Full stack foundation + home + Nekroz archetype/detail/presentation + date filter + deployment.
- **B.** Local Nekroz page first; deployment later.
- **C.** Build every archetype immediately.
- **Recommended:** A. Proves complete vertical slice while honoring one-page pilot.
- **Your answer:** TODO

### T108. Future archetype onboarding target?

- **A.** Add one registry entry and ensure renders exist; no component edits.
- **B.** Copy page/component per archetype.
- **Recommended:** A, matching identical-page requirement.
- **Your answer:** TODO

### T109. Content-edit boundary?

- **A.** Website never writes MSE; rebuild reflects source changes.
- **B.** Website admin writes back to MSE.
- **Recommended:** A, already required.
- **Your answer:** TODO

### T110. Documentation deliverable?

- **A.** README section covering install, dev, build, render prerequisite, archetype onboarding, deploy.
- **B.** `website/README.md` only.
- **C.** Both root summary and website details.
- **Recommended:** C.
- **Your answer:** TODO

### T111. Explicitly forbidden technical choices?

Examples: React, Tailwind, external APIs, analytics, GitHub Pages, large dependencies, generated files, custom domain.

- **Your answer:** TODO

### T112. Existing web-stack preferences or experience?

Examples: Astro, React, Vue, Svelte, plain TypeScript, Python generators, no preference.

- **Your answer:** TODO

---

# Technical confirmation

Complete after answering all applicable questions:

- **Technical understanding reached:** TODO (`YES` / `NO`)
- **Implementation authorized:** TODO (`YES` / `NO`)
- **Extra constraints:** TODO
