from pathlib import Path
import re, unicodedata
from datetime import datetime

repo = Path(__file__).resolve().parents[1]
source_set = repo / 'mse' / 'set'
out_root = repo / 'MSE_projects'
out_root.mkdir(parents=True, exist_ok=True)

TYPE_MAP = {
    'Créature': 'Creature',
    'Rituel': 'Sorcery',
    'Éphémère': 'Instant',
    'Enchantement': 'Enchantment',
}
RARITY_CODE = {'common': 'C', 'uncommon': 'U', 'rare': 'R', 'mythic rare': 'M'}
PROJECTS = {
    # Shaddoll and Necroz are intentionally excluded: their checked-in MSE saves are the source of truth.
    '09_non_archetype_non_creature.md': (
        '09_YGO_Non_Archetype_Non_Creatures.mse-set',
        'YGO x MTG -- Non-archetype Non-creatures',
        'YNN',
    ),
    'docs/13_archetype_spellbook.md': ('13_YGO_Spellbook.mse-set', 'YGO x MTG -- Spellbook', 'YSB'),
}

def parse_blocks(text):
    blocks = re.split(r'(?m)^card:\n', text)[1:]
    cards = []
    for raw in blocks:
        block = 'card:\n' + raw
        fields = {}
        current = None
        for line in block.splitlines()[1:]:
            if line.startswith('\t') and not line.startswith('\t\t') and ':' in line:
                key, val = line[1:].split(':', 1)
                current = key
                fields[key] = val[1:] if val.startswith(' ') else val
            elif line.startswith('\t\t') and current:
                fields[current] += '\n' + line[2:]
        cards.append(fields)
    return cards

def include_name(name):
    cleaned = name.lower().replace('&', 'and')
    cleaned = unicodedata.normalize('NFKD', cleaned).encode('ascii', 'ignore').decode('ascii')
    cleaned = re.sub(r'[^a-z0-9]+', ' ', cleaned).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return f'card {cleaned}'

def rich_type(super_type):
    return f'<word-list-type-en>{super_type}</word-list-type-en>' if super_type else ''

def rich_subtype(sub_type):
    if not sub_type:
        return ''
    parts = [p.strip() for p in re.split(r'\s+et\s+|\s*[—-]\s*', sub_type) if p.strip()]
    if not parts:
        parts = [sub_type]
    first = f'<word-list-race-en>{parts[0]}</word-list-race-en>'
    rest = ''.join(f'<soft><atom-sep> </atom-sep></soft><word-list-class-en>{p}</word-list-class-en>' for p in parts[1:])
    return first + rest

KEYWORDS = [
    'Book Affinity',
    'Spell Affinity',
    'Malédiction abyssale, Descente',
    'Descente',
    'On Send Grave by Effect',
    'On Send Grave',
    'On Enter',
    'On Your Cast',
    'Flip',
    'Corruption',
    'Fusion Summon',
    'Fusion',
    'Xyz 2',
    'Xyz',
    'Synchro',
    'Rituel',
]

def bold_keywords(line):
    for keyword in KEYWORDS:
        if line == keyword:
            return f'<b>{keyword}</b>'
        for separator in (' —', ' -', ' :', ':'):
            if line.startswith(keyword + separator):
                return f'<b>{keyword}</b>{line[len(keyword):]}'
    return line

def emit_multiline(key, value):
    if not value:
        return [f'\t{key}: ']
    lines = [f'\t{key}:']
    for line in value.split('\n'):
        if line.strip():
            lines.append(f'\t\t{bold_keywords(line)}')
    return lines

