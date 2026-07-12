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

Les coûts, coûts alternatifs, coûts supplémentaires et conditions de lancement ne sont pas des effets : ils ne doivent pas recevoir leur propre numéro de capacité. Tous les types de coûts et conditions de lancement doivent être listés avant les capacités numérotées et avant les mots-clés evergreen.

- Les coûts supplémentaires d'un effet sont intégrés à la capacité qu'ils modifient, avant `;` ou `:` selon le templating.
- Les coûts alternatifs de lancement sont écrits sur une ligne non numérotée avec le label français `Coût Alternatif -`.
- Les coûts alternatifs de lancement Xyz utilisent le label français spécifique `Xyz Coût Alternatif —`. Ne pas écrire `Lancez en Xyz depuis votre sideboard en utilisant` : après les deux-points, indiquer seulement le matériel requis, par exemple `1 “Dante” que vous contrôlez`. Finir par `Ses matériels se transfèrent.` si les matériels de la créature utilisée doivent être conservés.

Exemples :

- Écrire `**Piège**` sur une ligne non numérotée, puis `(1 - Résolution) Sacrifiez 2 créatures “Burning Abyss” ; détruisez jusqu’à 3 permanents non-terrain ciblés.`
- Écrire `**Piège**` sur une ligne non numérotée, puis `(1 - Résolution) Renvoyez sur le terrain n’importe quel nombre de créatures “Burning Abyss” envoyées à votre GY ce tour-ci.`
- Écrire `Xyz Coût Alternatif — W, défaussez 1 créature “Burning Abyss” : 1 “Dante” que vous contrôlez. Ses matériels se transfèrent.`
- Pour les effets Ritual, utiliser le sous-type `Invocation Ritual`, mais ne jamais répéter **Invocation Ritual** en gras dans le texte de règle.
- Pour les effets Fusion, utiliser le sous-type `Invocation Fusion`, mais ne jamais répéter **Invocation Fusion** en gras dans le texte de règle.
- Ne pas écrire `(1 - Passif) **Piège**` : `Piège` est une condition/mot-clé de lancement, pas une capacité numérotée.
- Ne pas écrire `(2 - Trap Supplemental Cost) ...`.
- Ne pas écrire `(1 - Alternative Cost) ...`.

Pour les capacités **Activable**, ajouter le timing d'activation juste après `Activable` :

- **Ritual** : capacité utilisable uniquement à vitesse rituel / sorcery speed.
- **Flash** : capacité utilisable à tout moment où vous pourriez lancer un éphémère / instant speed.

Exemples :

```text
(1 - Activable Sorcery Soft) ...
(1 - Activable Flash Hard) ...
```

Pour les capacités **Activable**, ajouter si nécessaire une fréquence d'activation après le type/timing.

Les capacités **Déclenchable** ne peuvent pas être **Soft** : elles se déclenchent selon leur événement, sans fréquence Soft.

Pour les capacités **Déclenchable** et **Activable**, ajouter si nécessaire une fréquence d'activation après le type/timing :

- **Soft** : « Vous ne pouvez utiliser cette capacité qu'une fois par tour. » Cette limite n'est pas liée au nom de la carte. Si la carte quitte le terrain et revient, elle peut utiliser l'effet à nouveau.
- **Hard** : « Vous ne pouvez activer l'effet de X qu'une seule fois par tour. » Cette limite est liée au nom de la carte. Les autres copies ne peuvent pas activer la même capacité ce tour-ci.
- **Hard Linked** : « Vous ne pouvez utiliser qu’un seul des Y effets de X qu’une seule fois par tour. » Cette limite est liée au nom de la carte et verrouille aussi les autres effets **Hard Linked** de cette carte.

Exemple :

```text
(1 - Passif) **Malédiction abyssale**
(2 - Activable Hard Linked) **Descente**
(3 - Déclenchable Hard Linked) **On Send GY** — À la prochaine étape de fin, cherchez une créature “Burning Abyss”.
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
- Ne pas écrire `(2 - Activable Hard) La créature ciblée gagne +1/+1 jusqu'à la fin du tour.`

Garder les nombres en toutes lettres seulement dans les titres, commentaires de design, ou formulations où le nombre n'est pas une quantité de règle.

Toujours utiliser les raccourcis suivants dans les textes de carte :

