# Rule review — 06 YGO Staples Synchro

- Status: APPLIED
- Applied: 2026-07-17
- Review ID: 2026-07-17-06-ygo-staples-synchro
- Generated: 2026-07-17
- Normalize after approval: false
- Source request: fix-mse-cards — MSE_projects/06_YGO_Staples_Synchro.mse-set

## How to complete this review

Answer directly in this Markdown file. For every item, replace `TODO` with exactly one decision:

- `ACCEPT` — apply the proposed rule;
- `REJECT` — keep the current rule;
- `REVISE` — use the text in `Final wording`.

For `REVISE`, write the replacement rule under `Final wording`. Use `Notes` for rationale or implementation constraints. Do not remove IDs, questions, or evidence. When finished, change `Status` to `READY`, save the file, and tell the agent `continue`.

## Ruling contradictions — pattern destroyers

### D1 — Ability timing label `Activable Ritual Soft`

- Scope: general (`docs/context.md`, `docs/02_rules_keywords_card_design.md`)
- Existing rule: Activable timing is `Sorcery` or `Flash` after `Activable` (`docs/02_rules_keywords_card_design.md` Activable section). `Ritual` is a super-type / summon procedure, not an activation speed.
- Conflicting evidence: Pre-fix MSE on Black Rose Dragon used `(2 - Activable Ritual Soft)` with a plant-exile cost (`card black rose dragon`).
- Why this destroys a pattern: Introduces a third activation speed token that is not defined and collides with Ritual Summon vocabulary.
- Question: Confirm that `Ritual` is never a legal Activable timing token and that the Black Rose line must use `Activable Sorcery Soft` (or Flash if intended)?
- Impacted cards/files: `MSE_projects/06_YGO_Staples_Synchro.mse-set/card black rose dragon` (already corrected mechanically to Sorcery Soft pending this ruling).
- Proposed resolution: Document explicitly that Activable timing tokens are only `Sorcery` and `Flash`. Never write `Activable Ritual`.
- Side effects: Any future `Activable Ritual` is invalid markup.
- Decision: REJECT
- Final wording:
- Notes:

## Application result

- Accepted: R1 Hand Summon; R3 On Opponent Activation or Attack (+ `or` separator rule); R4 Exile N [selector] from Grave (AGREE→ACCEPT); R5 Protection contre tout (AGREE→ACCEPT)
- Revised: R2 → keyword **On Enter Synchro** (not On Enter Your Synchro); default controller-side for events without Opponent
- Rejected: D1 (keep Activable **Ritual** as legal timing; Black Rose restored to Activable Ritual Soft)
- Docs: `docs/context.md`, `docs/02_rules_keywords_card_design.md`
- MSE: Black Rose Ritual Soft; Moonlight `or`; Hyper Librarian On Enter Synchro; slash→or on Xyz/BA/Shaddoll hits
- Generator: `.script/create_extra_deck_staples_projects.py`
- Skipped/failed: none

## New possible rules — pattern makers

### R1 — Keyword **Hand Summon**

- Scope: general (`docs/context.md`, `docs/02_rules_keywords_card_design.md`)
- Evidence: Ancient Fairy Dragon ability 1: `<b>Hand Summon</b> 1 créature MV 1 ou moins.` (`card ancient fairy dragon`).
- Existing rule: **Summon** puts a card onto the battlefield from a stated zone without casting (`docs/context.md` Summon).
- Question: Should **Hand Summon** become a documented action keyword meaning « **Summon** 1 créature depuis votre main » (with optional filters after the keyword)?
- Proposed rule: **Hand Summon** signifie : « **Summon** la créature indiquée depuis votre main. » Sur une carte, écrire `**Hand Summon**` puis les filtres (`1 créature MV 1 ou moins`, etc.). Même restrictions d’invocation correcte que **Summon**.
- Boundary and exceptions: Does not bypass Extra Deck / Ritual correct-invocation rules unless the effect also grants `en ignorant les restrictions de Summon`.
- Impacted cards/files: `card ancient fairy dragon`; global keyword docs; keyword inventory.
- Side effects: Shortens repeated « Summon depuis votre main » lines.
- Decision: ACCEPT
- Final wording:
- Notes:

### R2 — Event keyword **On Enter Your Synchro**

