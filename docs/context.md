---
date: 2026-07-06
title: Contexte du projet
tags:
  - project
  - context
  - game-design
  - cube
  - yugioh
  - magic-the-gathering
---

# Contexte du projet

## Portée des documents de règles

`docs/context.md` contient uniquement les règles générales de syntaxe, de PSCT, de formatage, de vocabulaire et de structure qui s’appliquent à toutes les cartes du projet. `docs/02_rules_keywords_card_design.md` détaille ces conventions globales lorsqu’elles nécessitent davantage d’exemples.

Chaque archétype possède ses propres règles, mécaniques, exceptions et valeurs carte par carte dans son document numéroté sous `docs/`. Une règle propre à un archétype doit être écrite dans ce document d’archétype, pas dans `docs/context.md`. Une observation ne devient une règle générale que si elle constitue un motif réutilisable à l’échelle du projet.

## Langue de rédaction

Tout le contenu de ce projet doit être rédigé en **français**.

Cela inclut :

- les documents de design ;
- les règles ;
- les descriptions de mécaniques ;
- les notes d'équilibrage ;
- les contraintes de design ;
- les explications de gameplay.

## Exception : noms propres

Les noms d'archétypes et les noms de cartes restent en **anglais**.

Exemples :

- **Burning Abyss** ;
- **Shaddoll** ;
- **Scarm, Burning Abyss** ;
- **El Shaddoll Construct** ;
- **Shaddoll Fusion**.

## Convention de nommage des cartes

Chaque carte dans les documents d'archétype doit afficher le nom original complet de la carte Yu-Gi-Oh, suivi du nom raccourci utilisé dans le cube.

Format obligatoire :

```text
[original name] => [shortened name]
```

Exemple :

```text
Scarm, Malebranche of the Burning Abyss => Burning Abyss - Scarm
```

Le nom raccourci est celui à utiliser sur les cartes MSE si l'espace est limité, mais le document de design doit toujours conserver le nom original complet pour faciliter la traçabilité avec Yu-Gi-Oh.

## Langue des noms et types de cartes

Les **noms de cartes**, **types** et **sous-types** doivent toujours être en **anglais**, même dans les documents français.

Exemples :

- `Creature — Fiend`
- `Tuner Creature — Wizard`
- `Fusion Tuner Creature — Zombie`
- `Instant`
- `Sorcery`
- `Enchantment`
- `Fairy`

`Tuner` est un super-type de carte, pas un sous-type/race/classe et pas une capacité écrite dans le texte de règle. Une carte Tuner doit donc utiliser une ligne de type comme `Tuner Creature — Fiend` ou `Fusion Tuner Creature — Zombie`, et ne doit pas avoir `(1 - Passif) **Tuner**`.

## Convention générale

Rédiger les phrases, titres explicatifs et commentaires en français, mais conserver les noms officiels ou choisis des cartes et archétypes en anglais pour préserver leur identité Yu-Gi-Oh.

Dans les textes de carte, tout nom de carte, nom d'archétype ou fragment de nom de carte cité comme référence mécanique doit être entre guillemets typographiques français `“...”`. Exemple : écrire `les créatures “Lyrilusc” que vous contrôlez`, pas `les créatures “Lyrilusc” que vous contrôlez`. Ne pas mettre entre guillemets les types, sous-types, attributs ou supertypes génériques comme `Fiend`, `Wizard`, `Xyz`, `LIGHT`, `DARK`, `Fusion` ou `Rituel`.

## Mise en forme des capacités et mots-clés

Tous les mots-clés de carte doivent être en **gras** dans les documents et dans les fichiers MSE.

Chaque effet ou capacité d'une carte doit être numéroté avec son type de capacité. Format obligatoire :

```text
(x - Type) Texte de l'effet.
```

Types de capacité :

- **Passif** : effet statique ou mot-clé toujours actif.
- **Déclenchable** : effet déclenché par un événement.
- **Activable** : effet activé ou action que le joueur choisit d'utiliser.
- **Résolution** : effet appliqué quand le rituel ou l'éphémère se résout normalement.

Ne pas utiliser de types de capacité en anglais dans les textes de carte. Écrire `Résolution`, pas `Resolution`.

### Ordre PSCT des effets

Formater les effets selon le **Problem-Solving Card Text (PSCT)** et les rulings officiels Yu-Gi-Oh!, adaptés au français et au vocabulaire de zones du cube. Le PSCT détermine notamment ce qui est une condition, un coût, un ciblage, une action à l’activation ou une action à la résolution ; la reformulation ne doit jamais déplacer un élément d’un de ces rôles vers un autre.

L’ordre canonique d’une capacité est :

```text
(numéro - type timing fréquence) **mot-clé de condition** — procédure d’activation, coûts et cibles ; résolution de l’effet.
```

