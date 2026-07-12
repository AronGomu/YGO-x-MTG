---
date: 2026-07-11
title: 01 - Présentation générale du cube
tags:
  - project
  - game-design
  - cube
  - magic-the-gathering
  - yugioh
---

# 01 - Présentation générale du cube

## Objectif du projet

Créer un cube composé de cartes originales inspirées de Yu-Gi-Oh., mais jouables avec les règles de Magic: The Gathering.

Le projet ne cherche pas une traduction littérale des cartes Yu-Gi-Oh. : chaque carte est adaptée pour retrouver son rôle, son rythme et ses sensations de jeu dans le moteur de Magic.

## Méthode de traduction Yu-Gi-Oh. → Magic

- Les noms de cartes, types et sous-types restent en anglais.
- Les explications, règles et textes de design sont en français.
- Les coûts de mana équilibrent la puissance explosive héritée de Yu-Gi-Oh.
- Les effets longs sont condensés en mots-clés de cube si ils représentent une action récurrente.
- Les cartes d'Extra Deck deviennent des créatures Fusion, Synchro, Xyz ou Link avec des conditions d'invocation explicites.

## Structure de jeu

Le cube est un environnement fermé : toutes les cartes sont équilibrées uniquement entre elles. Le niveau de puissance est volontairement supérieur à un Limited Magic classique pour permettre :

- plusieurs actions par tour ;
- du développement rapide ;
- des invocations fréquentes depuis l'Extra Deck ;
- de l'interaction forte pour empêcher les boucles infinies et les fins de partie non interactives.

## Mulligan spécifique au cube

À la place du mulligan de Magic, avant le début de la partie, chaque joueur peut effectuer une seule fois la procédure suivante :

1. choisir n'importe quel nombre de cartes de sa main de départ, y compris zéro ;
2. placer les cartes choisies sous son Deck, dans l'ordre de son choix ;
3. piocher le même nombre de cartes.

Le Deck n'est pas mélangé pendant cette procédure.

## Archétypes documentés

### Burning Abyss

Archétype noir centré sur les petites créatures Fiend, le cimetière, le sacrifice et les invocations Xyz. Les cartes veulent être envoyées au cimetière et convertissent chaque ressource perdue en value.

### Shaddoll

Archétype noir orienté Flip, envoi au cimetière et Fusion. Les créatures ont souvent un effet lorsqu'elles sont retournées face visible et un autre lorsqu'elles sont envoyées au cimetière par un effet.

### Nekroz

Archétype bleu de créatures Ritual, toolbox et contrôle. Le deck cherche ses pièces, recycle ses ressources et utilise les invocations Ritual pour accéder à ses menaces principales.

### Spellbook

Archétype Wizard / sort-chain. Le deck accumule des cartes “Spellbook”, transforme les sorts en avantage progressif et récompense les séquences de plusieurs sorts dans le même tour.

## Documents principaux

- [[02_rules_keywords_card_design|02 - Règles, mots-clés et design des cartes]]
- [[03_non_archetype_creature|03 - Non-archetype Creature]]
- [[04_ritual|04 - Ritual]]
- [[05_fusion|05 - Fusion]]
- [[06_synchro|06 - Synchro]]
- [[07_xyz|07 - Xyz]]
- [[08_link|08 - Link]]
- [[09_non_archetype_non_creature|09 - Non-archetype Non-creature]]
- [[10_archetype_burning_abyss|10 - Archétype : Burning Abyss]]
- [[11_archetype_shaddoll|11 - Archétype : Shaddoll]]
- [[12_archetype_necroz|12 - Archétype : Nekroz]]
- [[13_archetype_spellbook|13 - Archétype : Spellbook]]