def emit_card_file(project, card, idx, total, source_project_exists):
    name = card.get('name', '')
    filename = include_name(name)
    card_path = project / filename

    existing = (
        card_path.read_text(encoding='utf-8-sig', errors='replace')
        if card_path.exists()
        else ''
    )

    def existing_field(key):
        match = re.search(rf'(?m)^\t{re.escape(key)}:\s*(.*)$', existing)
        return match.group(1) if match else ''

    # Keep manual edits to Scarm's rules text; it was corrected directly in MSE by the user.
    existing_rule_text = None
    if name == 'Scarm, Burning Abyss' and existing:
        m = re.search(r'(?ms)^\trule_text:\s*\n((?:\t\t.*\n?)*)', existing)
        if m:
            existing_rule_text = m.group(1).rstrip('\n')

    rarity = card.get('rarity', 'common') or 'common'
    rarity_code = RARITY_CODE.get(rarity, 'C')
    card_type = TYPE_MAP.get(card.get('card type', ''), card.get('card type', ''))
    source_super_type = card.get('super type', '').strip()
    sub_type = card.get('sub type', '').strip()
    if sub_type == 'Piège':
        source_super_type = 'Trap'
        sub_type = ''
    super_type = ' '.join(part for part in (source_super_type, card_type) if part)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    card_stylesheets = {
        'Xyz': ('m15-spellbook', '2024-09-01'),
        'Synchro': ('m15-sketch', '2024-09-01'),
        'Fusion': ('genevensis-00-main', '2022-02-22'),
        'Link': ('m15-showcase-capenna-art-deco', '2024-10-01'),
        'Ritual': ('m15-showcase-praetor', '2024-09-01'),
    }
    card_style = None
    for key, style in card_stylesheets.items():
        if key.lower() not in super_type.lower():
            continue
        if key in {'Fusion', 'Ritual'} and 'creature' not in super_type.lower():
            continue
        card_style = style
        break
    lines = [
        'mse_version: 2.5.8',
        'card:',
    ]
    if card_style:
        lines += [f'\tstylesheet: {card_style[0]}', f'\tstylesheet_version: {card_style[1]}']
    lines += [
        '\thas_styling: false',
        f"\tnotes: Source: {card.get('notes', '').replace('Source: ', '')}",
        f'\ttime_created: {now}',
        f'\ttime_modified: {now}',
        f'\tname: {name}',
        f"\tcasting_cost: {card.get('casting cost','')}",
        f"\timage: {existing_field('image')}",
        f"\timage_2: {existing_field('image_2')}",
        f"\tmainframe_image: {existing_field('mainframe_image')}",
        f"\tmainframe_image_2: {existing_field('mainframe_image_2')}",
        f'\tsuper_type: {rich_type(super_type)}',
        f'\tsub_type: {rich_subtype(sub_type)}',
        f'\trarity: {rarity}',
    ]
    if existing_rule_text is not None:
        lines.append('\trule_text:')
        lines.extend(existing_rule_text.splitlines())
    else:
        lines.extend(emit_multiline('rule_text', card.get('rule text', '')))
    lines += [
        '\tflavor_text: <i-flavor></i-flavor>',
    ]
    if card.get('power') or card.get('toughness'):
        lines += [f"\tpower: {card.get('power','')}", f"\ttoughness: {card.get('toughness','')}"]
    lines.append(f'\tcard_code_text: {idx:03d}/{total:03d} {rarity_code}')
    card_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return filename

def emit_project(cards, dirname, title, code):
    project = out_root / dirname
    existed = project.exists()
    project.mkdir(parents=True, exist_ok=True)

    include_files = [emit_card_file(project, c, i, len(cards), existed) for i, c in enumerate(cards, 1)]
    for child in project.glob('card *'):
        if child.name not in include_files:
            child.unlink()
    lines = [
        '\ufeffmse_version: 2.0.2',
        'game: magic',
        'game_version: 2025-06-14',
        'stylesheet: sevenhalf',
        'stylesheet_version: 2024-05-30',
        'set_info:',
        f'\ttitle: {title}',
        '\tdescription: Cartes personnalisées du cube Yu-Gi-Oh × Magic, générées depuis le projet Obsidian.',
        '\tartist: ',
        '\tcopyright: Fan-made custom cards for private cube playtesting',
        f'\tset_code: {code}',
        '\tset_language: FR',
        '\tsymbol: ',
        '\tmasterpiece_symbol: ',
        '\tcard_language: French',
        '\tautomatic_reminder_text: ',
        '\tautomatic_copyright: yes',
        '\tautomatic_card_numbers: yes',
        'styling:',
        '\tmagic-m15:',
        '\t\ttext_box_mana_symbols: magic-mana-small.mse-symbol-font',
        '\t\toverlay: ',
    ]
    lines += [f'include_file: {f}' for f in include_files]
    lines += ['version_control:', '\ttype: none', 'apprentice_code: ']
    (project / 'set').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return project

cards = parse_blocks(source_set.read_text(encoding='utf-8'))
by_source = {src: [] for src in PROJECTS}
for c in cards:
    notes = c.get('notes', '')
    m = re.search(r'Source: ([^\n]+)', notes)
    if m and m.group(1) in by_source:
        by_source[m.group(1)].append(c)

for src, spec in PROJECTS.items():
    document = repo / src if src.startswith('docs/') else repo / 'docs' / src
    documented_names = {
        name.strip()
        for heading in re.findall(
            r'(?m)^#{2,4}\s+(.+?)\s*$',
            document.read_text(encoding='utf-8-sig'),
        )
        for name in heading.split('=>')
    }
    cards_for_project = sorted(
        (card for card in by_source[src] if card.get('name', '') in documented_names),
        key=lambda card: card.get('name', '').casefold(),
    )
    project = emit_project(cards_for_project, *spec)
    print(f'{project}: {len(cards_for_project)} cards')