- Le numéro, le type de capacité, le timing éventuel et la fréquence viennent en premier.
- Lorsqu’un mot-clé exprime la condition ou l’événement déclencheur, il vient immédiatement après le préfixe de capacité, en gras, puis est séparé du PSCT par un tiret cadratin `—` (forme typographique canonique du séparateur `--`).
- Après le tiret, suivre l’ordre PSCT : conditions d’activation déjà non couvertes par le mot-clé, coûts et choix de cibles avant `;`, puis actions réalisées à la résolution après `;`.
- Le choix d’une cible reste une action à l’activation, jamais un coût, même lorsqu’il apparaît avant `;`.
- Utiliser `et` pour les actions simultanées, `puis` lorsque l’ordre ou la réussite de la première action conditionne la suivante, et `si vous faites ainsi` lorsqu’une action ultérieure dépend explicitement de la précédente.
- Conserver explicitement l’optionalité avec `vous pouvez` et distinguer `ciblez` de `choisissez` conformément au ruling Yu-Gi-Oh! d’origine.

Exemple :

```text
(2 - Déclenchable Hard) **On Send GYD** — Défaussez 1 carte et ciblez 1 créature contrôlée par un adversaire ; exilez-la.
```

Les coûts, coûts alternatifs, coûts supplémentaires et conditions de lancement ne sont pas des effets : ils ne doivent pas recevoir leur propre numéro de capacité. Tous les types de coûts et conditions de lancement doivent être listés avant les capacités numérotées et avant les mots-clés evergreen.

- Les coûts supplémentaires d'un effet sont intégrés à la capacité qu'ils modifient, avant `;` ou `:` selon le templating.
- Les coûts alternatifs de lancement sont écrits sur une ligne non numérotée avec le label français `Coût Alternatif -`.
- Les coûts alternatifs de lancement Xyz utilisent le label français spécifique `Xyz Coût Alternatif —`. Cette ligne remplace entièrement les matériaux normaux, utilise la créature indiquée comme matériel et réalise une invocation Xyz correcte. Le coût et le matériel peuvent être intégrés dans une même proposition avec `et utilisez`, par exemple `W, défaussez 1 créature “Burning Abyss” et utilisez 1 “Dante” que vous contrôlez.` Finir par `Ses matériels se transfèrent.` si les matériels de la créature utilisée doivent être conservés.

Exemples :

- Pour une carte Trap, écrire le super-type sur la ligne de type (`Trap Instant`, `Trap Sorcery`, `Trap Enchantment`, etc.), puis commencer directement son texte par ses coûts, conditions ou capacités numérotées. Ne pas ajouter de ligne de mot-clé `**Piège**`.
- Écrire `Xyz Coût Alternatif — W, défaussez 1 créature “Burning Abyss” et utilisez 1 “Dante” que vous contrôlez. Ses matériels se transfèrent.`
- Pour les effets Ritual, utiliser le super-type `Ritual Summon` et écrire **Ritual Summon** en gras dans le texte de règle.
- Pour les effets Fusion, utiliser le super-type `Fusion Summon` et écrire **Fusion Summon** en gras dans le texte de règle.
- Ne pas écrire `**Piège**` ni `(1 - Passif) **Piège**` : `Trap` est un super-type, pas un mot-clé ni une capacité.
- Ne pas écrire `(2 - Trap Supplemental Cost) ...`.
- Ne pas écrire `(1 - Alternative Cost) ...`.

Pour les capacités **Activable**, ajouter normalement le timing d'activation juste après `Activable`. Le timing peut être omis lorsqu’il est déjà fixé par un mot-clé défini ou par une action composée dont la règle fournit ce timing :

- **Ritual** : capacité utilisable uniquement à vitesse rituel / sorcery speed.
- **Flash** : capacité utilisable à tout moment où vous pourriez lancer un éphémère / instant speed.

Exemples :

```text
(1 - Activable Sorcery Soft) ...
(1 - Activable Flash Hard) ...
```

Pour les capacités **Activable**, ajouter si nécessaire une fréquence d'activation après le type/timing.

Les capacités **Déclenchable** n’emploient normalement pas de fréquence. Une capacité explicitement notée **Déclenchable Soft** ne peut toutefois se déclencher qu’une fois par tour pour cet objet ; une nouvelle instance de la carte constitue un nouvel objet.

Pour les capacités **Déclenchable** et **Activable**, ajouter si nécessaire une fréquence d'activation après le type/timing :

- **Soft** : « Vous ne pouvez utiliser cette capacité qu'une fois par tour. » Cette limite n'est pas liée au nom de la carte. Si la carte quitte le terrain et revient, elle peut utiliser l'effet à nouveau.
- **Hard** : « Vous ne pouvez activer l'effet de X qu'une seule fois par tour. » Cette limite est liée au nom de la carte. Les autres copies ne peuvent pas activer la même capacité ce tour-ci.
- **Hard Linked** : « Vous ne pouvez utiliser qu’un seul des Y effets de X qu’une seule fois par tour. » Cette limite est liée au nom de la carte et verrouille aussi les autres effets **Hard Linked** de cette carte.

Exemple :

```text
(1 - Passif) **Malédiction abyssale**
(2 - Activable Hard Linked) **Descente**
(3 - Déclenchable Hard Linked) **On Send GYD** — À la prochaine étape de fin, cherchez une créature “Burning Abyss”.
```

Ne pas regrouper plusieurs mots-clés sur une seule ligne si ce regroupement empêche de numéroter ou typer chaque capacité.

