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

Ce document détaille les choix généraux de design du cube : conversion des cartes, mots-clés, types, frames MSE et conventions de templating applicables à toutes les cartes. `docs/context.md` reste la source des conventions globales synthétiques. Les mécaniques, exceptions et valeurs propres à un archétype appartiennent à son document numéroté sous `docs/`.

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

### PSCT et ordre d’une capacité

Les effets suivent le **Problem-Solving Card Text (PSCT)** et les rulings officiels Yu-Gi-Oh!, adaptés au français et au vocabulaire du cube. L’ordre canonique est :

```text
(numéro - type timing fréquence) **mot-clé de condition** — procédure d’activation, coûts et cibles ; résolution.
```

Le mot-clé qui exprime la condition ou l’événement vient en gras immédiatement après le préfixe de capacité, puis avant le tiret cadratin `—`. Les coûts et les choix de cibles précèdent `;` ; la résolution suit `;`. Une cible n’est jamais un coût. Employer `et`, `puis`, `si vous faites ainsi`, `vous pouvez`, `ciblez` et `choisissez` selon leur sens PSCT et le ruling Yu-Gi-Oh! d’origine.

Exemple :

```text
(2 - Déclenchable Hard) **On Send GYD** — Défaussez 1 carte et ciblez 1 créature contrôlée par un adversaire ; exilez-la.
```

### Passif

Effet statique toujours actif.

### Activable Sorcery / Activable Flash

Effet activé. `Sorcery` signifie vitesse rituel ; `Flash` signifie vitesse éphémère. Le timing peut être omis lorsqu’un mot-clé défini le fixe déjà.

### Déclenchable

Effet déclenché par un événement. Une capacité `Déclenchable Soft` explicitement indiquée ne peut se déclencher qu’une fois par tour pour cet objet.

Le choix d’une cible n’est pas un coût. Le verbe `ciblez` peut néanmoins apparaître avec les instructions qui précèdent `;` ou `:` ; seuls les éléments explicitement définis comme coûts sont payés.

### Soft / Hard / Hard Linked

- `Soft` : une fois par tour par objet.
- `Hard` : une fois par tour par nom de carte.
- `Hard Linked` : une seule des capacités Hard Linked de cette carte par tour.

### On Opponent Summon

**On Opponent Summon** se déclenche lorsqu’un adversaire Summon une créature. Il répond uniquement à l’action **Summon**, pas au lancement normal d’une créature ; les lancements adverses relèvent de **On Opponent's Cast** ou d’une formulation explicite.

### On Send GYD

Lorsque cette carte est mise dans un GYD depuis n’importe quelle zone, appliquez son effet **On Send GYD**. `GYD` est la notation canonique de la zone historiquement appelée `GY`.

### On Send GYD by Effect

Lorsque cette carte est mise dans un GYD par un effet de carte, appliquez son effet **On Send GYD by Effect**. Contrairement à **On Send GYD**, cet événement exclut les coûts, règles et actions qui ne sont pas des effets.

### Mill X

Envoyez les X cartes du dessus de votre Deck dans votre GYD. Utiliser `**Mill 1**`, `**Mill 2**` ou `**Mill 3**` selon le nombre de cartes à envoyer. Si le joueur choisit librement la quantité, utiliser `**Mill up to 3**`.

### On Destroy

Lorsque cette carte est détruite et envoyée au cimetière, appliquez son effet On Destroy.

### On Link Summon

**On Link Summon** fonctionne comme **On Enter**, mais se déclenche uniquement lorsqu’une `Link Creature` arrive sur le champ de bataille via sa propre invocation Link. Une `Link Creature` mise directement sur le champ de bataille par un autre effet ne déclenche pas **On Link Summon**.

### On Blocked

**On Blocked** se déclenche lorsque cette créature devient bloquée par une ou plusieurs créatures.

### On Opponent Creature Enter

**On Opponent Creature Enter** signifie : « À chaque fois qu'une créature arrive sur le terrain sous le contrôle d'un adversaire. » Placé après une instruction, ce mot-clé répète cette instruction à chaque occurrence de l'événement pendant la durée indiquée, par exemple : `Piochez 1 carte **On Opponent Creature Enter**`.

### On Creature you Control Destroy

**On Creature you Control Destroy** se déclenche lorsqu’une créature que vous contrôlez est détruite, quelle que soit la cause sauf restriction écrite sur la carte.

### Flip

Lorsque cette créature est retournée face visible, son effet Flip se déclenche.

## Super-type Trap

`Trap` est un super-type anglais réservé aux cartes non-créature et placé avant leur type Magic, par exemple `Trap Instant`, `Trap Sorcery` ou `Trap Enchantment`. Ce n’est ni un mot-clé ni un sous-type : une carte Trap ne porte plus de ligne `**Piège**` ni de sous-type français `Piège`.

