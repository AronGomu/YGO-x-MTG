# 11 - Archétype : Shaddoll

# Règles générales

## Identité de l'archétype

Shaddoll est un deck **Contrôle / Value / Fusion**.

L'archétype repose sur deux mécaniques principales :

- **Flip** ;
- **Corruption**.

## Conventions propres à Shaddoll

Les noms cube utilisent le format `[préfixe optionnel] Shaddoll - [nom]`. Les préfixes officiels `El`, `Hel`, `Nael`, `Puru`, `Qad`, `Ree` et `Resh` sont séparés de `Shaddoll`. `Curse of the Shadow Prison` et `Sinister Shadow Games` conservent exceptionnellement leur nom officiel complet.

Les créatures Shaddoll conservent le type et le sous-type individuels définis dans leur carte MSE ; leur race n’est pas uniformisée en `Puppet`. `Shaddoll - Falco` est une `Tuner Creature`. `Resh Shaddoll - Incarnation` et `Sinister Shadow Games` sont des `Trap Instant`, tandis que `Shaddoll - Core` est un `Trap Enchantment`.

Les cartes incluses par `MSE_projects/11_YGO_Shaddoll.mse-set/set` sont la source de vérité des valeurs carte par carte de cet archétype. Ce document, les scripts et les tests doivent les refléter. Les restrictions générales de Summon restent applicables sauf mention explicite contraire sur une carte.

---

## Couleur

Couleur principale : **Noir**

---

## Mécaniques

### Flip

Lorsque cette créature est retournée face visible, appliquez l'effet indiqué.

### Corruption

Lorsque cette carte est mise dans votre Grave par un effet de carte, appliquez l'effet indiqué.

---

# Monstres du Main Deck

---

## Shaddoll Beast => Shaddoll - Beast

**Coût :** {1}{B}

Creature — Beast

**4 / 3**

(1 - Déclenchable Hard Linked) **Flip** — Piochez 2 cartes, puis défaussez 1 carte.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — Piochez 1 carte.

---

## Shaddoll Dragon => Shaddoll - Dragon

**Coût :** {B}

Creature — Dragon

**3 / 2**

(1 - Déclenchable Hard Linked) **Flip** — Ciblez 1 permanent non-terrain ; renvoyez-le dans la main de son propriétaire.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — Ciblez 1 permanent non-terrain non-créature ; détruisez-le.

---

## Shaddoll Hedgehog => Shaddoll - Hedgehog

**Coût :** {B}

Creature — Beast

**2 / 2**

(1 - Déclenchable Hard Linked) **Flip** — Cherchez 1 carte “Shaddoll” non-créature.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — Cherchez 1 créature “Shaddoll”.

---

## Shaddoll Squamata => Shaddoll - Squamata

**Coût :** {B}

Creature — Puppet

**3 / 2**

(1 - Déclenchable Hard Linked) **Flip** — Détruisez 1 créature ciblée.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — Envoyez 1 carte “Shaddoll” depuis votre Deck au Grave.

---

## Shaddoll Falco => Shaddoll - Falco

**Coût :** {B}

Tuner Creature — Bird

**1 / 2**

(1 - Déclenchable Hard Linked) **Flip** — Ciblez 1 créature “Shaddoll” dans votre Grave ; **Reanimate** la créature ciblée face verso.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — **Reanimate** cette carte face verso.

---

## Shaddoll Hound => Shaddoll - Hound

**Coût :** {B}

Creature — Beast

(1 - Déclenchable Hard Linked) **Flip** — Ciblez 1 carte “Shaddoll” dans votre Grave ; renvoyez-la dans votre main.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — Vous pouvez retourner face visible ou face verso 1 créature que vous contrôlez.

---

## Reeshaddoll Wendi => Ree Shaddoll - Wendi

**Coût :** {G}

Creature — Psychic

(1 - Déclenchable Hard Linked) **Flip** — **Summon** 1 créature “Shaddoll” depuis votre Deck face visible ou face verso.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — **Summon** 1 créature “Shaddoll” depuis votre Deck face verso.

---

## Naelshaddoll Ariel => Nael Shaddoll - Ariel

**Coût :** {U}

Creature — Psychic

**2 / 3**

(1 - Déclenchable Hard Linked) **Flip** — Ciblez 1 de vos créatures “Shaddoll” exilées ; **Summon**-la face verso.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — Ciblez 3 cartes dans les Grave ; exilez-les.

