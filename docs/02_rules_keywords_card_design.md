---
date: 2026-07-11
title: 02 - Rules, keywords and card design
tags:
  - project
  - rules
  - keywords
  - card-design
  - mse
---

# 02 – Rules, keywords and card design

This document details the general cube design choices: card conversion, keywords, types, MSE frames and templating conventions applicable to all cards. `docs/context.md` remains the source of concise global conventions. The mechanics and exceptions specific to an archetype belong to its document numbered under `docs/`. Card-by-card values only live in `MSE_projects/*.mse-set/`.

## Language and naming

- Explanatory content is written in English.
- Card names, types, and subtypes remain in English.
- Archetype documents use the format `[original Yu-Gi-Oh! name] => [cube name]`.
- MSE cards use the cube name in the `name:` field.
- `MSE_projects/French/`, `docs/French/`, `rule_reviews/French/`, and `mse/French/` are immutable archives. Canonical maintenance, normalization, generators, rendering, proxy generation, global rewrites, and counterpart checks exclude them. Ordinary work may inspect them and verify `FRENCH_ARCHIVE_SHA256SUMS`, but only an explicit archival operation may replace archived bytes and regenerate the manifest.

## Level conversion

| Yu-Gi-Oh! Level | Magic mana value |
| --- | ---: |
| 1 to 4 | 1 |
| 5 to 6 | 2 |
| 7 or more | 3 |

This rule applies to the Main Deck monsters and Fusion, Synchro, and Xyz creatures. Ritual monsters remain in the Main Deck.

## Statistics conversion

- Power = `⌊ATK / 500⌋`.
- Toughness = `⌊DEF / 500⌋`.
- Minimum: `1`, except voluntary adaptation for hand traps or defensive non-archetypal cards.

## Colors

| Yu-Gi-Oh! Attribute | Color Magic |
| --- | --- |
| DARK | Black |
| LIGHT | White |
| WATER | Blue |
| EARTH | Green |
| FIRE | Red |
| WIND | Red / Blue / Green depending on role |

## Extra Deck card types

- `Fusion Creature`
- `Synchro Creature`
- `Xyz Creature`
- `Link Creature`

These cards start in the Extra Deck and cannot start in the Main Deck.

## Face-down creatures

All creatures can be cast face down by paying their normal cost. A face-down creature has no name, color, type, ability, power, or toughness.

It cannot be Flipped during the turn it enters. Starting the next turn, its controller may Flip it any time they could cast a sorcery.

A face-down creature can be used as Fusion or Ritual material, but not as Synchro or Xyz material.

## Standard keywords and abilities

### PSCT and ability order

The effects follow the **Problem-Solving Card Text (PSCT)** and the official Yu-Gi-Oh! rulings, adapted to English and cube vocabulary. The canonical order is:

```text
(number - type timing frequency) **condition keyword** — activation procedure, costs and targets; resolution.
```

A keyword expressing a condition or event appears in bold immediately after the ability prefix and before the em dash `—`. Every keyword (event, action, cost, affinity, evergreen Magic, **Grave**, **Set**, **Bounded**, **Indestructible** / **Effect Indestructible**, **Alternative Cost**) must be bold. Costs and target choices precede `;`; resolution follows `;`. This boundary also applies to **Resolution** abilities: text before `;` is performed or paid on activation and text after `;` resolves. Targeting is never cost. Use `and`, `then`, `if you do so`, `you may`, `target`, and `choose` according to PSCT meaning and original Yu-Gi-Oh! ruling.

Example:

```text
(2 - Triggered Hard) **On Send Grave** — Discard 1 card and target 1 creature an opponent controls; exile it.
```

### Alternative costs and affinity keywords

An alternate cost is placed on an unnumbered line before the abilities. The general label is the bold keyword **Alternative Cost**, followed by ` — ` and the condition or payment. An affinity keyword specific to an archetype can replace this label when it is explicitly defined as an alternative cost: its name must be written in bold on an unnumbered line and the archetype document must specify its condition, the substitution of the cost, its frequency and the card types affected.

### Named card selectors

When an effect selects one or more objects already restricted by a card name, archetype name, or name fragment in quotes, omit the generic name `card(s)`, regardless of zone or action. Write `Search 1 “Spellbook”`, `target 1 “Spellbook” in Grave`, `reveal 3 “Spellbook” from hand`, `1 “Spellbook” creature` or `1 non-creature Ritual Summon “Nekroz”`. Keep the restrictive types and qualifiers, but not the generic word `card(s)`. Retain `card(s)` when no quoted name follows or when removing it would create ambiguity with a permanent, spell, ability, or counter.

Unqualified `hand`, `Deck`, `Grave`, and `exile` in card text mean the corresponding personal zone of the effect's controller. Specify `opponent`, `any player`, or another owner only when scope differs. Battlefield/field remains shared.

Write inclusive numeric ranges with an en dash: `1–3` requires at least 1 and allows at most 3; `0–2` allows none. Always prefer a compact dash range over `up to N` when the same bounds are `0–N`; never use a hyphen-minus for ranges.

### Static

A static effect is always active.

### Activated Ritual / Activated Flash (and Sorcery)

An activated effect. The documented activation timings are **`Ritual`** (sorcery speed) and **`Flash`** (instant speed). `Sorcery` remains accepted as a synonym for `Ritual` for activation speed. Timing can be omitted when a defined keyword already fixes it. `Ritual` as activation timing is not summon supertype Ritual Summon.

### Triggered

An effect triggered by an event. An explicitly stated `Triggered Soft` ability can only trigger once per turn for this object.

Choosing a target is not a cost. The verb `target` may appear with instructions preceding `;` or `:`; only elements explicitly defined as costs are paid. A selector without `target` chooses on resolution; add `This effect does not target.` only when omission leaves genuine ambiguity.

### Soft / Hard / Hard Linked

- `Soft`: once per turn per object.
- `Hard`: once per turn per card name.
- `Hard Linked`: only one of this card's Hard Linked abilities per turn.

`Hard` may suffix `Resolution`. `Resolution Hard` means the card can be activated only once per turn, shared by all copies with the same card name.

### On Opponent Summon

**On Opponent Summon** triggers when an opponent **Summons** a creature. It responds only to **Summon** action, not normal creature casting; an opponent's casts use **On Opponent Cast** or explicit wording.

### On Send Grave

When this card is put into a **Grave** from any zone, trigger its **On Send Grave** effect. **Grave** is canonical zone keyword and must be bold. Do not use `graveyard`, `GY`, or `GYD`.

### On Send Grave by Effect

When this card is put into a **Grave** by a card effect, trigger its **On Send Grave by Effect** effect. Unlike **On Send Grave**, this event excludes costs, rules, and actions that are not effects.

### Mill

Send the X cards from the top of your Deck to your **Grave**. Use `**Mill 1**`, `**Mill 2**` or `**Mill 3**` depending on the number of cards to send. Never write `**Mill**` without quantity: a card that sends 1 card uses `**Mill 1**`. If the player freely chooses zero through three, use `**Mill 0–3**`.

### On Destroy

When this card is destroyed and sent to Grave, trigger its **On Destroy** effect.

### On Leave Field

**On Leave Field** means: “When this card leaves the battlefield.”

### On Upkeep

**On Upkeep** means: “At the start of your upkeep.” Specify another player if necessary (for example **On Opponent Upkeep**).

### On End Step

**On End Step** means: “At the beginning of your end step.” Specify another player if necessary, for example **On Opponent End Step**.

Use `**This turn On End Step** — [effect]` for a non-recurring delayed end-step ability created by a resolving effect. **On End Step** alone is the recurring controller-default permanent trigger.

### On Fusion Summon

**On Fusion Summon** works like **On Enter**, but only triggers when a `Fusion Creature` enters the battlefield via its own Fusion Summon. A `Fusion Creature` put directly onto the battlefield by another effect does not trigger **On Fusion Summon**.

### On Link Summon

**On Link Summon** functions like **On Enter**, but only triggers when a `Link Creature` enters the battlefield via its own Link Summon. A `Link Creature` put directly onto the battlefield by another effect does not trigger **On Link Summon**.

### On Blocked

**On Blocked** triggers when this creature becomes blocked by one or more creatures.

### On Block or Blocked

**On Block or Blocked** means: “When this creature blocks or becomes blocked.”

### Event keyword combinations

Multiple event keywords already defined can be combined on the same ability when they share the same effect. The only allowed separator is ` or ` (in bold), for example `**On Enter or MV2+ Opponent Creature Enter**` or `**On Attack or Block**`. Do not use `/` or `OR`. By default, without `Opponent` or `Any`, the trigger looks at your side. Never add `Your` to a controller-default event keyword.

