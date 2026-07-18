# Rule review — 12_YGO_Necroz MSE reconciliation

- Status: AWAITING_USER
- Review ID: 2026-07-17-12-ygo-necroz-rule-proposals
- Generated: 2026-07-17
- Normalize after approval: false
- Source request: fix-mse-cards — MSE_projects/12_YGO_Necroz.mse-set

## How to complete this review

Answer directly in this Markdown file. For every item, replace `TODO` with exactly one decision:

- `ACCEPT` — apply the proposed rule;
- `REJECT` — keep the current rule;
- `REVISE` — use the text in `Final wording`.

For `REVISE`, write the replacement rule under `Final wording`. Use `Notes` for rationale or implementation constraints. Do not remove IDs, questions, or evidence. When finished, change `Status` to `READY`, save the file, and tell the agent `continue`.

## Ruling contradictions — pattern destroyers

### D1 — Ritual MV check: “satisfait son coût Ritual” vs explicit equality

- Scope: general (`docs/context.md` Ritual MV comparison)
- Existing rule: For Ritual Summon mana-value costs, compare MV values explicitly; default is equality (`docs/context.md` Ritual Summon / MV cost section).
- Conflicting MSE evidence: `card nekroz - cycle`, `card nekroz - mirror`, `card nekroz - kaleidoscope` use `dont la MV satisfait son/leur(s) coût(s) Ritual` instead of `dont la MV totale est égale à …`.
- Why this destroys a pattern: “Satisfait” is vaguer than explicit equality / ≥ and may hide overpay policy.
- Exact ruling question: May Ritual material lines use `dont la MV satisfait son coût Ritual` as the project default for exact-match ritual costs, or must cards keep explicit `égale` / `supérieure ou égale`?
- Impacted cards/files: Cycle, Mirror, Kaleidoscope; future Ritual spells; `docs/context.md`.
- Proposed resolution: Allow `dont la MV satisfait son coût Ritual` as shorthand for the documented default equality check. Keep `supérieure ou égale` when overpay is intended.
- Side effects: Shorter ritual templates; equality remains the rules default unless stated otherwise.
- Decision: TODO
- Final wording:
- Notes:

### D2 — Gungnir ability 1 replaced Grave-return with indestructible grant

- Scope: archetype card identity (not general rule), listed here only if treated as reusable “discard this for protection” pattern
- Existing rule: Prior Gungnir (1) returned a “Nekroz” from Grave to hand; (2) discarded a “Nekroz” for indestructible on a “Nekroz” creature.
- Conflicting MSE evidence: Both abilities now grant indestructible (discard this / discard 1 “Nekroz” + target “Nekroz” creature).
- Why this destroys a pattern: Two nearly identical indestructible grants on one card collapse the old toolbox split (recursion vs protection).
- Exact ruling question: Accept dual indestructible modes as the new Gungnir design (card change only), or restore ability 1 as Grave return?
- Impacted cards/files: `card nekroz - gungnir` only unless a general “discard this for indestructible” keyword is desired.
- Proposed resolution: Accept as card-specific design; no general rule. (If REJECT, restore prior ability 1.)
- Side effects: Less recursion, more protection stacking.
- Decision: TODO
- Final wording:
- Notes:

## New possible rules — pattern makers

### R1 — Keyword **Bounce**

- Scope: general (`docs/context.md`, `docs/02_rules_keywords_card_design.md`)
- Evidence: `card nekroz - brionac` ability 2: `Ciblez 1 créature qui a été mise en jeu depuis un Sideboard ; <b>Bounce</b> la cible.` Replaces prior “Mélangez dans le Sideboard …”.
- Existing rule: None for **Bounce**. Sideboard return was fully written.
- Exact proposed wording: **Bounce** means return the targeted permanent to its owner’s Sideboard (Extra Deck analogue), shuffled in if the zone is ordered as a deck zone; if Bounce targets a permanent not from Sideboard, return it to its owner’s hand instead—or define strictly as “return to Sideboard only when legal, else hand.” Prefer: **Bounce** = « Renvoyez le permanent ciblé dans le Sideboard de son propriétaire. »
- Boundary and exceptions: Only for Sideboard-origin interaction unless Final wording expands.
- Impacted cards/files: Brionac; any future bounce-to-sideboard effects.
- Side effects: Needs bold keyword + optional reminder on first print.
- Decision: TODO
- Final wording:
- Notes:

### R2 — Discard self by short card name (`Défaussez Brionac`)

- Scope: general reusable templating
- Evidence: Multiple Nekroz rituals: `Défaussez Brionac`, `Défaussez Catastor`, `Défaussez Clausolas`, `Défaussez Armor`, `Défaussez Trishula`, `Défaussez Unicore`, `Défaussez Valkyrus` instead of `Défaussez cette carte`.
- Existing rule: Self-discard usually `Défaussez cette carte`.
- Exact proposed wording: On a named creature, a hand ability may use the short display name after `Défaussez` (`Défaussez Brionac`) as equivalent to discarding this card from hand. Prefer short name when the MSE `name` line is `Nekroz - X` and the reminder name is `X` / last token.
- Boundary and exceptions: Keep `cette carte` when the short name is ambiguous.
- Impacted cards/files: Most Nekroz ritual monsters; generators/tests.
- Side effects: Clearer YGO flavor; name must match printed short name.
- Decision: TODO
- Final wording:
- Notes:

### R3 — **Summon** from exile with `en ignorant les restrictions de Summon`

- Scope: general (Summon restriction permission already exists)
- Evidence: `card nekroz - exa` (2): `Ciblez 1 autre créature “Nekroz” dans votre exil ; <b>Summon</b> la cible en ignorant les restrictions de Summon.`
- Existing rule: Illegal Summons need explicit `en ignorant les restrictions de Summon` (`docs/context.md` / Summon rules).
- Exact proposed wording: When Summoning a Ritual (or Extra Deck) creature from exile/hand/Grave without the proper invocation method, always append `en ignorant les restrictions de Summon`. Reaffirm that this does not count as a correct Ritual Summon for future restriction checks unless the card says so.
- Boundary and exceptions: Pure hand-to-hand returns do not need it.
- Impacted cards/files: Exa; similar revive/summon-from-exile designs.
- Side effects: Legal Summon of restricted types without fixing invocation correctness.
- Decision: TODO
- Final wording:
- Notes:
