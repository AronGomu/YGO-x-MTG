# 11 - Archétype : Shaddoll

# Règles générales

## Identité de l'archétype

Shaddoll est un deck **Contrôle / Value / Fusion**.

L'archétype repose sur deux mécaniques principales :

- **Flip** ;
- **Shaddoll Recovery**.

## Conventions propres à Shaddoll

Les noms cube utilisent le format `[préfixe optionnel] Shaddoll - [nom]`. Les préfixes officiels `El`, `Hel`, `Nael`, `Puru`, `Qad`, `Ree` et `Resh` sont séparés de `Shaddoll`. `Curse of the Shadow Prison` et `Sinister Shadow Games` conservent exceptionnellement leur nom officiel complet.

Les créatures Shaddoll conservent le type et le sous-type individuels définis dans leur carte MSE ; leur race n’est pas uniformisée en `Puppet`. `Shaddoll - Falco` est une `Tuner Creature`. `Resh Shaddoll - Incarnation` et `Sinister Shadow Games` sont des `Trap Instant`, tandis que `Shaddoll - Core` est un `Trap Enchantment`.

Les cartes incluses par `MSE_projects/11_YGO_Shaddoll.mse-set/set` sont la source de vérité des valeurs carte par carte. Les scripts et les tests doivent les refléter. Les restrictions générales de Summon restent applicables sauf mention explicite contraire sur une carte.

---

## Couleur

Couleur principale : **Noir**

---

## Mécaniques

### Flip

Lorsque cette créature est retournée face visible, appliquez l'effet indiqué.

### Shaddoll Recovery

**Shaddoll Recovery** signifie : « **On Send Grave** — **Salvage** 1 “Shaddoll” non-créature. » Sur les cartes, écrire uniquement le mot-clé en gras après le préfixe de capacité, sans rappeler le texte complet. **Salvage** est le mot-clé général Grave → main (`docs/context.md`).

`On Send Grave by Effect` reste un événement distinct. Il n’est pas absorbé par **Shaddoll Recovery** sauf si la carte imprime explicitement ce mot-clé.

---

## Source de vérité des cartes

Les valeurs carte par carte de cet archétype sont définies uniquement dans `MSE_projects/11_YGO_Shaddoll.mse-set/`. Ce document ne conserve que l’identité, les conventions de nommage et les mécaniques d’archétype.
