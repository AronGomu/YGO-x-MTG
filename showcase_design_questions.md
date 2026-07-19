# YGO × MTG Showcase — Design Questions

**Status:** PRODUCT DIRECTION SETTLED — TECHNICAL STACK OPEN  
**Resolution rule:** User accepted every recommendation unless overridden below. Existing `TODO` markers remain archived worksheet fields; they no longer mean product decisions are unanswered. Technical choices superseded by new website direction move to `showcase_technical_stack_questions.md`.

## User overrides — 2026-07-18

- Deliverable is now fully functional card-showcase website, not temporary recording document.
- Nekroz is pilot page proving website pattern; every later archetype page must use identical structure and behavior.
- Nekroz pilot includes all 19 cards from its MSE manifest.
- `.mse-set` card files are source of truth for card text and metadata.
- Final card images rendered by MSE are source of truth for website card visuals.
- Parsed MSE text should power searchable/accessibility/detail content; rendered card remains primary visual.
- All non-conflicting recommendations below are accepted.
- Prior static/offline stack recommendations are superseded. Hosting, framework, build pipeline, and deployment are resolved in technical-stack review.

## Additional website decisions — 2026-07-18

- Astro remains static-site shell; interactive components use Svelte.
- Homepage shows newest cards plus large animated catalog-section menu tiles using iconic monster illustrations.
- First release includes non-archetype staple sections plus defined archetypes beyond Nekroz.
- Header contains global card-name search; results link to dedicated card pages.
- Dedicated card page: final MSE render left, parsed MSE card text right, authored explanation below.
- Persistent left navbar navigates catalog sections: collapsible Non-Archetype parent first (Creatures, Fusions, Synchro, Xyz, Link, Non-creature), then defined archetypes alphabetical.
- A card belongs to a defined-archetype gallery only when its owning MSE project is one of the four registered archetypes; every other published card lives under Non-Archetype even if the original Yu-Gi-Oh! card had archetype flavor.
- MVP website is English only: interface copy, routes, metadata, explanations, accessibility text, MSE card content, and renders. Localization is deferred until after MVP.
- Mana symbols are vendored from `F:/Softwares/Magic-Set-Editor-Full` MSE assets.

## Facts already verified

These are repository facts, not decisions:

- Nekroz project: `MSE_projects/12_YGO_Necroz.mse-set/`.
- Its `set` manifest includes 19 cards: 15 named Nekroz cards plus Herald of the Arc Light, Manju of the Ten Thousand Hands, Preparation of Rites, and Senju of the Thousand Hands.
- Each included card currently has `time_created` and `time_modified` metadata.
- Current Nekroz `time_modified` dates form two calendar groups: 4 cards on 2026-07-12 and 15 cards on 2026-07-17.
- Git records latest committed changes separately; these dates can differ from MSE `time_modified`.
- Project rules define each `.mse-set/render/` folder as canonical final card-image output.
- Other projects have canonical rendered card PNGs. Nekroz currently has no `render/` folder.
- Nekroz has 19 source artwork PNGs (`image1.png` through `image19.png`), but these are cropped illustrations, not final rendered cards.
- MSE CLI is configured through `mse_config.py` / local `.env`; it can generate missing final renders.
- Repository has Python scripts and `unittest` tests, but no existing HTML/static-site framework and no `package.json`.
- Unrelated uncommitted files currently exist. Showcase work will not touch them.

---

# Design tree

## Round 1 — Product root

### Q1. What is one “showcase document”?

- **A.** One living page per archetype, regenerated as cards change.
- **B.** One immutable page per recording/update batch.
- **C.** Both: living archetype page plus immutable dated snapshots.
- **Recommended:** C. Living page supports browsing; dated snapshots preserve exactly what was recorded.
- **Your answer:** TODO

### Q2. Who is intended audience?

- **A.** Only you, opened locally while recording.
- **B.** Private viewers receiving folder/file.
- **C.** Public web audience.
- **D.** Local recording first, public publishing later.
- **Recommended:** D. Build offline-first static output without blocking later hosting.
- **Your answer:** TODO

