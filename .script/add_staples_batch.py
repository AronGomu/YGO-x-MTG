from pathlib import Path
import re, requests, shutil, time
from io import BytesIO
try:
    from PIL import Image
except Exception:
    Image = None

from original_image_assets import original_image_path

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
MSE=ROOT/'MSE_projects'

def slug(s): return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()

def fetch(name):
    for key in ('name','fname'):
        
        for attempt in range(4):
            try:
                r=requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php', params={key:name}, timeout=30)
                break
            except requests.RequestException:
                if attempt == 3: raise
                time.sleep(2+attempt)
        if r.ok and 'data' in r.json():
            data=r.json()['data']
            if key=='name': return data[0]
            low=name.lower()
            return next((c for c in data if c['name'].lower()==low), data[0])
    raise RuntimeError(name)

def image(data, out):
    out.parent.mkdir(exist_ok=True)
    if out.exists(): return
    url=data['card_images'][0].get('image_url_cropped') or data['card_images'][0].get('image_url')
    
    for attempt in range(4):
        try:
            b=requests.get(url, timeout=60).content; break
        except requests.RequestException:
            if attempt == 3: raise
            time.sleep(2+attempt)
    if Image:
        im=Image.open(BytesIO(b)).convert('RGB'); im.save(out)
    else:
        out.write_bytes(b)

def resize_cover(source, output, width=316, height=231):
    if Image is None:
        raise RuntimeError('Pillow is required to create MSE-resized artwork')
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as im:
        im = im.convert('RGB')
        scale = max(width / im.width, height / im.height)
        resized = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        left = (resized.width - width) // 2
        top = (resized.height - height) // 2
        resized.crop((left, top, left + width, top + height)).save(output, 'PNG')

def append_doc(doc, entries):
    p=DOCS/doc
    txt=p.read_text(encoding='utf-8')
    add=[]
    for e in entries:
        if f"#### {e['name']} =>" in txt: continue
        lines=[f"#### {e['name']} => {e['name']}","",f"**Coût :** {{{e['cost']}}}","",e['type'],"",f"**{e['pt']}**",""]
        if e.get('req'): lines += [f"*{e['req']}*",""]
        lines += e['rules'] + ["","---",""]
        add.append('\n'.join(lines))
    if add:
        txt=txt.rstrip()+"\n\n"+"\n".join(add)
        p.write_text(txt,encoding='utf-8')

def append_mse(project, source, entries):
    base=MSE/project; setp=base/'set'; txt=setp.read_text(encoding='utf-8-sig')
    n=len(re.findall(r'^include_file:', txt, re.M))
    added=[]
    for e in entries:
        fn='card '+slug(e['name'])
        existing_names='\n'.join([q.read_text(encoding='utf-8-sig', errors='ignore') for q in base.glob('card *')])
        if f'name: {e["name"]}' in existing_names: continue
        if (base/fn).exists() or f'include_file: {fn}' in txt: continue
        n+=1
        data=fetch(e['name'])
        source_image=original_image_path(data)
        image(data, source_image)
        resize_cover(source_image, base/'mse_images'/f'image{n}.png')
        rules=[]
        if e.get('req'): rules.append(f"\t\t<i>{e['req']}</i>")
        rules += ['\t\t'+r.replace('**','<b>',1).replace('**','</b>',1) if '**' in r else '\t\t'+r for r in e['rules']]
        power,tough=e['pt'].split(' / ')
        content=f"\ufeffmse_version: 2.5.8\ncard:\n\tstylesheet: kasu-eldrazi_750\n\tstylesheet_version: 2024-08-01\n\thas_styling: false\n\tnotes: Source: {source}\n\ttime_created: 2026-07-11 16:45:00\n\ttime_modified: 2026-07-11 16:45:00\n\tname: {e['name']}\n\tcasting_cost: {e['cost']}\n\timage: mse_images/image{n}.png\n\timage_2:\n\tmainframe_image:\n\tmainframe_image_2:\n\tsuper_type: <word-list-type-en>{e['type'].split(' — ')[0]}</word-list-type-en>\n\tsub_type: <word-list-race-en>{e['type'].split(' — ')[1] if ' — ' in e['type'] else ''}</word-list-race-en>\n\trarity: rare\n\trule_text:\n"+'\n'.join(rules)+f"\n\tflavor_text: <i-flavor></i-flavor>\n\tpower: {power}\n\ttoughness: {tough}\n\tcard_code_text: {n:03d}/030 R\n"
        (base/fn).write_text(content,encoding='utf-8')
        line=f"include_file: {fn}\n"
        if 'version_control:' in txt:
            txt=txt.replace('version_control:', line+'version_control:', 1)
        else:
            txt=txt.rstrip()+f"\n{line}"
        added.append(e['name'])
    setp.write_text('\ufeff'+txt.lstrip('\ufeff'),encoding='utf-8')
    return added

