from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPDATE_RULES = ROOT / ".agents" / "skills" / "update-rules" / "SKILL.md"
VALIDATE_MSE = ROOT / ".agents" / "skills" / "validate-mse-updates" / "SKILL.md"
CONTEXT = ROOT / "docs" / "context.md"
RULES = ROOT / "docs" / "02_rules_keywords_card_design.md"
SHADDOLL = ROOT / "docs" / "11_archetype_shaddoll.md"


class UpdateRulesSkillTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = UPDATE_RULES.read_text(encoding="utf-8-sig")
        cls.validate_skill = VALIDATE_MSE.read_text(encoding="utf-8-sig")
        cls.context = CONTEXT.read_text(encoding="utf-8-sig")
        cls.rules = RULES.read_text(encoding="utf-8-sig")
        cls.shaddoll = SHADDOLL.read_text(encoding="utf-8-sig")

    def test_rule_skill_uses_a_markdown_review_gate_instead_of_questions(self) -> None:
        self.assertIn("rule_reviews/YYYY-MM-DD-<scope-slug>.md", self.skill)
        self.assertIn("## Ruling contradictions — pattern destroyers", self.skill)
        self.assertIn("## New possible rules — pattern makers", self.skill)
        self.assertIn("Status: AWAITING_USER", self.skill)
        self.assertIn("Status: READY", self.skill)
        self.assertIn("- Question: <the exact ruling choice", self.skill)
        self.assertIn("Answer directly in this Markdown file", self.skill)
        self.assertIn("Never use `AskUserQuestion`", self.skill)
        self.assertNotIn("Call `AskUserQuestion`", self.skill)

    def test_continue_resumes_the_review_without_another_interview(self) -> None:
        self.assertIn("## Phase 3 — Resume when the user says continue", self.skill)
        self.assertIn("use the exact review path generated earlier", self.skill)
        self.assertIn("Resume only when exactly one candidate exists", self.skill)
        self.assertIn("apply every completed item immediately without asking", self.skill)
        self.assertIn("Never poll or watch the review file", self.skill)

    def test_only_pattern_destroyers_and_makers_create_rule_items(self) -> None:
        self.assertIn("### Pattern destroyer", self.skill)
        self.assertIn("### Pattern maker", self.skill)
        self.assertIn("a one-card mechanic with no reusable syntax implication", self.skill)
        self.assertIn("Depuis votre GYD, exilez cette carte ; ...", self.skill)

    def test_general_and_archetype_rules_have_separate_owners(self) -> None:
        self.assertIn("docs/context.md` contient uniquement les règles générales", self.context)
        self.assertIn("Chaque archétype possède ses propres règles", self.context)
        self.assertNotIn("Les créatures Shaddoll conservent le type", self.context)
        self.assertIn("## Conventions propres à Shaddoll", self.shaddoll)
        self.assertIn("Les créatures Shaddoll conservent le type", self.shaddoll)
        self.assertIn("Les mécaniques, exceptions et valeurs propres à un archétype", self.rules)

    def test_psct_order_is_documented(self) -> None:
        for text in (self.context, self.rules):
            self.assertIn("Problem-Solving Card Text (PSCT)", text)
            self.assertIn("**mot-clé de condition** —", text)
            self.assertIn("coûts et cibles ;", text)
            self.assertIn("**On Send GYD** — Défaussez 1 carte", text)

    def test_validate_mse_waits_for_the_completed_review_file(self) -> None:
        self.assertIn("only pattern destroyers and pattern makers", self.validate_skill)
        self.assertIn("Status: READY", self.validate_skill)
        self.assertIn("Status: APPLIED", self.validate_skill)
        self.assertIn("accepted archetype/card change", self.validate_skill)
        self.assertIn("say `continue`", self.validate_skill)


if __name__ == "__main__":
    unittest.main()