### Q3. What should first Nekroz example prove?

- **A.** Visual direction only.
- **B.** Complete reusable generator workflow.
- **C.** Finished Nekroz page only; generalize later.
- **D.** Generator, first page, date filtering, and recording presentation mode.
- **Recommended:** D. Covers both requests without creating disposable code.
- **Your answer:** TODO

### Q4. Which cards belong to first Nekroz showcase?

- **A.** All 19 cards included by Nekroz MSE manifest.
- **B.** Only 15 cards whose names contain “Nekroz”.
- **C.** Choose explicit card list.
- **Recommended:** A. Manifest defines playable archetype package, including support cards.
- **Your answer:** TODO

### Q5. Which future inputs must system support?

- **A.** Only numbered archetype projects (`10`–`13`).
- **B.** Any `.mse-set` project with manifest, card files, and renders.
- **C.** Archetype docs rather than MSE projects.
- **Recommended:** B. Same parser can support archetypes and future sections without extra architecture.
- **Your answer:** TODO

### Q6. Should one showcase mix archetypes?

- **A.** Never; one archetype per page.
- **B.** Optional multi-project compilation.
- **C.** Always combine all newly changed cards across projects.
- **Recommended:** A now. Add compilation only when concrete need appears.
- **Your answer:** TODO

---

## Round 2A — Date meaning

> Depends on Q1–Q3.

### Q7. What does “last card change” mean?

- **A.** Card’s MSE `time_modified` value.
- **B.** Date of latest Git commit touching card file.
- **C.** Date final render PNG changed.
- **D.** Manual editorial date entered for showcase.
- **E.** MSE date first, Git fallback when missing.
- **Recommended:** E. MSE catches uncommitted edits; Git provides stable fallback.
- **Your answer:** TODO

### Q8. Which changes should advance last-change date?

- **A.** Any saved card-file change.
- **B.** Only visible/mechanical card content changes.
- **C.** Rules/stats/art changes, but not numbering/path/format maintenance.
- **D.** Manual choice each time.
- **Recommended:** C. Showcase date should represent viewer-visible changes, not maintenance churn.
- **Your answer:** TODO

### Q9. Should artwork-only changes count as new showcase changes?

- **A.** Yes.
- **B.** No.
- **C.** Only when final render visibly changes.
- **Recommended:** C.
- **Your answer:** TODO

### Q10. Should formatting/templating-only card changes count?

- **A.** Yes, every visible text change matters.
- **B.** No, only mechanics/new cards matter.
- **C.** Track date but let generator exclude formatting-only changes through explicit metadata.
- **Recommended:** A initially. C needs extra change classification system.
- **Your answer:** TODO

### Q11. Required date precision?

- **A.** Calendar day only.
- **B.** Date and time.
- **C.** Store time, display day by default.
- **Recommended:** C. Precise filtering remains possible; page stays readable.
- **Your answer:** TODO

### Q12. Which timezone governs grouping by day?

- **A.** Local timezone recorded by MSE.
- **B.** UTC.
- **C.** Configurable timezone.
- **Recommended:** A. Existing MSE timestamps are local and timezone-free.
- **Your answer:** TODO

### Q13. Visible date format?

- **A.** `2026-07-17`.
- **B.** `July 17, 2026`.
- **C.** Both English human-readable label and ISO machine value.
- **Recommended:** C.
- **Your answer:** TODO

### Q14. What happens when `time_modified` is absent or invalid?

- **A.** Fail generation.
- **B.** Use latest Git commit date.
- **C.** Use filesystem modification time.
- **D.** Show “date inconnue”.
- **Recommended:** B, then fail clearly if Git also has no date. Filesystem time is unstable across copies.
- **Your answer:** TODO

### Q15. Should uncommitted MSE changes appear immediately as new?

