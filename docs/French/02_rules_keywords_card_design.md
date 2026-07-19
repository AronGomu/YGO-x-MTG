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

Ce document détaille les choix généraux de design du cube : conversion des cartes, mots-clés, types, frames MSE et conventions de templating applicables à toutes les cartes. `docs/context.md` reste la source des conventions globales synthétiques. Les mécaniques et exceptions propres à un archétype appartiennent à son document numéroté sous `docs/`. Les valeurs carte par carte vivent uniquement dans `MSE_projects/*.mse-set/`.

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

Le mot-clé qui exprime la condition ou l’événement vient en gras immédiatement après le préfixe de capacité, puis avant le tiret cadratin `—`. Tout mot-clé (événement, action, coût, affinité, evergreen Magic, **Grave**, **Set**, **Bounded**, **Indestructible** / **Indestructible des Effets**, **Alternative Cost** / **Coût alternatif**) doit être imprimé en gras. Les coûts et les choix de cibles précèdent `;` ; la résolution suit `;`. Une cible n’est jamais un coût. Employer `et`, `puis`, `si vous faites ainsi`, `vous pouvez`, `ciblez` et `choisissez` selon leur sens PSCT et le ruling Yu-Gi-Oh! d’origine.

Exemple :

```text
(2 - Déclenchable Hard) **On Send Grave** — Défaussez 1 carte et ciblez 1 créature contrôlée par un adversaire ; exilez-la.
```

### Coûts alternatifs et mots-clés d’affinité

Un coût alternatif est placé sur une ligne non numérotée avant les capacités. Le label général est le mot-clé gras **Alternative Cost** (forme française acceptée : **Coût alternatif**), suivi de ` — ` et de la condition ou du paiement. Un mot-clé d’affinité propre à un archétype peut remplacer ce label lorsqu’il est explicitement défini comme coût alternatif : son nom est écrit en gras sur une ligne non numérotée et le document de l’archétype précise sa condition, la substitution du coût, sa fréquence et les types de cartes concernés.

### Sélecteurs de cartes nommées

Lorsqu’un effet sélectionne un ou plusieurs objets déjà restreints par un nom de carte, un nom d’archétype ou un fragment de nom entre guillemets, omettre le nom générique `carte(s)`, quelle que soit la zone ou l’action. Écrire `Cherchez 1 “Spellbook”`, `ciblez 1 “Spellbook” dans votre Grave`, `révélez 3 “Spellbook” de votre main`, `1 créature “Spellbook”` ou `1 non-créature Ritual Summon “Nekroz”`. Conserver les types et qualificatifs restrictifs, mais pas le mot générique `carte(s)`. Conserver `carte(s)` lorsqu’aucun nom entre guillemets ne suit ou lorsque son retrait créerait une ambiguïté avec un permanent, un sort, une capacité ou un marqueur.

### Passif

Effet statique toujours actif.

### Activable Ritual / Activable Flash (et Sorcery)

Effet activé. Les timings d’activation documentés sont **`Ritual`** (vitesse rituel / sorcery speed) et **`Flash`** (vitesse éphémère). La forme `Sorcery` reste acceptée comme synonyme de `Ritual` pour la vitesse d’activation. Le timing peut être omis lorsqu’un mot-clé défini le fixe déjà. `Ritual` en tant que timing d’activation n’est pas le super-type d’invocation Ritual Summon.

### Déclenchable

Effet déclenché par un événement. Une capacité `Déclenchable Soft` explicitement indiquée ne peut se déclencher qu’une fois par tour pour cet objet.

Le choix d’une cible n’est pas un coût. Le verbe `ciblez` peut néanmoins apparaître avec les instructions qui précèdent `;` ou `:` ; seuls les éléments explicitement définis comme coûts sont payés.

### Soft / Hard / Hard Linked

- `Soft` : une fois par tour par objet.
- `Hard` : une fois par tour par nom de carte.
- `Hard Linked` : une seule des capacités Hard Linked de cette carte par tour.

### On Opponent Summon

**On Opponent Summon** se déclenche lorsqu’un adversaire Summon une créature. Il répond uniquement à l’action **Summon**, pas au lancement normal d’une créature ; les lancements adverses relèvent de **On Opponent's Cast** ou d’une formulation explicite.

### On Send Grave

Lorsque cette carte est mise dans un **Grave** depuis n’importe quelle zone, appliquez son effet **On Send Grave**. **Grave** est le mot-clé de zone unique pour le cimetière ; s’écrit en gras. Ne pas utiliser `cimetière`, `GY` ni `GYD`.

### On Send Grave by Effect

Lorsque cette carte est mise dans un **Grave** par un effet de carte, appliquez son effet **On Send Grave by Effect**. Contrairement à **On Send Grave**, cet événement exclut les coûts, règles et actions qui ne sont pas des effets.

### Mill X

Envoyez les X cartes du dessus de votre Deck dans votre **Grave**. Utiliser `**Mill 1**`, `**Mill 2**` ou `**Mill 3**` selon le nombre de cartes à envoyer. Ne jamais écrire `**Mill**` sans quantité : une carte qui envoie 1 carte utilise `**Mill 1**`. Si le joueur choisit librement la quantité, utiliser `**Mill up to 3**`.

### On Destroy

Lorsque cette carte est détruite et envoyée au Grave, appliquez son effet **On Destroy**.

### On Leave Field

**On Leave Field** signifie : « Lorsque cette carte quitte le champ de bataille. »

### On Upkeep

**On Upkeep** signifie : « Au début de votre entretien. » Préciser un autre joueur si besoin (par exemple **On Opponent Upkeep**).

### On Fusion Summon

**On Fusion Summon** fonctionne comme **On Enter**, mais se déclenche uniquement lorsqu’une `Fusion Creature` arrive sur le champ de bataille via sa propre invocation Fusion. Une `Fusion Creature` mise directement sur le champ de bataille par un autre effet ne déclenche pas **On Fusion Summon**.

### On Link Summon

**On Link Summon** fonctionne comme **On Enter**, mais se déclenche uniquement lorsqu’une `Link Creature` arrive sur le champ de bataille via sa propre invocation Link. Une `Link Creature` mise directement sur le champ de bataille par un autre effet ne déclenche pas **On Link Summon**.

### On Blocked

**On Blocked** se déclenche lorsque cette créature devient bloquée par une ou plusieurs créatures.

### On Block or Blocked

**On Block or Blocked** signifie : « Lorsque cette créature bloque ou devient bloquée. »

### Combinaisons de mots-clés d’événement

Plusieurs mots-clés d’événement déjà définis peuvent être combinés sur une même capacité lorsqu’ils partagent le même effet. Le seul séparateur autorisé est ` or ` (en gras), par exemple `**On Enter or MV2+ Opponent Creature Enter**` ou `**On Attack or Block**`. Ne pas utiliser `/` ni `OR`. Par défaut sans `Opponent`, le déclencheur regarde votre côté.

### On Enter Synchro

**On Enter Synchro** signifie : « À chaque fois qu’une Synchro Creature arrive sur le champ de bataille sous votre contrôle. »

### On Opponent Activation or Attack

**On Opponent Activation or Attack** signifie : « Lorsqu’un adversaire active une capacité ou déclare une attaque avec une créature. »

### On Opponent Creature Enter

**On Opponent Creature Enter** signifie : « À chaque fois qu'une créature arrive sur le terrain sous le contrôle d'un adversaire. » Placé après une instruction, ce mot-clé répète cette instruction à chaque occurrence de l'événement pendant la durée indiquée, par exemple : `Piochez 1 carte **On Opponent Creature Enter**`.

### On Creature you Control Destroy

**On Creature you Control Destroy** se déclenche lorsqu’une créature que vous contrôlez est détruite, quelle que soit la cause sauf restriction écrite sur la carte.

### Flip

**Flip** : lorsque cette créature est retournée face visible, son effet Flip se déclenche. Le mot-clé s’écrit en gras.

## Super-type Trap

`Trap` est un super-type anglais réservé aux cartes non-créature et placé avant leur type Magic, par exemple `Trap Instant`, `Trap Sorcery` ou `Trap Enchantment`. Ce n’est ni un mot-clé ni un sous-type : une carte Trap ne porte plus de ligne `**Piège**` ni de sous-type français `Piège`.