- Scope: general
- Evidence: T.G. Hyper Librarian: `<b>On Enter Your Synchro</b> — Piochez 1 carte.` (`card t.g. hyper librarian`).
- Existing rule: **On Enter** is self-enter only; opponent/filtered enters use other On* forms (`docs/context.md` event keywords).
- Question: Document **On Enter Your Synchro** as « À chaque fois qu’une Synchro Creature arrive sur le champ de bataille sous votre contrôle »?
- Proposed rule: **On Enter Your Synchro** signifie : « À chaque fois qu’une Synchro Creature arrive sur le champ de bataille sous votre contrôle. » Inclut cette carte si elle est elle-même une Synchro Creature qui arrive.
- Boundary and exceptions: Scope is controller-based, type Synchro only. Other types need their own keyword or full PSCT.
- Impacted cards/files: `card t.g. hyper librarian`; global docs.
- Side effects: Parallel forms could appear later (On Enter Your Fusion, etc.).
- Decision: REJECT 
- Final wording: On Enter Synchro
- Notes: For all effect, if not precised, its always from card from our side that triggers it. Otherwise it would be : On Enter (Yours &) Opponent

### R3 — Event / timing keyword **On Opponent Activation or Attack**

- Scope: general
- Evidence: Red Supernova Dragon ability 2 uses `<b>On Opponent Activation or Attack</b>` as the trigger window on an Activable Flash Soft line (`card red supernova dragon`).
- Existing rule: Attack events use **On Attack** family; cast/activation events use **On Cast** / ability responses; slash/OR combines defined events (`docs/context.md`).
- Question: Should **On Opponent Activation or Attack** be a defined global keyword meaning « Lorsqu’un adversaire active une capacité ou attaque avec une créature » (and usable as a condition on Activable Flash lines)?
- Proposed rule: **On Opponent Activation or Attack** signifie : « Lorsqu’un adversaire active une capacité ou déclare une attaque avec une créature. » Peut introduire une capacité Déclenchable ou restreindre le moment d’activation d’une capacité Activable Flash. Toujours en gras. Casing canonique : `Opponent` capitalisé.
- Boundary and exceptions: « Activation » = activation de capacité (pile), pas le simple lancement de sort (use **On Opponent's Cast** for spells). Attack = declare attackers step / attack declaration as used elsewhere in the cube.
- Impacted cards/files: `card red supernova dragon`; global docs.
- Side effects: Distinct from pure **On Attack** on the source creature.
- Decision: ACCEPT
- Final wording:
- Notes: Replace all '/' by 'or'. 'or' is the only way to allow several trigger conditions

### R4 — Cost keyword pattern **Exile N [filter] from Grave**

- Scope: general
- Evidence: Black Rose Dragon: `<b>Exile 1 Plant from Grave</b> : …` (`card black rose dragon`). Related existing keyword **Exile from Grave** only covers exiling *this* card from your Grave as activation (`docs/context.md`).
- Question: Document a reusable cost form **Exile N [selector] from Grave** meaning « En tant que coût, exilez N carte(s) correspondant au sélecteur depuis votre Grave » (other cards, not necessarily this card)?
- Proposed rule: **Exile N [selector] from Grave** signifie : « En tant que coût, exilez N cartes de votre **Grave** qui correspondent au sélecteur. » Exemple : `**Exile 1 Plant from Grave**`. Distinct de **Exile from Grave**, qui exile *cette* carte et fixe la zone d’activation.
- Boundary and exceptions: Selector uses project naming/type rules. N is a positive integer.
- Impacted cards/files: `card black rose dragon`; global docs.
- Side effects: Prevents overloading **Exile from Grave** for unrelated mill/cost exiles.
- Decision: AGREE
- Final wording:
- Notes:

### R5 — Evergreen **Protection contre tout**

- Scope: general
- Evidence: Chaos Angel: `<b>Protection contre tout</b>` (`card chaos angel`).
- Existing rule: Evergreen Magic keywords print bold on their own line or in text; French list includes Protection (`docs/context.md` evergreen paragraph).
- Question: Confirm French evergreen form **Protection contre tout** (and **Protection contre [qualité]**) as bold keywords equivalent to Magic’s protection from everything / protection from [quality]?
- Proposed rule: Les formes **Protection contre tout** et **Protection contre [qualité]** sont des mots-clés evergreen Magic en français. Les écrire en gras. **Protection contre tout** signifie la protection contre tout (comme *protection from everything*).
- Boundary and exceptions: Same layered rules as Magic protection.
- Impacted cards/files: `card chaos angel`; global docs.
- Side effects: Aligns French protection wording.
- Decision: AGREE
- Final wording:
- Notes:
