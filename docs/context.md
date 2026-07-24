---
date: 2026-07-06
title: Project context
tags:
  - project
  - context
  - game-design
  - cube
  - yugioh
  - magic-the-gathering
---

# Project context

## Scope of rules documents

`docs/context.md` contains only the general syntax, PSCT, formatting, vocabulary, and structure rules that apply to all cards in the project. `docs/02_rules_keywords_card_design.md` details these global conventions when they require more examples.

Each archetype has its own rules, mechanics, exceptions and design philosophy in its numbered document under `docs/`. **Card-by-card values** (Magic text, cost, stats, type, frame) are defined only in `MSE_projects/*.mse-set/` projects; the docs no longer duplicate them. An archetype-specific rule must be written in this archetype document, not in `docs/context.md`. An observation only becomes a general rule if it constitutes a reusable project-wide pattern.

## Writing language

All canonical project content must be written in **English**. Frozen snapshots under `MSE_projects/French/`, `docs/French/`, `rule_reviews/French/`, and `mse/French/` are immutable archival exceptions, not canonical sources.

Canonical maintenance, reconciliation, normalization, generators, rendering, proxy generation, global rewrites, and English-file counterpart checks must exclude these four archive roots. Ordinary work may inspect them and verify their bytes against `FRENCH_ARCHIVE_SHA256SUMS`, but must never edit or expand them. Replacing archive content requires a separate explicit archival operation and regeneration of the checksum manifest.

This includes:

- design documents;
- the rules;
- descriptions of mechanics;
- balancing notes;
- design constraints;
- gameplay explanations.

## Exception: proper nouns

Archetype names and card names remain in **English**.

Examples:

- **Burning Abyss**;
- **Shaddoll**;
- **Scarm, Burning Abyss**;
- **El Shaddoll Construct**;
- **Shaddoll Fusion**.

## Card naming convention

MSE cards use the chosen cube name in their `name:` field. Full official Yu-Gi-Oh! names remain in `original_cards/`, which provides traceability without duplicating card-by-card values in archetype documents.

When a document must explicitly map an official name to a cube name, use:

```text
[original name] => [cube name]
```

Example:

```text
Scarm, Malebranche of the Burning Abyss => Burning Abyss - Scarm
```

## Name language and card types

**Card names**, **types**, and **subtypes** must always be written in **English**.

Examples:

- `Creature — Fiend`
- `Tuner Creature — Wizard`
- `Fusion Tuner Creature — Zombie`
- `Instant`
- `Sorcery`
- `Enchantment`
- `Fairy`

`Tuner` is a supertype of card, not a subtype/race/class and not an ability written in the rules text. A Tuner card must therefore use a type line like `Tuner Creature — Fiend` or `Fusion Tuner Creature — Zombie`, and must not have `(1 - Static) **Tuner**`.

## General convention

Write prose, explanatory headings, and comments in English. Keep official or chosen card and archetype names in English to preserve their Yu-Gi-Oh! identity.

In card texts, any card name, archetype name, or card-name fragment cited as a mechanical reference must be italic, including a self-name used as an activation condition, cost, target, or instruction. Full self-name references are italic without quotation marks; other card names, archetype names, and name fragments keep typographic quotation marks inside the italics. In Markdown write `*D.D. Crow*` and `*“Lyrilusc”*`; in MSE write `<i-auto>D.D. Crow</i-auto>` and `<i-auto>“Lyrilusc”</i-auto>`. For example, write `**Discard** *Effect Veiler*`, never `**Discard** Effect Veiler`. Do not italicize or quote generic types, subtypes, attributes, supertypes, zones, `this card`, or an archetype word that belongs to a bold custom keyword such as **Shaddoll Recovery**.

## Formatting abilities and keywords

A **keyword** is an atomic game term whose meaning is supplied by Magic rules, the global cube rules, or an archetype rule instead of being fully explained on each card. The closed keyword taxonomy is:

1. **Action keywords** — named commands that perform a defined operation.
2. **Ability keywords** — Magic evergreen abilities or custom global/archetype abilities.
3. **Event keywords** — named trigger or event conditions.
4. **Cost/procedure keywords** — named costs, summon procedures, or activation shortcuts.

Render a complete keyword invocation in bold with canonical capitalization (`**Keyword**` in Markdown, `<b>Keyword</b>` in MSE). Unknown bold phrases are invalid until documented and added to the keyword catalog.

Each effect or ability on a card must be numbered with its ability type. Mandatory format:

```text
(x - Type) Text of the effect.
```

Ability types:

- **Static**: static effect or keyword always active.
- **Triggered**: effect triggered by an event.
- **Activated**: activated effect or action that its controller chooses to activate.
- **Resolution**: effect applied when the sorcery or instant resolves normally.

Use canonical English ability labels in card text.

### PSCT order of effects

Format the effects according to the **Problem-Solving Card Text (PSCT)** and the official Yu-Gi-Oh! rulings, adapted to English and to the vocabulary of the cube zones. The PSCT determines in particular what is a condition, a cost, targeting, an action on activation or an action on resolution; reformulation should never move an element from one of these roles to another.

The canonical order of an ability is:

```text
(number - type timing frequency) **condition keyword** — activation procedure, costs and targets; resolution of the effect.
```

