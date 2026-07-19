# YGO × MTG Showcase — Technical Follow-up Frontier

**Status:** INCORPORATED INTO IMPLEMENTATION PLAN AS RECOMMENDED DEFAULTS  
**Scope:** Decisions unlocked by custom answers T5, T22, T54, T55, and T63. User requested planning without more implementation. Recommendations therefore become explicit plan assumptions unless contradicted by prior overrides. Mana-symbol public redistribution remains a deployment gate because no package license was found.

## New facts verified

- Four defined archetype projects exist:
  - Burning Abyss: 30 manifest cards, 30 renders.
  - Shaddoll: 25 manifest cards, 25 renders.
  - Nekroz: 19 manifest cards, 19 renders.
  - Spellbook: 16 manifest cards, 16 renders.
- Six non-archetype/staple projects also ship in first release:
  - Non-Archetype Creatures: 4
  - Fusion Staples: 12
  - Synchro Staples: 15
  - Xyz Staples: 17
  - Link Staples: 29
  - Non-Archetype Non-Creatures: 17
- All current first-release MSE sets are English and declare `set_language: EN` plus `card_language: English`.
- Known ownership collisions where defined-archetype project wins: `Herald of the Arc Light` → Nekroz; `Downerd Magician` and `Leviair the Sea Dragon` → Burning Abyss.
- Seven-and-a-Half MSE style uses `magic-mana-large` for casting cost and `magic-mana-small` for rules text.
- Supplied MSE install contains 169 large-symbol PNGs and 244 small-symbol PNGs (~3.05 MiB total).
- Current cube casting costs need normal colors, generic values, and several hybrid symbols. No inline `<sym>` rules-text symbols currently occur.
- No license file was found inside either supplied mana-symbol package.
- Nekroz directory contains legacy duplicate card files, but manifest correctly selects only 19 active cards.

---

## Frontier A — First public catalog

### F1. First release project scope?

- **Decision:** Ten first-release MSE projects: six non-archetype sections plus four defined archetypes.
- **Non-archetype sections:** Creatures, Fusions, Synchro, Xyz, Link, Non-creature.
- **Defined archetypes:** Burning Abyss, Nekroz, Shaddoll, Spellbook.
- **Ownership:** defined-archetype project wins when the same display name also appears in a staple project.

### F2. Iconic homepage monster for each archetype?

Suggested defaults:

- Burning Abyss: **Burning Abyss - Dante**
- Shaddoll: **El Shaddoll - Construct**
- Nekroz: **Nekroz - Trishula**
- Spellbook: **High Priestess of Prophecy**

- **A.** Accept all suggested defaults.
- **B.** Provide replacements below.
- **Recommended:** A.
- **Your answer:** TODO
- **Replacements:** TODO

### F3. Iconic tile artwork source?

- **A.** Cropped illustration referenced by iconic card’s MSE `image:` field.
- **B.** Central `original_images/` JPG.
- **C.** Full final MSE card render.
- **Recommended:** A. MSE remains source of truth; tile receives clean illustration rather than card frame.
- **Your answer:** TODO

### F4. Homepage “new cards” definition?

- **A.** Changed since latest immutable showcase snapshot for each archetype.
- **B.** Changed during latest calendar day present in MSE metadata.
- **C.** Changed within rolling 30 days.
- **D.** Manually selected release batch.
- **Recommended:** A. Directly links homepage freshness to accepted snapshot/date system.
- **Your answer:** TODO

### F5. Homepage new-card quantity?

- **A.** Latest 12 across all archetypes, with “Voir toutes” link.
- **B.** Every card matching current new period.
- **C.** Latest 4 per archetype.
- **Recommended:** A. Fast homepage, balanced across normal screen sizes.
- **Your answer:** TODO

### F6. Homepage new-card ordering?

- **A.** Exact `time_modified`, newest first.
- **B.** Group by archetype, then newest.
- **C.** Manual editorial order.
- **Recommended:** A, with archetype badge on every card.
- **Your answer:** TODO

---

## Frontier B — Astro/Svelte boundary

### F7. Svelte ownership?

- **A.** Astro owns routes/static content; Svelte islands own header search, filters, left nav, modal/presentation, and animated card grids.
- **B.** One hydrated Svelte app owns entire site inside Astro shell.
- **C.** Switch from Astro to SvelteKit static adapter.
- **Recommended:** A. Future-ready interaction without turning content pages into SPA payloads.
- **Your answer:** TODO

### F8. Page transitions?

- **A.** Astro View Transitions; Svelte islands rehydrate per route.
- **B.** Normal browser navigation.
- **C.** Svelte client router/SPA navigation.
- **Recommended:** A, with reduced-motion fallback.
- **Your answer:** TODO

### F9. Left catalog navigation behavior?

- **Decision:** Persistent/collapsible desktop rail + modal mobile drawer.
- **Order:** collapsible Non-Archetype parent first, children Creatures → Fusions → Synchro → Xyz → Link → Non-creature, then defined archetypes alphabetical (Burning Abyss, Nekroz, Shaddoll, Spellbook).
- **Collapse:** Non-Archetype parent uses `aria-expanded`/`aria-controls`; children remain individually linkable when expanded.

---

## Frontier C — Global card search