- `MV` pour `Mana Value` / `valeur de mana`.
- `Deck` pour `bibliothèque` / `library`.

Exemples :

- Écrire `1 créature MV 1`, pas `1 créature avec une valeur de mana de 1`.
- Écrire `depuis votre Deck`, pas `depuis votre bibliothèque`.
- Écrire `du Deck au GY`, pas `depuis votre bibliothèque dans votre cimetière`.

Toujours utiliser `GY` pour `cimetière` dans les textes de carte. Garder `cimetière` seulement dans les explications de règles, commentaires de design ou documentation hors texte de carte.

Pour donner indestructible, écrire `gagne indestructible`, pas `a indestructible`.

Dans les textes d'effets, écrire `Si` au lieu de `Quand` pour les déclencheurs et conditions d'événement.

Exemples :

- Écrire **On Enter** — ..., pas `Si cette créature arrive`.
- Écrire `Si cette carte est détruite, ...`, pas `Quand cette carte est détruite, ...`.

## Mots-clés d'événement

**On Enter** signifie : « Lorsque cette carte arrive sur le champ de bataille. » Dans l'implémentation, ce déclencheur est `onEnterField`.

**On Attack** signifie : « Lorsque cette créature attaque. »

**On Block** signifie : « Lorsque cette créature bloque. »

**On Attack / Block** signifie : « Lorsque cette créature attaque ou bloque. » Utiliser une barre oblique lorsque plusieurs mots-clés d'événement s'appliquent au même effet.

**On Cast** signifie : « À chaque fois qu'un sort est lancé, avant sa résolution. » Cette famille de mots-clés se compose d'un périmètre, puis de paramètres optionnels, suivis de `:` et de l'effet :

- **On Your Cast** compte uniquement les sorts lancés par vous ;
- **On Opponent's Cast** compte uniquement les sorts lancés par un adversaire ;
- **On Any Cast** compte les sorts lancés par n'importe quel joueur.

Après le périmètre, ajouter si nécessaire les paramètres qui définissent les sorts concernés, par exemple `“Nekroz” Ritual` pour un sort Rituel dont le nom contient “Nekroz”. Le format est donc **On Your Cast [paramètres]** : effet.

**On Send GY** signifie : « Lorsque cette carte est mise dans un GY depuis n’importe quelle zone. » Utiliser ce mot-clé pour toute capacité de cette carte qui se déclenche lorsqu’elle est envoyée au GY.

**On Destroy** signifie : « Lorsque cette carte est détruite et envoyée au cimetière. »

**On Exile** signifie : « Lorsque cette carte est exilée. » Utiliser ce mot-clé pour toute capacité de cette carte qui se déclenche lorsqu’elle est exilée, quelle que soit la zone depuis laquelle elle est exilée.

**On Sacrifice** signifie : « Lorsque cette carte est sacrifiée ou utilisée comme matériel pour lancer une créature Ritual. » Utiliser ce mot-clé pour remplacer les formulations comme `Si cette carte est utilisée comme matériel Ritual`.

**Detach X** signifie : « Détachez X matériels de cette Xyz Creature et envoyez-les au GY. » `X` représente le nombre de matériels à détacher. Sur une carte, remplacer X par la valeur requise (`**Detach 1**`, `**Detach 2**`, etc.). Si n’importe quel nombre peut être détaché, conserver `**Detach X**`. Ce mot-clé constitue un coût et doit être placé avant `:` ou `;` selon le templating de la capacité.

**Mill X** signifie : « Envoyez les X cartes du dessus de votre Deck dans votre GY. » Sur une carte, remplacer X par la valeur requise : `**Mill 1**`, `**Mill 2**` ou `**Mill 3**`. Si le joueur choisit librement entre ces trois valeurs, écrire `**Mill up to 3**`.

**Nekroz Recovery** signifie : « Si vous ne contrôlez aucune créature : exilez cette carte et 1 autre carte “Nekroz” depuis votre GY ; cherchez 1 carte non-créature Invocation Ritual “Nekroz”. » Utiliser ce mot-clé sur les cartes non-créature “Nekroz” qui partagent cet effet, puis écrire le texte complet après un tiret cadratin.