- The number, type of ability, possible timing and frequency come first.
- When a keyword expresses the triggering condition or event, it comes immediately after the ability prefix, in bold, then is separated from the PSCT by an em dash `—` (canonical typographic form of the separator `--`).
- After the em dash, follow the order PSCT: activation conditions already not covered by the keyword, costs and choice of targets before `;`, then actions carried out at resolution after `;`.
- This boundary applies to every ability type, including **Resolution**: text before `;` is performed or paid when the card or ability is activated, while text after `;` is its resolution. A **Resolution** label does not move a preceding cost into resolution.
- Choosing a target remains an action upon activation, never a cost, even when it appears before `;`.
- Use `and` for simultaneous actions, `then` when the order or success of the first action conditions the next one, and `if you do so` when a subsequent action explicitly depends on the previous one.
- Explicitly retain optionality with `you may` and distinguish `target` from `choose` in accordance with the Yu-Gi-Oh! original.

Example:

```text
(2 - Triggered Hard) **On Send Grave** — **Discard** 1 card and **Target** 1 Creature an opponent controls; **Exile** it.
```

Costs, alternative costs, additional costs, and casting conditions are not effects: they should not be given their own ability number. All cost types and casting conditions must be listed before numbered abilities and before evergreen keywords.

- The additional costs of an effect are integrated into the ability they modify, before `;` or `:` depending on the templating.
- The alternative casting costs are written on an unnumbered line with the bold keyword **Alternative Cost**, followed by ` — ` and the condition or payment.
- An affinity keyword specific to an archetype can replace this label when explicitly documented as an alternative cost. Its name must be written in bold on an unnumbered line before the abilities; the archetype document defines its condition, cost substitution, frequency, and card types involved.
- Alternative Xyz casting costs use the bold label `**Xyz Alternative Cost** —`. This line completely replaces normal materials, uses the indicated creature as material, and performs a proper Xyz Summon. The cost/material can share one proposition, for example `W, **Discard** 1 *“Burning Abyss”* Creature and use 1 *“Dante”* you control.` End with `Its materials transfer.` when materials must be retained.

Examples:

- For a Trap card, write the super-type on the type line (`Trap Instant`, `Trap Sorcery`, `Trap Enchantment`, etc.), then start its text directly with its costs, conditions or numbered abilities. Do not add a `**Trap**` keyword line.
- Write `**Xyz Alternative Cost** — W, **Discard** 1 *“Burning Abyss”* Creature and use 1 *“Dante”* you control. Its materials are transferred.`
- For Ritual effects, use the super-type `Ritual Summon` and write **Ritual Summon** in bold in the rule text.
- For Fusion effects, use the super-type `Fusion Summon` and write **Fusion Summon** in bold in the rule text.
- Do not write `**Trap**` nor `(1 - Static) **Trap**`: `Trap` is a super-type, not a keyword or an ability.
- Do not write `(2 - Trap Supplemental Cost) ...`.
- Do not write `(1 - Alternative Cost) ...`.

For **Activated** abilities, normally add the activation timing just after `Activated`. The timing can be omitted when it is already fixed by a defined keyword or by a compound action whose rule provides this timing:

- **Ritual**: ability usable only at sorcery speed.
- **Flash**: ability usable at any time when you could cast an instant / instant speed.

Examples:

```text
(1 - Activated Sorcery Soft) ...
(1 - Activated Flash Hard) ...
```

For **Activated** abilities, add an activation frequency after the type/timing if necessary.

**Triggered** abilities do not normally use frequency. An ability explicitly noted **Triggered Soft**, however, can only be triggered once per turn for this object; a new instance of the card constitutes a new object.

For abilities **Triggered** and **Activated**, add an activation frequency after the type/timing if necessary:

- **Soft**: “You can only use this ability once per turn.” This limit is not linked to the name of the card. If the card leaves the Field and returns, it can use the effect again.
- **Hard**: “You can only activate the effect of X once per turn.” This limit is linked to the name of the card. Other copies cannot activate the same ability this turn.
- **Hard Linked**: “You can only use one of the Y effects of X once per turn.” This limit is linked to the name of the card and also locks other **Hard Linked** effects of this card.

**Hard** may also suffix a **Resolution** ability. **Resolution Hard** means the card can be activated only once per turn; every copy with the same card name shares that limit.

Example:

```text
(1 - Static) **Abyssal Curse**
(2 - Activated Hard Linked) **Descent**
(3 - Triggered Hard Linked) **On Send Grave** — At the next end step, **Search** 1 *“Burning Abyss”* Creature.
```

Do not group several keywords on a single line if this grouping prevents each ability from being numbered or typed.

The closed action-keyword catalog is **Discard**, **Exile**, **Search**, **Summon**, **Hand Summon**, **Ritual Summon**, **Fusion Summon**, **Reanimate**, **Salvage**, **Reclaim**, **Release**, **Attach**, **Bounce**, **Negate**, **Negate & Destroy**, **Set**, **Detach N**, **Mill N**, **Scry N**, **Slow Blink N Any Creature**, **Draw**, **Target**, **Counter**, **Return**, **Destroy**, **Send**, **Cast**, **Sacrifice**, and **Reveal**. Bold and capitalize an exact base-form command wherever it performs that action. Homonymous nouns, adjectives, and participles remain plain and follow sentence casing: `the target`, `Predator counter`, `draw step`, `was cast`. `Choose` and `Put` remain ordinary instructions.

Bold complete atomic compounds, including required arguments and connectors: **Detach 1 and Mill 3**, **Exile 1 Plant from Grave**, **Protection from Creatures**, **Ward 2**. Connectors remain lowercase; arguments and domain terms retain canonical case. A zone inside a compound inherits the compound's bold styling.

Ability metadata — `Static`, `Triggered`, `Activated`, `Resolution`, `Flash`, `Sorcery`, activation-timing `Ritual`, `Soft`, `Hard`, and `Hard Linked` — stays inside the italic ability prefix and is not bold keyword text. Existing MSE `<kw-a><key>Flash</key></kw-a>` template styling may remain. Standalone evergreen **Flash**, if printed as an ability outside metadata, is bold.

Evergreen Magic keywords like **Trample**, **Flying**, **Vigilance**, **Lifelink**, **Menace**, **Protection from everything**, **Protection from [quality]**, etc. should not be written as numbered passive abilities. Write them alone on their own line, in bold, without `(x - Static)`. They should come after the cost/alternative cost/casting condition lines, but before the numbered abilities. **Protection from everything** is equivalent to *protection from everything*; **Protection from [quality]** follows Magic rules for protection.

### Compactness of card text

In the card texts, write the quantities with Arabic numerals rather than in full to save space and remain consistent with the Yu-Gi-Oh / Magic templating of the cube.

Examples:

- Write `Choose 1 other Creature`, not `Choose another Creature`.
- Write `**Draw** 2 cards`, not `**Draw** two cards`.
- Write `**Send** 1 card`, not `**Send** a card`.

Choose targets explicitly during the current ability: write `**Target** 1 Creature; ...` before `;`, then refer to it as `the target`. Use `the targeted Creature` only when an earlier instruction or linked effect has already designated that target.

Example:

- Write `(2 - Activated Hard) **Target** 1 Creature; the target gains +1/+1 until the end of the turn.`
- Do not write `(2 - Activated Hard) The targeted Creature gains +1/+1 until the end of the turn.` when no target was previously chosen.

Keep numbers spelled out only in titles, design comments, or wording where the number is not a governing quantity.

Write inclusive numeric ranges with an en dash: `1–3` requires at least 1 and allows at most 3; `0–2` allows none. Always prefer compact dash ranges over `up to N` when the same bounds can be expressed as `0–N`. Never use a hyphen-minus for a numeric range.

Unqualified personal zones in card text are controller-scoped shortcuts: `Hand`, `Deck`, `Grave`, and `Exile` mean your corresponding zone. Specify `opponent`, `any player`, or another owner only when a different scope applies. The Field is shared and has no such default.

Always use the following shortcuts in card texts:

- `MV` for `Mana Value` / `mana value`.
- `Deck` for `library` / `library`.

Examples:

- Write `1 Creature MV 1`, not `1 Creature with a mana value of 1`.
- Write `from Deck`, not `from your library`.
- Write `from Deck to Grave`, not `from your library into your Grave`.

Always use `Grave` for the graveyard zone throughout the project; do not write `graveyard`, `GY`, `GYD`, or `G.Y.`. Canonical location/type terms in card text use initial uppercase: zones `Hand`, `Field`, `Deck`, `Grave`, `Exile`, `Sideboard`, `Stack`; card types `Creature`, `Creatures`, `Spell`, and `Spells`. Keep these terms plain when standalone. They remain bold only inside a larger atomic keyword such as **Exile from Grave**, **Protection from Creatures**, or **On Opponent Creature Enter**.

To give indestructible, write `gains **Indestructible**` (or `gains **Effect Indestructible**` for the variant), not `indestructible` without bold.

In effect texts, write `If` instead of `When` for triggers and event conditions.

Examples:

- Write **On Enter** — ..., not `If this Creature arrives`.
- Write `If this card is destroyed, ...`, not `When this card is destroyed, ...`.

## Event Keywords

**On Enter** means: “When this card enters the battlefield.” In the implementation, this trigger is `onEnterField`.

**On Attack** means: “When this creature attacks.”

**On Block** means: “When this creature blocks.”

**On Blocked** means: “When this creature becomes blocked by one or more creatures.”

**On Attack or Block** means: “When this creature attacks or blocks.”

**On Block or Blocked** means: “When this creature blocks or becomes blocked.”

Multiple event keywords already defined can be combined on the same ability when they share the same effect. The only allowed separator is ` or ` (bold in the combined keyword), for example `**On Enter or MV2+ Opponent Creature Enter**`. Do not use `/` or `OR` in capital letters. Each component retains its definition; the combined text does not introduce a new isolated keyword.

By default, an event keyword without controller specification only looks at **your side** (this card, or objects you control, depending on the keyword). Never add `Your` to this controller-default form. To include an opponent, write `Opponent` or **On Opponent …**; to include every player, write **On Any …**. Example: **On Enter Synchro** looks at your Synchro; an effect that also looks at the opponent is written with `Opponent` in the keyword.

**On Leave Field** means: “When this card leaves the battlefield.”

**On Upkeep** means: “At the start of your upkeep.” If the trigger is for the upkeep of another player, write it explicitly (for example **On Opponent Upkeep**).

**On End Step** means: “At the beginning of your end step.” If the trigger is for another player, write it explicitly (for example **On Opponent End Step**).

**This turn On End Step** introduces a non-recurring delayed end-step ability created by a resolving effect. Write `**This turn On End Step** — [effect]`. **On End Step** alone remains a recurring controller-default permanent trigger.

**On Fusion Summon** works like **On Enter**, but only when a `Fusion Creature` enters the battlefield via its own Fusion Summon. A `Fusion Creature` put directly onto the battlefield by another effect does not trigger **On Fusion Summon**.

**On Link Summon** works like **On Enter**, but only when a `Link Creature` enters the battlefield via its own Link Summon. A `Link Creature` put directly onto the battlefield by another effect does not trigger **On Link Summon**.

**On Enter Synchro** means: “Whenever a Synchro Creature enters the battlefield under your control.” Include this card if it itself is an arriving Synchro Creature. Do not write `On Enter Your Synchro`: the “you” side is the default (see rule above).

**On Opponent Activation or Attack** means: “When an opponent activates an ability or declares an attack with a creature.” May introduce a Triggered ability or restrict when an Activated Flash ability activates. “Activation” = ability activation on the Stack, not casting a spell (use **On Opponent Cast** for spells).

**On Opponent Creature Enter** means: “Whenever a creature enters the Field under an opponent's control.” When placed after an instruction, that instruction is repeated on each occurrence of that event for the specified duration.

**MV2+ Opponent Creature Enter** means: “Whenever a creature with MV 2 or greater enters the Field under an opponent's control.” It may be combined with another defined event by ` or `; **On Enter or MV2+ Opponent Creature Enter** therefore triggers when this card enters or when an opponent's MV 2+ creature enters.

**On Cast** means: “Every time you cast a spell, before it resolves.” This keyword family uses controller scope by default, followed by optional parameters:

- **On Cast** counts only spells cast by you;
- **On Opponent Cast** counts only spells cast by an opponent;
- **On Any Cast** counts spells cast by any player.

After the scope, add parameters that define the spells concerned, for example `“Nekroz” Ritual`. The format is **On Cast [parameters]**. Reserve `cast` for spells; never use `played` when this spell-casting action is intended.

**On Opponent Summon** means: “When an opponent summons a creature.” This trigger only responds to the **Summon** action, not to normal creature casting; use **On Opponent Cast** or explicit wording for casting events.

**On Send Grave** means: “When this card is put into a Grave from any zone.” Use this keyword for any ability on this card that triggers when sent to Grave.

**On Send Grave by Effect** means: “When this card is put into a Grave by a card effect.” Unlike **On Send Grave**, it does not trigger when the card is put into Grave by a cost, a rule or an action that is not an effect.

**On Creature you Control Destroy** means: “When a creature you control is destroyed.” Unless there is a restriction written on the card, the event counts regardless of the cause of the destruction.

**On Destroy** means: “When this card is destroyed and sent to Grave.”

**On Exile** means: “When this card is exiled.” Use this keyword for any ability of this card that triggers when it is exiled, regardless of the zone it is exiled from.

**On Sacrifice** means: “When this card is sacrificed or used as material to cast a Ritual Creature.” Use this keyword to replace wording like `If this card is used as Ritual material`.

**Detach X** means: “Detach X materials from this Xyz Creature and send them to Grave.” `X` represents number of materials to detach. On a card, replace X with the required value (`**Detach 1**`, `**Detach 2**`, etc.). If any number can be detached, keep `**Detach X**`. Detach is a cost when it precedes `:` or `;`. Placed after an event with an em-dash, such as `**On Attack or Block** — **Detach 1**`, it is a mandatory action of the triggered effect.

**Mill X** means: “Send top X cards of your Deck to Grave.” On a card, replace X with required value: `**Mill 1**`, `**Mill 2**` or `**Mill 3**`. Never write the bare keyword `**Mill**` without quantity: a card that sends 1 card uses `**Mill 1**`. If the player freely chooses the quantity from zero through three, write `**Mill 0–3**`.

**Summon** means: “Put the indicated card onto the Field from the specified zone, without casting it and without paying its mana cost.” A summon alone does not constitute a proper summon of an Extra Deck or Ritual card. Any effect allowed to perform a normally illegal **Summon** must explicitly write `ignoring the restrictions of summon`. This permission only makes **Summon** legal: it does not constitute a proper summon for future zone changes.

**Hand Summon** means: “**Summon** the creature indicated from your Hand.” On a card, write `**Hand Summon**` then the filters (`1 Creature MV 1 or less`, etc.). Same proper-summon restrictions as **Summon**.

When adding or updating a card, if an effect would perform an illegal summon — especially from Sideboard without the required summon method — ask the user whether to add `ignoring the restrictions of summon` to the effect. Never infer this permission silently.

**Reanimate** means: “**Return** target card from its Grave to Field.” This action does not circumvent the proper-summon requirement for Extra Deck or Ritual cards.

For an exact-count gate with post-success cleanup, write `**Target** 1 [Creature] MV X in Grave and choose X [additional cards] from Grave; **Reanimate** it, if you do, **Exile** [move] chosen cards.` Only the creature is targeted unless the effect explicitly targets the additional cards.

**Salvage** means: “**Return** indicated card from your Grave to your Hand.” On a card, write the keyword in bold then the selector: `**Salvage** 1 non-Creature *“Shaddoll”*`, `**Salvage** 1 other *“Burning Abyss”*`, `**Target** 1 *“Nekroz”* from Grave; **Salvage** the target`. **Salvage** does not return to Field (**Reanimate**), does not exile (**Exile from Grave**), and does not return a permanent from Field (**Bounce**).

**Reclaim** means: “**Return** indicated card from Exile to your Hand.” Write `**Reclaim**` in bold, then the selector or `target`: `**Target** 1 *“Spellbook”* from Exile; **Reclaim** the target`. Distinct from **Salvage** (Grave → Hand) and **Release** (Exile → Field).