Une carte Trap ne peut pas être lancée depuis la main. Elle doit d’abord être **Set** face cachée sur le terrain. **Set** est un mot-clé d’action spéciale qui n’utilise pas la pile, ne paie pas le coût de lancement, ne lance pas la carte et ne déclenche pas **On Cast**. Un effet qui met une Trap face cachée sur le terrain la Set ; son activation ultérieure la lance. Une permission explicite peut autoriser ce lancement pendant le tour où elle a été Set.

Face cachée, elle est traitée comme un permanent non-créature non-terrain sans nom, couleur, coût de mana, MV, type, sous-type, super-type, capacité, force ni endurance. Elle reste sur le terrain sans effet et n’est pas un `Enchantment`.

À partir du tour suivant celui où elle a été Set, son contrôleur peut la retourner face visible et la lancer depuis le terrain à tout moment où il pourrait lancer un `Instant`, en payant normalement son coût de mana et ses coûts supplémentaires. Elle quitte alors le terrain pour la pile, utilise la pile et compte comme lancée depuis le terrain. Si un effet précise qu’une Trap peut être lancée ou activée pendant le tour où elle a été Set, cette permission contourne explicitement et uniquement l’attente d’un tour ; toutes les autres règles de lancement des Trap restent applicables.

Après résolution, une `Trap Instant` ou `Trap Sorcery` est mise au Grave normalement. Une Trap d’un type de permanent arrive face visible sur le terrain selon les règles normales de ce type. Une permission explicite de lancement depuis une autre zone reste applicable et ne compte pas comme un lancement depuis le terrain.

## Invocations spéciales

### Invocation correcte obligatoire

Une `Fusion Creature`, `Synchro Creature`, `Xyz Creature`, `Ritual Creature` ou `Link Creature` ne peut pas être lancée ni mise sur le champ de bataille, par elle-même ou par l'effet d'une carte, tant qu'elle n'a pas d'abord été mise sur le champ de bataille en respectant la méthode d'invocation propre à son type.

Une créature est **correctement invoquée** lorsqu'elle a été mise sur le champ de bataille de la manière suivante :

- une `Fusion Creature` par une invocation Fusion ;
- une `Synchro Creature` par une invocation Synchro ;
- une `Xyz Creature` par une invocation Xyz ;
- une `Ritual Creature` par une invocation Ritual ;
- une `Link Creature` par une invocation Link.

Un effet qui met directement une de ces cartes sur le champ de bataille ne contourne pas cette restriction, sauf s’il effectue explicitement l’invocation correspondante ou porte la mention `en ignorant les restrictions de Summon`. Dans ce second cas, la mise sur le terrain est légale, mais ne constitue pas une invocation correcte. Par exemple, un effet qui « met une créature depuis votre Grave sur le champ de bataille » ne peut pas choisir une de ces créatures si elle n’a jamais été correctement invoquée auparavant et si l’effet ne porte pas cette permission.

Après avoir été correctement invoquée au moins une fois, la carte peut être lancée ou remise sur le champ de bataille par d'autres moyens, sous réserve des restrictions indiquées sur la carte ou imposées par d'autres règles.

### Summon et Reanimate

**Summon** met la carte indiquée sur le terrain depuis la zone précisée, sans la lancer ni payer son coût de mana. **Reanimate** renvoie la carte ciblée depuis son Grave sur le terrain. Ces actions ne contournent pas l’obligation d’invocation correcte des cartes d’Extra Deck ou Ritual. Une capacité qui autorise une Summon normalement illégale doit porter la mention explicite `en ignorant les restrictions de Summon`. Cette permission rend la Summon légale, mais ne constitue pas une invocation correcte pour les déplacements futurs. Lors de la conception ou de la mise à jour d’une telle carte, toujours demander à l’utilisateur s’il faut ajouter cette permission au lieu de la déduire.

### Salvage

**Salvage** renvoie la carte indiquée depuis votre Grave dans votre main. Écrire `**Salvage**` en gras, puis le sélecteur ou `la cible`. Distinct de **Reanimate** (Grave → terrain), **Bounce** (permanent → main), et **Exile from Grave** (activation depuis le Grave + exil de cette carte).