B={
'fusion':('05_fusion.md','YGO_Staples_Fusion.mse-set','05_fusion.md','Fusion — 2+ matériaux appropriés','Fusion Creature'),
'synchro':('06_synchro.md','YGO_Staples_Synchro.mse-set','06_synchro.md','Synchro — 1 Tuner + 1+ non-Tuner','Synchro Creature'),
'xyz':('07_xyz.md','YGO_Staples_Xyz.mse-set','07_xyz.md','Xyz 2','Xyz Creature'),
'link':('08_link.md','YGO_Staples_Link.mse-set','08_link.md',None,'Link Lvl 2+ Creature'),
}
# concise hand-converted staple identities
fusion=[
('Starving Venom Fusion Dragon','B','Fusion Creature — Dragon','3 / 2','Fusion — 2 créatures DARK', ['(1 - Déclenchable) Si Starving Venom arrive, il gagne la force d’une créature adverse jusqu’à la fin du tour.','(2 - Déclenchable) Si Starving Venom meurt, détruisez toutes les créatures invoquées spécialement adverses.']),
('Predaplant Triphyoverutum','G','Fusion Creature — Plant','3 / 3','Fusion — 3 créatures DARK', ['(1 - Passif) Triphyoverutum gagne +1/+1 pour chaque créature avec un marqueur Predator.','(2 - Activable Flash Soft) Contrecarrez l’invocation d’une créature depuis l’extra deck.']),
('Chimeratech Fortress Dragon','B','Fusion Creature — Machine','3 / 3','Fusion — Cyber Dragon + 1+ Machine', ['(1 - Passif) Vous pouvez utiliser les Machines adverses comme matériaux.','(2 - Passif) Fortress gagne +1/+1 pour chaque matériau utilisé.']),
('Chimeratech Megafleet Dragon','B','Fusion Creature — Machine','3 / 2','Fusion — Cyber Dragon + 1+ créatures dans une zone extra', ['(1 - Passif) Vous pouvez utiliser les créatures adverses dans une zone extra comme matériaux.','(2 - Passif) Megafleet gagne +1/+0 pour chaque matériau utilisé.']),
('El Shaddoll Winda','B','Fusion Creature — Wizard','2 / 2','Fusion — 1 Shaddoll + 1 DARK', ['(1 - Passif) Chaque joueur ne peut invoquer spécialement qu’une fois par tour.','(2 - Déclenchable) **On Send Grave** — Renvoyez une carte Shaddoll depuis votre Grave dans votre main.']),
('Guardian Chimera','B','Fusion Creature — Beast','3 / 3','Fusion — 3 créatures avec des noms différents', ['(1 - Déclenchable) Si Guardian Chimera arrive, piochez deux cartes puis détruisez jusqu’à deux cartes ciblées.','(2 - Passif) Tant que vous avez une carte Fusion dans votre Grave, Guardian Chimera a ward 2.']),
('Naturia Exterio','G','Fusion Creature — Beast','3 / 3','Fusion — Naturia Beast + Naturia Barkion', ['(1 - Activable Flash) Exilez une carte de votre Grave : contrecarrez un sort non-créature ou une capacité non-créature ciblé.']),
('Invoked Mechaba','W','Fusion Creature — Machine','3 / 2','Fusion — Aleister + 1 LIGHT', ['(1 - Activable Flash Soft) Défaussez-vous d’une carte qui partage un type avec un sort ou une capacité ciblé : contrecarrez-le et exilez-le.']),
('Invoked Caliga','B','Fusion Creature — Beast','1 / 2','Fusion — Aleister + 1 DARK', ['(1 - Passif) Chaque joueur ne peut activer qu’une capacité de créature par tour.','(2 - Passif) Chaque joueur ne peut attaquer qu’avec une créature par combat.']),
('Invoked Purgatrio','R','Fusion Creature — Fiend','3 / 1','Fusion — Aleister + 1 FIRE', ['(1 - Passif) Menace.','(2 - Passif) Purgatrio gagne +1/+0 pour chaque carte adverse et peut attaquer chaque créature adverse.']),
('Thunder Dragon Colossus','W','Fusion Creature — Thunder','3 / 2','Fusion — 1 Thunder Dragon', ['(1 - Passif) Les adversaires ne peuvent pas chercher dans leur bibliothèque sauf en piochant.','(2 - Passif) Si Colossus devait être détruit, exilez une créature Thunder de votre Grave à la place.']),
('Thunder Dragon Titan','R','Fusion Creature — Thunder','3 / 3','Fusion — 3 créatures Thunder', ['(1 - Déclenchable Soft) Si vous activez une capacité Thunder, détruisez une carte ciblée.','(2 - Passif) Si Titan devait être détruit, exilez deux cartes de votre Grave à la place.']),
('Albion the Branded Dragon','W','Fusion Creature — Dragon','2 / 2','Fusion — Fallen of Albaz + 1 LIGHT', ['(1 - Déclenchable) Si Albion arrive, vous pouvez invoquer une Fusion Creature depuis votre extra deck en exilant ses matériaux depuis votre main, champ de bataille ou Grave.','(2 - Déclenchable) **On Send Grave** — Cherchez une carte Branded.']),
('Mirrorjade the Iceblade Dragon','B','Fusion Creature — Wyrm','3 / 3','Fusion — Fallen of Albaz + 1 Fusion/Synchro/Xyz/Link', ['(1 - Activable Flash Soft) Envoyez une Fusion Creature depuis votre extra deck au Grave : exilez une créature ciblée.','(2 - Déclenchable) Si Mirrorjade quitte le champ de bataille, détruisez les créatures adverses à la prochaine étape de fin.']),
('First of the Dragons','W','Fusion Creature — Dragon','3 / 3','Fusion — 2 Normal Creatures', ['(1 - Passif) First of the Dragons a indestructible contre les créatures non-Normal et les sorts non-créature adverses.']),
('Grapha, Dragon Overlord of Dark World','B','Fusion Creature — Fiend','3 / 3','Fusion — Grapha + 1 DARK', ['(1 - Activable Flash Soft) Quand un adversaire active un sort ou une capacité, transformez son effet en « votre adversaire se défausse d’une carte ».','(2 - Déclenchable) Si Grapha quitte le champ de bataille, renvoyez une créature Dark World depuis votre Grave.']),
]

