# Frames MSE candidates pour les types Extra Deck / spéciaux

Chemin analysé : `MSE_DATA_DIR` dans le fichier `.env` local, généré avec `python setup_mse.py`.

Ce document liste les styles/frames MSE repérés pour différencier visuellement les types spéciaux du cube Yu-Gi-Oh × Magic.

## Mapping validé actuel

```text
Normal / autres -> 7.5th Edition (`sevenhalf` / `magic-sevenhalf.mse-style`) — standard validé
Fusion Creature  -> `gen main` — hi-res (`genevensis-00-main` / `magic-genevensis-00-main.mse-style`) — standard validé
Xyz Creature     -> M15 Spellbook (`m15-spellbook` / `magic-m15-spellbook.mse-style`) — standard validé
Synchro Creature -> M15 Sketch (`m15-sketch` / `magic-m15-sketch.mse-style`) — standard validé
Link Creature    -> Art Deco — Capenna Showcase (`m15-showcase-capenna-art-deco`) — standard validé
Ritual Creature  -> Praetor / Phyrexian Showcase (`m15-showcase-praetor` / `magic-m15-showcase-praetor.mse-style`) — standard validé
Fusion/Ritual non-créature -> 7.5th Edition (`sevenhalf`) — standard validé
```

Validation Synchro : le style **Sketch** a été choisi pour les cartes/projets Synchro et appliqué au projet MSE `06_YGO_Staples_Synchro.mse-set`.

À noter : `M15 big text` existe pour les cartes avec trop de texte.

---

## Frames intéressantes par type

### Fusion

- `m15 spellbook` — w/ flavor bar
- `gen main` — hi-res — **validé, frame standard obligatoire pour les Fusion Creature**
- `Eldrazi` — by kasu_mtg
- `Elemental` — Avatar Showcase
- `Woodland` — Bloomburrow Showcase
- `Fable` — Lorwyn showcase
- `Mystical Archive` — Strixhaven Showcase

### Synchro

- `m15 spellbook` — w/ flavor bar
- `gen main` — hi-res
- `Eldrazi` — by katsu_mtg
- `M15 Sketch` — MH2 Sketch
- `Art Deco` — Capenna Showcase
- `Ninja` — Kamigawa Showcase
- `Ghostfire` — Tarkir showcase
- `Vault` — Thunder Junction Showcase

### Ritual

- `m15 spellbook` — w/ flavor bar
- `Eldrazi` — by katsu_mtg
- `Art Deco` — Capenna Showcase
- `TARDIS` — Doctor Who Showcase
- `Fable` — Lorwyn showcase
- `Scroll` — LotR Showcase
- `Praetor` — Phyrexian Showcase — **validé, frame standard obligatoire pour les cartes Ritual**
- `Mystical Archive` — Strixhaven Showcase

### Link

- `gen main` — hi-res
- `Memory Corridor` — Assassin's Creed Showcase
- `Eternal Night` — Double Feature
- `Ninja` — Kamigawa Showcase

### Xyz

- `Art Deco` — Capenna Showcase — **validé, frame standard obligatoire pour les créatures Xyz**.
- `M15 black promo` — M15 Sleek — option historique non standard.

---

## Frames repérées mais classées “other”

- `b1234 style` — Buttock 1234 style
- `sevenhalf` — 7.5 edition frames
- `agClassic` — AgClassic Normal
- `old style` — before 8th edition
- `8th test` — 8th edition test prints
- `classic shifted` — classic timeshift
- `future mirror` — mirrored futureshift
- `future clear` — futureshifted clear
- `future` — futureshift
- `planeshifted` — planar chaos timeshift

---

## Ancien mapping exploratoire

Une exploration précédente proposait ces équivalents visuels Magic Set Editor :

```text
Fusion  -> magic-m15-split-fusable
Synchro -> magic-m15-future
Ritual  -> magic-m15-invocation
Link    -> magic-m15-showcase-spiderman-web-slinger
Xyz     -> magic-m15-devoid
```

Ces options restent utilisables comme références historiques, mais la liste ci-dessus reflète les choix visuels repérés ensuite dans l'installation MSE.


## Configuration MSE validée pour Xyz

```text
stylesheet: m15-showcase-capenna-art-deco
stylesheet_version: 2024-10-01
styling:
	magic-m15-showcase-capenna-art-deco:
		overlay:
		casting_cost_mana_symbols: magic-mana-large.mse-symbol-font
		text_box_mana_symbols: magic-mana-small.mse-symbol-font
```