- **A.** Yes, trust `time_modified`.
- **B.** No, only committed changes count.
- **C.** Show them with “non publié” badge.
- **Recommended:** C if Git comparison remains simple; otherwise A.
- **Your answer:** TODO

### Q16. Should creation date also appear?

- **A.** No; only last change.
- **B.** Yes on every card.
- **C.** Only when creation date equals selected showcase batch.
- **Recommended:** A. Keep recording UI focused.
- **Your answer:** TODO

### Q17. How should renamed cards be dated?

- **A.** Rename counts as change on rename date.
- **B.** Preserve prior date unless mechanics/art changed.
- **Recommended:** A. Viewer sees new name.
- **Your answer:** TODO

### Q18. How should removed cards appear?

- **A.** Never appear; current manifest only.
- **B.** Dated snapshots preserve them, living page removes them.
- **C.** Living page includes “retired” section.
- **Recommended:** B.
- **Your answer:** TODO

### Q19. Must card update workflows enforce timestamp updates?

- **A.** Yes: scripts/skills must update `time_modified` only for meaningful changed cards.
- **B.** No: generator should derive all dates from Git.
- **C.** No enforcement yet; trust current MSE behavior.
- **Recommended:** A. Date system fails if producers do not maintain source metadata.
- **Your answer:** TODO

### Q20. Where should “last showcased” state live?

- **A.** Nowhere; always pass `--since` manually.
- **B.** One tracked state file per archetype.
- **C.** Browser `localStorage` only.
- **D.** Dated snapshot filenames define history; latest snapshot date becomes cutoff.
- **Recommended:** D. No hidden machine state; Git-visible history remains auditable.
- **Your answer:** TODO

### Q21. When selecting “since date,” is boundary inclusive?

- **A.** Include cards changed exactly on supplied date.
- **B.** Include only later cards.
- **Recommended:** A, matching common `--since` semantics for date-only input.
- **Your answer:** TODO

---

## Round 2B — Showcase selection and history

> Depends on Q1, Q4, Q7, and Q20.

### Q22. Living page default content?

- **A.** Full archetype.
- **B.** Latest change day only.
- **C.** Cards since latest snapshot only.
- **Recommended:** A, with visible filters.
- **Your answer:** TODO

### Q23. Snapshot default content?

- **A.** Full archetype state at recording time.
- **B.** Only cards changed since prior snapshot.
- **C.** Both changed cards first, full archive below.
- **Recommended:** B. Snapshot becomes focused recording document.
- **Your answer:** TODO

### Q24. Which date filters should generator support?

- **A.** `--since YYYY-MM-DD` only.
- **B.** `--on`, `--since`, and `--until`.
- **C.** No CLI date filtering; browser filters only.
- **Recommended:** B. Small implementation, flexible batches.
- **Your answer:** TODO

### Q25. Should page itself include date filter controls?

- **A.** Yes: date range and “latest wave” shortcut.
- **B.** No: generated selection is fixed.
- **C.** Living page yes; immutable snapshot no.
- **Recommended:** C.
- **Your answer:** TODO

### Q26. How are cards grouped into big sections?

- **A.** Last-change day, newest first.
- **B.** Card type.
- **C.** Creature/non-creature role.
- **D.** Manual editorial chapters.
- **E.** Date sections containing optional manual subchapters.
- **Recommended:** A now. E only if recording scripts need authored narrative.
- **Your answer:** TODO

### Q27. Order inside one section?

- **A.** MSE manifest/card number.
- **B.** Alphabetical display name.
- **C.** Exact timestamp, newest first.
- **D.** Manual order.
- **Recommended:** A. Matches set sequence and stays stable.
- **Your answer:** TODO

### Q28. How should multiple edits to same card between recordings appear?

- **A.** One final card entry using latest date.
- **B.** Full change history per card.
- **C.** One entry plus optional manually written summary.
- **Recommended:** A. Repository lacks field-level history model; Git remains available separately.
- **Your answer:** TODO

