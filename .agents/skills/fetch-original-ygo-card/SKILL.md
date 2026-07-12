---
name: fetch-original-ygo-card
description: Fetches authoritative original Yu-Gi-Oh! card information from Konami's official Yu-Gi-Oh! Neuron card database and stores it as a typed markdown record under original_cards/. Use whenever the user asks to search, find, check, look up, research, or retrieve an original Yu-Gi-Oh! card, its stats, type, or effect text, and before converting a Yu-Gi-Oh! card for this project.
---

# Fetch Original Yu-Gi-Oh! Card

Use this project-specific skill from the `YGO-x-MTG` repository.

## Source of truth

Use the official Konami database in English:

```text
https://www.db.yugioh-card.com/yugiohdb/card_search.action?request_locale=en
```

Do not substitute converted MSE text, project docs, memory, fan wikis, or translated card text for the original card data. YGOPRODeck may only help canonicalize a misspelled name; verify and extract the final name, stats, property, and card text from the official Konami result.

## Workflow

1. Resolve the repository root with `git rev-parse --show-toplevel` and run all commands there.
2. Fetch the requested card and write or refresh its record:

```bash
python .script/generate_original_cards.py --card "CARD NAME"
```

3. Read the path printed by the command. It will be under exactly one of:
   - `original_cards/Effect Monster/`
   - `original_cards/Normal Monster/`
   - `original_cards/Ritual/`
   - `original_cards/Fusion/`
   - `original_cards/Synchro/`
   - `original_cards/Xyz/`
   - `original_cards/Link/`
   - `original_cards/Spell/`
   - `original_cards/Trap/`
4. Verify that the file includes the official name, card type, all applicable original stats, exact English card text, official source URL, database CID, and retrieval date.
5. Use that file as the source for the answer or for downstream conversion work.

## File rules

- The canonical destination is `original_cards`, not `originals_cards`.
- Use the official English card name as the heading and filename.
- On Windows, replace filename-forbidden characters deterministically while preserving the exact name in the H1: `:` becomes ` -`, `"` becomes `'`, slashes become ` - `, and `?*<>|` are removed or replaced.
- Refresh an existing matching record rather than creating a duplicate.
- Keep original Yu-Gi-Oh! text separate from Magic conversion text.

## Failure handling

- If exact lookup fails, use the script's fuzzy canonical-name fallback, then confirm the official result is the intended card.
- If the official site is temporarily unavailable, retry with backoff. Do not fabricate or write an unverified record.
- If multiple plausible cards remain, choose the exact archetype/name match supported by the user's request and report the assumption.

## Response

State the canonical card name and the `original_cards/.../*.md` path. Summarize requested facts from that file and link the official source already recorded there.
