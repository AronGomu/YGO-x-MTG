---
date: 2026-07-09
title: 12 - Archetype: Nekroz
tags:
  - project
  - game-design
  - cube
  - magic-the-gathering
  - yugioh
  - archetype
  - necroz
---

# 12 - Archetype: Nekroz

#Nekroz

## Archetype identity

Nekroz is a **Ritual / Toolbox / Anti-Extra Deck** deck.

### Short-name convention

In Magic Set Editor, each archetype card uses `Nekroz - [card name]`. The full official name remains under `original_cards/`; MSE notes and cube display name provide traceability.

## Color

Main color: **Blue**

## Mechanics

- **Ritual**
- **Sideboard**
- **Toolbox**
- **Anti-Extra Deck**
- **Grave**
- **Exile**

## Archetype-specific rule

**Nekroz Ritual Creatures** can only be cast through a **Ritual Summon**.

Unless stated otherwise:

> You can only use each effect of a **Nekroz** creature once per turn.

### Nekroz Recovery

**Nekroz Recovery** means: “If you control no creatures: exile this card and 1 other “Nekroz” from Grave; Search 1 non-creature Ritual Summon “Nekroz”.” Non-Nekroz cards sharing this effect print full text after em dash.

## Card source of truth

Card-by-card values for this archetype exist only in `MSE_projects/12_YGO_Necroz.mse-set/`. This document retains only identity, archetype rules, and design philosophy.

## Design philosophy

Nekroz should remain highly consistent but should depend on correct resource sequencing.

Cards should encourage:

- searching for specific pieces;
- converting cards in hand into utility effects;
- strategic use of Grave and exile;
- punishing creatures from Sideboard;
- incremental advantage rather than immediate lethal combos.

## Expected game progression

1. Search for a Ritual spell and a Nekroz Ritual Creature through discard effects or support cards.
2. Use **Shurit**, **Great Sorcerer**, **Manju**, or **Senju** to stabilize the hand.
3. Cast the first Nekroz Ritual Creature.
4. Control opposing Sideboard creatures with **Unicore**, **Brionac**, or **Trishula**.
5. Recycle Ritual spells from Grave while the field is empty.
6. Regain advantage with **Cycle**, **Mirror**, and **Kaleidoscope**.
7. Finish the game with resilient Ritual Creatures and continuously replenished hand.

## Design constraints

All future “Nekroz” cards must:

- maintain strong **Ritual** identity;
- avoid making normally cast Creatures too efficient;
- give Ritual Creatures useful effects while in hand;
- limit search effects through once-per-turn restrictions;
- make the Sideboard both a resource and an interaction target;
- keep blue as the main color for consistency, tempo, and control.
