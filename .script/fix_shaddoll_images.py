from pathlib import Path
import re, urllib.parse, requests, time

ROOT = Path(__file__).resolve().parents[1] / 'MSE_projects'
PROJECTS = [ROOT / 'YGO_Shaddoll.mse-set', ROOT / 'YGO_Shaddoll_embedded.mse-set']
API = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name='

NAME_MAP = {
    'Shaddoll - Shadow Prison': 'Curse of the Shadow Prison',
    'Shaddoll - Anoyatyllis': 'El Shaddoll Anoyatyllis',
    'Shaddoll - Apkallone': 'El Shaddoll Apkallone',
    'Shaddoll - Construct': 'El Shaddoll Construct',
    'Shaddoll - El Fusion': 'El Shaddoll Fusion',
    'Shaddoll - Grysta': 'El Shaddoll Grysta',
    'Shaddoll - Shekhinaga': 'El Shaddoll Shekhinaga',
    'Shaddoll - Wendigo': 'El Shaddoll Wendigo',
    'Shaddoll - Winda': 'El Shaddoll Winda',
    'Shaddoll - Hollow': 'Helshaddoll Hollow',
    'Shaddoll - Ariel': 'Naelshaddoll Ariel',
    'Shaddoll - Aeon': 'Purushaddoll Aeon',
    'Shaddoll - Keios': 'Qadshaddoll Keios',
    'Shaddoll - Wendi': 'Reeshaddoll Wendi',
    'Shaddoll - Incarnation': 'Resh Shaddoll Incarnation',
    'Shaddoll - Beast': 'Shaddoll Beast',
    'Shaddoll - Core': 'Shaddoll Core',
    'Shaddoll - Dragon': 'Shaddoll Dragon',
    'Shaddoll - Falco': 'Shaddoll Falco',
    'Shaddoll - Fusion': 'Shaddoll Fusion',
    'Shaddoll - Hedgehog': 'Shaddoll Hedgehog',
    'Shaddoll - Hound': 'Shaddoll Hound',
    'Shaddoll - Schism': 'Shaddoll Schism',
    'Shaddoll - Squamata': 'Shaddoll Squamata',
    'Shaddoll - Sinister Shadow Games': 'Sinister Shadow Games',
}

def slug(s):
    return re.sub(r'_+', '_', re.sub(r'[^a-z0-9]+', '_', s.lower())).strip('_')

def name_of(text):
    m = re.search(r'(?m)^\s*name:\s*(.+)$', text)
    return m.group(1).strip() if m else None

def download(query, out):
    r = requests.get(API + urllib.parse.quote(query), timeout=30)
    r.raise_for_status()
    data = r.json()['data'][0]
    url = data['card_images'][0].get('image_url_cropped') or data['card_images'][0]['image_url']
    img = requests.get(url, timeout=45)
    img.raise_for_status()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(img.content)
    return data['name']

def set_image_in_text(text, rel):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r'^\s*image:\s*', line):
            indent = line.split('image:', 1)[0]
            lines[i] = f'{indent}image: {rel}'
            # remove accidental orphan image path line after image field, if present
            if i + 1 < len(lines) and re.match(r'^\s*images/', lines[i + 1]):
                del lines[i + 1]
            return '\n'.join(lines) + '\n'
    return text.rstrip() + f'\n\timage: {rel}\n'

errors = []
for project in PROJECTS:
    if not project.exists():
        continue
    img_dir = project / 'images' / 'Shaddoll'
    files = sorted(project.glob('card *'))
    for card in files:
        text = card.read_text(encoding='utf-8-sig', errors='replace')
        display = name_of(text)
        if not display:
            continue
        query = NAME_MAP.get(display, display)
        out = img_dir / f'{slug(query)}.jpg'
        if not out.exists():
            try:
                found = download(query, out)
                print(f'DOWNLOADED | {display} -> {found}')
                time.sleep(0.15)
            except Exception as e:
                errors.append(f'{display} -> {query}: {e}')
                print('ERROR | ' + errors[-1])
                continue
        rel = out.relative_to(project).as_posix()
        new = set_image_in_text(text, rel)
        if new != text:
            card.write_text(new, encoding='utf-8')
            print(f'LINKED | {card.relative_to(ROOT)} | {rel}')

if errors:
    raise SystemExit('\n'.join(errors))