Les mots-clés evergreen Magic comme `Piétinement`, `Vol`, `Vigilance`, `Lien de vie`, `Menace`, etc. ne doivent pas être écrits comme des capacités passives numérotées. Les écrire seuls sur leur propre ligne, sans `(x - Passif)`. Ils doivent venir après les lignes de coût / coût alternatif / condition de lancement, mais avant les capacités numérotées.

### Compacité du texte de carte

Dans les textes de carte, écrire les quantités avec des chiffres arabes plutôt qu'en toutes lettres pour gagner de la place et rester cohérent avec le templating Yu-Gi-Oh / Magic du cube.

Exemples :

- Écrire `Choisissez 1 autre créature`, pas `Choisissez une autre créature`.
- Écrire `piochez 2 cartes`, pas `piochez deux cartes`.
- Écrire `envoyez 1 carte`, pas `envoyez une carte`.

Exception pour une cible déjà désignée : lorsqu'un effet commencerait par `1 créature ciblée`, remplacer cette formulation par `La créature ciblée`. Cette règle s'applique au début du texte de l'effet, immédiatement après son préfixe numéroté et son type. Elle ne s'applique pas lorsqu'une action introduit ensuite la cible, par exemple `Détruisez 1 créature ciblée`.

Exemple :

- Écrire `(2 - Activable Hard) La créature ciblée gagne +1/+1 jusqu'à la fin du tour.`
- Ne pas écrire `(2 - Activable Hard) 1 créature ciblée gagne +1/+1 jusqu'à la fin du tour.`

Garder les nombres en toutes lettres seulement dans les titres, commentaires de design, ou formulations où le nombre n'est pas une quantité de règle.

Toujours utiliser les raccourcis suivants dans les textes de carte :

- `MV` pour `Mana Value` / `valeur de mana`.
- `Deck` pour `bibliothèque` / `library`.

Exemples :

- Écrire `1 créature MV 1`, pas `1 créature avec une valeur de mana de 1`.
- Écrire `depuis votre Deck`, pas `depuis votre bibliothèque`.
- Écrire `du Deck au GYD`, pas `depuis votre bibliothèque dans votre cimetière`.

Toujours utiliser `GYD` pour `cimetière` dans les textes de carte. `GYD` désigne la même zone que l’ancien raccourci `GY`, désormais conservé uniquement comme notation historique. Garder `cimetière` seulement dans les explications de règles, commentaires de design ou documentation hors texte de carte.

Pour donner indestructible, écrire `gagne indestructible`, pas `a indestructible`.

Dans les textes d'effets, écrire `Si` au lieu de `Quand` pour les déclencheurs et conditions d'événement.

Exemples :

- Écrire **On Enter** — ..., pas `Si cette créature arrive`.
- Écrire `Si cette carte est détruite, ...`, pas `Quand cette carte est détruite, ...`.

## Mots-clés d'événement

**On Enter** signifie : « Lorsque cette carte arrive sur le champ de bataille. » Dans l'implémentation, ce déclencheur est `onEnterField`.

**On Attack** signifie : « Lorsque cette créature attaque. »

**On Block** signifie : « Lorsque cette créature bloque. »

**On Blocked** signifie : « Lorsque cette créature devient bloquée par une ou plusieurs créatures. »

**On Attack / Block** signifie : « Lorsque cette créature attaque ou bloque. » Utiliser une barre oblique lorsque plusieurs mots-clés d'événement s'appliquent au même effet.

**On Link Summon** fonctionne comme **On Enter**, mais uniquement lorsqu’une `Link Creature` arrive sur le champ de bataille via sa propre invocation Link. Une `Link Creature` mise directement sur le champ de bataille par un autre effet ne déclenche pas **On Link Summon**.

**On Opponent Creature Enter** signifie : « À chaque fois qu'une créature arrive sur le terrain sous le contrôle d'un adversaire. » Lorsqu'il est placé après une instruction, cette instruction est répétée à chaque occurrence de cet événement pendant la durée indiquée.

**On Cast** signifie : « À chaque fois qu'un sort est lancé, avant sa résolution. » Cette famille de mots-clés se compose d'un périmètre, puis de paramètres optionnels, suivis de `:` et de l'effet :

- **On Your Cast** compte uniquement les sorts lancés par vous ;
- **On Opponent's Cast** compte uniquement les sorts lancés par un adversaire ;
- **On Any Cast** compte les sorts lancés par n'importe quel joueur.

Après le périmètre, ajouter si nécessaire les paramètres qui définissent les sorts concernés, par exemple `“Nekroz” Ritual` pour un sort Rituel dont le nom contient “Nekroz”. Le format est donc **On Your Cast [paramètres]** : effet.

**On Opponent Summon** signifie : « Lorsqu’un adversaire Summon une créature. » Ce déclencheur répond uniquement à l’action **Summon**, pas au lancement normal d’une créature ; utiliser **On Opponent's Cast** ou une formulation explicite pour les événements de lancement.

**On Send GYD** signifie : « Lorsque cette carte est mise dans un GYD depuis n’importe quelle zone. » Utiliser ce mot-clé pour toute capacité de cette carte qui se déclenche lorsqu’elle est envoyée au GYD.