When an effect copies only a target card's **Resolution** ability, identify the target before `;`, then write `copy the target's Resolution effect and resolve it`. This does not cast the copied card. It replaces the copying effect's resolution with the copied card's Resolution effect only; it does not copy casting costs, alternative costs, restrictions, or non-Resolution abilities.

**Release** means: “Put the indicated card from Exile onto the Field.” Write `**Release**` in bold, then the selector or `target`. Same restrictions on correct summoning as **Summon** / **Reanimate**: add `ignoring the restrictions of summon` if casting would otherwise be illegal. Distinct from **Reanimate** (Grave → Field) and **Reclaim** (Exile → Hand).

**Exile from Grave** means: “Activate only from your Grave. As a cost, **Exile** this card from your Grave.” On a card, write only the compound keyword instead of `From your Grave, **Exile** this card`. Additional costs or choices remain before `;` or `:`. Examples: `**Exile from Grave**; **Reveal**…`, `**Exile from Grave** and **Discard** 1 *“Burning Abyss”* Creature; …`, `**Exile from Grave**, **Target** 1 Creature; …`.

**Exile N [selector] from Grave** means: “As a cost, **Exile** N cards from your Grave that match the selector.” Example: `**Exile 1 Plant from Grave**`. Distinct from **Exile from Grave**, which exiles *this* card and fixes the activation zone. `N` is a positive integer; the selector follows project naming/type rules.

**Attach** means: “Attach indicated card to indicated Xyz Creature as material.”

**Bounce** means: “Return indicated permanent to its owner's hand.”

**Negate** requires a target: a permanent, spell, or ability on the Stack. If the target is a permanent, it loses all abilities and its abilities already on the Stack are countered. If the target is a spell or ability, counter it.

**Negate & Destroy** means the same as **Negate**, then **Destroy** the card that activated the effect (or the targeted permanent/spell depending on context). A card can be destroyed this way from Field, Hand, Deck, or Sideboard. It cannot be destroyed from Grave or Exile. This destruction triggers applicable **On Destroy** effects.

`Grave` is a canonical game-zone name, not a keyword. Capitalize it and keep it plain in card text. It is bold only within a larger atomic keyword such as **On Send Grave** or **Exile from Grave**.

**Set** means: “Put a card face down on the Field according to Trap rules (or equivalent permission).” **Set** is an action keyword: write it in bold in rules text. Setting does not use the Stack, cast the card, pay its casting cost, or trigger **On Cast**.

**Alternative Cost** denotes an alternative casting cost. On a card, write label in bold, then condition or payment: `**Alternative Cost** — ...`. A documented affinity keyword can replace this label.

**Bounded X** binds up to X other creatures you control to the card carrying the ability, called the `bounder`. When active, the bounder's controller chooses up to X other creatures they control; those become `bounded`. A bounded permanent benefits only while its bounder remains on Field. If the bounder leaves Field, all Bounded links/effects end. If a bounded permanent leaves Field, its controller may immediately choose a replacement within limit X.

**Indestructible** (evergreen Magic) and **Effect Indestructible** are keywords to write in bold. **Effect Indestructible** means that the creature cannot be destroyed by a spell or ability, but can still be destroyed by the rules of combat or by an action that is not an effect. For full evergreen, write **Indestructible**; for the variant limited to effects, write **Effect Indestructible**.

**Hexproof** means: “This card cannot be targeted by your opponents' spells or abilities.”

**Slow Blink X Any Creature** means: “**Target** 0–X creatures; **Exile** them until the next end step, then **Return** them to the Field under their owner's control.”

**Ritual Summon** puts one or more `Ritual Creatures` onto the Field while respecting indicated materials/conditions. A noncreature carrying this effect uses a supertype like `Ritual Summon Sorcery`. A `Ritual Creature` not yet properly summoned can only be put on Field by this effect.

**Fusion Summon** puts a `Fusion Creature` onto the Field from Sideboard using indicated materials/zones. A noncreature carrying this effect uses a supertype like `Fusion Summon Sorcery`. A `Fusion Creature` not yet properly summoned can only be put onto Field by this effect.

The name or archetype placed after **Ritual Summon** or **Fusion Summon** filters compatible creatures without the need to repeat `Ritual Creature`, `Fusion Creature` or `Sideboard` in the card text.

For any effect triggered by the card entering the battlefield, use **On Enter**, **On Fusion Summon** if the effect specifically requires a Fusion Summon, or **On Link Summon** if the effect specifically requires a Link Summon. For any effect triggered by an attack, a successful block, or becoming blocked, use **On Attack**, **On Block**, or **On Blocked** respectively. Use **On Attack or Block** or **On Block or Blocked** if the combined events trigger the same effect. For a Synchro that comes under your control (not just this card), use **On Enter Synchro**. To leave the battlefield, use **On Leave Field**. For an upkeep trigger, use **On Upkeep**. Do not rephrase these events with `If... happens`, `If... attacks` or `If... blocks`.

An event keyword that introduces an ability must be written in bold and followed by an em dash: `**On Enter** — ...`, `**On Exile** — ...`, `**On Leave Field** — ...`, `**On Upkeep** — ...`, etc. A keyword placed after a repeated instruction, such as `**Draw** 1 card **On Opponent Creature Enter**`, does not take an em dash.

Use event keywords to shorten triggered effects.

## Super-type Trap

`Trap` is an English supertype reserved for noncreature cards. It precedes the Magic type on the type line: `Trap Instant`, `Trap Sorcery`, `Trap Enchantment`, etc. `Trap` is not a keyword, ability or subtype: do not write `**Trap**` in the rule text or `Instant — Trap` on the type line.

A Trap card cannot be cast from Hand. From Hand, its owner may **Set** it face down on Field. Setting is a special action that does not use Stack, cast the card, pay its casting cost, or trigger **On Cast**. An effect that puts a Trap face down on Field sets it and satisfies this prerequisite; later activation casts it. Explicit permission can allow activation during the turn it was set.

While face down, the card is a nonland noncreature permanent with no name, color, mana cost, MV, type, subtype, supertype, ability, power, or toughness. It remains on Field without effect and is not an `Enchantment`.

Starting the next turn, its controller can turn it face up and cast it from Field any time they could cast an `Instant`, paying normal costs. The card moves from Field to Stack; this uses Stack and counts as cast from Field. Permission to activate during the turn it was set bypasses only the one-turn wait.

After resolution, a `Trap Instant` or `Trap Sorcery` goes to Grave. A Trap with a permanent type enters face up on Field. Explicit permission to cast from another zone remains applicable and does not count as casting from Field.

## Search shortcut

To simplify card texts, any effect that searches the library for a card to reveal it, put it in hand, and then shuffle must be written in the short form: **“Search X”**.

Example:

- Do not write: “search your library for a *“Burning Abyss”* creature, reveal it, put it into your Hand, then shuffle.”
- Write: “**Search** 1 *“Burning Abyss”* creature.”

This convention defaults to searching the library, revealing if necessary, putting it in your hand, then shuffling.

For any effect and zone, when a selector is already restricted by a card name, archetype name, or name fragment, omit generic `card(s)`. Write `**Search** 1 *“Spellbook”*`, `**Target** 1 *“Spellbook”* in Grave`, `**Reveal** 3 *“Spellbook”* from Hand`, `1 *“Spellbook”* Creature`, or `1 non-Creature **Ritual Summon** *“Nekroz”*`. Keep restrictive types/qualifiers. Retain `card(s)` when no named selector follows or removal would create ambiguity.

## Magic Set Editor

Editing and final rendering of the cards is done with **Magic Set Editor (MSE)**.

- Mandatory local configuration: run `python setup_mse.py` after each clone to generate the `.env` file ignored by Git.
- MSE installation: `MSE_ROOT` path of the `.env` file.
- MSE technical context to read before any generation or modification: `CONTEXT.md` under `MSE_ROOT`, if it exists.
- Cube MSE projects folder: `MSE_PROJECTS_DIR` path of the `.env` file.

MSE projects must be saved in the vault project in the `.mse-set` folder format containing a `set` file, rather than in a zipped `.mse-set` archive. Each archetype or group of non-archetypal cards should have its own MSE project to facilitate separate editing and rendering. The MSE installation remains only the opening/rendering tool, not the canonical save location for cube cards.

### MSE save title convention

Any MSE save file that matches a project document must use this convention in `set_info.title`:

```text
YGO x MTG -- [name]
```

Examples:

- `YGO x MTG -- Burning Abyss`
- `YGO x MTG -- Shaddoll`
- `YGO x MTG -- Synchro Staples`

Do not use the old prefixes `Yu-Gi-Oh × Magic Cube —` or `Yugioh X Magic Cube --` in MSE titles.

### Diagnosing MSE errors / apparent corruption

If MSE reports corruption, refuses to save, or if `mse.com --export-images` returns `3221225477` / `0xC0000005`, do not immediately conclude that a card is corrupt.

Mandatory procedure:

1. Create a standalone `.mse-set` test project with a single card:
- a minimal `set` file;
- a single `include_file: card ...`;
- the corresponding `card ...` file;
- referenced images copied locally in `images/...`.
2. Place these diagnostic projects in a separate/sibling folder, not in the middle of the production MSE project, unless explicitly temporary testing. Avoid `.mse-set` folders nested in another production `.mse-set`.
3. Check with a direct command, one card at a time:

```powershell
<MSE_CLI from .env> --export-images "PATH\Card_Test.mse-set" "PATH\Card_Test.mse-set\out_direct.png"
```

4. If the command returns an error but still creates the PNG, rerun the same test directly from the shell before declaring the card corrupt. Quick automated runs via Python `subprocess` produced false `0xC0000005` on all cards while direct exports passed.
5. To isolate a real corruption, remove/change one field at a time in the single-board project: `image`, `rule_text`, `name`, `casting_cost`, `super_type`, `sub_type`, then the `set` settings. Then reintroduce the fields one by one to identify the faulty field.

### Order and numbering of MSE cards

After each addition, deletion or regeneration of cards in a `.mse-set` project, sort the `include_file:` alphabetically from the visible `name:` field of the card, then update the collection numbers in the save files.

- Mandatory format: `001/NNN R`, `002/NNN R`, etc.
- Update all fields present: `card_code_text`, `card_code_text_2`, `card_code_text_3`.
- Keep the existing rarity suffix (`C`, `U`, `R`, etc.).
- The `NNN` total must correspond to the number of cards currently included in the respective project.

### Mandatory verification after MSE creation or modification

After each creation or modification of canonical English MSE cards, run the read-only style linter before export:

```bash
python .script/lint_mse_card_style.py
```

The linter excludes frozen French archives, reports `path:line` plus a rule ID and correction, and exits nonzero for invalid keyword bolding/capitalization, zone styling, card-name italics, ability-prefix styling, or unbalanced rich-text markup. It never rewrites cards. The test suite also runs this contract for CI enforcement.

After lint passes, check that the `.mse-set` project is not corrupted before considering the task complete.

1. Run at least one CLI export:

```powershell
<MSE_CLI from .env> --export-images "PATH\Project.mse-set" "PATH\Project.mse-set\verify_export\card.png"
```

2. Do not consider export as sufficient: a project can export correctly but fail when saving in the MSE interface with `Referencing an inexistant file!`.
3. When the project has been created or restructured, open the project in MSE with this exact form of command, then do a real test of **Save** or **Save As**:

```powershell
<MSE_EXECUTABLE from .env> "PATH/Project.mse-set"
```

4. If Save/Save As fails, search as a priority:
- `include_file:` entries that point to an absent file;
- non-empty `image`, `image_2`, `mainframe_image`, `mainframe_image_2`, `symbol`, `masterpiece_symbol` fields whose file does not exist;
- obsolete backup files like `set.include_backup` containing old references;
- `.mse-set` folders nested in the active project;
- export/test files generated within the active project.
5. Keep a backup copy of the project before any destructive corrections.

Cube MSE Image Convention:

- `original_images/<card_type>/` contains all high-resolution source illustrations downloaded from YGOPRODeck (`image_url_cropped`). The folders match exactly the categories of `original_cards/`: `Effect Monster`, `Normal Monster`, `Ritual`, `Fusion`, `Synchro`, `Xyz`, `Link`, `Spell` and `Trap`. Each JPG bears the official English name of the card using the same Windows convention as its Markdown file (`:` becomes ` -`, `"` becomes `'`, slashes become ` - `); an alternate illustration adds ` - variant N`.
- No `.mse-set` project may contain an `original_images/` or `images/` source folder. These centralized sources are used to crop or regenerate MSE images.
- `mse_images/` remains specific to each `.mse-set` project and preferably contains the new adapted imports: cropped/resized PNGs, typically `316x231`, named `imageN.png` or with a stable slug. Existing `imageN.png` root paths and named JPEGs remain valid when they resolve into the project and pass save/export.
- `render/` contains the final images rendered/exported by MSE for a `.mse-set` project; this is the canonical output folder for card renderings.
- After any validated modification of an MSE card, regenerate `render/` from the final project. Each image should be renamed with the exact name defined in `name:`, for example `Burning Abyss - Dante.png`, and not left in the generic `card.png`, `card.1.png`, etc. format. Delete old renderings whose names no longer match.
- Any non-empty `image:` reference must resolve in the project. Prefer `mse_images/imageN.png` for new imports; preserve existing root or JPEG paths when saving and exporting successfully. Never point directly to `original_images/...`.