### Q29. Should page distinguish brand-new cards from modified cards?

- **A.** Yes, compare `time_created` and selected cutoff.
- **B.** Yes, compare first Git appearance and latest change.
- **C.** No; all selected cards are “new in this showcase.”
- **Recommended:** B for accuracy, if this distinction matters; otherwise C.
- **Your answer:** TODO

### Q30. Should change type be shown (new/text/stats/art/rename)?

- **A.** No.
- **B.** Manual label in showcase config.
- **C.** Automatically infer from Git diff.
- **Recommended:** A initially. Automatic semantic inference is unreliable; add manual labels only when needed.
- **Your answer:** TODO

---

## Round 2C — Visual and recording experience

> Depends on Q2 and Q3.

### Q31. Primary page mode?

- **A.** Scrollable gallery.
- **B.** Fullscreen slide deck.
- **C.** Gallery with click-to-open fullscreen stage.
- **Recommended:** C.
- **Your answer:** TODO

### Q32. Recording viewport target?

- **A.** 1920×1080 landscape.
- **B.** 1080×1920 vertical.
- **C.** Responsive support for both, optimized for landscape.
- **D.** Responsive support for both, optimized for vertical.
- **Recommended:** C unless primary platform is Shorts/TikTok.
- **Your answer:** TODO

### Q33. Fullscreen stage layout?

- **A.** Card centered alone.
- **B.** Large card left, name/date/notes right.
- **C.** Large card center with compact lower caption.
- **D.** Original YGO card beside converted MTG card.
- **Recommended:** B for spoken presentation room and readable hierarchy.
- **Your answer:** TODO

### Q34. Should original Yu-Gi-Oh card image appear beside conversion?

- **A.** Never.
- **B.** Optional comparison toggle.
- **C.** Always in fullscreen stage.
- **Recommended:** B. Strong YGO × MTG story without crowding default view.
- **Your answer:** TODO

### Q35. Should old converted render appear for before/after comparisons?

- **A.** No.
- **B.** Optional when manually supplied.
- **C.** Automatically retrieve previous Git version.
- **Recommended:** A initially. C greatly expands asset/history complexity.
- **Your answer:** TODO

### Q36. Visual theme direction?

- **A.** Nekroz-specific ice, ritual glyphs, blue crystalline glow.
- **B.** Shared YGO × MTG dark arcane base with archetype accent colors.
- **C.** MTG tabletop/parchment.
- **D.** YGO holographic/duel-interface.
- **Recommended:** B, with icy Nekroz accent for first page. Reusable base; distinct archetype identity.
- **Your answer:** TODO

### Q37. Balance between YGO and MTG visual language?

- **A.** Mostly YGO energy/UI.
- **B.** Mostly MTG editorial/tabletop.
- **C.** Equal hybrid.
- **Recommended:** C: YGO energy through light/glyphs, MTG through restrained typography/composition.
- **Your answer:** TODO

### Q38. Hover animation intensity?

- **A.** Subtle lift/glow.
- **B.** 3D tilt + foil sheen + glow.
- **C.** Strong particles/parallax/audio.
- **Recommended:** B. “Cool” but recording-safe and dependency-free.
- **Your answer:** TODO

### Q39. Should 3D tilt follow pointer position?

- **A.** Yes.
- **B.** Fixed CSS hover tilt only.
- **C.** No tilt.
- **Recommended:** A, disabled under reduced-motion and coarse pointers.
- **Your answer:** TODO

### Q40. Background motion?

- **A.** Static gradient/glyphs.
- **B.** Slow ambient particles and drifting light.
- **C.** Strong animated scene.
- **Recommended:** B, reduced or removed during fullscreen card focus.
- **Your answer:** TODO

### Q41. Should recording mode hide controls/cursor?

- **A.** Yes, dedicated clean mode.
- **B.** No.
- **C.** Auto-hide after inactivity.
- **Recommended:** C plus explicit toggle.
- **Your answer:** TODO

