---
name: update-rules
description: Detect reusable card-text rule changes, write ruling contradictions and possible new rules to a Markdown review file, pause for the user to complete it, then apply only the completed decisions to the correct general or archetype documentation. Use when the user asks to add, change, refine, or update wording, grammar, typography, keywords, PSCT templating, or card-design rules.
compatibility: YGO-x-MTG repository with the normalize-card-formatting project skill.
metadata:
  project: YGO-x-MTG
---

# Update Rules

Review and evolve card-text rules without conducting an interactive interview. Never use `AskUserQuestion` in this workflow. Write every decision that genuinely needs a ruling to a Markdown review file, stop, and wait for the user to complete that file before continuing.

## Inputs

- New or revised wording, rule text, card evidence, or a completed review-file path.
- `normalize=true|false`; default: `false`.
- Optional `review_file=rule_reviews/<file>.md` when resuming.

## Rule-document scope

Keep general rules separate from archetype-specific design:

- `docs/context.md` contains only syntax, PSCT, formatting, vocabulary, and structural conventions that apply to every card in the project.
- `docs/02_rules_keywords_card_design.md` mirrors detailed global card-design and templating rules when the same global rule belongs there.
- Each archetype’s numbered document under `docs/` owns that archetype’s names, mechanics, card-specific exceptions, costs, stats, types, and effects. Do not promote those facts into `docs/context.md` unless they form a reusable project-wide pattern.

## What merits a rule review

Create a rule item only for a **pattern destroyer** or a **pattern maker**.

### Pattern destroyer

A pattern destroyer is syntax or templating for an effect that contradicts an established general rule. Examples:

- putting a target, cost, condition, timing, or resolution clause in the wrong PSCT segment;
- using a condition keyword in a position that conflicts with the canonical ability shape;
- introducing a second syntax for a process already standardized globally;
- breaking a project-wide capitalization, zone, punctuation, keyword, or frequency convention in a way that could be intentional.

A pattern destroyer is a ruling contradiction. The review must explain the existing pattern, the conflicting evidence, and the consequences of restoring or changing the pattern.

### Pattern maker

A pattern maker is a reusable convention that is not yet documented clearly. Examples:

- a new event or action keyword;
- a repeated, consistent way to express a process;
- a reusable PSCT clause such as `Depuis votre GYD, exilez cette carte ; ...`;
- a generalization that replaces several equivalent wordings with one stable form.

Prefer at least two supporting examples. A single example is allowed only when it introduces an explicit keyword or an obviously reusable process boundary.

### Not a rule item

Do not create a rule review item for:

- card balance, mana cost, color, stats, rarity, frame, or artwork;
- a one-card mechanic with no reusable syntax implication;
- an archetype-specific fact that belongs only in its numbered document;
- a simple typo, agreement, accent, punctuation, or unambiguous PSCT cleanup;
- a rule already stated clearly in the global docs.

Apply or report those changes through the owning card/archetype workflow instead.

## Phase 1 — Analyze

1. Read `docs/context.md` completely.
2. Read the relevant sections of `docs/02_rules_keywords_card_design.md`.
3. Read the affected archetype documents, included MSE card files, generators, and tests.
4. Search the repository for both the established pattern and the proposed pattern.
5. Classify every finding as:
   - `pattern-destroyer`;
   - `pattern-maker`;
   - `archetype-only`;
   - `mechanical-cleanup`;
   - `already-documented`.
6. Record exact `path:line` evidence and all impacted cards.

If there are no pattern destroyers or pattern makers, do not create a pending decision gate. Report that no general rule review is required and route archetype-only or mechanical work back to the owning workflow.

## Phase 2 — Generate the review file and stop

Create `rule_reviews/` if needed. Write a deterministic Markdown file named:

```text
rule_reviews/YYYY-MM-DD-<scope-slug>.md
```

If that path exists for a different review, append `-2`, `-3`, and so on. Never overwrite a user-completed review.

The file must use this structure:

```markdown
# Rule review — <scope>

- Status: AWAITING_USER
- Generated: YYYY-MM-DD
- Normalize after approval: false
- Source request: <concise request>

## How to complete this review

For every item, replace `TODO` with exactly one decision:

- `ACCEPT` — apply the proposed rule;
- `REJECT` — keep the current rule;
- `REVISE` — use the text in `Final wording`.

Do not remove IDs or evidence. When finished, change `Status` to `READY` and ask the agent to continue with this file.

## Ruling contradictions — pattern destroyers

### D1 — <title>

- Scope: general | <archetype document>
- Existing rule: <wording and path:line>
- Conflicting evidence: <card text and path:line>
- Why this destroys a pattern: <explanation>
- Impacted cards/files: <list>
- Proposed resolution: <smallest reusable resolution>
- Side effects: <meaning, targeting, cost, timing, zones, rendering, tests>
- Decision: TODO
- Final wording:
- Notes:

## New possible rules — pattern makers

### R1 — <title>

- Scope: general | <archetype document>
- Evidence: <examples with path:line>
- Existing rule: <rule if this evolves one, otherwise “None”>
- Proposed rule: <exact reusable wording>
- Boundary and exceptions: <scope limits>
- Impacted cards/files: <list>
- Side effects: <meaning, rendering, generators, tests>
- Decision: TODO
- Final wording:
- Notes:
```

Include `None.` under an empty section. Do not apply rules, normalize cards, or edit rule docs in this phase. Return only the review-file path, a count of pattern destroyers and pattern makers, and the instruction to set `Status: READY` after completing every decision. Then stop.

## Phase 3 — Resume from a completed review

When invoked with `review_file=...`, or when the user asks to continue a named review:

1. Read the whole review file.
2. Require `Status: READY`.
3. Require every `D*` and `R*` item to have `Decision: ACCEPT`, `REJECT`, or `REVISE`.
4. For every `REVISE`, require non-empty `Final wording`.
5. If anything is incomplete, do not ask questions and do not apply partial decisions. Report the unresolved IDs and stop.
6. Re-read current rules and evidence to ensure the review has not become stale. If evidence changed materially, add a `## Stale evidence` section, set `Status: NEEDS_REVISION`, and stop.

## Phase 4 — Apply completed decisions

For each completed item:

- `REJECT`: leave the current rule unchanged.
- `ACCEPT`: apply the exact proposed resolution/rule.
- `REVISE`: apply the exact `Final wording`.

Choose the owning document by scope:

- project-wide syntax, PSCT, formatting, vocabulary, or structural convention → `docs/context.md`, plus the corresponding statement in `docs/02_rules_keywords_card_design.md` when duplicated there;
- archetype-only mechanic, exception, or card convention → that archetype’s numbered document only;
- never add a card-specific fact to `docs/context.md` merely because one card uses it.

Replace the closest existing rule instead of appending a contradictory duplicate. Preserve unrelated working-tree changes.

If `normalize=true`, invoke `normalize-card-formatting` only for cards explicitly listed by accepted/revised items. If every included card in one project is impacted, pass the project folder once. If `normalize=false`, do not modify MSE cards.

## Phase 5 — Finalize and verify

1. Update the review file:
   - `Status: APPLIED`;
   - add `Applied: YYYY-MM-DD`;
   - append `## Application result` listing accepted, revised, rejected, skipped, and failed IDs.
2. Run `git diff --check`.
3. Rescan for stale old formatting and contradictory duplicate rules.
4. Run relevant tests and Python compilation for changed scripts.
5. Report:
   - review-file path;
   - rules changed and their owning documents;
   - accepted, revised, and rejected IDs;
   - impacted and normalized cards;
   - validation results.

## Never

- Never use `AskUserQuestion` for rule approval or classification.
- Never infer a decision from prose outside the completed review file once the gate has been created.
- Never continue while any review item is `TODO` or the status is not `READY`.
- Never place archetype-specific rulings in `docs/context.md`.
- Never create rule items for ordinary card data or mechanical cleanup.
- Never normalize cards before the review file is complete.
