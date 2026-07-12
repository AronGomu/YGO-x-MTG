---
name: normalize-card-formatting
description: Normalize existing YGO-x-MTG card statistics and rules text to the current French templating and formatting rules, using an MSE card file or an entire .mse-set project as input, then mirror every scoped card into its numbered docs, validate MSE integrity, export renders, and build a printable proxy PDF. Use when the user asks to update, refresh, reformat, normalize, or bring card text in docs or MSE up to the current rules without redesigning the cards.
compatibility: YGO-x-MTG repository with Python 3, Pillow, and a configured Magic Set Editor installation for render validation.
metadata:
  project: YGO-x-MTG
---

# Normalize Card Formatting

Bring existing cards up to the repository's **current** wording, grammar, typography, statistics representation, and MSE markup conventions. This is a formatting and synchronization workflow, not a card-design or rule-evolution workflow.

The supplied MSE save data is the source of truth for mechanics. Preserve targets, costs, optionality, timing, zones, quantities, durations, frequency limits, names, colors, types, and numeric values unless a current project rule makes a correction mechanical and unambiguous.

Use the neighboring workflows instead when appropriate:

- `validate-mse-updates` for user-authored MSE changes that may intentionally alter mechanics or project rules;
- `update-card-from-ai` for `[ADD]` or `[UPDATE]` Markdown card definitions;
- `add-ygo-card` for a new conversion from an original Yu-Gi-Oh! card name.

## Accepted input and scope

Accept one checked-in input beneath `MSE_projects/`:

- `MSE_projects/<project>.mse-set/card <slug>`: normalize that card only;
- `MSE_projects/<project>.mse-set/set`: normalize every `include_file:` card;
- `MSE_projects/<project>.mse-set/`: normalize every `include_file:` card.

A project means **all cards included by its manifest**, including cards whose docs section is currently only a heading. Do not silently limit project scope to modified cards.

If the user omits a path, use an exact uniquely named project/card from the request. Otherwise, select a unique modified MSE card/project from `git status --short`; if there is no unique safe scope, stop without editing and report the candidate paths.

Canonical projects are folder-form `.mse-set` saves, not zip archives. Do not edit an archive in place. Never include nested backups, diagnostic projects, or export folders as cards.

## Phase 0 — Protect the working tree

1. Resolve the repository root and inspect existing work:

   ```bash
   git rev-parse --show-toplevel
   git status --short
   git diff --name-status -- MSE_projects docs
   ```

2. Record the exact input, parent project, manifest, scoped cards, and expected numbered docs file.
3. Preserve unrelated changes. Never reset, checkout, clean, or regenerate another project.
4. Read MSE text with `utf-8-sig` semantics and preserve its BOM/newline convention. Do not create backups inside an active `.mse-set` folder.

## Phase 1 — Load the complete current formatting contract

Read these files **completely on every invocation**, because this skill exists specifically to apply their latest state:

1. `docs/context.md`;
2. `docs/02_rules_keywords_card_design.md`;
3. the numbered card document matching the project;
4. two or three complete sibling card files demonstrating each relevant card type/frame;
5. `CONTEXT.md` under `MSE_ROOT`, if it exists, after loading `MSEConfig` from `mse_config.py`;
6. any project-specific tests or generator/synchronizer that can rewrite the scoped cards.

Treat `docs/02_rules_keywords_card_design.md` as the concrete card-design/templating source and `docs/context.md` as the broader mandatory project contract. Apply rules dynamically from the files, not from a remembered copy or only from the examples below. If the two current files directly contradict each other, do not guess or rewrite mechanics: preserve the affected text and report the contradiction with `path:line` evidence.

Build a short rules checklist before editing. It must cover every applicable current rule for:

- French grammar, spelling, apostrophes, accents, punctuation, and compact quantities;
- English card names, types, and subtypes;
- quoted card/archetype references;
- ability numbering, labels, timings, and frequencies;
- costs, alternative costs, casting conditions, and evergreen keywords;
- bold event/action keywords and em-dash placement;
- canonical vocabulary and zones such as `MV`, `Deck`, `GYD`, and `Sideboard`;
- material/invocation lines and Extra Deck types;
- MSE markup, field order, frame selection, image fields, collection numbers, and docs equivalents;
- casting-cost and power/toughness representation.