### Q42. Presentation navigation?

- **A.** Click only.
- **B.** Previous/next buttons.
- **C.** Buttons plus Left/Right, Space, Home/End, Escape.
- **Recommended:** C.
- **Your answer:** TODO

### Q43. Autoplay?

- **A.** None.
- **B.** Optional fixed interval.
- **C.** Automatic by default.
- **Recommended:** A. Spoken pacing is variable; keyboard navigation is safer.
- **Your answer:** TODO

### Q44. Should page include speaker notes/prompts?

- **A.** No.
- **B.** Visible notes beside card.
- **C.** Hidden presenter notes toggle.
- **D.** Separate Markdown script.
- **Recommended:** C if notes are desired; otherwise A.
- **Your answer:** TODO

### Q45. Where would speaker-note content come from?

- **A.** Manual per-card showcase config.
- **B.** MSE `notes` field.
- **C.** Archetype document.
- **D.** Generated summary from rules text.
- **Recommended:** A. MSE notes currently hold source traceability, not presentation copy.
- **Your answer:** TODO

### Q46. Page text language?

- **Decision:** English only for MVP.
- **Scope:** Interface copy, routes, metadata, authored explanations, dates, status labels, accessibility text, MSE card content, and renders.
- **Deferred:** Localization, locale-prefixed routes, language switching, translation placeholders, and `hreflang`.

### Q47. How much card data should HTML duplicate?

- **A.** Image, name, last-change date only.
- **B.** Add mana cost, type, stats, rarity.
- **C.** Duplicate full rules text.
- **Recommended:** A. Render already contains card data; duplication risks drift.
- **Your answer:** TODO

### Q48. Archetype intro content?

- **A.** Name and one-line identity only.
- **B.** Pull identity/mechanics/philosophy from archetype doc.
- **C.** Manual showcase-specific intro.
- **D.** Doc-derived defaults with optional manual override.
- **Recommended:** D.
- **Your answer:** TODO

### Q49. Accessibility target?

- **A.** Keyboard, focus states, image alt text, semantic controls.
- **B.** Visual-only recording artifact.
- **Recommended:** A. Minimal cost; improves keyboard recording flow.
- **Your answer:** TODO

### Q50. Reduced-motion behavior?

- **A.** Respect `prefers-reduced-motion` and remove tilt/ambient movement.
- **B.** Always animate.
- **Recommended:** A.
- **Your answer:** TODO

### Q51. Mobile behavior?

- **A.** Fully responsive.
- **B.** Desktop recording only.
- **C.** Desktop-first, usable mobile fallback.
- **Recommended:** C.
- **Your answer:** TODO

### Q52. Audio/video integration?

- **A.** None; page is visual recording backdrop.
- **B.** Background audio controls.
- **C.** Embed final recorded video afterward.
- **Recommended:** A now.
- **Your answer:** TODO

---

## Round 2D — Technical delivery

> Depends on Q2, Q5, and Q31.

### Q53. Runtime architecture?

- **A.** Single static HTML with inline CSS/JS, no dependencies.
- **B.** Static HTML plus shared CSS/JS files.
- **C.** Frontend framework/build system.
- **Recommended:** B. Shared theme avoids duplicating large code across archetypes while remaining offline/static.
- **Your answer:** TODO

### Q54. Asset portability?

- **A.** Reference canonical `MSE_projects/.../render/*.png` files.
- **B.** Copy selected renders into showcase folder.
- **C.** Embed images as base64 in HTML.
- **Recommended:** A for repository use; B for shareable snapshots.
- **Your answer:** TODO

### Q55. Must one snapshot folder be independently shareable?

- **A.** Yes, copying its folder must preserve everything.
- **B.** No, it may depend on repository paths.
- **C.** Add explicit `--portable` mode.
- **Recommended:** C.
- **Your answer:** TODO

### Q56. Font policy?