### F10. Search matching?

- **A.** Case/accent-insensitive substring over card names only.
- **B.** Fuzzy name matching with typo tolerance.
- **C.** Exact/prefix matching only.
- **Recommended:** B, restricted to names. “Trisula” can still find “Trishula” without searching rules text.
- **Your answer:** TODO

### F11. Search interaction?

- **A.** Header input plus `Ctrl/Cmd+K` command palette; Enter opens selected card.
- **B.** Header input only.
- **Recommended:** A.
- **Your answer:** TODO

### F12. MVP search language?

- **Decision:** Index English current and former card names only.
- **Excluded from MVP:** Cross-language matching, locale ranking, and alternate-language destinations.

---

## Frontier D — Card-detail explanations

### F13. Source for description/explanation below card?

MSE currently contains card rules/flavor but no long-form design explanation.

- **A.** Optional Markdown file per stable card ID under website content.
- **B.** One archetype Markdown file containing sections keyed by card ID.
- **C.** Generate explanation automatically from card rules.
- **D.** Show no long explanation until source exists.
- **Recommended:** A. Human-authored, diffable, optional, and easy to extend after MVP. Never invent design intent.
- **Your answer:** TODO

### F14. Publication requirement for explanation?

- **A.** Card page publishes without it; explanation section omitted.
- **B.** Every published card must have explanation.
- **C.** Show “Analysis coming soon” placeholder.
- **Recommended:** A. First release spans ten catalog sections; missing prose should not block catalog.
- **Your answer:** TODO

### F15. Explanation language storage?

- **Decision:** One optional English Markdown file per stable card ID for MVP.
- **Deferred:** Locale directories and translated explanation variants.

### F16. Related cards on detail page?

- **A.** Previous/next in manifest plus 3 cards from same catalog section.
- **B.** Previous/next only.
- **C.** None.
- **Recommended:** A, derived automatically; no manual relationship model.
- **Your answer:** TODO

---

## Frontier E — English-only MVP content model

### F17. MVP MSE source layout?

- **Decision:** Use current English projects under `MSE_projects/*.mse-set/` directly.
- **Validation:** Every published project must declare `set_language: EN` and `card_language: English`.

### F18. MVP URL structure?

- **Decision:** Use unprefixed English routes: `/`, catalog section routes for Non-Archetype children and defined archetypes, `/cards/<stable-id>/`, `/updates/`, and section snapshot routes.
- **Excluded:** `/en`, `/fr`, or client-side language swapping.

### F19. Root behavior?

- **Decision:** `/` renders English homepage directly; no locale detection, redirect, or chooser.

### F20. Non-English content during MVP?

- **Decision:** Do not publish it. Add no translation-pending badges or availability pages.
- **Deferred:** Non-English source ingestion and publishing require a separate post-MVP design.

### F21. Stable identity for MVP?

- **Decision:** Each stable website ID maps one English MSE source filename. Future localization may extend that record without changing the stable ID.

### F22. Site-interface language architecture?

- **Decision:** Keep UI copy English without an i18n dependency or locale dictionary layer.
- **Deferred:** Introduce typed locale dictionaries only when localization is approved.

---

## Frontier F — Vendored MSE mana symbols

### F23. Which symbol sets should be copied into repository?

- **A.** Entire `magic-mana-large` and `magic-mana-small` packages (~3.05 MiB, 413 PNGs).
- **B.** Only currently/futuristically required symbols from both sets, enforced by parser/build validation.
- **C.** Large package only; scale same assets for casting costs and rules text.
- **Recommended:** B. Exact context-specific appearance without hundreds of unused custom symbols.
- **Your answer:** TODO

### F24. External MSE installation dependency after initial copy?

- **A.** Vendor selected PNGs in repository; CI/site build never reads `F:`.
- **B.** Build copies from `F:` every time.
- **Recommended:** A. Public/CI builds must be portable.
- **Your answer:** TODO

### F25. Symbol synchronization workflow?

- **A.** Explicit Python sync command reads configured `MSE_DATA_DIR`, copies allowed symbols, updates manifest/hashes.
- **B.** Copy files once manually.
- **C.** Node script hardcodes `F:` path.
- **Recommended:** A. Reuses portable MSE configuration; no machine path enters repository.
- **Your answer:** TODO

### F26. Public redistribution decision?

No license file was found in supplied `magic-mana-large` or `magic-mana-small` packages. Symbols resemble official Magic assets.

- **A.** Proceed with required copied assets and fan-project attribution/disclaimer.
- **B.** Use an explicitly licensed alternative symbol set.
- **C.** Keep accessible text tokens until rights are confirmed.
- **Recommended:** C for safest public launch; A only if you accept/hold redistribution basis.
- **Your answer:** A — Proceed with copied MSE mana assets for this noncommercial fan project, with attribution/disclaimer. User states assets are free to use because distributed with MIT-licensed MSE and explicitly accepts publication risk. Repository inspection found no root/package license covering these symbol PNGs, so documentation must not claim verified MIT coverage for assets.

---

# Frontier confirmation

- **All custom branches answered:** TODO (`YES` / `NO`)
- **Implementation authorized after answers:** TODO (`YES` / `NO`)
- **Extra notes:** TODO