## Phase 2 — Inventory and parse the MSE source

For project scope, parse `include_file:` entries in manifest order and require every target to exist exactly once. For card scope, require the card to belong to its parent manifest exactly once.

Read every scoped card completely and capture:

- file path and `name`;
- `casting_cost`;
- stylesheet/frame;
- `super_type` and `sub_type`;
- material/invocation line;
- every `rule_text` line and ability label;
- `power` and `toughness`;
- rarity and every present `card_code_text*` field;
- image fields;
- `notes: Source:` and matching docs heading.

Use `notes: Source:` first to identify the docs file, then the numeric project prefix and existing exact card heading. Archetype headings may use `[original name] => [cube name]`; keep the original-name side intact while matching MSE `name:` to the cube-name side. A blank docs heading is a valid destination that should be populated from a complete MSE card.

Do not invent fields for incomplete placeholder cards. Record them as skipped/incomplete and continue with the remaining cards.

## Phase 3 — Normalize without redesigning

Correct each complete scoped card according to the live Phase 1 checklist.

### Safe automatic corrections

Apply formatting-neutral corrections such as:

- French spelling, agreement, accents, apostrophes, and punctuation;
- Arabic digits for rule quantities;
- canonical abbreviations and capitalization;
- typographic French quotes around mechanically referenced card or archetype names;
- `(x - Type)` labels and sequential ability numbers;
- valid `Passif`, `Déclenchable`, `Activable Sorcery`, `Activable Flash`, `Résolution`, `Soft`, `Hard`, and `Hard Linked` forms;
- costs/conditions before evergreen keywords, and evergreen keywords before numbered abilities;
- bold current keywords and event-keyword em dashes;
- current material-line wording and italics;
- removal of blank lines from MSE `rule_text`;
- `<b>...</b>` and `<i>...</i>` in MSE, with `**...**` and `*...*` equivalents in Markdown;
- MSE mana costs without braces and docs costs with braces;
- MSE `power`/`toughness` fields and docs `**P / T**` representation;
- current type wrappers and frame fields when the card's existing super-type determines them unambiguously.

For statistics, synchronize cost, type, subtype, power, and toughness from MSE into docs and normalize their representation. Do **not** rebalance a card or recompute numeric P/T merely because the generic ATK/DEF conversion formula exists: the documented minimum and intentional adaptations make that a design decision. Recompute only when the user explicitly asks for conversion validation and an authoritative `original_cards/` record plus the current rules yield one unambiguous value with no applicable exception.

### Semantic boundary

Never silently change:

- targeting versus non-targeting selection;
- a cost into an effect, or an effect into a cost;
- optional versus mandatory text;
- trigger event, activation timing, or spell speed;
- source/destination zone;
- quantity, duration, or resolution order;
- once-per-turn scope;
- card name, mana value, color, type, material requirement, or numeric stats;
- the definition or behavior of a keyword.

If a proposed grammar/templating correction crosses this boundary, leave the original mechanic unchanged and add it to an unresolved semantic ledger. This skill does not evolve `docs/context.md` or `docs/02_rules_keywords_card_design.md`; route those entries through `validate-mse-updates`.

If a scoped effect would perform a normally illegal Summon, especially from the Sideboard without the required invocation method, call `AskUserQuestion` for that card before editing and ask whether to add `en ignorant les restrictions de Summon`. Offer exactly: **Add the explicit permission**, **Keep Summon restrictions**, and **Send a message** with custom text enabled. Never infer or insert the bypass silently. The permission makes the Summon legal but does not make it a correct invocation.

Preserve unrelated metadata and artwork. Update `time_modified` only on cards whose content changed.

## Phase 4 — Mirror the final cards into docs

For every complete scoped card, update the matching numbered document in the same pass:

- MSE remains the mechanics source of truth;
- mirror name, cost, type/subtype, P/T, material line, evergreen keywords, and all rule text;
- preserve the document's heading depth, separators, original Yu-Gi-Oh! name, notes, and ordering;
- strip MSE word-list wrappers from visible Markdown;
- convert MSE bold/italics to Markdown;
- never leave raw MSE tags in docs;
- never erase a complete docs section because its MSE card is only a placeholder.

