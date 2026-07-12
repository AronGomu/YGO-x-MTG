---
name: validate-mse-updates
description: Treat directly edited Magic Set Editor save files as the source of truth, reconcile their differences with YGO-x-MTG rules, delegate every proposed rule change to update-rules, correct language and MSE formatting, then synchronize docs, generators, tests, and related assets. Use when the user says they directly edited an MSE save/card/set file, asks to validate MSE updates, or invokes /skill:validate-mse-updates.
compatibility: YGO-x-MTG repository with Python 3 and a configured Magic Set Editor installation for final export validation.
metadata:
  project: YGO-x-MTG
---

# Validate MSE Updates

Reconcile hand-edited Magic Set Editor files into the rest of this repository. The newly edited MSE data is the **provisional source of truth**: preserve it unless the user explicitly classifies a difference as an editing error.

This workflow has two mandatory decision gates:

1. **Card-conflict interview** — semantic differences in the edited cards are classified as editing errors or accepted card/archetype changes.
2. **Rule-review file** — only pattern destroyers and pattern makers are delegated to `update-rules`, which writes a Markdown review file and pauses until the user completes it.

Use `AskUserQuestion` only for direct card-mechanic classifications, missing values, and mandatory Summon-permission rulings. Do not use it to approve general rules. Every picker that remains must have **Send a message** as its third option with custom text enabled. General rule decisions are completed exclusively in the review file created by `update-rules`.

## Project contracts

- MSE projects live in `MSE_projects/*.mse-set/` as folders, not zip archives.
- A project manifest is `MSE_projects/<project>.mse-set/set`.
- Cards are `card <slug>` files referenced by `include_file:` entries in `set`.
- `docs/context.md` contains general syntax, PSCT, formatting, vocabulary, and structural conventions that apply to every card.
- `docs/02_rules_keywords_card_design.md` details duplicated global card-design and templating rules.
- Numbered archetype documents own their archetype-specific mechanics, exceptions, and card values, and mirror the corresponding MSE project.
- Generator/update scripts under `.script/` must not be allowed to regenerate stale data over accepted MSE edits.
- Local MSE paths come from the gitignored `.env` through `mse_config.py`; never hardcode an installation path.
- Original source illustrations live under `assets/original_images/<archetype_ygo>/`, classified by actual Yu-Gi-Oh! archetype metadata; project-local `mse_images/` contains only imported/resized copies used by MSE cards.
- Preserve unrelated working-tree changes. Do not reset, checkout, or regenerate an entire project over hand edits.

## Phase 0 — Establish scope and protect the hand edit

1. Run:

   ```bash
   git status --short
   git diff --name-status -- MSE_projects
   git diff -- MSE_projects
   ```

2. If the user supplied paths, use those paths. Otherwise, scope to modified/untracked files beneath `MSE_projects/*.mse-set/`.
3. Separate files into:
   - manifest changes (`set`);
   - card data changes (`card *`);
   - image/art changes;
   - generated exports or temporary files.
4. Record the exact scoped paths before editing anything.
5. Read each changed MSE text file completely using `utf-8-sig` semantics. Preserve whether MSE-compatible UTF-8/BOM handling is needed.
6. Capture the pre-reconciliation diff as evidence. Do not make a backup inside an active `.mse-set` folder because nested backups can break MSE save validation.

If no MSE save file is modified or identified, stop and report that there is no direct MSE update to validate.

## Phase 1 — Read and analyze the updated MSE data

For every changed `set` and `card *` file, extract a normalized record without rewriting it:

- project and included card filename;
- `name`;
- casting cost;
- stylesheet/frame;
- super-type and subtype;
- material/invocation line;
- rule text and ability labels;
- power/toughness;
- rarity and card-code fields;
- image fields;
- any added, removed, or renamed cards;
- any newly introduced vocabulary, keyword, trigger, timing, zone, counter, or summoning rule.

Also verify structural invariants:

- every `include_file:` target exists;
- every card file is included exactly once;
- every non-empty image reference resolves inside the project;
- removed cards do not leave orphaned card files or card-specific images;
- card totals and `card_code_text*` totals agree where those fields are present;
- filenames and card names follow existing project conventions.

At this stage, report facts only. Do not “correct” a hand edit from memory.

## Phase 2 — Compare against established rules

Read these files completely before classifying differences:

- `docs/context.md`
- `docs/02_rules_keywords_card_design.md`
- the numbered document corresponding to the edited MSE project
- 2–3 sibling card files that demonstrate the relevant established pattern
- any `.script/` generator or updater that names the edited project/cards
- existing tests covering the affected project

Compare the MSE source against rules in these categories:

1. domain meaning and game mechanics;
2. keyword definitions and event timing;
3. ability labels (`Passif`, `Activable`, `Déclenchable`, `Soft`, `Hard`, `Hard Linked`);
4. invocation/material syntax;
5. zones and project vocabulary (`GY`, Extra Deck, terrain, etc.);
6. card type, Link Lvl, frame, and stylesheet mapping;
7. cost/stat conversion rules;
8. French grammar, spelling, punctuation, accents, and templating;
9. MSE file structure and reference integrity;
10. docs/generator/test assumptions that now disagree with the MSE data.

Before creating the difference ledger, detect every edited effect that would perform a normally illegal Summon, especially from the Sideboard without the required invocation method. For each affected card, call `AskUserQuestion` and ask whether to add `en ignorant les restrictions de Summon`. Offer exactly: **Add the explicit permission**, **Keep Summon restrictions**, and **Send a message** with custom text enabled. Never infer or insert the bypass silently. The permission makes the Summon legal but does not make it a correct invocation. Record the answer in the ledger.

Create a **difference ledger**. Each entry must contain:

- stable ID (`D1`, `D2`, ...);
- MSE evidence with `path:line`;
- conflicting rule or convention with `path:line`;
- concise explanation of the semantic difference;
- affected cards/files;
- proposed interpretations: `user error`, `accepted archetype/card change`, or `pattern destroyer`.

A card-specific cost, stat, type, effect, or archetype exception is not a general rule. Classify a difference as a `pattern destroyer` only when its syntax or templating contradicts a reusable project-wide convention.

Do not classify pure grammar/style errors as rule conflicts when the intended mechanic is unambiguous; queue those for Phase 5. If wording could change targeting, timing, cost, zone, optionality, frequency, or resolution, it is a semantic conflict and must enter the ledger.

## Phase 3 — Mandatory conflict interview

Interview every unresolved difference. Prefer one cohesive round containing several independent questions, but keep option labels and evidence short enough to understand.

For each ledger entry call `AskUserQuestion` with:

- the difference ID and affected card/rule;
- the MSE wording/value;
- the current documented rule;
- the concrete consequence of each answer;
- options:
  - **User error — restore the documented value**
  - **Accept card change — preserve MSE and update the archetype document**
  - **Send a message — provide context or revised wording**

Enable custom text. For **Send a message**, incorporate the message into the ledger evidence and ask the same three-option question again.

If the user chooses **User error**:

- mark the ledger entry `restore-rule`;
- later correct only the conflicting MSE value;
- do not change the governing rule because of this entry.

If the user chooses **Accept card change**:

- mark the entry `accept-card-change`;
- preserve the MSE mechanic;
- synchronize it to the owning numbered archetype document in Phase 6;
- separately classify its syntax as a pattern destroyer only if it contradicts a reusable general convention.

After each round, show unresolved IDs and continue interviewing. Phase 3 ends only when every ledger entry has an answer. Never infer an unanswered choice from another answer.

## Phase 4 — Delegate pattern destroyers

Do not delegate ordinary card or archetype changes. For every confirmed pattern destroyer, invoke:

```text
Skill(skill="update-rules", args="Pattern destroyer: <conflicting syntax>. Evidence: <difference ID, MSE card text, affected cards, current general rule>. normalize=false")
```

`update-rules` writes a Markdown review file under `rule_reviews/` and stops. Record its path and stop this workflow without making partial rule-dependent edits. Ask the user to complete every decision in that file, set `Status: READY`, and resume with:

```text
Skill(skill="update-rules", args="review_file=<path> normalize=false")
```

Continue only after the review file reaches `Status: APPLIED`. Rejected pattern changes return to Phase 3 if the provisional MSE syntax still contradicts the established general rule. Accepted archetype-only changes never edit `docs/context.md`.

For every `restore-rule` decision, defer the MSE correction to Phase 5 and leave rule docs unchanged.

## Phase 5 — Correct the edited MSE files

Apply two kinds of corrections:

1. The exact MSE corrections approved as `restore-rule`.
2. Mechanical language/style corrections that do not change mechanics.

Correct:

- French spelling, grammar, accents, agreement, and punctuation;
- established capitalization (`Link Lvl`, keyword names, zones);
- bold event keywords and em-dash formatting in MSE markup;
- ability-label typography;
- malformed MSE indentation/fields;
- stale counts and broken references caused by the direct edit.

Never silently change:

- targets versus non-targeting choices;
- costs versus effects;
- optional versus mandatory actions;
- timing or speed;
- zones;
- once-per-turn restrictions;
- card types, materials, colors, costs, or stats;
- the accepted meaning of a new keyword.

If a “grammar fix” could change any item above, add a new difference to the ledger and return to Phase 3.

