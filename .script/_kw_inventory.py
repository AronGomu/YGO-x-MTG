# -*- coding: utf-8 -*-
import re
import collections
from pathlib import Path

root = Path(__file__).resolve().parents[1]
docs = root / "docs"
mse_root = root / "MSE_projects"

GLOBAL = {
    "On Enter": "event",
    "On Attack": "event",
    "On Block": "event",
    "On Blocked": "event",
    "On Attack / Block": "event",
    "On Link Summon": "event",
    "On Fusion Summon": "event",
    "On Leave Field": "event",
    "On Upkeep": "event",
    "On End Step": "event",
    "This turn On End Step": "delayed-event",
    "On Block / Blocked": "event",
    "On Opponent Creature Enter": "event",
    "Bounce": "action",
    "Negate": "action",
    "Negate & Destroy": "action",
    "Grave": "zone",
    "Set": "action",
    "Indestructible": "static",
    "Alternative Cost": "cost-label",
    "On Cast": "event-family",
    "On Opponent Cast": "event-family",
    "On Any Cast": "event-family",
    "On Opponent Summon": "event",
    "On Send Grave": "event",
    "On Send Grave by Effect": "event",
    "On Creature you Control Destroy": "event",
    "On Destroy": "event",
    "On Exile": "event",
    "On Sacrifice": "event",
    "Detach X": "action/cost",
    "Mill X": "action",
    "Summon": "action",
    "Reanimate": "action",
    "Exile from Grave": "activation",
    "Attach": "action",
    "Bounded X": "static",
    "Indestructible des Effets": "static",
    "Défense talismanique": "static",
    "Slow Blink X Any Creature": "action",
    "Ritual Summon": "summon-procedure",
    "Fusion Summon": "summon-procedure",
    "Flip": "event/mechanic",
}

ARCH = {
    "Burning Abyss": {
        "Descente": "docs/10_archetype_burning_abyss.md",
        "Malédiction abyssale": "docs/10_archetype_burning_abyss.md",
    },
    "Shaddoll": {
        "Flip": "docs/11 + global 02",
        "Shaddoll Recovery": "docs/11_archetype_shaddoll.md",
    },
    "Necroz": {
        "Nekroz Recovery": "docs/12_archetype_necroz.md",
    },
    "Spellbook": {
        "Spell Affinity": "docs/13_archetype_spellbook.md",
    },
}

EVERGREEN = {
    "Piétinement",
    "Vol",
    "Vigilance",
    "Lien de vie",
    "Menace",
    "Initiative",
    "Portée",
    "Touche-à-tout",
    "Défenseur",
    "Double initiative",
    "Célérité",
    "Ralliement",
    "Protection",
}

NOISE = {
    "Negate la",  # partial French fragment, not Negate keyword
    "Indestructibles",
    "bounded",
    "Ritual",
    "Xyz",
    "Synchro",
    "Link",
    "Noir",
    "Bleu",
}

pat_b = re.compile(r"<b>([^<]+)</b>")
usage = collections.defaultdict(lambda: collections.Counter())
cards_using = collections.defaultdict(set)

for card in sorted(mse_root.rglob("card *")):
    if not card.is_file() or "French" in card.parts:
        continue
    try:
        t = card.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    proj = card.parent.name
    short = re.sub(r"^\d+_YGO_", "", proj).replace(".mse-set", "")
    rules = []
    for m in re.finditer(r"rule_text(?:_\d+)?:\s*(.*?)(?=^\t[a-z_]+:|\Z)", t, re.M | re.S):
        rules.append(m.group(1))
    body = "\n".join(rules) if rules else t
    for m in pat_b.finditer(body):
        k = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(".,;:")
        if not k or len(k) > 55:
            continue
        if k.lower() in ("i", "b"):
            continue
        usage[short][k] += 1
        cards_using[k].add(f"{short}/{card.name}")