### Reclaim

**Reclaim** renvoie la carte indiquée depuis l’exil dans votre main. Écrire `**Reclaim**` en gras, puis le sélecteur ou `la cible`. Distinct de **Salvage** (Grave → main) et de **Release** (exil → terrain).

### Release

**Release** met la carte indiquée depuis l’exil sur le terrain. Écrire `**Release**` en gras, puis le sélecteur ou `la cible`. Mêmes restrictions d’invocation correcte que **Summon** / **Reanimate** ; ajouter `en ignorant les restrictions de Summon` si nécessaire. Distinct de **Reanimate** (Grave → terrain) et de **Reclaim** (exil → main).

**Hand Summon** signifie : « **Summon** la créature indiquée depuis votre main. » Écrire `**Hand Summon**` puis les filtres. Mêmes restrictions d’invocation correcte que **Summon**.

### Exile from Grave

**Exile from Grave** signifie : « Activez uniquement depuis votre Grave. En tant que coût, exilez cette carte depuis votre Grave. » Remplace la phrase `Depuis votre Grave, exilez cette carte`. Écrire le mot-clé en gras ; conserver après lui tout coût ou choix supplémentaire (défausse, autre carte exilée, ciblage), puis `;` ou `:` avant la résolution.

**Exile N [selector] from Grave** signifie : « En tant que coût, exilez N cartes de votre **Grave** qui correspondent au sélecteur. » Exemple : `**Exile 1 Plant from Grave**`. Distinct de **Exile from Grave**.

### Attach

**Attach** attache la carte indiquée à une Xyz Creature comme matériel.

### Bounded X

Lorsque **Bounded X** devient actif, le contrôleur de la carte, appelée le `bounder`, choisit jusqu’à X autres créatures qu’il contrôle ; elles deviennent bounded. Un permanent bounded bénéficie du bonus ou de l’effet indiqué uniquement tant que son bounder reste sur le terrain. Si le bounder quitte le terrain, tous ses liens et effets Bounded prennent fin immédiatement. Si un permanent bounded quitte le terrain, son contrôleur peut immédiatement en choisir un nouveau dans la limite X.

### Indestructible / Indestructible des Effets

**Indestructible** (evergreen Magic) et **Indestructible des Effets** s’écrivent en gras. **Indestructible des Effets** : la créature ne peut pas être détruite par un sort ou une capacité, mais peut toujours être détruite par les règles du combat ou par une action qui n’est pas un effet.

### Défense talismanique

**Défense talismanique** : cette carte ne peut pas être ciblée par les sorts ou capacités de vos adversaires. Toujours en gras (casing canonique : `talismanique` en minuscules).

### Protection contre tout / Protection contre [qualité]

Formes evergreen Magic en français, toujours en gras. **Protection contre tout** = *protection from everything*.

### Bounce

**Bounce** signifie : « Renvoyez le permanent indiqué dans la main de son propriétaire. »

### Negate

**Negate** exige une cible : un permanent, un sort, ou une capacité sur la pile. Si la cible est un permanent : ce permanent perd toutes ses capacités et toutes ses capacités déjà sur la pile sont contrecarrées. Si la cible est un sort ou une capacité : contrecarrez-le / contrecarrez-la. Toujours en gras.

### Negate & Destroy

**Negate & Destroy** : même résolution que **Negate**, puis détruisez la carte qui a activé l’effet. Zones de destruction légales : terrain, main, Deck, Sideboard. Zones interdites : **Grave**, exil. Cette destruction déclenche **On Destroy** lorsque applicable. Toujours en gras.

### Slow Blink X Any Creature

**Slow Blink X Any Creature** : ciblez jusqu’à X créatures ; exilez-les jusqu’à la prochaine étape de fin, puis renvoyez-les sur le terrain sous le contrôle de leur propriétaire.

### Ritual Summon

**Ritual Summon** met sur le terrain une ou plusieurs `Ritual Creatures` en respectant les matériaux et conditions indiqués. Une carte non-créature qui porte cet effet utilise un super-type comme `Ritual Summon Sorcery`. Une `Ritual Creature` qui n’a pas encore été correctement invoquée ne peut être mise sur le terrain que par cet effet. La MV des matériaux est égale à celle de la créature par défaut ; une carte peut explicitement autoriser une MV supérieure ou égale.