**On Send GYD by Effect** signifie : « Lorsque cette carte est mise dans un GYD par un effet de carte. » Contrairement à **On Send GYD**, il ne se déclenche pas lorsque la carte est mise au GYD par un coût, une règle ou une action qui n’est pas un effet.

**On Creature you Control Destroy** signifie : « Lorsqu’une créature que vous contrôlez est détruite. » Sauf restriction écrite sur la carte, l’événement compte quelle que soit la cause de la destruction.

**On Destroy** signifie : « Lorsque cette carte est détruite et envoyée au cimetière. »

**On Exile** signifie : « Lorsque cette carte est exilée. » Utiliser ce mot-clé pour toute capacité de cette carte qui se déclenche lorsqu’elle est exilée, quelle que soit la zone depuis laquelle elle est exilée.

**On Sacrifice** signifie : « Lorsque cette carte est sacrifiée ou utilisée comme matériel pour lancer une créature Ritual. » Utiliser ce mot-clé pour remplacer les formulations comme `Si cette carte est utilisée comme matériel Ritual`.

**Detach X** signifie : « Détachez X matériels de cette Xyz Creature et envoyez-les au GYD. » `X` représente le nombre de matériels à détacher. Sur une carte, remplacer X par la valeur requise (`**Detach 1**`, `**Detach 2**`, etc.). Si n’importe quel nombre peut être détaché, conserver `**Detach X**`. Detach est un coût lorsqu’il précède `:` ou `;`. Placé après un événement avec un tiret cadratin, comme `**On Attack / Block** — **Detach 1**`, il est une action obligatoire de l’effet déclenché.

**Mill X** signifie : « Envoyez les X cartes du dessus de votre Deck dans votre GYD. » Sur une carte, remplacer X par la valeur requise : `**Mill 1**`, `**Mill 2**` ou `**Mill 3**`. Si le joueur choisit librement entre ces trois valeurs, écrire `**Mill up to 3**`.

**Summon** signifie : « Mettez la carte indiquée sur le terrain depuis la zone précisée, sans la lancer et sans payer son coût de mana. » Une Summon ne constitue pas à elle seule une invocation correcte d’une carte d’Extra Deck ou Ritual. Tout effet autorisé à effectuer une Summon normalement illégale doit écrire explicitement `en ignorant les restrictions de Summon`. Cette permission rend uniquement la Summon légale : elle ne constitue pas une invocation correcte pour les déplacements futurs.

Lors de l’ajout ou de la mise à jour d’une carte, si un effet effectuerait une Summon illégale — notamment depuis le Sideboard sans la méthode d’invocation requise — demander obligatoirement à l’utilisateur s’il faut ajouter `en ignorant les restrictions de Summon` à l’effet. Ne jamais déduire cette permission silencieusement.

**Reanimate** signifie : « Renvoyez la carte ciblée depuis son GYD sur le terrain. » Cette action ne contourne pas l’obligation d’invocation correcte des cartes d’Extra Deck ou Ritual.

**Attach** signifie : « Attachez la carte indiquée à la Xyz Creature indiquée comme matériel. »

**Bounded X** lie jusqu’à X autres créatures que vous contrôlez à la carte qui porte la capacité, appelée le `bounder`. Lorsque Bounded X devient actif, le contrôleur du bounder choisit jusqu’à X autres créatures qu’il contrôle ; elles deviennent `bounded`. Un permanent bounded bénéficie du bonus ou de l’effet indiqué uniquement tant que son bounder reste sur le terrain. Si le bounder quitte le terrain, tous ses liens et effets Bounded prennent fin immédiatement. Si un permanent bounded quitte le terrain, le contrôleur peut immédiatement en choisir un nouveau dans la limite X.

**Indestructible contre les effets** signifie que la créature ne peut pas être détruite par un sort ou une capacité, mais peut toujours être détruite par les règles du combat ou par une action qui n’est pas un effet.

**Défense talismanique** signifie : « Cette carte ne peut pas être ciblée par les sorts ou capacités de vos adversaires. »

**Slow Blink X Any Creature** signifie : « Ciblez jusqu’à X créatures ; exilez-les jusqu’à la prochaine étape de fin, puis renvoyez-les sur le terrain sous le contrôle de leur propriétaire. »

**Ritual Summon** met sur le terrain une ou plusieurs `Ritual Creatures` en respectant les matériaux et conditions indiqués. Une carte non-créature qui porte cet effet utilise un super-type comme `Ritual Summon Sorcery`. Une `Ritual Creature` qui n’a pas encore été correctement invoquée ne peut être mise sur le terrain que par cet effet.

**Fusion Summon** met sur le terrain une `Fusion Creature` depuis le Sideboard en utilisant les matériaux et zones indiqués. Une carte non-créature qui porte cet effet utilise un super-type comme `Fusion Summon Sorcery`. Une `Fusion Creature` qui n’a pas encore été correctement invoquée ne peut être mise sur le terrain que par cet effet.

Le nom ou l’archétype placé après **Ritual Summon** ou **Fusion Summon** filtre les créatures compatibles sans qu’il soit nécessaire de répéter `Ritual Creature`, `Fusion Creature` ou `Sideboard` dans le texte de la carte.