`Invocation Ritual` signifie : « Mettez en jeu par invocation Ritual une ou plusieurs `Ritual Creature` en respectant les matériaux et conditions indiqués par l’effet. » Toute carte qui contient cet effet doit avoir le sous-type `Invocation Ritual`. Une `Ritual Creature` ne peut être mise en jeu pour la première fois que par un effet provenant d’une carte avec ce sous-type. Ne jamais écrire **Invocation Ritual** en gras dans le texte de règle.

`Invocation Fusion` signifie : « Mettez en jeu par invocation Fusion une `Fusion Creature` en respectant ses matériaux et les zones indiquées par l’effet. » Toute carte qui contient cet effet doit avoir le sous-type `Invocation Fusion`. Une `Fusion Creature` ne peut être mise en jeu pour la première fois que par un effet provenant d’une carte avec ce sous-type. Ne jamais écrire **Invocation Fusion** en gras dans le texte de règle.

Ces mots-clés remplacent les formulations `Mettez en jeu ... par Ritual`, `Mettez en jeu ... par rituel` et `Mettez en jeu ... par fusion`. Le texte qui suit le tiret décrit les créatures, matériaux, zones et autres contraintes applicables.

Pour tout effet déclenché par l'arrivée de la carte sur le champ de bataille, utiliser **On Enter**. Pour tout effet déclenché par une attaque ou un blocage, utiliser respectivement **On Attack**, **On Block** ou **On Attack / Block**. Ne pas reformuler ces événements avec `Si ... arrive`, `Si ... attaque` ou `Si ... bloque`.

Tout mot-clé d’événement doit être écrit en gras et suivi d’un tiret cadratin : `**On Enter** — ...`, `**On Exile** — ...`, etc.

**Piège** signifie : « Cette carte doit d’abord être jouée face verso avant de pouvoir être lancée. »

Utiliser les mots-clés d'événement pour raccourcir les effets déclenchés. Ne pas écrire l'explication de **Piège** sur les cartes : le mot-clé suffit.

## Raccourci de recherche

Pour alléger les textes de cartes, tout effet qui cherche une carte dans la bibliothèque pour la révéler, la mettre en main, puis mélanger doit être écrit sous la forme courte : **« cherchez X »**.

Exemple :

- Ne pas écrire : « cherchez une créature “Burning Abyss” dans votre bibliothèque, révélez-la, mettez-la dans votre main, puis mélangez. »
- Écrire : « cherchez une créature “Burning Abyss”. »

Cette convention implique par défaut la recherche dans la bibliothèque, la révélation si nécessaire, la mise dans la main, puis le mélange.

## Magic Set Editor

L'édition et le rendu final des cartes se font avec **Magic Set Editor (MSE)**.

