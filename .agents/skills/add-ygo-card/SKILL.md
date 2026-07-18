---
name: add-ygo-card
description: Project-specific Yu-Gi-Oh! × Magic cube workflow to add a card from its Yu-Gi-Oh! name. First delegates to fetch-original-ygo-card to persist official Konami card data, then converts that record into concise French Magic-style cube text, updates the appropriate docs and MSE project, downloads cropped artwork, and verifies the result. Use when the user says add, create, import, or convert a Yu-Gi-Oh! card for this cube.
---

# Add Yu-Gi-Oh! Card to the Yu-Gi-Oh! × Magic Cube

Run from the `YGO-x-MTG` repository. User-facing explanations and project prose are French. Original card names, card types, and subtypes remain English.

## Mandatory first step: fetch the original

Before designing any conversion, delegate to the original-card skill:

```text
Skill(skill="fetch-original-ygo-card", args="CARD NAME")
```

Then read the generated `original_cards/<type>/<card name>.md` file. Treat that file—not memory, converted docs, MSE text, or a secondary API—as the source of truth for the original name, stats, type, materials, and effect text. Never convert first and fetch later.

## Context and precedent

1. Resolve the repository root with `git rev-parse --show-toplevel`.
2. Read `docs/context.md` and `docs/02_rules_keywords_card_design.md`.
3. Identify the target archetype or utility document and MSE project.
4. Read the complete target doc and at least three nearby converted cards from the same archetype/type before designing the new card.
5. Reuse existing archetype wording and mechanics before inventing new ones.

## Destination

Prefer the existing matching MSE project (source of truth for translated card text):

- Utility creatures: `MSE_projects/03_YGO_Non_Archetype_Creatures.mse-set`
- Fusion/Synchro/Xyz/Link staples: `MSE_projects/05_YGO_Staples_Fusion.mse-set` through `08_YGO_Staples_Link.mse-set`
- Utility spells/traps: `MSE_projects/09_YGO_Non_Archetype_Non_Creatures.mse-set`
- Archetypes: matching `MSE_projects/*_YGO_*.mse-set`

Archetype design docs under `docs/10_`–`docs/13_` keep identity/mechanics only — do not reintroduce full card blocks there. MSE `name:` uses the cube display name.

## Conversion

Convert the persisted official card record into concise, cube-playable French Magic rules text while preserving the Yu-Gi-Oh! identity.

- Use the current vocabulary from project context: **Passif**, **Activable Sorcery**, **Activable Flash**, **Déclenchable**, **On Send Grave**, **On Destroy**, **On Link Summon**, and existing summon mechanics.
- Match exact sibling wording for recurring archetype abilities.
- Number abilities as `(1 - Type Metadata) ...`.
- Docs use `**keyword**`; MSE uses `<b>keyword</b>`.
- MSE material/reminder lines use `<i>...</i>`.
- Before editing, detect every effect that would perform a normally illegal Summon, especially from the Sideboard without the required invocation method. For each affected card, call `AskUserQuestion` and ask whether to add `en ignorant les restrictions de Summon`. Offer exactly: **Add the explicit permission**, **Keep Summon restrictions**, and **Send a message** with custom text enabled. Never infer or insert the bypass silently. The permission makes the Summon legal but does not make it a correct invocation.
- Do not leave blank lines inside MSE `rule_text`.
- Keep card text compact enough for the selected frame.

## Artwork

Use YGOPRODeck only for artwork discovery. Prefer `card_images[0].image_url_cropped`; use the full card image only if cropped artwork is unavailable. Store the source illustration under `original_images/<card_type>/<official_card_name>.jpg`, using the same card-type folder and Windows-safe official-name convention as `original_cards/<card_type>/<official_card_name>.md`. Create a separate resized/imported copy under the target project's `mse_images/` folder and point the MSE card only to that project-local copy.

## Editing

- Match the target markdown section and formatting exactly.
- Match sibling MSE fields, stylesheet, filename style, image path, and `include_file:` convention.
- If an updater exists under `mse/` or `.script/`, update it so rerunning does not remove the card. Do not run an updater that would overwrite unsynchronized edits.
- Preserve unrelated working-tree changes.

## Verification

1. Confirm the original record exists and contains an official Konami URL:

```bash
rg -n "Official Yu-Gi-Oh|CARD NAME" original_cards
```

2. Confirm docs, MSE card file, set include, image, and any updater all agree:

```bash
rg -n "ORIGINAL NAME|CUBE NAME" docs MSE_projects mse .script
```

3. Run relevant tests and the project's MSE export verification using the configured `.env`/`mse_config.py`; do not hardcode a machine-specific MSE installation path.
4. Inspect the exported image when possible and remove temporary exports.

## Final response

Respond in French with the original-record path, conversion assumption, doc path, MSE project/card path, artwork path, and verification results.