Pour tout effet déclenché par l'arrivée de la carte sur le champ de bataille, utiliser **On Enter**, ou **On Link Summon** si l'effet exige spécifiquement une invocation Link. Pour tout effet déclenché par une attaque, un blocage effectué ou le fait de devenir bloqué, utiliser respectivement **On Attack**, **On Block** ou **On Blocked**. Utiliser **On Attack / Block** si les deux premiers événements déclenchent le même effet. Ne pas reformuler ces événements avec `Si ... arrive`, `Si ... attaque` ou `Si ... bloque`.

Un mot-clé d’événement qui introduit une capacité doit être écrit en gras et suivi d’un tiret cadratin : `**On Enter** — ...`, `**On Exile** — ...`, etc. Un mot-clé placé après une instruction répétée, comme `Piochez 1 carte **On Opponent Creature Enter**`, ne prend pas de tiret cadratin.

Utiliser les mots-clés d'événement pour raccourcir les effets déclenchés.

## Super-type Trap

`Trap` est un super-type anglais réservé aux cartes non-créature. Il précède le type Magic sur la ligne de type : `Trap Instant`, `Trap Sorcery`, `Trap Enchantment`, etc. `Trap` n’est pas un mot-clé, une capacité ou un sous-type : ne pas écrire `**Piège**` dans le texte de règle ni `Instant — Piège` sur la ligne de type.

Une carte Trap ne peut pas être lancée depuis la main. Depuis sa main, son propriétaire peut la **Set** face cachée sur le terrain. Set est une action spéciale qui n’utilise pas la pile, ne lance pas la carte, ne demande pas de payer son coût de lancement et ne déclenche pas **On Cast**. Un effet qui met une carte Trap face cachée sur le terrain la Set et satisfait ce prérequis ; activer ensuite cette carte revient à la lancer. Une permission explicite peut autoriser cette activation pendant le tour où elle a été Set.

Tant qu’elle est face cachée, la carte est traitée comme un permanent non-créature non-terrain sans nom, couleur, coût de mana, MV, type, sous-type, super-type, capacité, force ni endurance. Elle reste sur le terrain comme un permanent sans effet ; elle n’est pas un `Enchantment`.

À partir du tour suivant celui où elle a été Set, son contrôleur peut la retourner face visible et la lancer depuis le terrain à tout moment où il pourrait lancer un `Instant`. Il paie alors normalement son coût de mana et ses coûts supplémentaires. La carte quitte le terrain pour la pile : ce lancement utilise la pile et compte comme un sort lancé depuis le terrain. Lorsqu’un effet précise qu’une Trap peut être lancée ou activée pendant le tour où elle a été Set, cette permission contourne explicitement et uniquement la règle qui impose d’attendre le tour suivant ; toutes les autres règles de lancement des Trap restent applicables.

Après sa résolution, une `Trap Instant` ou `Trap Sorcery` est mise au GYD normalement. Une Trap d’un type de permanent se résout et arrive face visible sur le terrain selon les règles normales de ce type. Une Trap lancée depuis une autre zone par une permission explicite suit cette permission et n’est pas considérée comme lancée depuis le terrain.

## Raccourci de recherche

Pour alléger les textes de cartes, tout effet qui cherche une carte dans la bibliothèque pour la révéler, la mettre en main, puis mélanger doit être écrit sous la forme courte : **« cherchez X »**.

Exemple :

- Ne pas écrire : « cherchez une créature “Burning Abyss” dans votre bibliothèque, révélez-la, mettez-la dans votre main, puis mélangez. »
- Écrire : « cherchez une créature “Burning Abyss”. »

Cette convention implique par défaut la recherche dans la bibliothèque, la révélation si nécessaire, la mise dans la main, puis le mélange.

## Magic Set Editor

L'édition et le rendu final des cartes se font avec **Magic Set Editor (MSE)**.

- Configuration locale obligatoire : lancer `python setup_mse.py` après chaque clone pour générer le fichier `.env` ignoré par Git.
- Installation MSE : chemin `MSE_ROOT` du fichier `.env`.
- Contexte technique MSE à lire avant toute génération ou modification : `CONTEXT.md` sous `MSE_ROOT`, s'il existe.
- Dossier des projets MSE du cube : chemin `MSE_PROJECTS_DIR` du fichier `.env`.

Les projets MSE doivent être sauvegardés dans le projet du vault au format dossier `.mse-set` contenant un fichier `set`, plutôt qu'en archive `.mse-set` zippée. Chaque archétype ou groupe de cartes non-archétypales doit avoir son propre projet MSE pour faciliter l'édition et le rendu séparé. L'installation MSE reste seulement l'outil d'ouverture/rendu, pas l'emplacement de sauvegarde canonique des cartes du cube.

### Convention de titre des sauvegardes MSE

Tout fichier de sauvegarde MSE qui correspond à un document du projet doit utiliser cette convention dans `set_info.title` :

```text
YGO x MTG -- [name]
```

Exemples :

- `YGO x MTG -- Burning Abyss`
- `YGO x MTG -- Shaddoll`
- `YGO x MTG -- Staples Synchro`

Ne pas utiliser les anciens préfixes `Yu-Gi-Oh × Magic Cube —` ou `Yugioh X Magic Cube --` dans les titres MSE.

