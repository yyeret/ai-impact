"""Exercise attribution validation against an isolated skill installation."""

import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts import validate_skills


class AttributionValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skills = self.root / "skills"
        self.skill = self.skills / "example" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        source_root = Path(__file__).resolve().parents[1]
        for rel in (
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
            ".codex-plugin/plugin.json",
            ".agents/plugins/marketplace.json",
        ):
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_root / rel, target)
        for name in ("README.md", "CREDITS.md", "LICENSE", "LICENSE-CODE"):
            (self.root / name).write_text("Fixture\n", encoding="utf-8")

    def validate(self, section):
        self.skill.write_text(
            "---\nname: example\ndescription: Example for validation.\n"
            "metadata:\n  tags: product-strategy\n  version: 1.0.0\n---\n"
            "\n# Example\n\n" + section + "\n",
            encoding="utf-8",
        )
        errors = io.StringIO()
        with (
            patch.object(validate_skills, "ROOT", self.root),
            patch.object(validate_skills, "SKILLS", self.skills),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(errors),
        ):
            status = validate_skills.main()
        return status, errors.getvalue()

    def test_existing_source_heading_is_supported(self):
        self.assertEqual(self.validate("## Source\n\nOriginal methods.")[0], 0)

    def test_references_inspiration_credits_heading_is_supported(self):
        self.assertEqual(
            self.validate("## References/Inspiration/Credits\n\nOriginal methods.")[0],
            0,
        )

    def test_missing_attribution_is_rejected(self):
        status, errors = self.validate("## Workflow\n\nDo the work.")
        self.assertEqual(status, 1)
        self.assertIn("example:", errors)

    def test_heading_mentioned_in_prose_is_not_a_section(self):
        for heading in ("Source", "References/Inspiration/Credits"):
            with self.subTest(heading=heading):
                status, _ = self.validate(f"This mentions ## {heading} in prose.")
                self.assertEqual(status, 1)


if __name__ == "__main__":
    unittest.main()