- **A.** System fonts only.
- **B.** External Google Fonts.
- **C.** Commit local webfont files.
- **Recommended:** A initially. True offline operation, no licensing/download concerns.
- **Your answer:** TODO

### Q57. Browser target?

- **A.** Current Chromium/Chrome only for recording.
- **B.** Current Chrome, Firefox, Safari, Edge.
- **Recommended:** B for standard features; test recording flow in Chromium.
- **Your answer:** TODO

### Q58. Output paths?

- **A.** `showcase/<archetype>/index.html` and `showcase/<archetype>/snapshots/<date>.html`.
- **B.** `docs/showcase_<archetype>.html`.
- **C.** Beside each `.mse-set` project.
- **D.** Custom path every run.
- **Recommended:** A. Keeps presentation artifacts separate from rules docs and MSE internals.
- **Your answer:** TODO

### Q59. Snapshot naming?

- **A.** Date only: `2026-07-17.html`.
- **B.** Date range: `2026-07-12_to_2026-07-17.html`.
- **C.** Sequence plus date: `001_2026-07-17.html`.
- **D.** Custom title/slug required.
- **Recommended:** C. Stable ordering and collision resistance.
- **Your answer:** TODO

### Q60. Generated output committed to Git?

- **A.** Commit generator and generated HTML/renders.
- **B.** Commit generator only; regenerate locally.
- **C.** Commit living pages and snapshots, not temporary exports.
- **Recommended:** C.
- **Your answer:** TODO

### Q61. Shared showcase index?

- **A.** None.
- **B.** `showcase/index.html` listing archetypes, latest card date, and snapshots.
- **C.** Add later after second archetype.
- **Recommended:** C. First page defines pattern; second page proves index need.
- **Your answer:** TODO

### Q62. Public hosting now?

- **A.** No.
- **B.** GitHub Pages.
- **C.** Other host.
- **Recommended:** A unless Q2 requires public audience immediately.
- **Your answer:** TODO

### Q63. Social/SEO metadata?

- **A.** Basic title/description only.
- **B.** Full Open Graph/Twitter metadata.
- **C.** None.
- **Recommended:** A for local-first output.
- **Your answer:** TODO

### Q64. Copyright/source credit on page?

- **A.** Small footer crediting Yu-Gi-Oh!, Magic, and fan-project status.
- **B.** No footer.
- **C.** Custom wording.
- **Recommended:** A, without implying affiliation.
- **Your answer:** TODO

---

## Round 3A — Generator workflow

> Depends on Q5, Q7, Q20, Q24, Q53, and Q58.

### Q65. Generator interface?

- **A.** Python CLI receiving `.mse-set` path.
- **B.** Interactive picker.
- **C.** Hardcoded script per archetype.
- **Recommended:** A. Fits repository conventions and automation.
- **Your answer:** TODO

### Q66. Preferred base command shape?

- **A.** `python .script/create_card_showcase.py "MSE_projects/...mse-set"`.
- **B.** `python .script/create_card_showcase.py --archetype nekroz`.
- **C.** Support both path and archetype slug.
- **Recommended:** A initially; project path is unambiguous and needs no registry.
- **Your answer:** TODO

### Q67. Generator default output?

- **A.** Overwrite living `index.html`.
- **B.** Create dated snapshot.
- **C.** Dry-run inventory only unless output supplied.
- **Recommended:** A.
- **Your answer:** TODO

### Q68. How should archetype label/slug/accent be configured?

- **A.** Infer all from MSE set title/project name.
- **B.** CLI options every run.
- **C.** Small tracked config file per archetype.
- **D.** Infer defaults, allow CLI overrides.
- **Recommended:** D. Avoid config until custom need appears.
- **Your answer:** TODO

### Q69. Where should optional intro/notes/theme overrides live?

- **A.** Dedicated JSON file.
- **B.** Dedicated Python dictionary.
- **C.** YAML/Markdown frontmatter.
- **D.** Existing archetype Markdown document.
- **E.** No overrides in first version.
- **Recommended:** E unless Q44, Q45, or Q48 requires authored content.
- **Your answer:** TODO

