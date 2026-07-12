from pathlib import Path
import re, unicodedata

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / 'docs' / '10_archetype_burning_abyss.md'
PROJ = ROOT / 'MSE_projects' / 'YGO_Burning_Abyss.mse-set'

text = MD.read_text(encoding='utf-8')
old_images = {}
for f in PROJ.glob('card *'):
    t = f.read_text(encoding='utf-8-sig', errors='replace')
    name = re.search(r'(?m)^\s*name:\s*(.+)$', t)
    img = re.search(r'(?m)^\s*image:\s*([^\r\n]*)', t)
    if name and img and img.group(1).strip() and not img.group(1).strip().startswith('image_2'):
        old_images[name.group(1).strip()] = img.group(1).strip()
# carry over renamed Dante image
old_images["Dante, Traveller of the Burning Abyss"] = old_images.get("Dante, Voyageur de l'Ab�me Ardent", '') or 'images/Burning_Abyss/dante_traveler_of_the_burning_abyss.jpg'

def clean_filename(name: str) -> str:
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().replace('&', 'and')
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return 'card ' + s

def mse_cost(cost: str) -> str:
    return cost.replace('{','').replace('}','')

def strip_md(s: str) -> str:
    s = s.strip()
    if s.startswith('*') and s.endswith('*') and not s.startswith('**'):
        return '<i>' + s[1:-1].strip() + '</i>'
    s = s.replace('**', '')
    return s.strip()

def parse_type(line: str):
    line = strip_md(line)
    if '—' in line:
        left, right = [x.strip() for x in line.split('—', 1)]
    else:
        left, right = line, ''
    if left.startswith('Créature'):
        super_type = 'Creature'
        extra = left.removeprefix('Créature').strip()
        sub = ' '.join(x for x in [extra, right] if x).strip()
    elif left.startswith('Éphémère'):
        super_type, sub = 'Instant', right
    else:
        super_type, sub = left, right
    return super_type, sub

sections = re.split(r'(?m)^##\s+', text)[1:]
cards = []
for sec in sections:
    title, body = sec.split('\n', 1)
    title = title.strip().split('=>', 1)[0].strip()
    if title in {'Identité de l\'archétype'}:
        continue
    if '**Coût :**' not in body:
        continue
    cost = re.search(r'\*\*Coût :\*\*\s*([^\n]+)', body).group(1).strip()
    after_cost = body.split('**Coût :**',1)[1].split('\n',1)[1]
    raw_lines = after_cost.splitlines()
    type_idx = next(i for i, l in enumerate(raw_lines) if l.strip())
    type_line = raw_lines[type_idx].strip()
    super_type, sub_type = parse_type(type_line)
    pt = re.search(r'\*\*(\d+)\s*/\s*(\d+)\*\*', body)
    power, toughness = (pt.group(1), pt.group(2)) if pt else ('','')
    # rules: everything after type line and optional P/T, excluding markdown separators
    lines = raw_lines[type_idx + 1:]
    rules = []
    for l in lines:
        l = strip_md(l)
        if not l or l == '---':
            if rules and rules[-1] != '':
                rules.append('')
            continue
        if re.fullmatch(r'\d+\s*/\s*\d+', l):
            continue
        if l.startswith('* '):
            l = '• ' + l[2:]
        rules.append(l)
    while rules and rules[-1] == '':
        rules.pop()
    cards.append((title, cost, super_type, sub_type, power, toughness, rules))

# remove old included card files to avoid stale/bad filenames
for f in PROJ.glob('card *'):
    f.unlink()

includes = []
for i, (name, cost, st, sub, power, toughness, rules) in enumerate(cards, 1):
    fn = clean_filename(name)
    includes.append(fn)
    image = old_images.get(name, '')
    if image and not (PROJ / image).exists():
        image = ''
    lines = [
        'mse_version: 2.5.8',
        'card:',
        '\thas_styling: false',
        '\tnotes: Source: 10_archetype_burning_abyss.md',
        '\ttime_created: 2026-07-10 23:49:32',
        '\ttime_modified: 2026-07-10 23:49:32',
        f'\tname: {name}',
        f'\tcasting_cost: {mse_cost(cost)}',
        f'\timage: {image}',
        '\timage_2: ',
        '\tmainframe_image: ',
        '\tmainframe_image_2: ',
        f'\tsuper_type: <word-list-type-en>{st}</word-list-type-en>',
        f'\tsub_type: <word-list-race-en>{sub}</word-list-race-en>',
        '\trarity: common',
        '\trule_text:',
    ]
    if rules:
        for r in rules:
            lines.append('\t\t' + r if r else '\t\t')
    else:
        lines.append('\t\t')
    lines += ['\tflavor_text: <i-flavor></i-flavor>']
    if power:
        lines += [f'\tpower: {power}', f'\ttoughness: {toughness}']
    lines.append(f'\tcard_code_text: {i:03d}/{len(cards):03d} C')
    (PROJ / fn).write_text('\n'.join(lines) + '\n', encoding='utf-8')

set_path = PROJ / 'set'
set_text = set_path.read_text(encoding='utf-8-sig')
set_text = re.sub(r'(?m)^include_file: card .+\n', '', set_text)
insert = ''.join(f'include_file: {fn}\n' for fn in includes)
set_text = set_text.replace('version_control:\n', insert + 'version_control:\n')
set_path.write_text('\ufeff' + set_text, encoding='utf-8')

print(f'Updated {len(cards)} Burning Abyss cards')
for fn in includes:
    print(fn)
