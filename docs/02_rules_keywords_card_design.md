---
date: 2026-07-11
title: 02 - Règles, mots-clés et design des cartes
tags:
  - project
  - rules
  - keywords
  - card-design
  - mse
---

# 02 - Règles, mots-clés et design des cartes

Ce document est la source de vérité pour les choix concrets de design du cube : conversion des cartes, mots-clés, types, frames MSE et conventions de templating.

## Langue et nommage

- Le contenu explicatif est en français.
- Les noms de cartes, types et sous-types restent en anglais.
- Les documents d'archétype utilisent le format `[nom Yu-Gi-Oh original] => [nom cube]`.
- Les cartes MSE utilisent le nom cube dans le champ `name:`.

## Conversion des niveaux

| Niveau Yu-Gi-Oh. | Valeur de mana Magic |
| --- | ---: |
| 1 à 4 | 1 |
| 5 à 6 | 2 |
| 7 ou plus | 3 |

Cette règle s'applique aux monstres du Main Deck et aux créatures Fusion, Synchro et Xyz. Les monstres Ritual restent dans le Main Deck.

## Conversion des statistiques

- Force = `⌊ATK / 500⌋`.
- Endurance = `⌊DEF / 500⌋`.
- Minimum : `1`, sauf adaptation volontaire pour les hand traps ou cartes non-archétypales défensives.

## Couleurs

| Attribut Yu-Gi-Oh. | Couleur Magic |
| --- | --- |
| DARK | Black |
| LIGHT | White |
| WATER | Blue |
| EARTH | Green |
| FIRE | Red |
| WIND | Red / Blue / Green selon le rôle |

## Types Extra Deck

- `Fusion Creature`
- `Synchro Creature`
- `Xyz Creature`
- `Link Creature`

Ces cartes commencent dans l'Extra Deck et ne peuvent pas commencer dans le Main Deck.

## Créatures face verso

Toutes les créatures peuvent être jouées face verso en payant leur coût normal. Une créature face verso n'a pas de nom, couleur, type, capacité, force ou endurance.

Elle ne peut pas être Flip le tour où elle arrive. À partir du tour suivant, son contrôleur peut la Flip à tout moment où il pourrait lancer un rituel.

Une créature face verso peut être utilisée comme matériel de Fusion ou Ritual, mais pas comme matériel Synchro ou Xyz.

## Mots-clés et capacités standards

### Passif

Effet statique toujours actif.

### Activable Sorcery / Activable Flash

Effet activé. `Ritual` signifie vitesse rituel ; `Flash` signifie vitesse éphémère.

### Déclenchable

Effet déclenché par un événement. Les capacités Déclenchable ne sont jamais `Soft`.

### Soft / Hard / Hard Linked

- `Soft` : une fois par tour par objet.
- `Hard` : une fois par tour par nom de carte.
- `Hard Linked` : une seule des capacités Hard Linked de cette carte par tour.

### On Send GY

Lorsque cette carte est mise dans un GY depuis n’importe quelle zone, appliquez son effet **On Send GY**.

### Mill X

Envoyez les X cartes du dessus de votre Deck dans votre GY. Utiliser `**Mill 1**`, `**Mill 2**` ou `**Mill 3**` selon le nombre de cartes à envoyer. Si le joueur choisit librement la quantité, utiliser `**Mill up to 3**`.

### On Destroy

Lorsque cette carte est détruite et envoyée au cimetière, appliquez son effet On Destroy.

### Flip

Lorsque cette créature est retournée face visible, son effet Flip se déclenche.

### Descente

La première créature Burning Abyss que vous lancez chaque tour peut être lancée sans payer son coût de mana.

### Corruption

Lorsque cette carte est mise dans votre cimetière par un effet de carte, appliquez son effet Corruption.

### Piège

Une carte avec Piège peut être jouée face verso avant d'être lancée.

## Invocations spéciales

### Invocation correcte obligatoire

Une `Fusion Creature`, `Synchro Creature`, `Xyz Creature`, `Ritual Creature` ou `Link Creature` ne peut pas être lancée ni mise sur le champ de bataille, par elle-même ou par l'effet d'une carte, tant qu'elle n'a pas d'abord été mise sur le champ de bataille en respectant la méthode d'invocation propre à son type.

Une créature est **correctement invoquée** lorsqu'elle a été mise sur le champ de bataille de la manière suivante :

