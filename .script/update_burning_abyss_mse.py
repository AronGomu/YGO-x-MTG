from pathlib import Path
from datetime import datetime
import re

project = Path(__file__).resolve().parents[1] / 'MSE_projects' / 'YGO_Burning_Abyss.mse-set'
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

image_map = {
    'card scarm burning abyss': 'images/Burning_Abyss/scarm_malebranche_of_the_burning_abyss.jpg',
    'card graff burning abyss': 'images/Burning_Abyss/graff_malebranche_of_the_burning_abyss.jpg',
    'card cir burning abyss': 'images/Burning_Abyss/cir_malebranche_of_the_burning_abyss.jpg',
    'card farfa burning abyss': 'images/Burning_Abyss/farfa_malebranche_of_the_burning_abyss.jpg',
    'card libic burning abyss': 'images/Burning_Abyss/libic_malebranche_of_the_burning_abyss.jpg',
    'card barbar burning abyss': 'images/Burning_Abyss/barbar_malebranche_of_the_burning_abyss.jpg',
    'card alich burning abyss': 'images/Burning_Abyss/alich_malebranche_of_the_burning_abyss.jpg',
    'card calcab burning abyss': 'images/Burning_Abyss/calcab_malebranche_of_the_burning_abyss.jpg',
    'card cagna burning abyss': 'images/Burning_Abyss/cagna_malebranche_of_the_burning_abyss.jpg',
    'card draghig burning abyss': 'images/Burning_Abyss/draghig_malebranche_of_the_burning_abyss.jpg',
    'card rubic burning abyss': 'images/Burning_Abyss/rubic_malebranche_of_the_burning_abyss.jpg',
    'card dante traveller of the burning abyss': 'images/Burning_Abyss/dante_traveler_of_the_burning_abyss.jpg',
    'card virgil rock star of the burning abyss': 'images/Burning_Abyss/virgil_rock_star_of_the_burning_abyss.jpg',
    'card beatrice lady of the eternal': 'images/Burning_Abyss/beatrice_lady_of_the_eternal.jpg',
    'card fire lake of the burning abyss': 'images/Burning_Abyss/fire_lake_of_the_burning_abyss.jpg',
    'card malacoda netherlord of the burning abyss': 'images/Burning_Abyss/malacoda_netherlord_of_the_burning_abyss.jpg',
    'card dante pilgrim of the burning abyss': 'images/Burning_Abyss/dante_pilgrim_of_the_burning_abyss.jpg',
    'card cherubini ebon angel of the burning abyss': 'images/Burning_Abyss/cherubini_ebon_angel_of_the_burning_abyss.jpg',
    'card good evil in the burning abyss': 'images/Burning_Abyss/good_evil_in_the_burning_abyss.jpg',
    'card the terminus of the burning abyss': 'images/Burning_Abyss/the_terminus_of_the_burning_abyss.jpg',
    'card the traveler and the burning abyss': 'images/Burning_Abyss/the_traveler_and_the_burning_abyss.jpg',
}

cards = [
    ('card scarm burning abyss','Burning Abyss - Scarm','B','Creature','Fiend','common',[
        '(1 - Passif) <b>Malédiction abyssale</b>',
        '(2 - Activable Hard Linked) <b>Descente</b>',
        '(3 - Déclenchable Hard Linked) <b>On Send GY</b> — À la prochaine étape de fin, cherchez une créature "Burning Abyss".',
    ],'1','4'),
    ('card graff burning abyss','Burning Abyss - Graff','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Cherchez une créature "Burning Abyss" et mettez-la sur le terrain.'],'2','3'),
    ('card cir burning abyss','Burning Abyss - Cir','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Renvoyez une créature "Burning Abyss" ciblée depuis votre cimetière sur le terrain.'],'3','2'),
    ('card farfa burning abyss','Burning Abyss - Farfa','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Exilez la créature ciblée jusqu\'à la prochaine étape de fin.'],'2','3'),
    ('card libic burning abyss','Burning Abyss - Libic','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Mettez en jeu une créature "Burning Abyss" depuis votre main sans payer son coût de mana ce tour-ci.'],'2','1'),
    ('card barbar burning abyss','Burning Abyss - Barbar','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Exilez jusqu\'à trois cartes "Burning Abyss" de votre cimetière. Barbar inflige 1 blessure à l\'adversaire ciblé pour chaque carte exilée.'],'3','2'),
    ('card alich burning abyss','Burning Abyss - Alich','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Jusqu\'à la fin du tour, la créature ciblée perd toutes ses capacités et devient 0/0.'],'2','2'),
    ('card calcab burning abyss','Burning Abyss - Calcab','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Renvoyez un permanent non-terrain ciblé dans la main de son propriétaire.'],'3','1'),
    ('card cagna burning abyss','Burning Abyss - Cagna','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Cherchez une carte "Burning Abyss" et mettez-la dans votre cimetière.'],'2','2'),
    ('card draghig burning abyss','Burning Abyss - Draghig','B','Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard Linked) <b>Descente</b>','(3 - Déclenchable Hard Linked) <b>On Send GY</b> — Défaussez-vous d\'une carte, puis piochez une carte.'],'2','2'),
    ('card rubic burning abyss','Burning Abyss - Rubic','B','Tuner Creature','Fiend','common',['(1 - Passif) <b>Malédiction abyssale</b>','(2 - Activable Hard) <b>Descente</b>'],'2','2'),
    ('card dante traveller of the burning abyss','Burning Abyss - Dante','W','Xyz Creature','Human','common',['<i>2 Creatures Mana Value 1</i>','(1 - Activable Soft) <b>Detach 1<b> : meulez jusqu’à trois cartes ; pour chaque carte Burning Abyss meulée de cette manière, Dante gagne +1/+0 et acquiert la vigilance jusqu’à la fin du tour.','(2 - Déclenchable) <b>On Send GY</b> — Renvoyez une autre carte “Burning Abyss” depuis votre cimetière dans votre main.'],'2','5'),
    ('card virgil rock star of the burning abyss','Burning Abyss - Virgil','1W','Synchro Creature','Wizard','common',['<i>1+ Non-Tuner + 1 Tuner</i>','(1 - Activable Sorcery Soft) Défaussez-vous d’une carte ; Mélangez le permanent non-terrain ciblé dans la bibliothèque.','(2 - Déclenchable) <b>On Send GY</b> — Piochez une carte.'],'5','2'),
    ('card beatrice lady of the eternal','Beatrice, Lady of the Eternal','1W','Xyz Creature','Fairy','common',['<i>2 Creatures Mana Value 2</i>','(1 - Alternative Cost) <sym>W</sym>, Défaussez 1 créature “Burning Abyss” : Lancez en Xyz en utilisant une créature “Dante” que vous contrôlez. Ses matériels se transfèrent.','(2 - Activable Flash Soft) <b>Detach 1<b> ; Envoyez une carte de votre deck dans votre cimetière.','(3 - Déclenchable) <b>On Destroy</b> : Vous pouvez mettre en jeu une créature “Burning Abyss” depuis votre sideboard.'],'5','5'),
    ('card fire lake of the burning abyss','Burning Abyss - Fire Lake','B','Instant','','common',['(1 - Passif) <b>Piège</b>','(2 - Trap Supplemental Cost) Sacrifiez 2 créatures “Burning Abyss”.','(3 - Resolution) Détruisez jusqu’à 3 permanents non-terrain ciblés.'],'',''),
    ('card malacoda netherlord of the burning abyss','Burning Abyss - Malacoda','1BB','Ritual Creature','Fiend','common',['(1 - Activable Flash Soft) Envoyez une créature “Burning Abyss” depuis votre main dans votre cimetière ; la créature ciblée gagne -X/-X jusqu’à la fin du tour, où X est la force de la carte envoyée.','(2 - Déclenchable) <b>On Send GY</b> — Envoyez le permanent non-terrain ciblé dans le cimetière de son propriétaire.'],'5','4'),
    ('card dante pilgrim of the burning abyss','Burning Abyss - Dante, Pilgrim','1WW','Fusion Creature','Fairy','common',['<i>3 créatures “Burning Abyss” avec des noms différents</i>','(1 - Passif) Cette créature ne peut pas être ciblée par les sorts ou capacités de vos adversaires.','(2 - Activable Flash Soft) Envoyez une carte “Burning Abyss” depuis votre main dans votre cimetière ; piochez une carte.','(3 - Déclenchable) <b>On Destroy</b> : Un adversaire ciblé se défausse d’une carte au hasard.'],'5','5'),
    ('card cherubini ebon angel of the burning abyss','Burning Abyss - Cherubini','W','Link Lvl 2 Creature','Fairy','common',['<i>2 Creatures Mana Value 1</i>','(1 - Passif) Choisissez 1 autre créature que vous contrôlez. Elle ne peut pas être détruite par des effets de carte. Si la créature choisie quitte le terrain, vous pouvez choisir une autre créature.','(2 - Passif) Si Cherubini devait être détruite, vous pouvez envoyer un autre permanent que vous contrôlez dans votre cimetière à la place.','(3 - Activable Sorcery Soft) Envoyez une créature avec une valeur de mana de 1 depuis votre deck dans votre cimetière ; une créature “Burning Abyss” ciblée gagne +X/+X jusqu’à la fin du tour, où X est la force de la carte envoyée.'],'1','4'),
    ('card good evil in the burning abyss','Burning Abyss - Good & Evil','B','Ritual Sorcery','','common',['(1 - Resolution) Mettez en jeu 1 créature Rituel “Burning Abyss” <b>par rituel</b> en sacrifiant des créatures depuis votre main ou votre terrain avec une MV totale supérieure ou égale à 3.','(2 - Activable Sorcery Hard) Exilez Good & Evil depuis votre cimetière et envoyez une créature “Burning Abyss” depuis votre main dans votre cimetière ; cherchez une carte “Burning Abyss”.'],'',''),
    ('card the terminus of the burning abyss','Burning Abyss - Terminus','W','Fusion Sorcery','','common',['(1 - Resolution) Mettez en jeu 1 créature Fusion <b>par fusion</b> depuis votre sideboard en utilisant des créatures depuis votre main ou votre terrain comme matériaux Fusion.','(2 - Activable Sorcery Soft) Exilez Terminus depuis votre cimetière ; une créature “Burning Abyss” ciblée gagne +2/+2 jusqu’à la fin du prochain tour de votre adversaire.'],'',''),
    ('card the traveler and the burning abyss','Burning Abyss - Traveler','B','Instant','','common',['(1 - Passif) <b>Piège</b>','(2 - Resolution) Renvoyez sur le terrain n’importe quel nombre de créatures “Burning Abyss” depuis votre cimetière qui y ont été envoyées ce tour-ci.'],'',''),
]

def rich_type(t):
    return f'<word-list-type-en>{t}</word-list-type-en>'

def rich_subtype(s):
    if not s:
        return ''
    parts = [p.strip() for p in re.split(r'\s+(?:et|and)\s+', s) if p.strip()]
    out = f'<word-list-race-en>{parts[0]}</word-list-race-en>'
    for p in parts[1:]:
        out += f'<soft><atom-sep> </atom-sep></soft><word-list-class-en>{p}</word-list-class-en>'
    return out

for i, (filename, name, cost, typ, subtype, rarity, rules, power, toughness) in enumerate(cards, 1):
    lines = [
        'mse_version: 2.5.8', 'card:', '\thas_styling: false', '\tnotes: Source: 10_archetype_burning_abyss.md',
        f'\ttime_created: {now}', f'\ttime_modified: {now}', f'\tname: {name}', f'\tcasting_cost: {cost}',
        f'\timage: {image_map.get(filename, "")}', '\timage_2: ', '\tmainframe_image: ', '\tmainframe_image_2: ',
        f'\tsuper_type: {rich_type(typ)}', f'\tsub_type: {rich_subtype(subtype)}', f'\trarity: {rarity}', '\trule_text:',
    ]
    lines += [f'\t\t{r}' for r in rules]
    lines.append('\tflavor_text: <i-flavor></i-flavor>')
    if power or toughness:
        lines += [f'\tpower: {power}', f'\ttoughness: {toughness}']
    lines.append(f'\tcard_code_text: {i:03d}/{len(cards):03d} C')
    (project / filename).write_text('\n'.join(lines) + '\n', encoding='utf-8')

set_text = (project / 'set').read_text(encoding='utf-8-sig')
start = set_text.index('include_file:')
end = set_text.index('version_control:')
include_lines = ''.join(f'include_file: {c[0]}\n' for c in cards)
(project / 'set').write_text('\ufeff' + set_text[:start] + include_lines + set_text[end:], encoding='utf-8')
print(f'updated {len(cards)} Burning Abyss cards')