---

## Qadshaddoll Keios => Qad Shaddoll - Keios

**Coût :** {W}

Creature — Wizard

**1 / 1**

(1 - Déclenchable Hard Linked) **Flip** — **Summon** 1 créature “Shaddoll” depuis votre main face visible ou face verso.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — Défaussez-vous d’1 créature “Shaddoll” ; les créatures que vous contrôlez gagnent +X/+X jusqu’à la fin du tour, X étant la MV de la carte défaussée.

---

## Helshaddoll Hollow => Hel Shaddoll - Hollow

**Coût :** {2}{R}

Creature — Fiend

**5 / 5**

(1 - Déclenchable Hard Linked) **Flip** — Ciblez 1 créature contrôlée par un adversaire ; envoyez 1 créature “Shaddoll” depuis votre Sideboard dans votre Grave, puis, si les 2 cartes sont de la même couleur, exilez la cible.

(2 - Déclenchable Hard Linked) **On Send Grave by Effect** — **Mill X**, X étant le nombre de couleurs parmi les créatures que vous contrôlez.

---

# Créatures Fusion

---

## El Shaddoll Construct => El Shaddoll - Construct

**Coût :** {2}{W}

Fusion Creature — Fairy

**5 / 5**

*1 créature “Shaddoll” + 1 créature blanche*

(1 - Déclenchable) **On Enter** — Envoyez 1 carte “Shaddoll” depuis votre Deck au Grave.

(2 - Déclenchable) **On Block / Blocked** — Si l’autre créature a été Summon, détruisez-la.

(3 - Déclenchable) **On Send Grave** — Renvoyez 1 carte “Shaddoll” non-créature depuis votre Grave dans votre main.

---

## El Shaddoll Winda => El Shaddoll - Winda

**Coût :** {1}{B}

Fusion Creature — Wizard

**4 / 1**

*1 créature “Shaddoll” + 1 créature noire*

(1 - Passif) Chaque joueur ne peut lancer qu’1 créature par tour.

(2 - Passif) **Indestructible contre les effets**.

(3 - Déclenchable) **On Send Grave** — Renvoyez 1 carte “Shaddoll” non-créature depuis votre Grave dans votre main.

---

## El Shaddoll Apkallone => El Shaddoll - Apkallone

**Coût :** {2}{U}

Fusion Creature — Wizard

**5 / 5**

*1 créature “Shaddoll” + 1 créature bleue*

(1 - Déclenchable Hard) **On Enter** — Ciblez 1 permanent ; il perd toutes ses capacités tant que cette carte reste sur le terrain.

(2 - Déclenchable Hard) **Corruption** — Défaussez 1 carte, puis cherchez 1 carte “Shaddoll”.

---

## El Shaddoll Shekhinaga => El Shaddoll - Shekhinaga

**Coût :** {2}{G}

Fusion Creature — Machine

**5 / 6**

*1 créature “Shaddoll” + 1 créature verte*

(1 - Déclenchable Flash Hard) Vous pouvez révéler 1 carte “Shaddoll” de votre main et cibler 1 capacité ; défaussez la carte révélée et contrecarrez la capacité ciblée.

(2 - Déclenchable) **On Send Grave** — Renvoyez 1 carte “Shaddoll” non-créature depuis votre Grave dans votre main.

---

## El Shaddoll Grysta => El Shaddoll - Grysta

**Coût :** {2}{R}

Fusion Creature — Elemental

**5 / 4**

*1 créature “Shaddoll” + 1 créature rouge*

(1 - Déclenchable Soft) **On Opponent Summon** — Vous pouvez révéler 1 carte “Shaddoll” de votre main ; défaussez la carte révélée, contrecarrez toutes les capacités déclenchées de cette créature, puis détruisez-la.

(2 - Déclenchable Soft) **On Send Grave** — Renvoyez 1 carte “Shaddoll” non-créature depuis votre Grave dans votre main.

---

## El Shaddoll Anoyatyllis => El Shaddoll - Anoyatyllis

**Coût :** {2}{U}

Fusion Creature — Fiend

**5 / 5**

*1 créature “Shaddoll” + 1 créature bleue*

(1 - Passif) Si une créature devait arriver sur le terrain sans avoir été lancée depuis une main ou un Grave, exilez-la à la place.

