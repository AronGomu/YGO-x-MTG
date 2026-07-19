# Keyword inventory — cards vs rules/docs

Source: bold `<b>…</b>` in canonical MSE `rule_text` under `MSE_projects/*.mse-set/`; frozen `MSE_projects/French/` is excluded.
Rules: `docs/context.md`, `docs/02_rules_keywords_card_design.md`, `docs/*_archetype_*.md`.

## Legend

| Status | Meaning |
|--------|---------|
| GLOBAL | Defined in global rules (context / 02) |
| ARCH | Defined in archetype doc |
| EVERGREEN-MTG | Standard Magic keyword (not numbered passive) |
| LABEL | Structural label, not a game keyword |
| UNDOCUMENTED | Bold on cards, no matching definition found |
| NOISE | Likely bold markup accident / partial phrase |

## Global keyword catalog (rules)

| Keyword | Kind |
|---------|------|
| `Alternative Cost` | cost-label |
| `Attach` | action |
| `Bounce` | action |
| `Bounded X` | static |
| `Detach X` | action/cost |
| `Défense talismanique` | static |
| `Exile from Grave` | activation |
| `Flip` | event/mechanic |
| `Fusion Summon` | summon-procedure |
| `Grave` | zone |
| `Indestructible` | static |
| `Indestructible des Effets` | static |
| `Mill X` | action |
| `Negate` | action |
| `Negate & Destroy` | action |
| `On Any Cast` | event-family |
| `On Attack` | event |
| `On Attack / Block` | event |
| `On Block` | event |
| `On Block / Blocked` | event |
| `On Blocked` | event |
| `On Cast` | event-family |
| `On Creature you Control Destroy` | event |
| `On Destroy` | event |
| `On End Step` | event |
| `On Enter` | event |
| `On Exile` | event |
| `On Fusion Summon` | event |
| `On Leave Field` | event |
| `On Link Summon` | event |
| `On Opponent Cast` | event-family |
| `On Opponent Creature Enter` | event |
| `On Opponent Summon` | event |
| `On Sacrifice` | event |
| `On Send Grave` | event |
| `On Send Grave by Effect` | event |
| `On Upkeep` | event |
| `Reanimate` | action |
| `Ritual Summon` | summon-procedure |
| `Set` | action |
| `Slow Blink X Any Creature` | action |
| `Summon` | action |
| `This turn On End Step` | delayed-event |

## Archetype keyword catalog (docs)

### Burning Abyss

| Keyword | Doc |
|---------|-----|
| `Descente` | docs/10_archetype_burning_abyss.md |
| `Malédiction abyssale` | docs/10_archetype_burning_abyss.md |

### Shaddoll

| Keyword | Doc |
|---------|-----|
| `Flip` | docs/11 + global 02 |
| `Shaddoll Recovery` | docs/11_archetype_shaddoll.md |

### Necroz

| Keyword | Doc |
|---------|-----|
| `Nekroz Recovery` | docs/12_archetype_necroz.md |

### Spellbook

| Keyword | Doc |
|---------|-----|
| `Spell Affinity` | docs/13_archetype_spellbook.md |

## Keywords found on cards (MSE), by project

### Burning_Abyss

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 15 | `On Send Grave` | GLOBAL | event |
| 14 | `Grave` | GLOBAL | zone |
| 11 | `Abyssal Curse` | UNDOCUMENTED |  |
| 11 | `Descent` | UNDOCUMENTED |  |
| 5 | `Summon` | GLOBAL | action |
| 3 | `Exile from Grave` | GLOBAL | activation |
| 3 | `Detach 1` | GLOBAL | action/cost (Detach X) |
| 3 | `On Destroy` | GLOBAL | event |
| 3 | `On Enter` | GLOBAL | event |
| 2 | `Reanimate` | GLOBAL | action |
| 1 | `Detach 2` | GLOBAL | action/cost (Detach X) |
| 1 | `On Creature you Control Destroy` | GLOBAL | event |
| 1 | `Attach` | GLOBAL | action |
| 1 | `Set` | GLOBAL | action |
| 1 | `Bounded 1` | GLOBAL | static (Bounded X) |
| 1 | `bounded` | NOISE | not a keyword |
| 1 | `Detach 1 and Mill 3` | UNDOCUMENTED |  |
| 1 | `Salvage` | UNDOCUMENTED |  |
| 1 | `Slow Blink 1 Any Creature` | GLOBAL | action |
| 1 | `Ritual Summon` | GLOBAL | summon-procedure |
| 1 | `Fusion Summon` | GLOBAL | summon-procedure |
| 1 | `On Attack or Block` | UNDOCUMENTED |  |
| 1 | `Release` | UNDOCUMENTED |  |

### Necroz

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 10 | `Grave` | GLOBAL | zone |
| 9 | `On Sacrifice` | GLOBAL | event |
| 4 | `On Enter` | GLOBAL | event |
| 4 | `Ritual Summon` | GLOBAL | summon-procedure |
| 3 | `Nekroz Recovery` | ARCH:Necroz | docs/12_archetype_necroz.md |
| 2 | `Reclaim` | UNDOCUMENTED |  |
| 2 | `On Exile` | GLOBAL | event |
| 2 | `Salvage` | UNDOCUMENTED |  |
| 1 | `On Send Grave` | GLOBAL | event |
| 1 | `Bounce` | GLOBAL | action |
| 1 | `Reanimate` | GLOBAL | action |
| 1 | `Hexproof` | UNDOCUMENTED |  |
| 1 | `Release` | UNDOCUMENTED |  |

### Non_Archetype_Creatures

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 1 | `Mill X` | GLOBAL | action |
| 1 | `On Opponent Creature Enter` | GLOBAL | event |

### Non_Archetype_Non_Creatures

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 2 | `Grave` | GLOBAL | zone |
| 1 | `Summon` | GLOBAL | action |
| 1 | `Reanimate` | GLOBAL | action |
| 1 | `Fusion Summon` | GLOBAL | summon-procedure |
| 1 | `Alternative Cost` | GLOBAL | cost-label |

### Shaddoll

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 11 | `On Send Grave by Effect` | GLOBAL | event |
| 10 | `Flip` | GLOBAL | event/mechanic |
| 6 | `Shaddoll Recovery` | ARCH:Shaddoll | docs/11_archetype_shaddoll.md |
| 5 | `Grave` | GLOBAL | zone |
| 4 | `Fusion Summon` | GLOBAL | summon-procedure |
| 3 | `Summon` | GLOBAL | action |
| 2 | `On Send Grave` | GLOBAL | event |
| 2 | `On Enter` | GLOBAL | event |
| 2 | `Salvage` | UNDOCUMENTED |  |
| 2 | `Reanimate` | GLOBAL | action |
| 1 | `On Block or Blocked` | UNDOCUMENTED |  |
| 1 | `On Opponent Summon` | GLOBAL | event |
| 1 | `Effect Indestructible` | UNDOCUMENTED |  |
| 1 | `Mill X` | GLOBAL | action |
| 1 | `Release` | UNDOCUMENTED |  |
| 1 | `Exile from Grave` | GLOBAL | activation |

### Spellbook

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 10 | `Spell Affinity` | ARCH:Spellbook | docs/13_archetype_spellbook.md |
| 7 | `Grave` | GLOBAL | zone |
| 2 | `Alternative Cost` | GLOBAL | cost-label |
| 2 | `Summon` | GLOBAL | action |
| 2 | `Reanimate` | GLOBAL | action |
| 2 | `On Leave Field` | GLOBAL | event |
| 1 | `On End Step` | GLOBAL | event |
| 1 | `On Enter` | GLOBAL | event |
| 1 | `Reclaim` | UNDOCUMENTED |  |
| 1 | `Bounce` | GLOBAL | action |
| 1 | `This turn On End Step` | GLOBAL | delayed-event |
| 1 | `Attach` | GLOBAL | action |
| 1 | `Protection from everything` | UNDOCUMENTED |  |
| 1 | `On Cast “Spellbook”` | GLOBAL | event-family (On Cast) |
| 1 | `On Upkeep` | GLOBAL | event |

### Staples_Fusion

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 3 | `Grave` | GLOBAL | zone |
| 2 | `On Fusion Summon` | GLOBAL | event |
| 2 | `Summon` | GLOBAL | action |
| 2 | `On Send Grave` | GLOBAL | event |
| 2 | `On Destroy` | GLOBAL | event |
| 1 | `Fusion Alternative Cost` | UNDOCUMENTED |  |
| 1 | `Flying` | UNDOCUMENTED |  |
| 1 | `On Enter` | GLOBAL | event |
| 1 | `Hexproof` | UNDOCUMENTED |  |
| 1 | `Protection from creatures` | UNDOCUMENTED |  |

### Staples_Link

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 2 | `On Link Summon` | GLOBAL | event |
| 2 | `Grave` | GLOBAL | zone |
| 1 | `Haste` | UNDOCUMENTED |  |
| 1 | `Double Strike` | UNDOCUMENTED |  |
| 1 | `On Blocked` | GLOBAL | event |

### Staples_Synchro

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 9 | `Flying` | UNDOCUMENTED |  |
| 4 | `On Enter` | GLOBAL | event |
| 4 | `Grave` | GLOBAL | zone |
| 3 | `Reanimate` | GLOBAL | action |
| 2 | `On Send Grave` | GLOBAL | event |
| 1 | `Hand Summon` | UNDOCUMENTED |  |
| 1 | `Exile 1 Plant from Grave` | UNDOCUMENTED |  |
| 1 | `On Enter or MV2+ Opponent Creature Enter` | UNDOCUMENTED |  |
| 1 | `Bounce` | GLOBAL | action |
| 1 | `Protection from everything` | UNDOCUMENTED |  |
| 1 | `Negate` | GLOBAL | action |
| 1 | `On Opponent Activation or Attack` | UNDOCUMENTED |  |
| 1 | `Summon` | GLOBAL | action |
| 1 | `Negate & Destroy` | GLOBAL | action |
| 1 | `On Enter Synchro` | UNDOCUMENTED |  |

### Staples_Xyz

| Count | Keyword | Status | Note |
|------:|---------|--------|------|
| 12 | `Detach 1` | GLOBAL | action/cost (Detach X) |
| 6 | `Detach 2` | GLOBAL | action/cost (Detach X) |
| 3 | `Attach` | GLOBAL | action |
| 3 | `Grave` | GLOBAL | zone |
| 2 | `Xyz Alternative Cost` | UNDOCUMENTED |  |
| 1 | `Trample` | UNDOCUMENTED |  |
| 1 | `On Attack or Block` | UNDOCUMENTED |  |
| 1 | `Reanimate` | GLOBAL | action |
| 1 | `Release` | UNDOCUMENTED |  |
| 1 | `Detach X` | GLOBAL | action/cost |

## Master unique list + rules coverage

| Keyword | Total hits | Status | Docs home |
|---------|----------:|--------|-----------|
| `Grave` | 50 | GLOBAL | zone |
| `On Send Grave` | 22 | GLOBAL | event |
| `Detach 1` | 15 | GLOBAL | action/cost (Detach X) |
| `On Enter` | 15 | GLOBAL | event |
| `Summon` | 14 | GLOBAL | action |
| `Reanimate` | 12 | GLOBAL | action |
| `Abyssal Curse` | 11 | UNDOCUMENTED | — |
| `Descent` | 11 | UNDOCUMENTED | — |
| `On Send Grave by Effect` | 11 | GLOBAL | event |
| `Flip` | 10 | GLOBAL | event/mechanic |
| `Flying` | 10 | UNDOCUMENTED | — |
| `Spell Affinity` | 10 | ARCH:Spellbook | docs/13_archetype_spellbook.md |
| `On Sacrifice` | 9 | GLOBAL | event |
| `Detach 2` | 7 | GLOBAL | action/cost (Detach X) |
| `Fusion Summon` | 6 | GLOBAL | summon-procedure |
| `Shaddoll Recovery` | 6 | ARCH:Shaddoll | docs/11_archetype_shaddoll.md |
| `Attach` | 5 | GLOBAL | action |
| `On Destroy` | 5 | GLOBAL | event |
| `Ritual Summon` | 5 | GLOBAL | summon-procedure |
| `Salvage` | 5 | UNDOCUMENTED | — |
| `Exile from Grave` | 4 | GLOBAL | activation |
| `Release` | 4 | UNDOCUMENTED | — |
| `Alternative Cost` | 3 | GLOBAL | cost-label |
| `Bounce` | 3 | GLOBAL | action |
| `Nekroz Recovery` | 3 | ARCH:Necroz | docs/12_archetype_necroz.md |
| `Reclaim` | 3 | UNDOCUMENTED | — |
| `Hexproof` | 2 | UNDOCUMENTED | — |
| `Mill X` | 2 | GLOBAL | action |
| `On Attack or Block` | 2 | UNDOCUMENTED | — |
| `On Exile` | 2 | GLOBAL | event |
| `On Fusion Summon` | 2 | GLOBAL | event |
| `On Leave Field` | 2 | GLOBAL | event |
| `On Link Summon` | 2 | GLOBAL | event |
| `Protection from everything` | 2 | UNDOCUMENTED | — |
| `Xyz Alternative Cost` | 2 | UNDOCUMENTED | — |
| `bounded` | 1 | NOISE | — |
| `Bounded 1` | 1 | GLOBAL | static (Bounded X) |
| `Detach 1 and Mill 3` | 1 | UNDOCUMENTED | — |
| `Detach X` | 1 | GLOBAL | action/cost |
| `Double Strike` | 1 | UNDOCUMENTED | — |
| `Effect Indestructible` | 1 | UNDOCUMENTED | — |
| `Exile 1 Plant from Grave` | 1 | UNDOCUMENTED | — |
| `Fusion Alternative Cost` | 1 | UNDOCUMENTED | — |
| `Hand Summon` | 1 | UNDOCUMENTED | — |
| `Haste` | 1 | UNDOCUMENTED | — |
| `Negate` | 1 | GLOBAL | action |
| `Negate & Destroy` | 1 | GLOBAL | action |
| `On Block or Blocked` | 1 | UNDOCUMENTED | — |
| `On Blocked` | 1 | GLOBAL | event |
| `On Cast “Spellbook”` | 1 | GLOBAL | event-family (On Cast) |
| `On Creature you Control Destroy` | 1 | GLOBAL | event |
| `On End Step` | 1 | GLOBAL | event |
| `On Enter or MV2+ Opponent Creature Enter` | 1 | UNDOCUMENTED | — |
| `On Enter Synchro` | 1 | UNDOCUMENTED | — |
| `On Opponent Activation or Attack` | 1 | UNDOCUMENTED | — |
| `On Opponent Creature Enter` | 1 | GLOBAL | event |
| `On Opponent Summon` | 1 | GLOBAL | event |
| `On Upkeep` | 1 | GLOBAL | event |
| `Protection from creatures` | 1 | UNDOCUMENTED | — |
| `Set` | 1 | GLOBAL | action |
| `Slow Blink 1 Any Creature` | 1 | GLOBAL | action |
| `This turn On End Step` | 1 | GLOBAL | delayed-event |
| `Trample` | 1 | UNDOCUMENTED | — |

## Gaps: on cards but missing / weak in rules

| Keyword | Hits | Where used (sample) | Likely action |
|---------|-----:|---------------------|---------------|
| `Abyssal Curse` | 11 | Burning_Abyss/card burning abyss - alich, Burning_Abyss/card burning abyss - barbar, Burning_Abyss/card burning abyss - cagna, Burning_Abyss/card burning abyss - calcab | Document or un-bold |
| `Descent` | 11 | Burning_Abyss/card burning abyss - alich, Burning_Abyss/card burning abyss - barbar, Burning_Abyss/card burning abyss - cagna, Burning_Abyss/card burning abyss - calcab | Document or un-bold |
| `Flying` | 10 | Staples_Fusion/card garura wings of resonant life, Staples_Synchro/card ancient fairy dragon, Staples_Synchro/card black rose dragon, Staples_Synchro/card black rose moonlight dragon | Document or un-bold |
| `Salvage` | 5 | Burning_Abyss/card burning abyss - dante, Necroz/card nekroz - unicore, Necroz/card preparation of rites, Shaddoll/card shaddoll - core | Document or un-bold |
| `Release` | 4 | Burning_Abyss/card leviair the sea dragon, Necroz/card nekroz - exa, Shaddoll/card nael shaddoll - ariel, Staples_Xyz/card leviair the sea dragon | Document or un-bold |
| `Reclaim` | 3 | Necroz/card nekroz - dance princess, Necroz/card nekroz - great sorcerer, Spellbook/card spellbook of eternity | Document or un-bold |
| `Hexproof` | 2 | Necroz/card nekroz - dance princess, Staples_Fusion/card guardian chimera | Document or un-bold |
| `On Attack or Block` | 2 | Burning_Abyss/card downerd magician, Staples_Xyz/card downerd magician | Document or un-bold |
| `Protection from everything` | 2 | Spellbook/card spellbook of wisdom, Staples_Synchro/card chaos angel | Document or un-bold |
| `Xyz Alternative Cost` | 2 | Staples_Xyz/card aa zeus sky thunder, Staples_Xyz/card downerd magician | Document or un-bold |
| `Detach 1 and Mill 3` | 1 | Burning_Abyss/card burning abyss - dante | Document or un-bold |
| `Double Strike` | 1 | Staples_Link/card borrelsword dragon | Document or un-bold |
| `Effect Indestructible` | 1 | Shaddoll/card el shaddoll - winda | Document or un-bold |
| `Exile 1 Plant from Grave` | 1 | Staples_Synchro/card black rose dragon | Document or un-bold |
| `Fusion Alternative Cost` | 1 | Staples_Fusion/card elder entity ntss | Document or un-bold |
| `Hand Summon` | 1 | Staples_Synchro/card ancient fairy dragon | Document or un-bold |
| `Haste` | 1 | Staples_Link/card accesscode talker | Document or un-bold |
| `On Block or Blocked` | 1 | Shaddoll/card el shaddoll - construct | Document or un-bold |
| `On Enter or MV2+ Opponent Creature Enter` | 1 | Staples_Synchro/card black rose moonlight dragon | Document or un-bold |
| `On Enter Synchro` | 1 | Staples_Synchro/card t.g. hyper librarian | Document or un-bold |
| `On Opponent Activation or Attack` | 1 | Staples_Synchro/card red supernova dragon | Document or un-bold |
| `Protection from creatures` | 1 | Staples_Fusion/card world chalice guardragon almarduke | Document or un-bold |
| `Trample` | 1 | Staples_Xyz/card downerd magician | Document or un-bold |

## Documented global keywords with weak/no MSE hit

Defined but not observed as bold on current MSE cards:
- `Défense talismanique`
- `Indestructible`
- `Indestructible des Effets`
- `On Any Cast`
- `On Attack / Block`
- `On Block / Blocked`
- `On Opponent Cast`

## Notes

1. Variable forms: `Detach 1/2`, `Mill 3`, `Bounded 1`, `Slow Blink 1 Any Creature` = instances of X-forms.
2. On Cast family: unqualified `On Cast "Spellbook"` is controller-scoped; `On Opponent Cast` and `On Any Cast` provide explicit alternate scopes.
3. Spell Affinity lives in archetype doc 13; Book Affinity is retired and replaced by full Alternative Cost text.
4. Descente / Malédiction abyssale / Shaddoll Recovery / Nekroz Recovery: archetype-only.
5. Case drift: `Défense Talismanique` vs `Défense talismanique`.
6. Piétinement: evergreen MTG; print alone, not numbered passive.
7. Spellbook open proposals (`On Leave Field`, `On Upkeep`) already on MSE; now defined in global rules.