Case identified on 2026-07-11 for **Burning Abyss**: Save can fail as long as included cards point directly to the `.jpg` source images. After resizing/importing into MSE, the successful save produces a file approximately `316x231`, without EXIF metadata, and updates the card. To prevent this bug, keep the sources in `original_images/`, then use an imported/resized copy specific to the project; `mse_images/` remains the preferred location for new imports.

To generate this format without going through the MSE interface, use the helper:

```powershell
python .script/generate_mse_imported_image.py "PATH\Project.mse-set" "original_images/<card_type>/<card_name>.jpg" --card-file "card file to update"
```

The script creates the next `mse_images/imageN.png` available in the project and, if `--card-file` is provided, replaces the card's `image:` field with this new path.

To correct an entire project already generated with `images/.../*.jpg` references, use:

```powershell
python .script/fix_mse_project_images.py --backup "PATH\Project.mse-set"
```

This script saves the project, generates `mse_images/imageN.png` for all included cards, updates the image fields, sorts the `include_file:` by card name and renumbers the `card_code_text`.

## Writing conventions for types, searches and zones

- Always write `Ritual Creature`, never `Ritual Creature` nor `Ritual Creature`. In the plural, write `Ritual Creatures`.
- For a search, put type before archetype name: `**Search** 1 Ritual Creature *“Nekroz”*.` For a noncreature summon card: `**Search** 1 non-Creature **Ritual Summon** *“Nekroz”*.` If a race is required, place it before type: `Dragon Ritual Creature`.
- For a cost of Ritual Summon based on mana value, compare the values explicitly. The default is equality; a card may say `greater than or equal` to allow overpayment, such as Good & Evil.
- If several Ritual Creatures can be put onto field, use plural agreement: `their Ritual cost(s)`.
- Personal zones are controller-scoped by default. Write `from Hand or Field`, not `from your Hand or Field`; specify another player only when needed.
- A selector without `target` chooses on resolution. Add `This effect does not target.` only when omission leaves genuine ambiguity.
- Bold one complete span only when several actions form a documented atomic compound, for example **Detach 1 and Mill 3**. Independent actions keep separate bold spans joined by ordinary prose, for example `**Discard** 1 card and **Target** 1 Creature`.
- Choosing a target is never a cost, even when `target...` is placed in the group of instructions that precedes `;` or `:`.
- An effect activated from Grave by exiling this card begins with the bold keyword `**Exile from Grave**` (definition above), never with the long phrase `From your Grave, exile this card`. Additional costs and choices remain before `;` or `:`.
- To designate the card itself, use its name if it is as short or shorter than `this card`; otherwise, use `this card`.
- To move a card from Deck, reserve **Search** for cards put into Hand. Use `**Send** ... from Deck to Grave` and `Put ... onto Field from Deck` for other destinations.
- Always write standalone location/type terms with validated capitalization and no bold: `Hand`, `Field`, `Deck`, `Grave`, `Exile`, `Sideboard`, `Stack`, `Creature(s)`, and `Spell(s)`. Keep compounds/mechanics in validated case, including `Ritual Creature`, `Fusion Creature`, and `Trap`.
- In cube cards, `Sideboard` is the name of the MSE zone that represents the Extra Deck. General rules can talk about Extra Deck; compact text of cards uses Sideboard.
- For any creature of type Sideboard / Extra Deck (`Xyz Creature`, `Synchro Creature`, `Fusion Creature`, `Link Creature`), the italicized material line **never repeats** the summon type: no prefix `Xyz —`, `Synchro —`, `Fusion —` nor `Link —`. The card's supertype already carries this information. Write only the materials, e.g. `*2 Creatures MV 1*`, `*1 Tuner + 1+ non-Tuner*`, `*1 “Shaddoll” Creature + 1 white Creature*`, `*2+ Creatures*`.
- A Fusion Creature's material line uses `*[materials]*`; the super-type `Fusion Creature` already carries the Fusion information.
- The material line of a Synchro Creature always places the Tuner first: `*1 Tuner + 1+ non-Tuner*`; the `Synchro —` prefix is omitted.
- A destruction replacement protection uses `If this card would be destroyed, you may sacrifice... instead.`
- A loss of abilities accompanied by a change in statistics uses the command `The target Creature loses all its abilities and becomes 0/0 until the end of the turn.`
- When a material line requires `different` creatures, their names must be different.
- A loss of abilities specified `on the Field` ceases as soon as the card leaves Field and does not apply in other zones.

## Extra Deck / MSE type convention

For Extra Deck creatures, the special type must be placed in the `super_type`, before `Creature`, and not in the subtype/race:

- `Xyz Creature` for Xyz creatures;

### Xyz material line

The first line of text of an `Xyz Creature` must indicate its materials in italics, **without** `Xyz —` / `Xyz -` prefix (the `Xyz Creature` supertype is sufficient). By default, use:

```text
2 Creatures MV N
```

where `N` is the mana value of the Xyz card itself. Example: an Xyz costing `{2}{U}` uses `2 Creatures MV 3`. Exceptions only exist if the card design explicitly requires `2+ Creatures` or named material, but the project baseline is `2 Creatures MV N`. Never write `Xyz — 2 Creatures MV 1`; write `2 Creatures MV 1`. The alternative cost label `Xyz Alternative Cost —` remains distinct and permitted.
- `Synchro Creature` for Synchro creatures;
- `Fusion Creature` for Fusion creatures;
- `Link Creature` for Link creatures.

For any non-creature card that explicitly performs a Special Summon, place the mechanic before its Magic type in the supertype:

- `Ritual Summon Sorcery`, `Ritual Summon Instant`, etc. for a card that bears **Ritual Summon**;
- `Fusion Summon Sorcery`, `Fusion Summon Instant`, etc. for a card that bears **Fusion Summon**;
- do not repeat this mechanic in the subtype.