### On Enter Synchro

**On Enter Synchro** means: “Whenever a Synchro Creature enters the battlefield under your control.”

### On Opponent Activation or Attack

**On Opponent Activation or Attack** means: “When an opponent activates an ability or declares an attack with a creature.”

### On Cast

**On Cast** counts spells cast by you. **On Opponent Cast** counts spells cast by an opponent. **On Any Cast** counts spells cast by every player. Add optional spell parameters after the scope, for example `**On Cast “Spellbook”**`. Reserve `cast` for spells; do not use `played` for this action.

### On Opponent Creature Enter

**On Opponent Creature Enter** means: “Whenever a creature enters the field under an opponent's control.” Placed after an instruction, this keyword repeats this instruction at each occurrence of the event for the indicated duration, for example: `Draw 1 card **On Opponent Creature Enter**`.

### On Creature you Control Destroy

**On Creature you Control Destroy** triggers when a creature you control is destroyed, regardless of the cause unless the card explicitly restricts the event.

### Flip

**Flip**: When this creature is turned face up, its Flip effect is triggered. The keyword must be written in bold.

## Super-type Trap

`Trap` is an English supertype reserved for non-creature cards and placed before Magic type, for example `Trap Instant`, `Trap Sorcery`, or `Trap Enchantment`. It is neither a keyword nor a subtype: a Trap card carries no separate Trap keyword line or subtype.

A Trap card cannot be cast from the hand. It must first be **Set** face down on the field. **Set** is a special action keyword that does not use the stack, pay a casting cost, cast a card, or trigger **On Cast**. An effect that puts a Trap face down on the field Sets it; its later activation casts it. Explicit permission may allow casting during turn it was Set.

Face down, it is treated as a nonland noncreature permanent with no name, color, mana cost, MV, type, subtype, supertype, ability, power, or toughness. It remains on the field without effect and is not an `Enchantment`.

Starting the turn after it was Set, its controller may turn it face up and cast it from the field any time they could cast an `Instant`, paying its mana cost and additional costs normally. The card moves from the field to the stack, uses the stack, and counts as cast from the field. If an effect says a Trap may be cast or activated during the turn it was Set, that permission bypasses only the one-turn wait; all other Trap casting rules still apply.

After resolution, a `Trap Instant` or `Trap Sorcery` is put into **Grave** normally. A Trap of a permanent type enters face up on the field according to the normal rules for that type. Explicit permission to cast from another zone remains applicable and does not count as casting from the field.

## Special Summons

### Proper summon required

A `Fusion Creature`, `Synchro Creature`, `Xyz Creature`, `Ritual Creature`, or `Link Creature` cannot be cast or put onto the battlefield, by itself or by the effect of a card, until it has first been put onto the battlefield according to the summoning method specific to its type.

A creature is **properly summoned** when it has been put onto the battlefield as follows:

- a `Fusion Creature` by a Fusion summon;
- a `Synchro Creature` by a Synchro summon;
- an `Xyz Creature` by an Xyz summon;
- a `Ritual Creature` by a Ritual summon;
- a `Link Creature` by a Link summon.

An effect that directly puts one of these cards onto the battlefield does not bypass this restriction, unless it explicitly performs the corresponding summon or is marked `ignoring the restrictions of Summon`. In this second case, putting it onto the field is legal, but does not constitute a proper summon. For example, an effect that "puts a creature from Grave onto the battlefield" cannot choose one of those creatures if it has never been properly summoned before and the effect does not carry this permission.

After being properly summoned at least once, the card can be cast or returned to the battlefield by other means, subject to restrictions noted on the card or imposed by other rules.

### Summon and Reanimate

**Summon** puts the indicated card onto the field from the specified zone, without casting it or paying its mana cost. **Reanimate** returns the targeted card from its Grave to the field. These actions do not circumvent the proper-summon requirement for Extra Deck or Ritual cards. An ability that allows a normally illegal Summon must be explicitly marked `ignoring the restrictions of Summon`. This permission makes Summon legal but does not count as a proper summon for future zone changes. When designing or updating such a card, always ask the user whether to add this permission instead of inferring it.

For an exact-count gate with post-success cleanup, write `Target 1 [creature] MV X in Grave and choose X [additional cards] from Grave; **Reanimate** it, if you do, exile [move] chosen cards.` Only the creature is targeted unless the effect explicitly targets the additional cards.

### Salvage

**Salvage** returns the indicated card from your Grave to your hand. Write `**Salvage**` in bold, then the selector or `target`. Distinct from **Reanimate** (Grave → field), **Bounce** (permanent → hand), and **Exile from Grave** (activation from Grave + exile of this card).

### Reclaim

**Reclaim** returns the specified card from exile to your hand. Write `**Reclaim**` in bold, then the selector or `target`. Distinct from **Salvage** (Grave → hand) and **Release** (exile → field).

### Copy Resolution effect

When an effect copies only a target card's **Resolution** ability, identify the target before `;`, then write `copy the target's Resolution effect and resolve it`. This does not cast the copied card. It replaces the copying effect's resolution with that Resolution effect only; it does not copy casting costs, alternative costs, restrictions, or non-Resolution abilities.

### Release

**Release** puts the indicated card from exile onto the field. Write `**Release**` in bold, then the selector or `target`. The same proper-summon restrictions as **Summon** / **Reanimate** apply; add `ignoring the restrictions of Summon` if necessary. Distinct from **Reanimate** (Grave → field) and **Reclaim** (exile → hand).

**Hand Summon** means: “**Summon** the creature indicated from your hand.” Write `**Hand Summon**` then the filters. The same proper-summon restrictions as **Summon** apply.

### Exile from Grave

**Exile from Grave** means: “Activate only from your Grave. As a cost, exile this card from your Grave.” Replaces the sentence `From your Grave, exile this card`. Write the keyword in bold; keep after it any additional cost or choice (discard, other exiled card, targeting), then `;` or `:` before resolution.

**Exile N [selector] from Grave** means: “As a cost, exile N cards from your **Grave** that match the selector.” Example: `**Exile 1 Plant from Grave**`. Distinct from **Exile from Grave**.

### Attach

**Attach** attaches the indicated card to an Xyz Creature as material.

### Bounded

When **Bounded X** becomes active, the card's controller, called `bounder`, chooses up to X other creatures they control; those creatures become bounded. A bounded permanent receives the indicated bonus or effect only while its bounder remains on field. If the bounder leaves the field, all its Bounded links and effects end immediately. If a bounded permanent leaves the field, its controller may immediately choose a replacement within the limit X.

### Indestructible / Effect Indestructible

**Indestructible** (evergreen Magic) and **Effect Indestructible** are written in bold. **Effect Indestructible**: The creature cannot be destroyed by a spell or ability, but can still be destroyed by the rules of combat or by an action that is not an effect.

### Hexproof

**Hexproof**: This card cannot be targeted by opponents' spells or abilities. Always bold, with canonical casing `Hexproof`.

### Protection from everything / Protection from [quality]

Use canonical English evergreen Magic wording, always in bold. **Protection from everything** = *protection from everything*.

### Bounce

**Bounce** means: “Return the indicated permanent to its owner's hand.”

### Negate

**Negate** requires a target: a permanent, spell, or ability on the stack. If the target is a permanent: this permanent loses all its abilities and all its abilities already on the stack are countered. If the target is a spell or ability: counter it. Always in bold.

### Negate & Destroy

**Negate & Destroy**: same resolution as **Negate**, then destroy the card that activated the effect. Legal destruction zones: field, hand, Deck, Sideboard. Invalid zones: **Grave**, exile. This destruction triggers **On Destroy** when applicable. Always in bold.

### Slow Blink X Any Creature

**Slow Blink X Any Creature**: Target 0–X creatures; exile them until the next end step, then return them to the field under their owner's control.

### Ritual Summon

**Ritual Summon** puts one or more `Ritual Creatures` onto the field while respecting the materials and conditions indicated. A noncreature card carrying this effect uses a supertype like `Ritual Summon Sorcery`. A `Ritual Creature` that has not yet been properly summoned can only be put on the field by this effect. The MV of materials is equal to that of the creature by default; a card can explicitly allow greater or equal MV.

### Fusion Summon

**Fusion Summon** places a `Fusion Creature` on the field from the Sideboard — the name of the MSE zone representing the Extra Deck — using the indicated materials and zones. A noncreature card carrying this effect uses a supertype like `Fusion Summon Sorcery`. A `Fusion Creature` that has not yet been properly summoned can only be put onto the field by this effect. The materials are indicated on its first rule line, in italics, **without** `Fusion —` prefix (same rule as for Xyz / Synchro / Link).

### Synchro

A Synchro Creature is summoned from the Extra Deck / Sideboard with a Tuner creature and one or more non-Tuner creatures whose total mana value matches the Synchro's mana value. Its first line puts the Tuner first and **always omits** the `Synchro —` prefix, for example `1 Tuner + 1+ non-Tuner`.

### Xyz

An Xyz Creature is summoned from the Extra Deck / Sideboard with the number of creatures indicated, of the same mana value. The materials are placed under the Xyz creature. Its first line indicates **only** materials in italics (`2 MV N` creatures, etc.): **never** write `Xyz —` nor `Xyz -` on this line — the super-type `Xyz Creature` carries the summon type. A `Xyz Alternative Cost —` line (alternative cost, separate from materials) replaces those materials entirely, uses the indicated creature as material, and performs a correct Xyz Summon.

**Detach X** means: send X materials attached to this Xyz Creature to their Grave. On a card, replace X with the required number (`**Detach 1**`, `**Detach 2**`, etc.). Retain `**Detach X**` when any number of materials may be detached. Before `:` or `;`, Detach is cost; after event and em dash, it is mandatory action of triggered effect.

### Link

A Link Creature is summoned from the Extra Deck / Sideboard with the indicated number or type of materials. Its Link level is listed in its type (`Link Lvl 4 Creature`, for example) and its material requirements are listed on the first line **without** repeating `Link —`. The MV may be required explicitly, such as `2 Creatures MV 1` for Cherubini.

### Material line Sideboard (general rule)

For any creature Sideboard (`Xyz`, `Synchro`, `Fusion`, `Link`), the materials line **never** indicates the type of summon: no `Xyz —`, `Synchro —`, `Fusion —`, `Link —`. Only materials and filters (MV, Tuner, names, colors) appear in italics.

## Validated MSE frames

The detailed candidate file is [[frame_candidates]].

| Card supertype | Standard MSE frame |
| --- | --- |
| Normal / other cards | 7.5th Edition (`sevenhalf`) |
| Fusion Creature | `gen main` — hi-res (`genevensis-00-main`) |
| Xyz Creature | M15 Spellbook (`m15-spellbook`) |
| Synchro Creature | M15 Sketch (`m15-sketch`) |
| Link Creature | Art Deco — Capenna Showcase (`m15-showcase-capenna-art-deco`) |
| Ritual Creature | Praetor / Phyrexian Showcase (`m15-showcase-praetor`) |
| Fusion Summon/Ritual Summon non-creature | 7.5th Edition (`sevenhalf`) |

MSE frames are defined by **card super-type** (`Normal`, `Fusion`, `Xyz`, `Synchro`, `Link`, `Ritual`) and never by archetype. The non-creature cards `Fusion Summon` and `Ritual Summon` keep the normal frame `sevenhalf`. Cards of a given archetype must therefore not receive a frame specific to this archetype.

An archetype can contain individual cards of several super-types: for example `10_YGO_Burning_Abyss` contains cards `Xyz`, `Synchro`, `Ritual`, `Fusion`, `Link`, `Ritual Summon` and `Fusion Summon`. Each card then follows the frame of its own super-type.

In MSE, this choice is made at the `card ...` file level with the `stylesheet` and `stylesheet_version` fields placed just after `card:`. The `stylesheet` of the `set` file remains only the default frame of the project.

## MSE Images

All source illustrations are centralized under `original_images/<card_type>/`, with the same categories as `original_cards/` (`Effect Monster`, `Normal Monster`, `Ritual`, `Fusion`, `Synchro`, `Xyz`, `Link`, `Spell`, `Trap`). Each JPG bears the official English name of the card, made compatible with Windows using the same convention as the corresponding Markdown file (`:` becomes ` -`, `"` becomes `'`, slashes become ` - `); only the extension differs. An alternative illustration adds ` - variant N` after the card name.

Each MSE project retains imported and resized copies locally. Prefer `mse_images/imageN.png` for new imports, but preserve existing root `imageN.png` or JPEG paths when they resolve and pass Save/export checks. Never point directly to JPGs under `original_images/`. After validated changes, regenerate `render/`, use exact `name:` values, and remove obsolete renders.

```powershell
python .script/fix_mse_project_images.py --backup "PATH\Project.mse-set"
```
