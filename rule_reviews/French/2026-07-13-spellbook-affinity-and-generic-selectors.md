# Rule review — Spellbook affinities and generic named-card selectors

- Status: APPLIED
- Review ID: 2026-07-13-spellbook-affinity-and-generic-selectors
- Generated: 2026-07-13
- Applied: 2026-07-13
- Normalize after approval: false
- Source request: Add Book Affinity and Spell Affinity to Spellbook, and omit redundant `carte(s)` from selectors that accept any card type.

## How to complete this review

Answer directly in this Markdown file. For every item, replace `TODO` with exactly one decision:

- `ACCEPT` — apply the proposed rule;
- `REJECT` — keep the current rule;
- `REVISE` — use the text in `Final wording`.

For `REVISE`, write the replacement rule under `Final wording`. Use `Notes` for rationale, scope choices, or implementation constraints. Do not remove IDs, questions, or evidence. Chat replies such as “yes”, “looks good”, or revised prose do not count as decisions once this file exists.

When finished:

1. change `Status: AWAITING_USER` to `Status: READY`;
2. save this file;
3. tell the agent `continue`.

## Ruling contradictions — pattern destroyers

### D1 — Affinity keywords versus the mandatory alternative-cost label

- Scope: general rule with a Spellbook archetype application
- Existing rule: Alternative casting costs must appear on an unnumbered line using the French label `Coût Alternatif -` (`docs/context.md:131`). All card keywords must be bold in docs and MSE (`docs/context.md:88`).
- Conflicting evidence: The requested `Book Affinity` and `Spell Affinity` are named keywords intended to represent alternative casting costs currently written with `Coût Alternatif —` (`MSE_projects/13_YGO_Spellbook.mse-set/card justice of prophecy:19`, `docs/13_archetype_spellbook.md:64`, `docs/13_archetype_spellbook.md:74`).
- Why this destroys a pattern: Replacing `Coût Alternatif —` with an affinity keyword introduces a second label for the same project-wide process unless the general rule explicitly permits documented affinity keywords as alternative-cost labels.
- Question: May a documented archetype-specific affinity keyword replace the visible `Coût Alternatif —` label, or must cards retain `Coût Alternatif —` and show the affinity name within/after that label?
- Impacted cards/files: `docs/context.md`; `docs/02_rules_keywords_card_design.md`; `docs/13_archetype_spellbook.md`; all 16 included Spellbook MSE cards if normalized; `mse/set`; `.script/create_archetype_projects.py`; `tests/test_spellbook_cards.py`.
- Proposed resolution: Allow a documented archetype-specific affinity keyword to replace `Coût Alternatif —` only when the keyword is explicitly defined as an alternative casting cost. Keep the keyword on an unnumbered line before numbered abilities and render its name in bold. The owning archetype document must define its exact condition, cost substitution, frequency, and card-type scope.
- Side effects: Changes the visible label but not the casting mechanic; requires consistent Markdown/MSE bold markup, generator support, and updated tests. `R1` and `R2` require this item to be accepted or revised; if rejected, their card text must retain `Coût Alternatif —`.
- Decision: ACCEPT
- Final wording: keyword can be alternative cost. document of keyword should mention its alternative cost.
- Notes:

## New possible rules — pattern makers

### R1 — Book Affinity for Spellbook and Prophecy creatures

- Scope: `docs/13_archetype_spellbook.md`
- Evidence: Direct MSE edit uses “Si vous avez lancez 1 “Spellbook” ce tour-ci, vous pouvez lancer ce sort sans payer son coût de mana.” (`MSE_projects/13_YGO_Spellbook.mse-set/card justice of prophecy:19`). Related creature alternative costs currently differ: Spellbook Magician requires a non-creature “Spellbook” cast (`docs/13_archetype_spellbook.md:26`), while Justice checks a card moved from the Deck to hand (`docs/13_archetype_spellbook.md:40`).
- Existing rule: Creature-specific alternative costs are written separately with `Coût Alternatif —`; no `Book Affinity` keyword is documented.
- Question: Should `Book Affinity` apply to every Creature whose card identity is “Spellbook” or “Prophecy”, including High Priestess, Justice, and Spellbook Magician; should it replace their existing distinct alternative costs; and should cards display only the bold keyword or the keyword plus its reminder text?
- Proposed rule: **Book Affinity** — For a “Spellbook” or “Prophecy” Creature, “Si vous avez lancé 1 “Spellbook” ce tour-ci, vous pouvez lancer ce sort sans payer son coût de mana.” Put this unnumbered alternative-cost keyword before numbered abilities.
- Boundary and exceptions: Archetype-only. “Spellbook” means a card whose mechanically referenced name/archetype matches “Spellbook”. The cast this turn may be a creature or non-creature unless `Final wording` narrows it. Decide explicitly whether High Priestess keeps her reveal-3 alternative instead of, or in addition to, Book Affinity.
- Impacted cards/files: `card high priestess of prophecy`, `card justice of prophecy`, `card spellbook magician of prophecy`; their sections in `docs/13_archetype_spellbook.md`; `mse/set`; `.script/create_archetype_projects.py`; `tests/test_spellbook_cards.py`; renders and proxy PDF if later normalized.
- Side effects: Can replace three mechanically different creature casting conditions with one condition; may materially broaden Spellbook Magician and Justice and materially change High Priestess. Requires D1 to define the visible alternative-cost label.
- Decision: REVISE
- Final wording: For a “Spellbook” or “Prophecy” Creature, “Si vous avez lancé 1 “Spellbook” non-creature ce tour-ci, vous pouvez lancer ce sort sans payer son coût de mana.” Put this unnumbered alternative-cost keyword before numbered abilities.
- Notes:

### R2 — Spell Affinity for Spellbook spells

- Scope: `docs/13_archetype_spellbook.md`
- Evidence: The same alternative cost appears as a common Sorcery rule and on 11 Spellbook Sorceries (`docs/13_archetype_spellbook.md:64`, `:74`, `:86`, `:98`, `:114`, `:126`, `:138`, `:150`, `:162`, `:176`, `:190`, `:202`). Current MSE examples include `card spellbook of secrets:19` and `card spellbook of knowledge:19`.
- Existing rule: “Coût Alternatif — Si vous contrôlez 1 créature “Spellbook”, vous pouvez lancer ce sort sans payer son coût de mana. Vous ne pouvez utiliser ce coût alternatif qu’une fois par tour.” No `Spell Affinity` keyword is documented.
- Question: Should `Spell Affinity` apply only to the 11 current Spellbook Sorceries, or to every non-creature “Spellbook” spell including Spellbook Star Hall and The Grand Spellbook Tower; is the once-per-turn sentence part of the keyword; and should cards show only the bold keyword or the keyword plus reminder text?
- Proposed rule: **Spell Affinity** — For a non-creature “Spellbook” spell, “Si vous contrôlez 1 créature “Spellbook”, vous pouvez lancer ce sort sans payer son coût de mana. Vous ne pouvez utiliser ce coût alternatif qu’une fois par tour.” Put this unnumbered alternative-cost keyword before additional costs and numbered abilities.
- Boundary and exceptions: Archetype-only. By default, apply to the 11 Sorceries that already carry the common alternative cost. Do not extend it to the two Enchantments unless the decision or `Final wording` says all non-creature Spellbook spells.
- Impacted cards/files: `card spellbook library of the crescent`; `card spellbook of eternity`; `card spellbook of fate`; `card spellbook of judgment`; `card spellbook of knowledge`; `card spellbook of life`; `card spellbook of miracles`; `card spellbook of power`; `card spellbook of secrets`; `card spellbook of the master`; `card spellbook of wisdom`; optionally `card spellbook star hall` and `card the grand spellbook tower`; `docs/13_archetype_spellbook.md`; `mse/set`; `.script/create_archetype_projects.py`; `tests/test_spellbook_cards.py`; renders and proxy PDF if later normalized.
- Side effects: Primarily deduplicates wording, but expanding the scope to Enchantments changes their casting mechanics. The keyword’s once-per-turn scope must remain mechanically identical to the current explicit sentence. Requires D1 to define the visible alternative-cost label.
- Decision: ACCEPT
- Final wording:
- Notes:

### R3 — Omit `carte(s)` from generic named-card selectors

- Scope: general (`docs/context.md` and mirrored detail in `docs/02_rules_keywords_card_design.md`)
- Evidence: The current search shortcut already reduces a full library operation to `cherchez X` (`docs/context.md:301-303`), but Spellbook still uses generic forms such as `Cherchez 1 carte “Spellbook”` (`docs/13_archetype_spellbook.md:28`, `:42`, `:76`, `:116`, `:192`) and `cherchez jusqu’à X cartes “Spellbook”` (`docs/13_archetype_spellbook.md:88`). Other generic selectors include `1 carte “Spellbook”` in the hand/Grave (`docs/13_archetype_spellbook.md:54`, `:152`, `:178`, `:204`, `:232`). A repository sweep found at least 24 potentially impacted files across Burning Abyss, Shaddoll, Nekroz, Spellbook, aggregate MSE data, generators, and tests.
- Existing rule: Use `cherchez X` for the complete library/reveal/hand/shuffle process (`docs/context.md:303`). Typed searches retain the type before the archetype, including `Cherchez 1 Ritual Creature “Nekroz”` and `Cherchez 1 carte non-créature Ritual Summon “Nekroz”` (`docs/context.md:426`). There is no general rule for removing the generic noun `carte` from named selectors in every zone/action.
- Question: Should `carte(s)` be omitted whenever a selector accepts any card type and is already constrained by a quoted name/archetype, for all actions and zones—not only `Cherchez`—while retaining explicit restrictive types such as `créature`, `Trap`, `Ritual Creature`, or `carte non-créature Ritual Summon`?
- Proposed rule: When an effect selects one or more cards of any type using a quoted card name, archetype, or name fragment, omit the redundant noun `carte(s)`: write `Cherchez 1 “Spellbook”`, `cherchez jusqu’à X “Spellbook”`, `ciblez 1 “Spellbook” dans votre Grave`, or `révélez 3 “Spellbook” de votre main`. Retain the explicit type when it restricts eligible objects, for example `1 créature “Spellbook”`, `1 Trap`, `1 Ritual Creature “Nekroz”`, or `1 carte non-créature Ritual Summon “Nekroz”`.
- Boundary and exceptions: General syntax rule. Apply only when the quoted name/archetype already identifies the selected card set and every card type is eligible. Keep `carte(s)` when required by a restrictive compound type, when no quoted identifier follows, or when removing it would create ambiguity about cards versus permanents, spells, abilities, or counters.
- Impacted cards/files: `docs/context.md`; `docs/02_rules_keywords_card_design.md`; `docs/10_archetype_burning_abyss.md`; `docs/11_archetype_shaddoll.md`; `docs/12_archetype_necroz.md`; `docs/13_archetype_spellbook.md`; matching MSE cards in projects 10–13; `mse/set`; `mse/update_nekroz_mse.py`; `.script` generators; tests including `tests/test_spellbook_cards.py`; at minimum the 24 files returned by the current repository sweep.
- Side effects: Widespread wording-only normalization with no intended targeting, zone, quantity, timing, or eligibility change. Requires careful per-occurrence classification so typed selectors do not lose restrictions; generators, tests, renders, and proxy PDFs may need regeneration if normalization is later requested.
- Decision: ACCEPT
- Final wording:
- Notes: `1 carte non-créature Ritual Summon “Nekroz”` should be `1 non-créature Ritual Summon “Nekroz”`

## Application result

- Accepted: D1, R2, R3.
- Revised: R1 — applied the completed `Final wording`, including the `non-creature` restriction.
- Rejected: None.
- Skipped: None.
- Failed: None.
- Owning documents changed: `docs/context.md`, `docs/02_rules_keywords_card_design.md`, and `docs/13_archetype_spellbook.md`.
- Normalized cards: None in this delegated rule step (`Normalize after approval: false`); card synchronization remains owned by the parent MSE-validation workflow.