Une carte Trap ne peut pas être lancée depuis la main. Elle doit d’abord être **Set** face cachée sur le terrain. Set est une action spéciale qui n’utilise pas la pile, ne paie pas le coût de lancement, ne lance pas la carte et ne déclenche pas **On Cast**. Un effet qui met une Trap face cachée sur le terrain la Set ; son activation ultérieure la lance. Une permission explicite peut autoriser ce lancement pendant le tour où elle a été Set.

Face cachée, elle est traitée comme un permanent non-créature non-terrain sans nom, couleur, coût de mana, MV, type, sous-type, super-type, capacité, force ni endurance. Elle reste sur le terrain sans effet et n’est pas un `Enchantment`.

À partir du tour suivant celui où elle a été Set, son contrôleur peut la retourner face visible et la lancer depuis le terrain à tout moment où il pourrait lancer un `Instant`, en payant normalement son coût de mana et ses coûts supplémentaires. Elle quitte alors le terrain pour la pile, utilise la pile et compte comme lancée depuis le terrain. Si un effet précise qu’une Trap peut être lancée ou activée pendant le tour où elle a été Set, cette permission contourne explicitement et uniquement l’attente d’un tour ; toutes les autres règles de lancement des Trap restent applicables.

Après résolution, une `Trap Instant` ou `Trap Sorcery` est mise au GYD normalement. Une Trap d’un type de permanent arrive face visible sur le terrain selon les règles normales de ce type. Une permission explicite de lancement depuis une autre zone reste applicable et ne compte pas comme un lancement depuis le terrain.

## Invocations spéciales

### Invocation correcte obligatoire

Une `Fusion Creature`, `Synchro Creature`, `Xyz Creature`, `Ritual Creature` ou `Link Creature` ne peut pas être lancée ni mise sur le champ de bataille, par elle-même ou par l'effet d'une carte, tant qu'elle n'a pas d'abord été mise sur le champ de bataille en respectant la méthode d'invocation propre à son type.

Une créature est **correctement invoquée** lorsqu'elle a été mise sur le champ de bataille de la manière suivante :

- une `Fusion Creature` par une invocation Fusion ;
- une `Synchro Creature` par une invocation Synchro ;
- une `Xyz Creature` par une invocation Xyz ;
- une `Ritual Creature` par une invocation Ritual ;
- une `Link Creature` par une invocation Link.

Un effet qui met directement une de ces cartes sur le champ de bataille ne contourne pas cette restriction, sauf s’il effectue explicitement l’invocation correspondante ou porte la mention `en ignorant les restrictions de Summon`. Dans ce second cas, la mise sur le terrain est légale, mais ne constitue pas une invocation correcte. Par exemple, un effet qui « met une créature depuis votre cimetière sur le champ de bataille » ne peut pas choisir une de ces créatures si elle n’a jamais été correctement invoquée auparavant et si l’effet ne porte pas cette permission.

Après avoir été correctement invoquée au moins une fois, la carte peut être lancée ou remise sur le champ de bataille par d'autres moyens, sous réserve des restrictions indiquées sur la carte ou imposées par d'autres règles.

### Summon et Reanimate

**Summon** met la carte indiquée sur le terrain depuis la zone précisée, sans la lancer ni payer son coût de mana. **Reanimate** renvoie la carte ciblée depuis son GYD sur le terrain. Ces actions ne contournent pas l’obligation d’invocation correcte des cartes d’Extra Deck ou Ritual. Une capacité qui autorise une Summon normalement illégale doit porter la mention explicite `en ignorant les restrictions de Summon`. Cette permission rend la Summon légale, mais ne constitue pas une invocation correcte pour les déplacements futurs. Lors de la conception ou de la mise à jour d’une telle carte, toujours demander à l’utilisateur s’il faut ajouter cette permission au lieu de la déduire.

### Attach

**Attach** attache la carte indiquée à une Xyz Creature comme matériel.

### Bounded X

Lorsque **Bounded X** devient actif, le contrôleur de la carte, appelée le `bounder`, choisit jusqu’à X autres créatures qu’il contrôle ; elles deviennent bounded. Un permanent bounded bénéficie du bonus ou de l’effet indiqué uniquement tant que son bounder reste sur le terrain. Si le bounder quitte le terrain, tous ses liens et effets Bounded prennent fin immédiatement. Si un permanent bounded quitte le terrain, son contrôleur peut immédiatement en choisir un nouveau dans la limite X.

### Indestructible contre les effets

La créature ne peut pas être détruite par un sort ou une capacité, mais peut toujours être détruite par les règles du combat ou par une action qui n’est pas un effet.

### Défense talismanique

Cette carte ne peut pas être ciblée par les sorts ou capacités de vos adversaires.