def E(rows, default_req, default_type): return [{'name':n,'cost':c,'type':t,'pt':pt,'req':req,'rules':r} for n,c,t,pt,req,r in rows]
# Other categories use compact generic conversions
synchro_names=['Trishula, Dragon of the Ice Barrier','Swordsoul Supreme Sovereign - Chengying','Swordsoul Grandmaster - Chixiao','Draco Berserker of the Tenyi','F.A. Dawn Dragster','T.G. Hyper Librarian','Naturia Beast','Naturia Barkion','Ancient Fairy Dragon','Adamancipator Risen - Dragite','Hot Red Dragon Archfiend Abyss','Red Supernova Dragon','Shooting Riser Dragon','Martial Metal Marcher','Denglong, First of the Yang Zing','Black Rose Moonlight Dragon','Clear Wing Synchro Dragon','Scarlight Red Dragon Archfiend']
synchro=[]
for n in synchro_names:
    synchro.append((n,'G','Synchro Creature — Dragon' if 'Dragon' in n or 'Trishula' in n else 'Synchro Creature — Warrior','3 / 2','Synchro — 1 Tuner + 1+ non-Tuner',[f'(1 - Déclenchable) Si {n.split(",")[0]} arrive, appliquez son effet de contrôle principal adapté au plateau.',f'(2 - Activable Flash Soft) Exilez ou recyclez une ressource liée à {n.split(",")[0]}.']))
xyz_names=['Tornado Dragon','Time Thief Redoer','Daigusto Emeral','Gagaga Cowboy','Number 39: Utopia','Number S39: Utopia the Lightning','Number 100: Numeron Dragon','Cyber Dragon Infinity','Cyber Dragon Nova','Constellar Pleiades','Toadally Awesome','Traptrix Rafflesia','The Phantom Knights of Break Sword','Lyrilusc - Assembled Nightingale','Downerd Magician','Leviair the Sea Dragon','Beatrice, Lady of the Eternal','Number 75: Bamboozling Gossip Shadow']
xyz=[]
for n in xyz_names:
    xyz.append((n,'U','Xyz Creature — Machine' if 'Cyber' in n else 'Xyz Creature — Warrior','2 / 2','Xyz 2',[f'(1 - Activable Flash Soft) Détachez un matériau : appliquez l’effet signature de {n.split(":")[-1].strip()} sur une carte ciblée.',f'(2 - Déclenchable Soft) Quand {n.split(":")[-1].strip()} quitte le champ de bataille, recyclez une ressource liée à ses matériaux.']))
# Link cards are curated directly in the MSE project. Do not
# regenerate them here: most intentionally contain only a name and artwork.
link=[]

batches=[('05_fusion.md','YGO_Staples_Fusion.mse-set','05_fusion.md',E(fusion,None,None)),('06_synchro.md','YGO_Staples_Synchro.mse-set','06_synchro.md',E(synchro,None,None)),('07_xyz.md','YGO_Staples_Xyz.mse-set','07_xyz.md',E(xyz,None,None)),('08_link.md','YGO_Staples_Link.mse-set','08_link.md',E(link,None,None))]
for doc,proj,src,entries in batches:
    append_doc(doc, entries)
    added=append_mse(proj, src, entries)
    print(proj, len(added), added)