def match_status(k: str):
    if k in GLOBAL:
        return "GLOBAL", GLOBAL[k]
    for g, t in GLOBAL.items():
        if g.lower() == k.lower():
            return "GLOBAL", t
    if re.match(r"^(Detach) (\d+|X)$", k):
        return "GLOBAL", "action/cost (Detach X)"
    if k == "Mill":
        return "GLOBAL", "use Mill 1 (never bare Mill)"
    if re.match(r"^(Mill) (\d+|X|0–\d+)$", k, re.I):
        return "GLOBAL", "action (Mill X)"
    if re.match(r"^(Bounded) (\d+|X)$", k, re.I):
        return "GLOBAL", "static (Bounded X)"
    if re.match(r"^Slow Blink (\d+|X) Any Creature$", k):
        return "GLOBAL", "action"
    if re.match(r"^Detach \d+ et Mill \d+$", k):
        return "GLOBAL", "compound Detach+Mill"
    if k.startswith(("On Cast", "On Opponent Cast", "On Any Cast")):
        return "GLOBAL", "event-family (On Cast)"
    if " OR " in k and k.startswith("On "):
        return "GLOBAL", "combined event keywords"
    for arch, kws in ARCH.items():
        for ak, src in kws.items():
            if ak.lower() == k.lower():
                return f"ARCH:{arch}", src
    if k in EVERGREEN or k.lower() in {e.lower() for e in EVERGREEN}:
        return "EVERGREEN-MTG", "context.md evergreen line"
    if (
        k.lower().startswith("coût alternatif")
        or k.lower().startswith("cout alternatif")
        or k.lower() == "alternative cost"
    ):
        return "GLOBAL", "cost-label (Alternative Cost / Coût alternatif)"
    return "UNDOCUMENTED", ""


all_k = collections.Counter()
by_arch = collections.defaultdict(collections.Counter)
for short, ctr in usage.items():
    for k, c in ctr.items():
        all_k[k] += c
        by_arch[short][k] += c

lines = []
lines.append("# Keyword inventory — cards vs rules/docs")
lines.append("")
lines.append(
    "Source: bold `<b>…</b>` in canonical MSE `rule_text` under `MSE_projects/*.mse-set/`; frozen `MSE_projects/French/` is excluded."
)
lines.append(
    "Rules: `docs/context.md`, `docs/02_rules_keywords_card_design.md`, `docs/*_archetype_*.md`."
)
lines.append("")
lines.append("## Legend")
lines.append("")
lines.append("| Status | Meaning |")
lines.append("|--------|---------|")
lines.append("| GLOBAL | Defined in global rules (context / 02) |")
lines.append("| ARCH | Defined in archetype doc |")
lines.append("| EVERGREEN-MTG | Standard Magic keyword (not numbered passive) |")
lines.append("| LABEL | Structural label, not a game keyword |")
lines.append("| UNDOCUMENTED | Bold on cards, no matching definition found |")
lines.append("| NOISE | Likely bold markup accident / partial phrase |")
lines.append("")

lines.append("## Global keyword catalog (rules)")
lines.append("")
lines.append("| Keyword | Kind |")
lines.append("|---------|------|")
for k, t in sorted(GLOBAL.items(), key=lambda x: x[0].lower()):
    lines.append(f"| `{k}` | {t} |")

lines.append("")
lines.append("## Archetype keyword catalog (docs)")
lines.append("")
for arch, kws in ARCH.items():
    lines.append(f"### {arch}")
    lines.append("")
    lines.append("| Keyword | Doc |")
    lines.append("|---------|-----|")
    for k, d in kws.items():
        lines.append(f"| `{k}` | {d} |")
    lines.append("")

lines.append("## Keywords found on cards (MSE), by project")
lines.append("")

for short in sorted(by_arch.keys()):
    lines.append(f"### {short}")
    lines.append("")
    lines.append("| Count | Keyword | Status | Note |")
    lines.append("|------:|---------|--------|------|")
    for k, c in by_arch[short].most_common():
        if k in NOISE:
            st, note = "NOISE", "not a keyword"
        else:
            st, note = match_status(k)
        lines.append(f"| {c} | `{k}` | {st} | {note} |")
    lines.append("")

lines.append("## Master unique list + rules coverage")
lines.append("")
lines.append("| Keyword | Total hits | Status | Docs home |")
lines.append("|---------|----------:|--------|-----------|")
rows = []
for k, c in sorted(all_k.items(), key=lambda x: (-x[1], x[0].lower())):
    if k in NOISE:
        st, note = "NOISE", "—"
    else:
        st, note = match_status(k)
    rows.append((k, c, st, note))
    lines.append(f"| `{k}` | {c} | {st} | {note or '—'} |")