### Q70. Can generated HTML be edited manually?

- **A.** No; regenerate from source/config.
- **B.** Yes; generator preserves marked editable regions.
- **C.** Snapshots may be hand-edited after generation; living page may not.
- **Recommended:** A. Preserved editable regions add fragility.
- **Your answer:** TODO

### Q71. Missing canonical renders?

- **A.** Generator fails and prints export command.
- **B.** Generator automatically runs MSE export.
- **C.** Use source artwork as placeholder.
- **D.** Skip missing cards with warning.
- **Recommended:** A. Keep content generation deterministic; separate render generation may mutate many binary files.
- **Your answer:** TODO

### Q72. Should first implementation export missing Nekroz renders?

- **A.** Yes, generate and commit all 19 canonical final renders.
- **B.** No, build page using cropped source artwork temporarily.
- **C.** Stop until renders are supplied manually.
- **Recommended:** A. Showcase must display actual converted cards, not artwork.
- **Your answer:** TODO

### Q73. If MSE export fails for one card?

- **A.** Fail entire page generation.
- **B.** Build partial page with visible error tile.
- **C.** Keep older render when available and warn.
- **Recommended:** A for initial canonical generation; C for later living-page refreshes only if clearly marked in logs.
- **Your answer:** TODO

### Q74. How should exported generic PNG names map to cards?

- **A.** Manifest order, then rename to exact `name:` values.
- **B.** Keep generic names.
- **Recommended:** A, matching repository rule.
- **Your answer:** TODO

### Q75. Duplicate card display names?

- **A.** Fail generation.
- **B.** Suffix output names automatically.
- **Recommended:** A. Duplicate names make canonical render mapping ambiguous.
- **Your answer:** TODO

### Q76. Validation depth?

- **A.** Parse-only tests.
- **B.** Parser/date/filter/output tests plus HTML link validation and image decode checks.
- **C.** Add browser end-to-end tests.
- **Recommended:** B. No browser harness currently exists.
- **Your answer:** TODO

### Q77. Should generator offer dry-run inventory?

- **A.** Yes: list selected cards, dates, missing renders, output path.
- **B.** No.
- **Recommended:** A. Useful before recording and cheap to implement.
- **Your answer:** TODO

### Q78. Should README document showcase command?

- **A.** Yes.
- **B.** No; script `--help` is enough.
- **C.** Add docs only after workflow stabilizes.
- **Recommended:** A, concise section only.
- **Your answer:** TODO

### Q79. Should existing card-edit skills/scripts be updated in same work?

- **A.** Yes, enforce timestamp contract everywhere.
- **B.** Only add tests proving included cards have timestamps.
- **C.** No producer changes; generator consumes current values.
- **Recommended:** B first. Expand only when test reveals producers violating contract.
- **Your answer:** TODO

### Q80. Should render freshness be checked against card timestamp?

- **A.** Yes: warn/fail when render filesystem/Git date predates card change.
- **B.** No: only require render existence.
- **C.** Compare render and card Git commits, not filesystem timestamps.
- **Recommended:** C if implemented; filesystem timestamps are unstable. For first version, B is simpler.
- **Your answer:** TODO

---

## Round 3B — First Nekroz page specifics

> Depends on Q4, Q22, Q26, Q32, Q36, Q46, Q48, and Q72.

### Q81. Canonical spelling in showcase?

- **A.** “Nekroz” (official card/archetype spelling and MSE names).
- **B.** “Necroz” (legacy alternate spelling).
- **C.** “Nekroz / Necroz”.
- **Recommended:** A.
- **Your answer:** TODO

### Q82. Initial living page content?

- **A.** All 19 cards.
- **B.** Latest MSE date only: 15 cards changed on 2026-07-17.
- **C.** Custom cutoff/list.
- **Recommended:** A.
- **Your answer:** TODO

### Q83. Initial dated snapshot content?

