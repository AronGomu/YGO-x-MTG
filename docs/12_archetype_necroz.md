---
date: 2026-07-09
title: 12 - Archétype : Necroz
tags:
  - project
  - game-design
  - cube
  - magic-the-gathering
  - yugioh
  - archetype
  - necroz
---

# 12 - Archétype : Necroz

# Necroz

## Identité de l'archétype

Necroz est un deck **Ritual / Toolbox / Anti-Extra Deck**.

### Convention des noms courts

Dans Magic Set Editor, chaque carte de cet archétype utilise le format `Nekroz - [card name]`. Le nom officiel complet est conservé dans `original_cards/` et la traçabilité se fait via les notes MSE / le nom d’affichage cube.

---

# Couleur

Couleur principale : **Bleu**

---

# Mécaniques utilisées

* Ritual
* Sideboard
* Toolbox
* Anti-Extra Deck
* Grave
* Exil

---

# Règle propre à l'archétype

Les créatures **Ritual Necroz** ne peuvent être lancées que par une invocation **Ritual**.

Sauf indication contraire :

> Vous ne pouvez utiliser chaque effet d'une créature **Necroz** qu'une seule fois par tour.

## Nekroz Recovery

**Nekroz Recovery** signifie : « Si vous ne contrôlez aucune créature : exilez cette carte et 1 autre “Nekroz” depuis votre Grave ; cherchez 1 non-créature Ritual Summon “Nekroz”. » Les non-créatures “Nekroz” qui partagent cet effet écrivent le texte complet après le tiret cadratin.

---

## Source de vérité des cartes

Les valeurs carte par carte de cet archétype sont définies uniquement dans `MSE_projects/12_YGO_Necroz.mse-set/`. Ce document ne conserve que l’identité, les règles d’archétype et la philosophie de design.


# Philosophie de design

Necroz doit être un archétype très consistant, mais dépendant de la bonne séquence de ressources.

Les cartes doivent encourager :

* la recherche de pièces spécifiques ;
* la transformation de cartes en main en effets utilitaires ;
* l'utilisation stratégique du Grave et de l'exil ;
* la punition des créatures issues du Sideboard ;
* une progression par avantage incrémental plutôt que par combo létal immédiat.

---

# Progression d'une partie

Le déroulement attendu d'une partie est le suivant :

1. Chercher une magie Ritual et une créature Ritual Necroz grâce aux effets de défausse ou aux cartes de soutien.
2. Utiliser **Shurit**, **Great Sorcerer**, **Manju** ou **Senju** pour stabiliser la main.
3. Lancer une première créature Ritual Necroz.
4. Contrôler les créatures adverses issues du Sideboard avec **Unicore**, **Brionac** ou **Trishula**.
5. Recycler les magies Ritual depuis le Grave lorsque le champ est vide.
6. Reprendre l'avantage grâce à **Cycle**, **Mirror** et **Kaleidoscope**.
7. Terminer la partie avec des créatures Ritual résilientes et une main continuellement rechargée.

---

# Contraintes de design

Toutes les futures cartes “Necroz” devront respecter les principes suivants :

* conserver une identité **Ritual** forte ;
* éviter les créatures lancées normalement trop efficaces ;
* donner aux créatures Ritual des effets utiles même lorsqu'elles sont en main ;
* limiter les effets de recherche par des restrictions « une fois par tour » ;
* faire du Sideboard une ressource et une cible d'interaction ;
* maintenir le bleu comme couleur principale de consistance, tempo et contrôle.