Preserve non-content metadata and artwork unless the accepted update removes or replaces the card. For removals, delete only proven card-specific orphan assets after checking all references.

## Phase 6 — Synchronize docs and related files

Treat the reconciled MSE files as the final data source and update every consumer:

- corresponding numbered card document under `docs/`;
- rule docs already changed through `update-rules`; do not edit `docs/context.md` or `docs/02_rules_keywords_card_design.md` directly in this phase;
- project manifest `set` and card include order;
- card numbering/totals where present;
- `.script/` generators, batch lists, update scripts, and fixtures that could restore old data;
- tests and validation fixtures;
- indexes or cross-references that list removed/renamed cards;
- central source artwork under `assets/original_images/` and project-local resized files under `mse_images/` only when they are added, replaced, or proven orphaned.

When updating a card document:

- mirror MSE mechanics, cost, type, subtype, stats, material line, and rule text;
- use Markdown equivalents of MSE markup (`<b>` → `**`, `<i>` → `*`);
- retain document structure and project vocabulary;
- do not invent flavor text or mechanics absent from MSE.

Search globally for stale values and old names after synchronization.

## Phase 7 — Mine reconciled data for rule candidates

Analyze the final MSE data across the edited cards and relevant siblings. Find repeated or structurally meaningful patterns that are not yet captured clearly in `docs/context.md`.

A candidate must be a pattern maker, such as:

- a genuinely new keyword or event;
- an evolution/generalization of an existing global rule;
- a repeated templating convention;
- a consistent reusable PSCT process such as `Depuis votre GYD, exilez cette carte ; ...`;
- a project-wide frame/type/material mapping;
- a consistent grammar or zone convention shared across cards.

Do not propose as a rule:

- a one-card mechanic with no reusable design implication;
- a simple typo correction;
- a fact already stated clearly in current docs;
- an accidental pattern created only by blank/incomplete cards.

Create a **rule-candidate ledger** with IDs (`R1`, `R2`, ...), evidence (`path:line`), current rule if evolving one, proposed wording, scope, and exceptions.

If no candidates exist, explicitly report that and proceed to verification.

## Phase 8 — Mandatory pattern-maker review through update-rules

Delegate all pattern makers together when they belong to the same scope:

```text
Skill(skill="update-rules", args="Pattern makers: <candidate wording and evidence for each R ID>. normalize=false")
```

The delegated skill writes a Markdown review file under `rule_reviews/` and pauses. Stop this workflow until the user completes every item, sets `Status: READY`, and asks to continue. Resume `update-rules` with that file; continue this workflow only after it reaches `Status: APPLIED`.

Record accepted, revised, and rejected candidate IDs from the completed file. Do not add rejected candidates to project docs. After application, rescan the MSE data against the final rules; any new contradiction returns to Phase 3.

## Phase 9 — Verify

Run all applicable checks:

1. structural MSE validation (includes, card files, image references, card totals);
2. repository tests, including project-specific MSE tests;
3. Python compilation for changed scripts;
4. `git diff --check`;
5. stale-reference search for renamed/removed cards and superseded rule text;
6. MSE export using `MSE_CLI` loaded from `.env`, writing to a temporary directory outside the `.mse-set` folder;
7. confirm expected exported PNG count, then delete all temporary export/cache files.

Never hardcode `mse.exe` or `mse.com`. Load `MSEConfig` from `mse_config.py`. If `.env` is absent or invalid, instruct the user to run `python setup_mse.py`; do not guess an installation path.

Do not claim GUI save compatibility from CLI export alone. Report GUI Save/Save As as manual verification when it cannot be performed interactively.

## Final report

Report:

- MSE files treated as source of truth;
- card-conflict decisions (`restore-rule` versus `accept-card-change`) and any pattern-destroyer review IDs;
- grammar/style fixes that preserved mechanics;
- docs/scripts/tests/assets synchronized;
- accepted, revised, and rejected rule candidates;
- structural/test/export results;
- any manual GUI verification still required.

## Never

- Never overwrite direct MSE edits by regenerating from stale docs.
- Never update a disputed rule before its review file is complete and applied.
- Never edit a general project rule directly; every pattern destroyer or pattern maker must run through `update-rules`.
- Never place archetype-specific card facts in `docs/context.md`.
- Never silently treat a semantic discrepancy as grammar cleanup.
- Never leave a card-conflict ledger or rule-review file partially answered.
- Never update only the card doc while leaving generators or tests stale.
- Never leave orphan `include_file`, card, image, or numbering references.
- Never create backups, exports, or temporary files inside an active `.mse-set` folder.
- Never commit the local `.env`, MSE installation paths, or generated temporary exports.