- **A.** No snapshot yet.
- **B.** 15 cards changed on 2026-07-17.
- **C.** All 19 cards as “first showcase”.
- **D.** Custom cutoff/list.
- **Recommended:** B if snapshots are selected in Q1; demonstrates date workflow.
- **Your answer:** TODO

### Q84. Initial hero title?

- **A.** `Nekroz — Rituals Under Ice`.
- **B.** `Nekroz — YGO × MTG Showcase`.
- **C.** Custom title.
- **Recommended:** A, with one smaller YGO × MTG label.
- **Your answer:** TODO

### Q85. Initial one-line identity?

- **A.** Reuse doc identity: `Ritual / Toolbox / Anti-Extra Deck`.
- **B.** Write custom recording intro.
- **C.** No identity copy.
- **Recommended:** A, presented as polished English display copy.
- **Your answer:** TODO

### Q86. Highlight one lead card in hero?

- **A.** No; equal gallery.
- **B.** Latest modified card (Preparation of Rites by current timestamp).
- **C.** Signature Nekroz card chosen manually.
- **Recommended:** C if you have signature card; otherwise no lead card.
- **Your answer:** TODO

### Q87. Support-card labeling?

- **A.** No distinction.
- **B.** Add “Soutien” badge to four non-Nekroz cards.
- **C.** Separate support section.
- **Recommended:** B.
- **Your answer:** TODO

### Q88. Nekroz accent palette?

- **A.** Ice blue + cyan + silver on midnight navy.
- **B.** Deep blue + violet ritual glow.
- **C.** Custom colors.
- **Recommended:** A.
- **Your answer:** TODO

### Q89. Decorative motif?

- **A.** Crystalline snow/ice sigils.
- **B.** Ritual circles and mana glyph geometry.
- **C.** Both, kept subtle.
- **D.** None.
- **Recommended:** C.
- **Your answer:** TODO

### Q90. Card hover treatment?

- **A.** Cyan edge glow and foil sweep.
- **B.** Frost forming around frame.
- **C.** Blue ritual circle behind lifted card.
- **D.** Combine A and C.
- **Recommended:** D, with low animation intensity.
- **Your answer:** TODO

---

## Round 4 — Completion and handoff

> Depends on all applicable prior answers.

### Q91. Definition of done for first pass?

- **A.** Generator + tests + first Nekroz living page.
- **B.** Add canonical 19 renders.
- **C.** Add dated snapshot.
- **D.** Add README workflow.
- **E.** All A–D.
- **Recommended:** E if Q1 selects both living and snapshots.
- **Your answer:** TODO

### Q92. Manual visual QA expectation?

- **A.** Automated file/link/image checks only.
- **B.** Open in browser and inspect desktop + mobile + reduced motion.
- **C.** Also test 1920×1080 fullscreen recording flow.
- **Recommended:** C.
- **Your answer:** TODO

### Q93. Should first pass create printable proxy PDF too?

- **A.** Yes.
- **B.** No; showcase scope only.
- **Recommended:** B. Existing PDF workflow is separate.
- **Your answer:** TODO

### Q94. Should first pass update archetype rules/docs?

- **A.** README workflow only; no card-design docs.
- **B.** Add showcase link to `docs/12_archetype_necroz.md`.
- **C.** No docs changes.
- **Recommended:** A, plus B only if Obsidian users should discover showcase from archetype doc.
- **Your answer:** TODO

### Q95. Anything explicitly forbidden?

Examples: external dependencies, public hosting, copied art, bright flashing animation, changes to card content, Git commits.

- **Your answer:** TODO

### Q96. Any required reference sites/styles?

Provide URLs, screenshots, game interfaces, color references, or `none`.

- **Your answer:** TODO

---

# Final confirmation

Complete after answering all applicable questions:

- **Shared understanding reached:** TODO (`YES` / `NO`)
- **Implementation authorized after review:** TODO (`YES` / `NO`)
- **Extra notes:** TODO