### Diagnostic des erreurs MSE / corruption apparente

Si MSE signale une corruption, refuse de sauvegarder, ou si `mse.com --export-images` retourne `3221225477` / `0xC0000005`, ne pas conclure immédiatement qu'une carte est corrompue.

Procédure obligatoire :

1. Créer un projet de test `.mse-set` autonome avec une seule carte :
   - un fichier `set` minimal ;
   - un seul `include_file: card ...` ;
   - le fichier `card ...` correspondant ;
   - les images référencées copiées localement dans `images/...`.
2. Placer ces projets de diagnostic dans un dossier séparé/sibling, pas au milieu du projet MSE de production, sauf test explicitement temporaire. Éviter les dossiers `.mse-set` imbriqués dans un autre `.mse-set` de production.
3. Vérifier avec une commande directe, une carte à la fois :

```powershell
<MSE_CLI depuis .env> --export-images "CHEMIN\Carte_Test.mse-set" "CHEMIN\Carte_Test.mse-set\out_direct.png"
```

4. Si la commande retourne une erreur mais crée quand même le PNG, relancer le même test directement depuis le shell avant de déclarer la carte corrompue. Des exécutions automatisées rapides via Python `subprocess` ont produit de faux `0xC0000005` sur toutes les cartes alors que les exports directs passaient.
5. Pour isoler une vraie corruption, retirer/changer un champ à la fois dans le projet mono-carte : `image`, `rule_text`, `name`, `casting_cost`, `super_type`, `sub_type`, puis les réglages du `set`. Réintroduire ensuite les champs un par un pour identifier le champ fautif.

Résultat connu du 2026-07-11 : les 21 cartes **Burning Abyss** ont été reconstruites en projets mono-carte sous `10_YGO_Burning_Abyss.mse-set/SingleCardProjectsClean/`. Les exports directs ont tous retourné `0` et produit `out_direct.png`. Aucun champ de carte spécifique, y compris Alich, n'a été identifié comme corrompu. Le bug observé était une corruption apparente/faux crash de diagnostic, probablement liée à la manière d'invoquer MSE en batch, pas aux données des cartes.

### Ordre et numérotation des cartes MSE

Après chaque ajout, suppression ou régénération de cartes dans un projet `.mse-set`, trier les `include_file:` par ordre alphabétique du champ `name:` visible de la carte, puis mettre à jour les numéros de collection dans les fichiers de sauvegarde.

- Format obligatoire : `001/NNN R`, `002/NNN R`, etc.
- Mettre à jour tous les champs présents : `card_code_text`, `card_code_text_2`, `card_code_text_3`.
- Conserver le suffixe de rareté existant (`C`, `U`, `R`, etc.).
- Le total `NNN` doit correspondre au nombre de cartes actuellement incluses dans le projet concerné.

### Vérification obligatoire après création ou modification MSE

Après chaque création ou modification d'un projet `.mse-set`, vérifier que le fichier n'est pas corrompu avant de considérer la tâche terminée.

1. Lancer au minimum un export CLI :

```powershell
<MSE_CLI depuis .env> --export-images "CHEMIN\Projet.mse-set" "CHEMIN\Projet.mse-set\verify_export\card.png"
```

2. Ne pas considérer l'export comme suffisant : un projet peut s'exporter correctement mais échouer au moment de sauvegarder dans l'interface MSE avec `Referencing an inexistant file!`.
3. Quand le projet a été créé ou restructuré, ouvrir le projet dans MSE avec cette forme exacte de commande, puis faire un vrai test de **Save** ou **Save As** :

```powershell
<MSE_EXECUTABLE depuis .env> "CHEMIN/Projet.mse-set"
```

4. Si la sauvegarde échoue, chercher en priorité :
   - des `include_file:` qui pointent vers un fichier absent ;
   - des champs `image`, `image_2`, `mainframe_image`, `mainframe_image_2`, `symbol`, `masterpiece_symbol` non vides dont le fichier n'existe pas ;
   - des fichiers de backup obsolètes comme `set.include_backup` contenant d'anciennes références ;
   - des dossiers `.mse-set` imbriqués dans le projet actif ;
   - des dossiers d'export/test générés à l'intérieur du projet actif.
5. Garder une copie de sauvegarde du projet avant toute correction destructive.

Convention d'images MSE du cube :

- `assets/original_images/<archetype_ygo>/` contient toutes les illustrations sources haute résolution téléchargées depuis YGOPRODeck (`image_url_cropped`). Le classement suit l'archétype réel indiqué par les données Yu-Gi-Oh!, jamais le document ou le projet MSE du cube. Une carte sans archétype Yu-Gi-Oh! va dans `assets/original_images/non_archetype/`.
- Aucun projet `.mse-set` ne doit contenir de dossier source `original_images/` ou `images/`. Ces sources centralisées servent à recadrer ou régénérer les images MSE.
- `mse_images/` reste propre à chaque projet `.mse-set` et contient de préférence les nouveaux imports adaptés : PNG recadrés/redimensionnés, typiquement `316x231`, nommés `imageN.png` ou avec un slug stable. Les chemins racine `imageN.png` et les JPEG nommés existants restent valides lorsqu’ils résolvent dans le projet et passent la sauvegarde/export.
- `render/` contient les images finales rendues/exportées par MSE pour un projet `.mse-set` ; c'est le dossier de sortie canonique des rendus de cartes.
- Après toute modification validée d’une carte MSE, régénérer `render/` depuis le projet final. Chaque image doit être renommée avec le nom exact défini dans `name:`, par exemple `Burning Abyss - Dante.png`, et non rester au format générique `card.png`, `card.1.png`, etc. Supprimer les anciens rendus dont le nom ne correspond plus.
- Toute référence `image:` non vide doit résoudre dans le projet. Préférer `mse_images/imageN.png` pour les nouveaux imports ; préserver les chemins racine ou JPEG existants lorsqu’ils se sauvegardent et s’exportent correctement. Ne jamais pointer directement vers `assets/original_images/...`.