Search docs, MSE files, `.script/`, `mse/`, and tests for stale old text. Update only generators/synchronizers or fixtures that would otherwise restore the old formatting. Do not run a stale generator before synchronizing it.

For project scope, sort all manifest `include_file:` entries alphabetically by visible MSE `name:` and renumber every present `card_code_text`, `card_code_text_2`, and `card_code_text_3` as `001/NNN`, preserving rarity suffixes. For card scope, validate existing order/numbers; fix them project-wide only when they violate the current mandatory convention.

## Phase 5 — Structural validation

Validate the complete parent project, even for one-card scope:

- every `include_file:` resolves exactly once;
- no included card is missing and no accidental duplicate card file exists;
- every non-empty `image`, `image_2`, `mainframe_image*`, `symbol`, and `masterpiece_symbol` reference resolves;
- card image fields follow the current project image convention;
- no backup, nested `.mse-set`, diagnostic, cache, or export folder can poison GUI save behavior;
- collection totals and positions agree with manifest order;
- docs and MSE agree for every scoped complete card;
- no stale superseded wording remains in a regeneration source.

Then run:

```bash
python -m unittest discover -s tests
git diff --check
```

Compile any changed Python generators/synchronizers with `python -m py_compile <paths>`.

## Phase 6 — Prove MSE export and update renders

Load executable paths only through `MSEConfig.load()` from `mse_config.py`. Never hardcode a local MSE path. If configuration is missing or invalid, report `python setup_mse.py` as the required blocker and do not claim export success.

1. Export to a temporary directory **outside** the active `.mse-set` folder.
2. Require a direct MSE CLI process exit code of `0` and a decodable PNG count equal to:
   - `1` for an isolated single-card export; or
   - the manifest count for a project export.
3. If the CLI reports `3221225477` / `0xC0000005`, follow the mono-card diagnostic procedure in `docs/context.md` and retry directly from the shell before declaring corruption.
4. Confirm every PNG opens successfully and inspect the changed renders when image analysis is available for missing art/symbols and text overflow.
5. Copy successful final renders into the project's canonical `render/` folder and name each image from the exact MSE `name:` value. For project scope, remove only stale generated render images proven not to correspond to a current card. For card scope, replace only that card's render.
6. Delete temporary exports and caches; never leave them inside the project.

Structural validation plus a successful direct export proves automated readability/renderability. It does **not** prove GUI Save/Save As compatibility. If GUI automation is available, open the project with `MSEConfig.executable` and perform a real Save/Save As. Otherwise, report that exact manual check as remaining instead of claiming complete non-corruption.

## Phase 7 — Produce print work

After successful render export, create a print-and-cut proxy PDF with the repository helper.

For project scope:

```bash
python .script/create_proxy_pdf.py --input "MSE_projects/<project>.mse-set/render"
```

For card scope, place only the scoped rendered PNG in a temporary folder outside the `.mse-set`, then run:

```bash
python .script/create_proxy_pdf.py --input "<temporary-single-card-render-folder>" --output "print/<safe-card-name>_proxies.pdf"
```

Delete the temporary folder afterward. Unless the user requests another quantity, keep the helper default of three copies per card. Require the PDF to exist, be non-empty, and report its page count/output path. Do not print to a physical printer automatically.

## Final response

Respond in French with:

- input path and whether scope was one card or the full project;
- cards normalized and incomplete cards skipped;
- formatting, grammar, markup, and stat-representation fixes;
- MSE/docs/generator files synchronized;
- unresolved semantic ledger entries, if any;
- structural checks, tests, and `git diff --check` results;
- MSE export count and render path;
- printable PDF path and page/card count;
- whether GUI Save/Save As was verified or remains manual.

## Never

- Never redesign cards under a formatting request.
- Never rewrite current project rules from patterns found in cards.
- Never use docs to overwrite newer MSE mechanics.
- Never update only MSE or only docs for a complete scoped card.
- Never erase complete docs from an incomplete MSE placeholder.
- Never run stale generators over the input.
- Never leave broken includes, image references, numbering, or stale renders.
- Never put backups, temporary projects, or validation exports inside an active `.mse-set` folder.
- Never hardcode `.env` values or commit machine-specific MSE paths.
- Never claim GUI save compatibility from CLI export alone.