### Fusion Summon

**Fusion Summon** met sur le terrain une `Fusion Creature` depuis le Sideboard — nom de la zone MSE représentant l’Extra Deck — en utilisant les matériaux et zones indiqués. Une carte non-créature qui porte cet effet utilise un super-type comme `Fusion Summon Sorcery`. Une `Fusion Creature` qui n’a pas encore été correctement invoquée ne peut être mise sur le terrain que par cet effet. Les matériaux sont indiqués sur sa première ligne de règle, en italique, **sans** préfixe `Fusion —` (même règle que pour Xyz / Synchro / Link).

### Synchro

Une Synchro Creature est invoquée depuis l'Extra Deck / Sideboard avec une créature Tuner et une ou plusieurs créatures non-Tuner dont la valeur de mana totale correspond à la valeur de mana de la Synchro. Sa première ligne place le Tuner en premier et **omet toujours** le préfixe `Synchro —`, par exemple `1 Tuner + 1+ non-Tuner`.

### Xyz

Une Xyz Creature est invoquée depuis l'Extra Deck / Sideboard avec le nombre de créatures indiqué, de même valeur de mana. Les matériaux sont placés sous la créature Xyz. Sa première ligne indique **uniquement** les matériaux en italique (`2 créatures MV N`, etc.) : **ne jamais** écrire `Xyz —` ni `Xyz -` sur cette ligne — le super-type `Xyz Creature` porte le type d’invocation. Une ligne `Xyz Coût Alternatif —` (coût alternatif, distinct des matériaux) remplace entièrement ces matériaux, utilise la créature indiquée comme matériel et réalise une invocation Xyz correcte.

**Detach X** signifie : envoyez X matériels attachés à cette Xyz Creature dans leur Grave. Sur une carte, remplacer X par le nombre requis (`**Detach 1**`, `**Detach 2**`, etc.). Conserver `**Detach X**` lorsque n’importe quel nombre de matériels peut être détaché. Avant `:` ou `;`, Detach est un coût ; après un événement et un tiret cadratin, il est une action de l’effet déclenché.

### Link

Une Link Creature est invoquée depuis l'Extra Deck / Sideboard avec le nombre ou type de matériaux indiqué. Son niveau Link est indiqué dans son type (`Link Lvl 4 Creature`, par exemple) et ses exigences de matériaux figurent sur la première ligne **sans** répéter `Link —`. La MV peut être exigée explicitement, comme `2 Creatures MV 1` pour Cherubini.

### Ligne de matériaux Sideboard (règle générale)

Pour toute créature Sideboard (`Xyz`, `Synchro`, `Fusion`, `Link`), la ligne de matériaux n’indique **jamais** le type d’invocation : pas de `Xyz —`, `Synchro —`, `Fusion —`, `Link —`. Seuls les matériaux et filtres (MV, Tuner, noms, couleurs) apparaissent en italique.

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

Toutes les illustrations sources sont centralisées sous `original_images/<type_de_carte>/`, avec les mêmes catégories que `original_cards/` (`Effect Monster`, `Normal Monster`, `Ritual`, `Fusion`, `Synchro`, `Xyz`, `Link`, `Spell`, `Trap`). Chaque JPG porte le nom anglais officiel de la carte, rendu compatible avec Windows selon la même convention que le fichier Markdown correspondant (`:` devient ` -`, `"` devient `'`, les slashs deviennent ` - `) ; seule l’extension diffère. Une illustration alternative ajoute ` - variant N` après le nom de la carte.

Chaque projet MSE conserve ses copies importées et redimensionnées dans le projet. Préférer `mse_images/imageN.png` pour les nouveaux imports, mais préserver les chemins racine `imageN.png` ou JPEG existants lorsqu’ils résolvent et passent la sauvegarde/export. Ne jamais pointer directement vers les JPG de `original_images/`. Après toute modification validée, régénérer `render/`, utiliser les noms `name:` exacts et supprimer les rendus obsolètes.

```powershell
python .script/fix_mse_project_images.py --backup "CHEMIN\Projet.mse-set"
```