Cas identifié le 2026-07-11 sur **Burning Abyss** : une sauvegarde peut échouer tant que des cartes incluses pointent directement vers les images sources `.jpg`. Après redimensionnement/import dans MSE, la sauvegarde réussie produit un fichier d'environ `316x231`, sans métadonnées EXIF, et met à jour la carte. Pour prévenir ce bug, conserver les sources dans `assets/original_images/`, puis utiliser une copie importée/redimensionnée propre au projet ; `mse_images/` reste l’emplacement préféré pour les nouveaux imports.

Pour générer ce format sans passer par l'interface MSE, utiliser le helper :

```powershell
python .script/generate_mse_imported_image.py "CHEMIN\Projet.mse-set" "assets/original_images/<archetype_ygo>/source.jpg" --card-file "card fichier a mettre a jour"
```

Le script crée le prochain `mse_images/imageN.png` disponible dans le projet et, si `--card-file` est fourni, remplace le champ `image:` de la carte par ce nouveau chemin.

Pour corriger un projet entier déjà généré avec des références `images/.../*.jpg`, utiliser :

```powershell
python .script/fix_mse_project_images.py --backup "CHEMIN\Projet.mse-set"
```

Ce script sauvegarde le projet, génère des `mse_images/imageN.png` pour toutes les cartes incluses, met à jour les champs d'image, trie les `include_file:` par nom de carte et renumérote les `card_code_text`.

## Conventions de rédaction des types, recherches et zones

- Toujours écrire `Ritual Creature`, jamais `créature Ritual` ni `Ritual créature`. Au pluriel, écrire `Ritual Creatures`.
- Pour une recherche, écrire le type avant le nom d’archétype : `Cherchez 1 Ritual Creature “Nekroz”.` Pour une carte d’invocation non-créature, écrire `Cherchez 1 carte non-créature Ritual Summon “Nekroz”.` Si une race est requise, la placer avant le type : `Dragon Ritual Creature`.
- Pour un coût de Ritual Summon fondé sur la valeur de mana, comparer explicitement les valeurs. La valeur par défaut est l’égalité ; une carte peut indiquer `supérieure ou égale` pour autoriser le surpaiement, comme Good & Evil.
- Si plusieurs Ritual Creatures peuvent être mises en jeu, accorder au pluriel : `leur(s) coût(s) Ritual`.
- Ne jamais énumérer les zones avec plusieurs possessifs. Écrire `depuis votre main ou terrain`, jamais `depuis votre main ou terrain`, `depuis votre main ou terrain` ni `depuis votre main ou terrain`.
- Lorsqu’un effet ne cible pas au sens des règles, l’indiquer explicitement avec `Cet effet ne cible pas.`
- Plusieurs actions à mot-clé appartenant à une même capacité sont écrites dans un même groupe en gras et reliées par `et`, par exemple `**Detach 1 et Mill 3**`.
- Le choix d’une cible n’est jamais un coût, même lorsque `ciblez ...` est placé dans le groupe d’instructions qui précède `;` ou `:`.
- Un effet activé depuis le GYD peut commencer par `Depuis votre GYD, exilez cette carte ; ...` ou intégrer l’exil et le ciblage avant `;` lorsque la carte emploie ce templating.
- Pour désigner la carte elle-même, utiliser son nom si celui-ci est aussi court ou plus court que `cette carte` ; sinon, utiliser `cette carte`.
- Pour déplacer une carte depuis le Deck, réserver `Cherchez` aux cartes mises en main. Utiliser `Envoyez ... depuis votre Deck au GYD` et `Mettez en jeu ... depuis votre Deck` pour les autres destinations.
- Toujours écrire les zones, types et mécaniques avec leur casse et leur orthographe validées : `Deck`, `GYD`, `Sideboard`, `Ritual Creature`, `Fusion Creature` et `Trap`.
- Dans les cartes du cube, `Sideboard` est le nom de la zone MSE qui représente l’Extra Deck. Les règles générales peuvent parler d’Extra Deck ; le texte compact des cartes emploie Sideboard.
- La ligne de matériaux d’une Fusion Creature utilise `*[matériaux]*` ; le super-type `Fusion Creature` porte déjà l’information Fusion.
- La ligne de matériaux d’une Synchro Creature place toujours le Tuner en premier : `*1 Tuner + 1+ non-Tuner*` ; le préfixe `Synchro —` est omis.
- Une protection par remplacement de destruction utilise `Si cette carte devait être détruite, vous pouvez sacrifier ... à la place.`
- Une perte de capacités accompagnée d’un changement de statistiques utilise l’ordre `La créature ciblée perd toutes ses capacités et devient 0/0 jusqu’à la fin du tour.`
- Lorsqu’une ligne de matériaux demande des créatures `différentes`, leurs noms doivent être différents.
- Une perte de capacités précisée `sur le terrain` cesse dès que la carte quitte le terrain et ne s’applique pas dans les autres zones.