In card documents, use the same shape on the type line, for example `Xyz Creature — Human`. For a Trap card, place `Trap` at the start of the super-type, for example `Trap Instant`; do not keep the legacy Trap subtype.

### Validated MSE styles

Validated frame/style choices must be retained in MSE projects and generator scripts. Frames are defined by **card super-type**, never by archetype.

An archetype project (`10_YGO_Burning_Abyss`, `12_YGO_Necroz`, `11_YGO_Shaddoll`, etc.) can therefore contain individual `Fusion`, `Synchro`, `Xyz`, `Link` or `Ritual` cards. These cards must use the frame of their individual supertype, not a global frame specific to the archetype.

In MSE files, a card-specific frame is declared directly in the `card ...` file, just after `card:`:

```text
card:
	stylesheet: m15-spellbook
	stylesheet_version: 2024-09-01
	has_styling: false
```

Do not create a separate `.mse-set` project just to change the frame of a card: use the `stylesheet` / `stylesheet_version` fields at the card level.

- **Xyz**: `m15-spellbook` (`magic-m15-spellbook.mse-style`) — M15 Spellbook frame validated.
- **Fusion Creature**: `genevensis-00-main` (`magic-genevensis-00-main.mse-style`) — `gen main` hi-res frame validated.
- **Synchro Creature**: `m15-sketch` (`magic-m15-sketch.mse-style`) — Sketch style validated.
- **Link Creature**: `m15-showcase-capenna-art-deco` (`magic-m15-showcase-capenna-art-deco.mse-style`) — Art Deco / Capenna Showcase validated.
- **Ritual Creature**: `m15-showcase-praetor` (`magic-m15-showcase-praetor.mse-style`) — Praetor / Phyrexian Showcase frame validated.
- **Normal, other cards and non-creatures Fusion Summon/Ritual Summon**: `sevenhalf` (`magic-sevenhalf.mse-style`) — frame 7.5th Edition validated.

Fusion and Ritual frames only apply to **creatures**. A non-creature card `Fusion Summon` or `Ritual Summon` keeps the default frame `sevenhalf`.

See also `frame_candidates.md` for the list of candidates and visual validations.

The first line of a creature's rule text from Extra Deck / Sideboard must be the summoning condition in italics, **without** repeating the summoning type or super-type (`Xyz`, `Synchro`, `Fusion`, `Link`):

- `*2 Creatures MV N*` for an Xyz Creature — never `*Xyz — 2 MV N*` creatures;
- `*1 Tuner + 1+ non-Tuner*` for a Synchro Creature — never `*Synchro — …*`;
- `*1 “Shaddoll” Creature + 1 white Creature*` for a Fusion Creature — never `*Fusion — …*`;
- `*2+ Creatures*` for a Link Creature — never `*Link — …*`.

For a `Link Creature`, the Link level remains carried by the card type (`Link Lvl 4 Creature`, for example), while the first line only indicates the number or properties of the required materials. MV or material level does not matter unless explicitly stated on the card, such as `2 Creatures MV 1` for Cherubini.