- Installation MSE de référence : `F:\Softwares\Magic-Set-Editor-Full`
- Contexte technique MSE à lire avant toute génération ou modification : `F:\Softwares\Magic-Set-Editor-Full\CONTEXT.md`
- Dossier des projets MSE du cube dans le vault : `1_projects/yugioh_x_magic_cube/MSE_projects`

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
F:\Softwares\Magic-Set-Editor-Full\mse.com --export-images "CHEMIN\Carte_Test.mse-set" "CHEMIN\Carte_Test.mse-set\out_direct.png"
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
F:\Softwares\Magic-Set-Editor-Full\mse.com --export-images "CHEMIN\Projet.mse-set" "CHEMIN\Projet.mse-set\verify_export\card.png"
```

2. Ne pas considérer l'export comme suffisant : un projet peut s'exporter correctement mais échouer au moment de sauvegarder dans l'interface MSE avec `Referencing an inexistant file!`.
3. Quand le projet a été créé ou restructuré, ouvrir le projet dans MSE avec cette forme exacte de commande, puis faire un vrai test de **Save** ou **Save As** :

```powershell
powershell.exe -NoProfile -Command "Start-Process -FilePath 'F:\Softwares\Magic-Set-Editor-Full\mse.exe' -ArgumentList @('C:\chemin\vers\Projet.mse-set')"
```

4. Si la sauvegarde échoue, chercher en priorité :
   - des `include_file:` qui pointent vers un fichier absent ;
   - des champs `image`, `image_2`, `mainframe_image`, `mainframe_image_2`, `symbol`, `masterpiece_symbol` non vides dont le fichier n'existe pas ;
   - des fichiers de backup obsolètes comme `set.include_backup` contenant d'anciennes références ;
   - des dossiers `.mse-set` imbriqués dans le projet actif ;
   - des dossiers d'export/test générés à l'intérieur du projet actif.
5. Garder une copie de sauvegarde du projet avant toute correction destructive.

Convention d'images MSE du cube :

- `original_images/` contient les images sources haute résolution / artwork original téléchargé depuis YGOProDeck (`image_url_cropped`). Ces fichiers servent de source de vérité pour recadrer ou régénérer les images MSE.
- `mse_images/` contient les images adaptées utilisées par les fichiers MSE : PNG recadrés/redimensionnés, typiquement `316x231`, nommés `imageN.png`.
- `render/` contient les images finales rendues/exportées par MSE pour un projet `.mse-set` ; c'est le dossier de sortie canonique des rendus de cartes.
- Lors d'un export MSE, chaque image de carte individuelle dans `render/` doit être renommée avec le nom exact de la carte défini dans le fichier MSE (`name:`), par exemple `Burning Abyss - Dante.png`, et non rester au format générique `card.png`, `card.1.png`, etc.
- Les champs `image:` des cartes MSE doivent pointer vers `mse_images/imageN.png`, pas directement vers `original_images/...` ni vers les anciens dossiers `images/...`.

Cas identifié le 2026-07-11 sur **Burning Abyss** : une sauvegarde peut échouer tant que des cartes incluses pointent directement vers les images sources `.jpg` dans `images/Burning_Abyss/...`. Après redimensionnement/import dans MSE, la sauvegarde réussie transforme l'image en fichier `imageN.png` d'environ `316x231`, sans métadonnées EXIF, et met à jour la carte vers `image: imageN.png`. Dans ce projet, stocker ces images importées sous `mse_images/imageN.png`. Pour prévenir ce bug, préférer conserver l'image MSE importée/redimensionnée, plutôt que de forcer les cartes à pointer directement vers les `.jpg` sources.

Pour générer ce format sans passer par l'interface MSE, utiliser le helper :

```powershell
python C:\Users\Natha\brain\1_projects\yugioh_x_magic_cube\.script\generate_mse_imported_image.py "CHEMIN\Projet.mse-set" "CHEMIN\source.jpg" --card-file "card fichier a mettre a jour"
```

Le script crée le prochain `imageN.png` disponible dans le dossier racine du projet et, si `--card-file` est fourni, remplace le champ `image:` de la carte par ce nouveau fichier.

Pour corriger un projet entier déjà généré avec des références `images/.../*.jpg`, utiliser :

```powershell
python C:\Users\Natha\brain\1_projects\yugioh_x_magic_cube\.script\fix_mse_project_images.py --backup "CHEMIN\Projet.mse-set"
```

Ce script sauvegarde le projet, génère des `imageN.png` racine pour toutes les cartes incluses, met à jour les champs d'image, trie les `include_file:` par nom de carte et renumérote les `card_code_text`.

## Conventions de rédaction des types, recherches et zones

- Toujours écrire `Ritual Creature`, jamais `créature Ritual` ni `Ritual créature`. Au pluriel, écrire `Ritual Creatures`.
- Pour une recherche, écrire le type avant le nom d’archétype : `Cherchez 1 Ritual Creature “Nekroz”.` Pour une carte d’invocation non-créature, écrire `Cherchez 1 carte non-créature Invocation Ritual “Nekroz”.` Si une race est requise, la placer avant le type : `Dragon Ritual Creature`.
- Pour un coût d’Invocation Ritual fondé sur la valeur de mana, comparer explicitement les valeurs : `dont la MV totale est égale à la MV de la créature mise en jeu`.
- Si plusieurs Ritual Creatures peuvent être mises en jeu, accorder au pluriel : `leur(s) coût(s) Ritual`.
- Ne jamais énumérer les zones avec plusieurs possessifs. Écrire `depuis votre main ou terrain`, jamais `depuis votre main ou terrain`, `depuis votre main ou terrain` ni `depuis votre main ou terrain`.
- Lorsqu’un effet ne cible pas au sens des règles, l’indiquer explicitement avec `Cet effet ne cible pas.`
- Plusieurs actions à mot-clé appartenant à une même capacité sont écrites dans un même groupe en gras et reliées par `et`, par exemple `**Detach 1 et Mill 3**`.
- Un effet activé depuis le GY commence par `Depuis votre GY, exilez cette carte : ...`.
- Pour désigner la carte elle-même, utiliser son nom si celui-ci est aussi court ou plus court que `cette carte` ; sinon, utiliser `cette carte`.
- Pour déplacer une carte depuis le Deck, réserver `Cherchez` aux cartes mises en main. Utiliser `Envoyez ... depuis votre Deck au GY` et `Mettez en jeu ... depuis votre Deck` pour les autres destinations.
- Toujours écrire les zones et mécaniques avec leur casse et leur orthographe validées : `Deck`, `GY`, `Sideboard`, `Ritual Creature`, `Fusion Creature` et `Piège`.
- La ligne de matériaux d’une Fusion Creature utilise `*Fusion — [matériaux]*`.
- La ligne de matériaux d’une Synchro Creature place toujours le Tuner en premier : `*Synchro — 1 Tuner + 1+ non-Tuner*`.
- Une protection par remplacement de destruction utilise `Si cette carte devait être détruite, vous pouvez sacrifier ... à la place.`
- Une perte de capacités accompagnée d’un changement de statistiques utilise l’ordre `La créature ciblée perd toutes ses capacités et devient 0/0 jusqu’à la fin du tour.`

## Convention Extra Deck / types MSE

Pour les créatures d'Extra Deck, le type spécial doit être placé dans le `super_type`, avant `Creature`, et non dans le sous-type/race :

- `Xyz Creature` pour les créatures Xyz ;

### Ligne de matériaux Xyz

La première ligne de texte d'une `Xyz Creature` doit indiquer ses matériaux en italique. Par défaut, utiliser toujours :

```text
Xyz — 2 créatures MV N
```

où `N` est la valeur de mana de la carte Xyz elle-même. Exemple : une Xyz coûtant `{2}{U}` utilise `Xyz — 2 créatures MV 3`. Les exceptions existent seulement si le design de la carte exige explicitement `2+ créatures` ou un matériel nommé, mais la baseline du projet est `2 créatures MV N`.
- `Synchro Creature` pour les créatures Synchro ;
- `Fusion Creature` pour les créatures Fusion ;
- `Link Creature` pour les créatures Link.

Pour toute carte qui permet explicitement une invocation spéciale, conserver son type Magic normal et ajouter la mécanique d’invocation dans son sous-type :

- une carte qui porte **Invocation Ritual** reste `Sorcery`, `Instant`, `Enchantment`, etc., et reçoit le sous-type `Invocation Ritual` ;
- une carte qui porte **Invocation Fusion** reste `Sorcery`, `Instant`, `Enchantment`, etc., et reçoit le sous-type `Invocation Fusion` ;
- une carte peut conserver un autre sous-type en plus, par exemple `Sorcery — Ritual, Invocation Ritual` ;
- appliquer la même règle aux futures mécaniques similaires.

Dans les documents de cartes, utiliser la même forme sur la ligne de type, par exemple `Xyz Creature — Humain`.

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
- **Normal, autres cartes et non-créatures Fusion/Ritual** : `sevenhalf` (`magic-sevenhalf.mse-style`) — frame 7.5th Edition validée.

Les frames Fusion et Ritual ne s'appliquent qu'aux **créatures**. Une carte non-créature avec le sous-type `Invocation Fusion` ou `Invocation Ritual` garde la frame par défaut `sevenhalf`.

Voir aussi `frame_candidates.md` pour la liste des candidats et validations visuelles.

La première ligne du texte de règle d'une créature d'Extra Deck doit être la condition d'invocation en italique, sauf pour les Link Creatures :

- `*Xyz — 2 créatures MV N*` dans les docs / `<i>Xyz — 2 créatures MV N</i>` dans MSE ;
- `*Synchro*` dans les docs / `<i>Synchro</i>` dans MSE ;
- `*Fusion — 1 créature “Shaddoll” + 1 créature blanche*` dans les docs / `<i>Fusion — ...</i>` dans MSE.

Exception Link : ne pas ajouter de première ligne d'invocation en italique aux `Link Creature`. Les Link Creatures se lancent depuis le sideboard avec un nombre de créatures égal au niveau Link ; la MV/niveau des matériaux n'a pas d'importance. Le niveau Link doit être porté par le type de carte (`Link Lvl 2 Creature`, etc.) ou référencé par les effets, pas répété en première ligne du texte de règle.