lines.append("")
lines.append("## Gaps: on cards but missing / weak in rules")
lines.append("")
gaps = [r for r in rows if r[2] == "UNDOCUMENTED"]
if not gaps:
    lines.append("_None._")
else:
    lines.append("| Keyword | Hits | Where used (sample) | Likely action |")
    lines.append("|---------|-----:|---------------------|---------------|")
    for k, c, st, note in gaps:
        sample = ", ".join(sorted(cards_using[k])[:4])
        if "Leave Field" in k or "Upkeep" in k:
            hint = "Pending rule_reviews Spellbook proposals"
        elif "Fusion Summon" in k and k.startswith("On"):
            hint = "Add event def next to On Link Summon"
        elif k == "On Block / Blocked":
            hint = "Normalize slash form or document"
        elif k.startswith("On Enter OR"):
            hint = "Allowed combined event keywords; OK if components defined"
        elif k == "Bounce":
            hint = "Should now match GLOBAL Bounce"
        else:
            hint = "Document or un-bold"
        lines.append(f"| `{k}` | {c} | {sample} | {hint} |")

lines.append("")
lines.append("## Documented global keywords with weak/no MSE hit")
lines.append("")


def has_use(g: str) -> bool:
    if all_k.get(g):
        return True
    if g == "Detach X" and any(re.match(r"^Detach ", kk) for kk in all_k):
        return True
    if g == "Mill X" and any(re.match(r"^Mill ", kk) for kk in all_k):
        return True
    if g == "Bounded X" and any(re.match(r"^Bounded ", kk, re.I) for kk in all_k):
        return True
    if g == "Slow Blink X Any Creature" and any(
        "Slow Blink" in kk for kk in all_k
    ):
        return True
    if g == "On Cast" and any(kk.startswith("On Cast") for kk in all_k):
        return True
    if g == "On Opponent Cast":
        return any(kk.startswith("On Opponent Cast") for kk in all_k)
    if g == "On Any Cast":
        return any(kk.startswith("On Any Cast") for kk in all_k)
    if g == "Défense talismanique" and any(
        "talismanique" in kk.lower() for kk in all_k
    ):
        return True
    if g == "On Attack" and any(
        kk == "On Attack" or kk.startswith("On Attack") for kk in all_k
    ):
        return True
    if g == "On Block" and any("Block" in kk for kk in all_k):
        return True
    return False


unused = [g for g in GLOBAL if not has_use(g)]
if unused:
    lines.append("Defined but not observed as bold on current MSE cards:")
    for g in sorted(unused):
        lines.append(f"- `{g}`")
else:
    lines.append(
        "_All global defs have at least a related card hit (or family variant)._"
    )

lines.append("")
lines.append("## Notes")
lines.append("")
lines.append(
    "1. Variable forms: `Detach 1/2`, `Mill 3`, `Bounded 1`, `Slow Blink 1 Any Creature` = instances of X-forms."
)
lines.append(
    '2. On Cast family: unqualified `On Cast "Spellbook"` is controller-scoped; `On Opponent Cast` and `On Any Cast` provide explicit alternate scopes.'
)
lines.append(
    "3. Spell Affinity lives in archetype doc 13; Book Affinity is retired and replaced by full Alternative Cost text."
)
lines.append(
    "4. Descente / Malédiction abyssale / Shaddoll Recovery / Nekroz Recovery: archetype-only."
)
lines.append(
    "5. Case drift: `Défense Talismanique` vs `Défense talismanique`."
)
lines.append(
    "6. Piétinement: evergreen MTG; print alone, not numbered passive."
)
lines.append(
    "7. Spellbook open proposals (`On Leave Field`, `On Upkeep`) already on MSE; now defined in global rules."
)
lines.append("")

report = "\n".join(lines)
out = root / "docs" / "_keyword_inventory_report.md"
out.write_text(report, encoding="utf-8")
print("wrote", out)
print("unique", len(all_k), "undoc", len(gaps))
