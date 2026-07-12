from pathlib import Path
import re, unicodedata
from datetime import datetime

repo = Path(__file__).resolve().parents[1]
doc = repo / 'docs' / '11_archetype_shaddoll.md'
project = repo / 'MSE_projects' / 'YGO_Shaddoll.mse-set'
project.mkdir(parents=True, exist_ok=True)
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

TYPE_MAP = {
    'Creature': 'Creature',
    'Fusion Creature': 'Fusion Creature',
    'Sorcery': 'Sorcery',
    'Instant': 'Instant',
    'Enchantment': 'Enchantment',
    'Legendary Enchantment': 'Legendary Enchantment',
    'Enchantment Creature': 'Enchantment Creature',
}

def slug(s):
    s = unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode('ascii')
    s = re.sub(r'[^a-z0-9]+', ' ', s).strip()
    return 'card ' + re.sub(r'\s+', ' ', s)

def clean_md(s):
    s = s.strip()
    s = s.replace('**', '')
    s = s.replace('*', '')
    s = s.replace('_', '')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def rich_type(t):
    return f'<word-list-type-en>{t}</word-list-type-en>' if t else ''

def rich_subtype(s):
    if not s:
        return ''
    s = s.replace(' and ', ' et ')
    parts = [p.strip() for p in re.split(r'\s+et\s+', s) if p.strip()]
    out = f'<word-list-race-en>{parts[0]}</word-list-race-en>' if parts else ''
    for p in parts[1:]:
        out += f'<soft><atom-sep> </atom-sep></soft><word-list-class-en>{p}</word-list-class-en>'
    return out

def format_rule(line):
    is_italic = line.strip().startswith('*') and line.strip().endswith('*')
    line = clean_md(line)
    line = line.replace('Flip —', '<b>Flip</b> —')
    line = line.replace('Corruption —', '<b>Corruption</b> —')
    line = line.replace('Corruption (une seule fois par tour) —', '<b>Corruption</b> (une seule fois par tour) —')
    line = line.replace('Fusion —', '<b>Fusion</b> —')
    line = line.replace('On Send GY —', '<b>On Send GY</b> —')
    line = line.replace('On Send GY —', '<b>On Send GY</b> —')
    line = line.replace('On Send GY —', '<b>On Send GY</b> —')
    if is_italic:
        line = f'<i>{line}</i>'
    return line

text = doc.read_text(encoding='utf-8')
sections = re.split(r'(?m)^## ', text)
cards = []
for sec in sections[1:]:
    title, body = sec.split('\n', 1)
    if '=>' not in title:
        continue
    original, short = [x.strip() for x in title.split('=>', 1)]
    cost_line = next((l for l in body.splitlines() if 'Coût :' in l), '')
    cost = ''.join(re.findall(r'\{([^}]+)\}', cost_line))
    lines = [l.rstrip() for l in body.splitlines()]
    type_line = ''
    for l in lines:
        c = clean_md(l)
        if c in TYPE_MAP or c.startswith('Creature —') or c.startswith('Fusion Creature —') or c.startswith('Enchantment') or c in ('Instant','Sorcery'):
            type_line = c
            break
    if '—' in type_line:
        left, subtype = [x.strip() for x in type_line.split('—',1)]
    else:
        left, subtype = type_line, ''
    super_type = TYPE_MAP.get(left, left)
    power = toughness = ''
    stat_m = re.search(r'\*\*(\d+)\s*/\s*(\d+)\*\*', body)
    if stat_m:
        power, toughness = stat_m.groups()
    rule_lines = []
    skip_prefixes = ('**Coût', 'Creature', 'Fusion Creature', '**Sorcery**', '**Instant**', 'Sorcery', 'Instant', 'Enchantment', '**Statistiques', '**0 /', '**1 /', '**2 /', '**3 /', '**4 /', '**5 /')
    in_rules = False
    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped == '---':
            continue
        if stripped.startswith('**Coût') or ' / ' in stripped and stripped.startswith('**'):
            continue
        c = clean_md(stripped)
        if c == type_line or c == 'Statistiques à déterminer':
            continue
        if stripped.startswith('- '):
            if rule_lines:
                rule_lines[-1] += ' ' + clean_md(stripped[2:])
            continue
        # skip section title leftovers and pure labels already handled
        if c.startswith('#') or c == original or c == short:
            continue
        # Anything after type/stat/cost that is not metadata is rules text.
        if stripped.startswith('**') or stripped.startswith('*') or rule_lines or c.startswith(('Choisissez','Mettez','Si ','Une ','Lorsque','À chaque','Chaque','Tant ','Renvoyez','Depuis','Exilez','Envoyez','Puis','Au début','Pendant','Shaddoll Core','Il ne','Lorsqu')):
            rule_lines.append(format_rule(stripped))
    cards.append({
        'original': original, 'name': short, 'cost': cost, 'super_type': super_type,
        'subtype': subtype, 'power': power, 'toughness': toughness, 'rules': rule_lines,
    })

# clean old generated card files
for child in project.iterdir():
    if child.is_file() and child.name not in ('set', 'set.include_backup'):
        child.unlink()

include_names = []
for i, c in enumerate(cards, 1):
    fname = slug(c['original'])
    include_names.append(fname)
    lines = [
        'mse_version: 2.5.8', 'card:', '\thas_styling: false', '\tnotes: Source: 11_archetype_shaddoll.md',
        f'\ttime_created: {now}', f'\ttime_modified: {now}', f"\tname: {c['name']}", f"\tcasting_cost: {c['cost']}",
        '\timage: ', '\timage_2: ', '\tmainframe_image: ', '\tmainframe_image_2: ',
        f"\tsuper_type: {rich_type(c['super_type'])}", f"\tsub_type: {rich_subtype(c['subtype'])}", '\trarity: common', '\trule_text:',
    ]
    lines += [f'\t\t{r}' for r in c['rules'] if r]
    lines.append('\tflavor_text: <i-flavor></i-flavor>')
    if c['power'] or c['toughness']:
        lines += [f"\tpower: {c['power']}", f"\ttoughness: {c['toughness']}"]
    lines.append(f'\tcard_code_text: {i:03d}/{len(cards):03d} C')
    (project / fname).write_text('\n'.join(lines) + '\n', encoding='utf-8')

set_lines = [
    'mse_version: 2.0.2', 'game: magic', 'game_version: 2025-06-14', 'stylesheet: m15', 'stylesheet_version: 2024-05-26',
    'set_info:', '\ttitle: YGO x MTG -- Shaddoll', '\tdescription: Cartes personnalisées du cube Yu-Gi-Oh × Magic, générées depuis le projet Obsidian.',
    '\tartist: ', '\tcopyright: Fan-made custom cards for private cube playtesting', '\tset_code: YSH', '\tset_language: FR', '\tsymbol: ', '\tmasterpiece_symbol: ', '\tcard_language: French', '\tautomatic_reminder_text: ', '\tautomatic_copyright: yes', '\tautomatic_card_numbers: yes',
    'styling:', '\tmagic-m15:', '\t\ttext_box_mana_symbols: magic-mana-small.mse-symbol-font', '\t\toverlay: ',
]
set_lines += [f'include_file: {n}' for n in include_names]
set_lines += ['version_control:', '\ttype: none', 'apprentice_code: ']
(project / 'set').write_text('\n'.join(set_lines) + '\n', encoding='utf-8')
print(f'updated {len(cards)} Shaddoll cards')