## Convention Extra Deck / types MSE

Pour les créatures d'Extra Deck, le type spécial doit être placé dans le `super_type`, avant `Creature`, et non dans le sous-type/race :

- `Xyz Creature` pour les créatures Xyz ;

### Ligne de matériaux Xyz

La première ligne de texte d'une `Xyz Creature` doit indiquer ses matériaux en italique, sans répéter le préfixe `Xyz —`. Par défaut, utiliser :

```text
2 créatures MV N
```

où `N` est la valeur de mana de la carte Xyz elle-même. Exemple : une Xyz coûtant `{2}{U}` utilise `2 créatures MV 3`. Les exceptions existent seulement si le design de la carte exige explicitement `2+ créatures` ou un matériel nommé, mais la baseline du projet est `2 créatures MV N`.
- `Synchro Creature` pour les créatures Synchro ;
- `Fusion Creature` pour les créatures Fusion ;
- `Link Creature` pour les créatures Link.

Pour toute carte non-créature qui effectue explicitement une invocation spéciale, placer la mécanique avant son type Magic dans le super-type :

- `Ritual Summon Sorcery`, `Ritual Summon Instant`, etc. pour une carte qui porte **Ritual Summon** ;
- `Fusion Summon Sorcery`, `Fusion Summon Instant`, etc. pour une carte qui porte **Fusion Summon** ;
- ne pas répéter cette mécanique dans le sous-type.

Dans les documents de cartes, utiliser la même forme sur la ligne de type, par exemple `Xyz Creature — Humain`. Pour une carte Trap, placer `Trap` au début du super-type, par exemple `Trap Instant` ; ne pas conserver le sous-type français `Piège`.

### Styles MSE validés

Les choix de frames/styles validés doivent être conservés dans les projets MSE et les scripts générateurs. Les frames sont définies par **super-type de carte**, jamais par archétype.

Un projet d'archétype (`10_YGO_Burning_Abyss`, `12_YGO_Necroz`, `11_YGO_Shaddoll`, etc.) peut donc contenir des cartes individuelles `Fusion`, `Synchro`, `Xyz`, `Link` ou `Ritual`. Ces cartes doivent utiliser la frame de leur super-type individuel, pas une frame globale propre à l'archétype.

Dans les fichiers MSE, une frame spécifique à une carte se déclare directement dans le fichier `card ...`, juste après `card:` :

```text
card:
	stylesheet: m15-spellbook
	stylesheet_version: 2024-09-01
	has_styling: false
```

Ne pas créer un projet `.mse-set` séparé uniquement pour changer la frame d'une carte : utiliser les champs `stylesheet` / `stylesheet_version` au niveau de la carte.

- **Xyz** : `m15-spellbook` (`magic-m15-spellbook.mse-style`) — frame M15 Spellbook validée.
- **Fusion Creature** : `genevensis-00-main` (`magic-genevensis-00-main.mse-style`) — frame `gen main` hi-res validée.
- **Synchro Creature** : `m15-sketch` (`magic-m15-sketch.mse-style`) — style Sketch validé.
- **Link Creature** : `m15-showcase-capenna-art-deco` (`magic-m15-showcase-capenna-art-deco.mse-style`) — Art Deco / Capenna Showcase validé.
- **Ritual Creature** : `m15-showcase-praetor` (`magic-m15-showcase-praetor.mse-style`) — frame Praetor / Phyrexian Showcase validée.
- **Normal, autres cartes et non-créatures Fusion Summon/Ritual Summon** : `sevenhalf` (`magic-sevenhalf.mse-style`) — frame 7.5th Edition validée.

Les frames Fusion et Ritual ne s'appliquent qu'aux **créatures**. Une carte non-créature `Fusion Summon` ou `Ritual Summon` garde la frame par défaut `sevenhalf`.

Voir aussi `frame_candidates.md` pour la liste des candidats et validations visuelles.

La première ligne du texte de règle d'une créature d'Extra Deck doit être la condition d'invocation en italique, sans répéter son super-type :

- `*2 créatures MV N*` pour une Xyz Creature ;
- `*1 Tuner + 1+ non-Tuner*` pour une Synchro Creature ;
- `*1 créature “Shaddoll” + 1 créature blanche*` pour une Fusion Creature ;
- `*2+ Creatures*` pour une Link Creature.

Pour une `Link Creature`, le niveau Link reste porté par le type de carte (`Link Lvl 4 Creature`, par exemple), tandis que la première ligne indique seulement le nombre ou les propriétés des matériaux requis. La MV ou le niveau des matériaux n'a pas d'importance sauf mention explicite sur la carte, comme `2 Creatures MV 1` pour Cherubini.
