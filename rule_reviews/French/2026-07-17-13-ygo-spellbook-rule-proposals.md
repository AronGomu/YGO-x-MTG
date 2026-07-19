# Rule review — 13_YGO_Spellbook MSE reconciliation

- Status: AWAITING_USER
- Review ID: 2026-07-17-13-ygo-spellbook-rule-proposals
- Generated: 2026-07-17
- Normalize after approval: false
- Source request: fix-mse-cards — MSE_projects/13_YGO_Spellbook.mse-set

## How to complete this review

Answer directly in this Markdown file. For every item, replace `TODO` with exactly one decision:

- `ACCEPT` — apply the proposed rule;
- `REJECT` — keep the current rule;
- `REVISE` — use the text in `Final wording`.

For `REVISE`, write the replacement rule under `Final wording`. Use `Notes` for rationale or implementation constraints. Do not remove IDs, questions, or evidence. Chat replies such as “yes”, “looks good”, or revised prose do not count as decisions once this file exists. When finished, change `Status` to `READY`, save the file, and tell the agent `continue`.

## Ruling contradictions — pattern destroyers

### D1 — High Priestess stacks Book Affinity with a second Coût alternatif

- Scope: general + archetype (`docs/13_archetype_spellbook.md`, affinity label rules)
- Existing rule: Documented affinity keywords replace the visible `Coût Alternatif —` label for alternative casting costs; **Book Affinity** is the only alternative-cost keyword for Spellbook/Prophecy Creatures (`docs/13_archetype_spellbook.md`, prior review `2026-07-13-spellbook-affinity-and-generic-selectors` D1/R1).
- Conflicting MSE evidence: `MSE_projects/13_YGO_Spellbook.mse-set/card high priestess of prophecy` shows both `<b>Book Affinity</b>` and `<b>Coût alternatif</b> — Révélez 3 “Spellbook” non-creature de votre main.` before the numbered activated ability.
- Why this destroys a pattern: Two alternative-cost labels on one card reintroduce the old `Coût alternatif` syntax next to an affinity keyword that was accepted as its replacement, and Book Affinity’s free-cast condition no longer uniquely describes High Priestess’s casting path.
- Exact ruling question: May a Creature keep **Book Affinity** and also print a second, card-specific **Coût alternatif** (reveal 3 non-creature Spellbooks), or must High Priestess use only one alternative-cost representation?
- Impacted cards/files: `card high priestess of prophecy`; `docs/13_archetype_spellbook.md`; affinity wording in `docs/context.md` / `docs/02_rules_keywords_card_design.md` if the exception is generalized; `tests/test_spellbook_cards.py`.
- Proposed resolution: Allow a card-specific additional alternative cost only when the archetype doc explicitly records the exception. Keep both lines on High Priestess; document that Book Affinity remains the free-cast affinity and that High Priestess also has a reveal-3 alternative cost that does not replace Book Affinity.
- Side effects: Other affinity cards must not casually reintroduce `Coût alternatif` without an archetype exception.
- Decision: TODO
- Final wording:
- Notes:

### D2 — Fate modes drop targeting and the non-targeting disclaimer

- Scope: general PSCT targeting conventions
- Existing rule: Targeting uses `ciblez` / `ciblé(e)` when the effect targets; non-targeting exile of a permanent was previously called out with `Cet effet ne cible pas.` on mode 3 (`docs/02_rules_keywords_card_design.md` targeting / cost vs target rules).
- Conflicting MSE evidence: `card spellbook of fate` modes are now non-targeting: `Retournez 1 créature face verso` / `Renvoyez 1 permanent non-terrain…` / `Exilez 1 permanent` without targets or disclaimer.
- Why this destroys a pattern: Modes that look like classic targeted bounce/flip/exile no longer use target language, so players cannot tell from shared templates whether interaction is targeted.
- Exact ruling question: Are Fate’s three modes intentionally non-targeting (choose on resolution), and should non-targeting permanent exile/bounce omit any disclaimer going forward?
- Impacted cards/files: `card spellbook of fate`; any mode cards that copy this shape; general PSCT notes if accepted.
- Proposed resolution: Accept intentional non-targeting modes for Fate. When a mode chooses a permanent on resolution without targeting, write `1 créature` / `1 permanent` without `ciblez`, and do not require `Cet effet ne cible pas.` unless ambiguity remains.
- Side effects: Future mode cards may copy non-targeting wording; targeted modes must still use `ciblez`.
- Decision: TODO
- Final wording:
- Notes:

## New possible rules — pattern makers

### R1 — Event keywords `On Leave Field` and `On Upkeep`

- Scope: general (`docs/context.md`, `docs/02_rules_keywords_card_design.md`)
- Evidence: `card spellbook star hall` ability 3 and `card the grand spellbook tower` abilities 1–2 use `<b>On Leave Field</b>` and `<b>On Upkeep</b>` instead of prose `Si cette carte quitte le terrain` / `Au début de votre entretien`.
- Existing rule: Event keywords such as `On Enter`, `On Send Grave`, `On Your Cast …` are bold after the ability prefix; leave-field and upkeep were still prose on these cards.
- Exact proposed wording: Standardize leave-field triggers as `<b>On Leave Field</b> — …` and controller-upkeep triggers as `<b>On Upkeep</b> — …` (Soft/Hard as needed). Prefer these over long French timing sentences when the trigger is pure zone/phase timing.
- Boundary and exceptions: Do not replace conditional leave triggers that need extra clauses before the event. Keep French for non-event conditions.
- Impacted cards/files: Spellbook Star Hall; The Grand Spellbook Tower; other cards still on prose leave/upkeep if later normalized.
- Side effects: Event dictionary growth; MSE bold consistency.
- Decision: TODO
- Final wording:
- Notes:

### R2 — Copy text then resolve (no free cast of the copy)

- Scope: general reusable process
- Evidence: `card spellbook of the master`: `Révélez 1 autre “Spellbook” de votre main et choisissez 1 “Spellbook” dans votre Grave ; copiez son texte et résolvez-le.` Former wording cast the copy without paying mana.
- Existing rule: No project-wide template for “copy rules text and resolve it” as distinct from casting a copy.
- Exact proposed wording: When an effect copies another spell’s rules text and applies it immediately without casting, write `copiez son texte et résolvez-le` after the reveal/choose clause separated by `;`. This is not casting and does not pay mana or alternative costs of the original.
- Boundary and exceptions: Do not use this wording when the player should cast a copy (`vous pouvez lancer la copie sans payer son coût de mana`).
- Impacted cards/files: Spellbook of the Master; future copy-resolve designs.
- Side effects: Timing/layer differences vs cast-a-copy; additional costs on the original are not paid.
- Decision: TODO
- Final wording:
- Notes:

### R3 — `Reanimate` gated by exact count `X égale la MV`

- Scope: general reusable process
- Evidence: `card spellbook of life`: `Ciblez 1 créature “Spellbook” et X “Spellbook” non-creature de votre Grave ; <b>Reanimate</b> la cible si X égale la MV de la cible.`
- Existing rule: **Reanimate** is defined; pairing it with an exact-count gate on co-selected cards is not templated.
- Exact proposed wording: When Reanimate requires selecting additional cards whose count must equal the target’s MV, write `Ciblez 1 [créature…] et X [cartes…] ; <b>Reanimate</b> la cible si X égale la MV de la cible.` Selected non-target cards are part of the effect’s selection, not a separate cost line, unless design needs a cost.
- Boundary and exceptions: Card-specific MV comparison may use `inférieure ou égale` when that is the mechanic; Life uses exact equality.
- Impacted cards/files: Spellbook of Life; similar Grave revive designs.
- Side effects: Targets both creature and X non-creatures; failure if X ≠ MV.
- Decision: TODO
- Final wording:
- Notes:
