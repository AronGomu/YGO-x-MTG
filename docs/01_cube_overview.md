---
date: 2026-07-11
title: 01 - Cube overview
tags:
  - project
  - game-design
  - cube
  - magic-the-gathering
  - yugioh
---

# 01 - Cube overview

## Project goal

Create a cube of original cards inspired by Yu-Gi-Oh! that remains playable under Magic: The Gathering rules.

This project does not translate Yu-Gi-Oh! cards literally. Each card is adapted to preserve its role, pace, and gameplay feel within Magic's rules engine.

## Yu-Gi-Oh! → Magic conversion method

- Card names, types, and subtypes remain in English.
- Explanations, rules, and design text are written in English.
- Mana costs balance the explosive power inherited from Yu-Gi-Oh!
- Long effects become cube keywords when they represent recurring actions.
- Extra Deck cards become Fusion, Synchro, Xyz, or Link Creatures with explicit summon requirements.

## Play structure

The cube is a closed environment: every card is balanced only against cards within it. Its power level intentionally exceeds typical Magic Limited to support:

- several actions per turn;
- rapid development;
- frequent summons from the Extra Deck;
- strong interaction that prevents infinite loops and non-interactive endings.

## Cube mulligan

Instead of a Magic mulligan, each player may perform the following procedure once before the game begins:

1. Choose any number of cards from their opening hand, including zero.
2. Put the chosen cards on the bottom of their Deck in any order.
3. Draw the same number of cards.

The Deck is not shuffled during this procedure.

## Documented archetypes

### Burning Abyss

Black archetype centered on small Fiend Creatures, Grave, sacrifice, and Xyz Summons. Cards want to enter Grave and turn each lost resource into value.

### Shaddoll

Black archetype centered on Flip, sending cards to Grave, and Fusion. Creatures often have one effect when turned face up and another when sent to Grave by effect.

### Nekroz

Blue Ritual toolbox/control archetype. The deck searches for pieces, recycles resources, and uses Ritual Summons to access its main threats.

### Spellbook

Wizard/spell-chain archetype. The deck accumulates “Spellbook” cards, converts spells into incremental advantage, and rewards casting several spells during the same turn.

## Main documents

- [[02_rules_keywords_card_design|02 - Rules, keywords, and card design]]
- [[10_archetype_burning_abyss|10 - Archetype: Burning Abyss]]
- [[11_archetype_shaddoll|11 - Archetype: Shaddoll]]
- [[12_archetype_necroz|12 - Archetype: Nekroz]]
- [[13_archetype_spellbook|13 - Archetype: Spellbook]]

Card-by-card lists and text no longer live under `docs/`. English projects under `MSE_projects/*.mse-set/` are card source of truth.
