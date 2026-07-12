from pathlib import Path
import re, urllib.parse, time
import requests

ROOT = Path(__file__).resolve().parent
API = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'

NAME_MAP = {
    'Burning Abyss - Alich': 'Alich, Malebranche of the Burning Abyss',
    'Burning Abyss - Barbar': 'Barbar, Malebranche of the Burning Abyss',
    'Burning Abyss - Cagna': 'Cagna, Malebranche of the Burning Abyss',
    'Burning Abyss - Calcab': 'Calcab, Malebranche of the Burning Abyss',
    'Burning Abyss - Cir': 'Cir, Malebranche of the Burning Abyss',
    'Burning Abyss - Draghig': 'Draghig, Malebranche of the Burning Abyss',
    'Burning Abyss - Farfa': 'Farfa, Malebranche of the Burning Abyss',
    'Burning Abyss - Graff': 'Graff, Malebranche of the Burning Abyss',
    'Burning Abyss - Libic': 'Libic, Malebranche of the Burning Abyss',
    'Burning Abyss - Rubic': 'Rubic, Malebranche of the Burning Abyss',
    'Burning Abyss - Scarm': 'Scarm, Malebranche of the Burning Abyss',
    'Burning Abyss - Dante': 'Dante, Traveler of the Burning Abyss',
    'Burning Abyss - Dante, Pilgrim': 'Dante, Pilgrim of the Burning Abyss',
    'Burning Abyss - Virgil': 'Virgil, Rock Star of the Burning Abyss',
    'Burning Abyss - Beatrice': 'Beatrice, Lady of the Eternal',
    'Burning Abyss - Cherubini': 'Cherubini, Ebon Angel of the Burning Abyss',
    'Burning Abyss - Fire Lake': 'Fire Lake of the Burning Abyss',
    'Burning Abyss - Good & Evil': 'Good & Evil in the Burning Abyss',
    'Burning Abyss - Malacoda': 'Malacoda, Netherlord of the Burning Abyss',
    'Burning Abyss - Terminus': 'The Terminus of the Burning Abyss',
    'Burning Abyss - Traveler': 'The Traveler and the Burning Abyss',
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
    'Shaddoll - Sinister Shadow Games': 'Sinister Shadow Games',
    'Comp�tence de Perc�e': 'Breakthrough Skill',
    'Corbeau D.D.': 'D.D. Crow',
    "Dispositif d'�vacuation Obligatoire": 'Compulsory Evacuation Device',
    'Double Tornade': 'Twin Twisters',
    'Enterrement Pr�cipit�': 'Foolish Burial',
    'Explosion Ail�e du Ph�nix': 'Phoenix Wing Wind Blast',
    'Fusion Instantan�e': 'Instant Fusion',
    'Gobelin Parvenu': 'Upstart Goblin',
    'Guide des Enfers': 'Tour Guide From the Underworld',
    'Hommage Torrentiel': 'Torrential Tribute',
    "Livre de l'�clipse": 'Book of Eclipse',
    'Livre de la Lune': 'Book of Moon',
    'Math�maticien': 'Mathematician',
    'Pr�paration des Rites': 'Preparation of Rites',
    'Renaissance du Monstre': 'Monster Reborn',
    'Super Polym�risation': 'Super Polymerization',
    'S�duction des T�n�bres': 'Allure of Darkness',
    'Trou Noir': 'Dark Hole',
    "Typhon d'Espace Mystique": 'Mystical Space Typhoon',
}

def slug(s):
    return re.sub(r'_+', '_', re.sub(r'[^a-z0-9]+', '_', s.lower())).strip('_')

def card_name(text):
    m = re.search(r'(?m)^\s*name:\s*(.+)$', text)
    return m.group(1).strip() if m else None

def fetch(query):
    for key in ('name', 'fname'):
        r = requests.get(API, params={key: query}, timeout=30)
        if r.status_code == 400:
            continue
        r.raise_for_status()
        data = r.json().get('data', [])
        if data:
            exact = [c for c in data if c['name'].lower() == query.lower()]
            return exact[0] if exact else data[0]
    raise RuntimeError(f'not found: {query}')

errors=[]
for project in sorted(ROOT.glob('*.mse-set')):
    orig = project / 'original_images'
    orig.mkdir(exist_ok=True)
    set_text = (project/'set').read_text(encoding='utf-8-sig', errors='replace') if (project/'set').exists() else ''
    includes = re.findall(r'(?m)^include_file:\s*(.+)$', set_text)
    card_files = [project/i.strip() for i in includes] if includes else list(project.glob('card *'))
    for card_file in card_files:
        if not card_file.exists():
            continue
        text = card_file.read_text(encoding='utf-8-sig', errors='replace')
        display = card_name(text)
        if not display:
            continue
        query = NAME_MAP.get(display, display)
        out = orig / f'{slug(query)}.jpg'
        if out.exists():
            continue
        try:
            data = fetch(query)
            url = data['card_images'][0].get('image_url_cropped') or data['card_images'][0]['image_url']
            img = requests.get(url, timeout=45)
            img.raise_for_status()
            out.write_bytes(img.content)
            print(f'DOWNLOADED | {project.name} | {display} -> {data["name"]}')
            time.sleep(0.1)
        except Exception as e:
            errors.append(f'{project.name} | {display} -> {query}: {e}')
            print('ERROR | ' + errors[-1])
    print(f'{project.name}: original_images={len(list(orig.glob("*")))}')
if errors:
    print('\nFAILED:')
    for e in errors:
        print('- ' + e)
    raise SystemExit(1)
