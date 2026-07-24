# 11 - Archetype: Shaddoll

## General rules

### Archetype identity

Shaddoll is a **Control / Value / Fusion** deck.

The archetype uses two main mechanics:

- **Flip**;
- **Shaddoll Recovery**.

### Shaddoll-specific conventions

Cube names use `[optional prefix] Shaddoll - [name]`. Official prefixes `El`, `Hel`, `Nael`, `Puru`, `Qad`, `Ree`, and `Resh` remain separate from `Shaddoll`. `Curse of the Shadow Prison` and `Sinister Shadow Games` exceptionally retain full official names.

Shaddoll creatures retain the type and subtype defined by their MSE cards; race is not standardized as `Puppet`. `Shaddoll - Falco` is a `Tuner Creature`. `Resh Shaddoll - Incarnation` and `Sinister Shadow Games` are `Trap Instant` cards, while `Shaddoll - Core` is a `Trap Enchantment`.

Cards included by `MSE_projects/11_YGO_Shaddoll.mse-set/set` are the source of truth for card-by-card values. Scripts and tests must reflect them. General Summon restrictions apply unless a card explicitly says otherwise.

## Color

Main color: **Black**

## Mechanics

### Flip

When this creature is turned face up, apply the indicated effect.

### Shaddoll Recovery

**Shaddoll Recovery** means: “**On Send Grave** — **Salvage** 1 non-creature *“Shaddoll”*.” Cards print only the bold keyword after the ability prefix, without repeating full text. **Salvage** is the general Grave → Hand keyword defined in `docs/context.md`.

`On Send Grave by Effect` remains a separate event. It is not absorbed by **Shaddoll Recovery** unless card explicitly prints that keyword.

## Card source of truth

Card-by-card values for this archetype exist only in `MSE_projects/11_YGO_Shaddoll.mse-set/`. This document retains only identity, naming conventions, and archetype mechanics.