- une `Fusion Creature` par une invocation Fusion ;
- une `Synchro Creature` par une invocation Synchro ;
- une `Xyz Creature` par une invocation Xyz ;
- une `Ritual Creature` par une invocation Ritual ;
- une `Link Creature` par une invocation Link.

Un effet qui met directement une de ces cartes sur le champ de bataille ne contourne pas cette restriction, sauf s'il effectue explicitement l'invocation correspondante. Par exemple, un effet qui « met une créature depuis votre cimetière sur le champ de bataille » ne peut pas choisir une de ces créatures si elle n'a jamais été correctement invoquée auparavant.

Après avoir été correctement invoquée au moins une fois, la carte peut être lancée ou remise sur le champ de bataille par d'autres moyens, sous réserve des restrictions indiquées sur la carte ou imposées par d'autres règles.

### Invocation Ritual

`Invocation Ritual` met en jeu une ou plusieurs `Ritual Creature` en respectant les matériaux et conditions indiqués. Toute carte qui porte cet effet a le sous-type `Invocation Ritual`, sans répéter ce sous-type en gras dans son texte de règle. Une `Ritual Creature` qui n’a pas encore été correctement invoquée ne peut être mise en jeu que par cet effet.

### Invocation Fusion

`Invocation Fusion` met en jeu une `Fusion Creature` depuis l’Extra Deck en utilisant les matériaux et zones indiqués. Toute carte qui porte cet effet a le sous-type `Invocation Fusion`, sans répéter ce sous-type en gras dans son texte de règle. Une `Fusion Creature` qui n’a pas encore été correctement invoquée ne peut être mise en jeu que par cet effet. Les matériaux de la créature Fusion sont indiqués sur sa première ligne de règle, en italique.

### Synchro

Une Synchro Creature est invoquée depuis l'Extra Deck avec une créature Tuner et une ou plusieurs créatures non-Tuner dont la valeur de mana totale correspond à la valeur de mana de la Synchro.

### Xyz

Une Xyz Creature est invoquée depuis l'Extra Deck avec le nombre de créatures indiqué, de même valeur de mana. Les matériaux sont placés sous la créature Xyz.

**Detach X** signifie : envoyez X matériels attachés à cette Xyz Creature dans leur GY. Sur une carte, remplacer X par le nombre requis (`**Detach 1**`, `**Detach 2**`, etc.). Conserver `**Detach X**` lorsque n’importe quel nombre de matériels peut être détaché.

### Link

Une Link Creature est invoquée depuis l'Extra Deck avec le nombre ou type de matériaux indiqué. Le niveau Link est représenté par la première ligne de règle (`Link 1`, `Link 2`, etc.).

## Frames MSE validées

Le fichier détaillé des candidates est [[frame_candidates]].

| Super-type de carte | Frame MSE standard |
| --- | --- |
| Normal / autres cartes | 7.5th Edition (`sevenhalf`) |
| Fusion Creature | `gen main` — hi-res (`genevensis-00-main`) |
| Xyz Creature | M15 Spellbook (`m15-spellbook`) |
| Synchro Creature | M15 Sketch (`m15-sketch`) |
| Link Creature | Art Deco — Capenna Showcase (`m15-showcase-capenna-art-deco`) |
| Ritual Creature | Praetor / Phyrexian Showcase (`m15-showcase-praetor`) |
| Fusion/Ritual non-créature | 7.5th Edition (`sevenhalf`) |

Les frames MSE sont définies par **super-type de carte** (`Normal`, `Fusion`, `Xyz`, `Synchro`, `Link`, `Ritual`) et jamais par archétype. Les cartes d'un archétype donné ne doivent donc pas recevoir une frame spécifique à cet archétype.

Un archétype peut contenir des cartes individuelles de plusieurs super-types : par exemple `10_YGO_Burning_Abyss` contient des cartes `Xyz`, `Synchro`, `Ritual`, `Fusion` et `Link`. Chaque carte suit alors la frame de son propre super-type.

Dans MSE, ce choix se met au niveau du fichier `card ...` avec les champs `stylesheet` et `stylesheet_version` placés juste après `card:`. Le `stylesheet` du fichier `set` reste seulement la frame par défaut du projet.

## Images MSE

Les cartes MSE doivent utiliser des images importées racine `imageN.png`, pas des chemins directs vers `images/.../*.jpg`, pour éviter l'erreur de sauvegarde GUI `Referencing an inexistant file!`.

```powershell
python C:\Users\Natha\brain\1_projects\yugioh_x_magic_cube\.script\fix_mse_project_images.py --backup "CHEMIN\Projet.mse-set"
```