(2 - Déclenchable) **On Send Grave** — Ciblez 1 carte “Shaddoll” non-créature dans votre Grave ; renvoyez-la dans votre main.

---

## El Shaddoll Wendigo => El Shaddoll - Wendigo

**Coût :** {2}{U}

Fusion Creature — Psychic

**1 / 5**

*1 créature “Shaddoll” + 1 créature verte*

(1 - Activable Flash Hard) La créature ciblée gagne **indestructible** jusqu’à la fin du tour.

(2 - Déclenchable) **On Send Grave** — Renvoyez 1 carte “Shaddoll” non-créature depuis votre Grave dans votre main.

---

# Magies et Pièges

---

## Shaddoll Fusion => Shaddoll - Fusion

**Coût :** {B/G}

Fusion Summon Sorcery

(1 - Résolution) **Fusion Summon** 1 créature en utilisant des créatures depuis votre main ou terrain comme matériaux. Si un adversaire contrôle une créature ayant commencé la partie dans un Sideboard, vous pouvez aussi utiliser des créatures depuis votre Deck.

---

## El Shaddoll Fusion => El Shaddoll - Fusion

**Coût :** {U/B}

Fusion Summon Instant

(1 - Résolution) **Fusion Summon** 1 créature “Shaddoll” en utilisant des créatures depuis votre main ou terrain comme matériaux.

---

## Shaddoll Schism => Shaddoll - Schism

**Coût :** {W/B}

Fusion Summon Enchantment

(1 - Activable Sorcery Soft) **Fusion Summon** 1 créature “Shaddoll” en exilant les matériaux indiqués depuis votre terrain ou Grave. Puis envoyez au Grave 1 créature contrôlée par un adversaire qui partage une couleur avec cette créature.

---

## Shaddoll Core => Shaddoll - Core

**Coût :** {B}

Trap Enchantment

**0 / 3**

(1 - Résolution) Core devient une Enchantment Creature — Puppet 2/3 de toutes les couleurs avec « Cette carte peut être utilisée comme matériau pour n’importe quelle Fusion Creature “Shaddoll” à la place d’un matériau requis. »

(2 - Déclenchable) **On Send Grave by Effect** — Renvoyez 1 carte “Shaddoll” non-créature depuis votre Grave dans votre main.

---

## Resh Shaddoll Incarnation => Resh Shaddoll - Incarnation

**Coût :** {B}

Trap Instant

(1 - Résolution Hard Linked) Renvoyez 1 créature “Shaddoll” ciblée depuis votre Grave sur le terrain face visible ou face verso.

(2 - Activable Flash Hard Linked) Depuis votre Grave, exilez cette carte et 1 autre carte “Shaddoll” ; choisissez 1 créature que vous contrôlez et retournez-la face visible ou face verso.

---

## Sinister Shadow Games => Sinister Shadow Games

**Coût :** {B}

Trap Instant

(1 - Résolution) Envoyez 1 carte “Shaddoll” depuis votre Deck au Grave, puis vous pouvez retourner face visible autant de créatures “Shaddoll” face verso que vous contrôlez.

---

## Curse of the Shadow Prison => Curse of the Shadow Prison

**Coût :** {B}

Legendary Enchantment

(1 - Déclenchable) Si 1+ cartes “Shaddoll” sont mises dans votre Grave par un effet de carte, mettez 1 compteur Magie sur cette carte.

(2 - Passif) Pendant le tour de chaque adversaire, les créatures qu’il contrôle gagnent -1/-0 pour chaque groupe de 5 compteurs Magie sur cette carte.

(3 - Passif) Si vous choisissez les matériaux pour une **Fusion Summon** “Shaddoll”, vous pouvez retirer 3 compteurs Magie de cette carte. Si vous faites ainsi, vous pouvez utiliser 1 créature contrôlée par un adversaire comme matériel pour cette invocation.

---

## Purushaddoll Aeon => Puru Shaddoll - Aeon

**Coût :** {0}

Trap Instant

(1 - Résolution) Ciblez 1 créature “Shaddoll” que vous contrôlez ; envoyez 1 carte “Shaddoll” depuis votre main au Grave, puis la créature ciblée gagne +2/+2 jusqu’à la fin du tour. Au début de l’étape de fin, retournez-la face verso.