### Slow Blink X Any Creature

Ciblez jusqu’à X créatures ; exilez-les jusqu’à la prochaine étape de fin, puis renvoyez-les sur le terrain sous le contrôle de leur propriétaire.

### Ritual Summon

**Ritual Summon** met sur le terrain une ou plusieurs `Ritual Creatures` en respectant les matériaux et conditions indiqués. Une carte non-créature qui porte cet effet utilise un super-type comme `Ritual Summon Sorcery`. Une `Ritual Creature` qui n’a pas encore été correctement invoquée ne peut être mise sur le terrain que par cet effet. La MV des matériaux est égale à celle de la créature par défaut ; une carte peut explicitement autoriser une MV supérieure ou égale.

### Fusion Summon

**Fusion Summon** met sur le terrain une `Fusion Creature` depuis le Sideboard — nom de la zone MSE représentant l’Extra Deck — en utilisant les matériaux et zones indiqués. Une carte non-créature qui porte cet effet utilise un super-type comme `Fusion Summon Sorcery`. Une `Fusion Creature` qui n’a pas encore été correctement invoquée ne peut être mise sur le terrain que par cet effet. Les matériaux sont indiqués sur sa première ligne de règle, en italique, sans préfixe `Fusion —`.

### Synchro

Une Synchro Creature est invoquée depuis l'Extra Deck avec une créature Tuner et une ou plusieurs créatures non-Tuner dont la valeur de mana totale correspond à la valeur de mana de la Synchro. Sa première ligne place le Tuner en premier et omet le préfixe `Synchro —`, par exemple `1 Tuner + 1+ non-Tuner`.

### Xyz

Une Xyz Creature est invoquée depuis l'Extra Deck avec le nombre de créatures indiqué, de même valeur de mana. Les matériaux sont placés sous la créature Xyz. Sa première ligne indique les matériaux sans répéter `Xyz —`. Une ligne `Xyz Coût Alternatif —` remplace entièrement ces matériaux, utilise la créature indiquée comme matériel et réalise une invocation Xyz correcte.

**Detach X** signifie : envoyez X matériels attachés à cette Xyz Creature dans leur GYD. Sur une carte, remplacer X par le nombre requis (`**Detach 1**`, `**Detach 2**`, etc.). Conserver `**Detach X**` lorsque n’importe quel nombre de matériels peut être détaché. Avant `:` ou `;`, Detach est un coût ; après un événement et un tiret cadratin, il est une action de l’effet déclenché.

### Link

Une Link Creature est invoquée depuis l'Extra Deck avec le nombre ou type de matériaux indiqué. Son niveau Link est indiqué dans son type (`Link Lvl 4 Creature`, par exemple) et ses exigences de matériaux figurent sur la première ligne sans répéter `Link —`. La MV peut être exigée explicitement, comme `2 Creatures MV 1` pour Cherubini.

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
| Fusion Summon/Ritual Summon non-créature | 7.5th Edition (`sevenhalf`) |

Les frames MSE sont définies par **super-type de carte** (`Normal`, `Fusion`, `Xyz`, `Synchro`, `Link`, `Ritual`) et jamais par archétype. Les cartes non-créature `Fusion Summon` et `Ritual Summon` gardent la frame normale `sevenhalf`. Les cartes d'un archétype donné ne doivent donc pas recevoir une frame spécifique à cet archétype.

Un archétype peut contenir des cartes individuelles de plusieurs super-types : par exemple `10_YGO_Burning_Abyss` contient des cartes `Xyz`, `Synchro`, `Ritual`, `Fusion`, `Link`, `Ritual Summon` et `Fusion Summon`. Chaque carte suit alors la frame de son propre super-type.

Dans MSE, ce choix se met au niveau du fichier `card ...` avec les champs `stylesheet` et `stylesheet_version` placés juste après `card:`. Le `stylesheet` du fichier `set` reste seulement la frame par défaut du projet.

## Images MSE

Toutes les illustrations sources sont centralisées sous `assets/original_images/<archetype_ygo>/`, selon leur archétype Yu-Gi-Oh! réel. Les cartes sans archétype vont dans `assets/original_images/non_archetype/`; le classement des documents et projets du cube ne doit pas influencer ce rangement.

Chaque projet MSE conserve ses copies importées et redimensionnées dans le projet. Préférer `mse_images/imageN.png` pour les nouveaux imports, mais préserver les chemins racine `imageN.png` ou JPEG existants lorsqu’ils résolvent et passent la sauvegarde/export. Ne jamais pointer directement vers les JPG de `assets/original_images/`. Après toute modification validée, régénérer `render/`, utiliser les noms `name:` exacts et supprimer les rendus obsolètes.

```powershell
python .script/fix_mse_project_images.py --backup "CHEMIN\Projet.mse-set"
```
