"""Tests for scripts/prioritize_issues.py."""

import json
import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

from scripts.prioritize_issues import (
    analyze_and_prioritize_issues,
    assess_goal_alignment,
    classify_issue_content,
    detect_repository,
    discover_repo_goals,
    format_prioritized_report,
    load_repo_goals,
    main,
    parse_goals_text,
    parse_repo_from_remote,
    fetch_open_issues,
)


class TestPrioritizeIssues(unittest.TestCase):
    def test_parse_repo_from_remote(self):
        self.assertEqual(
            parse_repo_from_remote("https://github.com/yyeret/ai-impact.git"),
            "yyeret/ai-impact",
        )
        self.assertEqual(
            parse_repo_from_remote("git@github.com:yyeret/ai-impact.git"),
            "yyeret/ai-impact",
        )
        self.assertEqual(
            parse_repo_from_remote("https://github.com/owner/sub-repo"),
            "owner/sub-repo",
        )
        self.assertIsNone(parse_repo_from_remote("https://gitlab.com/owner/repo.git"))
        self.assertIsNone(parse_repo_from_remote(""))

    def test_classify_issue_content_levels(self):
        # Outcome - SaaS phrasing
        res = classify_issue_content(
            "Self-service onboarding flow",
            "Users can configure their own settings without engineering support.",
        )
        self.assertEqual(res["level"], "Outcome")
        self.assertFalse(res["defaulted"])

        # Outcome - Generic title question / hook
        res = classify_issue_content(
            "AI Coding Made Code Review the Bottleneck. Now What?",
            "Analysis of review queue arrival rates.",
        )
        self.assertEqual(res["level"], "Outcome")

        # Outcome - Generic shift & JTBD
        res = classify_issue_content(
            "From Vibe Coding to Developing the Company",
            "JTBD: Reader delta shifts from babysitting prompt outputs to developing workflow specifications.",
        )
        self.assertEqual(res["level"], "Outcome")

        # Impact - Measuring business impact
        res = classify_issue_content(
            "You Can't Measure AI Impact If You Never Measured Delivery Before AI",
            "Baseline delivery metrics before AI adoption.",
        )
        self.assertEqual(res["level"], "Impact")

        # Outcome - Who can question and belief reframing
        res = classify_issue_content(
            "Who Can Actually Say No? AI Enablement Without Product Ownership",
            "Analysis of decision authority in product teams.",
        )
        self.assertEqual(res["level"], "Outcome")

        # Outcome - Friction constraint and bottleneck
        res = classify_issue_content(
            "My AI Bottleneck Wasn't Tokens. It Was Finishing.",
            "Finishing is the real flow constraint.",
        )
        self.assertEqual(res["level"], "Outcome")

        # Output
        res = classify_issue_content("Build CSV export dashboard modal", "")
        self.assertEqual(res["level"], "Output")
        self.assertIn("build", res["prescriptive_verbs"])

        # Activity - Bug
        res = classify_issue_content("fix: crash on empty profile payload", "")
        self.assertEqual(res["level"], "Activity")

        # Activity - Maintenance
        res = classify_issue_content("Upgrade dependencies and run regression tests", "")
        self.assertEqual(res["level"], "Activity")

        # Activity - Quarterly bucket
        res = classify_issue_content("FY26Q3 platform roadmap initiatives", "All key outputs")
        self.assertEqual(res["level"], "Activity")

        # Input
        res = classify_issue_content("Allocate headcount and contractor budget", "")
        self.assertEqual(res["level"], "Input")

        # Unknown / empty
        res = classify_issue_content("", "")
        self.assertEqual(res["level"], "Unknown")

    def test_parse_goals_and_alignment(self):
        goals_text = """
        # Project Goals & Strategy
        Our mission is to help engineering organizations scale AI and agentic workflows from activity to impact.
        ## Strategic Pillars
        - Developing the Factory: build repeatable spec-driven software factories.
        - Product Outcome Loop: focus on business metrics and user intent before code.
        - Flow at Agent Speed: manage review bottlenecks and WIP limits.
        """
        parsed = parse_goals_text(goals_text, source_name="README.md")
        self.assertIn("factory", parsed["keywords"])
        self.assertIn("bottlenecks", parsed["keywords"])
        self.assertIn("agentic", parsed["keywords"])
        self.assertIn("ai", parsed["keywords"])
        self.assertIn("wip", parsed["keywords"])

        # Test High Alignment Issue (Outcome aligned to factory/loop)
        high_align = assess_goal_alignment(
            "From Babysitting AI to Developing the Factory",
            "Observable delta: readers build repeatable spec-driven software factories instead of correcting prompts.",
            parsed,
        )
        self.assertEqual(high_align["alignment"], "High")
        self.assertIn("factory", high_align["matched_terms"])

        # Test Low Alignment Issue (Pre-AI generic topic)
        low_align = assess_goal_alignment(
            "Retro: Team retrospective templates for sprint 12",
            "Discussion points on team feelings and icebreakers.",
            parsed,
        )
        self.assertEqual(low_align["alignment"], "Low")

    @patch("subprocess.run")
    def test_discover_repo_goals_remote(self, mock_run):
        import base64
        readme_sample = b"# uv\nAn extremely fast Python package manager written in Rust.\n## Highlights\n- 10-100x faster than pip\n- Universal lockfile"
        b64_content = base64.b64encode(readme_sample).decode("utf-8")
        
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = b64_content

        goals = discover_repo_goals(repo="astral-sh/uv")
        self.assertIsNotNone(goals)
        self.assertIn("fast", goals["keywords"])
        self.assertIn("python", goals["keywords"])
        self.assertEqual(goals["source"], "remote:astral-sh/uv/README.md")

    def test_analyze_and_prioritize_with_goals_2d_grid(self):
        now = datetime(2026, 10, 26, 12, 0, 0, tzinfo=timezone.utc)
        goals = parse_goals_text(
            "Goals: Develop agentic software factory and optimize review bottlenecks.",
            source_name="GOALS.md",
        )

        issues = [
            {
                "number": 1,
                "title": "Build a generic database connector",  # Aligned? Low. Output.
                "body": "Implement mongo adapter.",
                "updatedAt": "2026-10-25T10:00:00Z",
            },
            {
                "number": 2,
                "title": "Develop agentic software factory specification",  # High align, Output
                "body": "Build the spec-driven framework for agents.",
                "updatedAt": "2026-10-24T10:00:00Z",
            },
            {
                "number": 3,
                "title": "Code review bottleneck: now what?",  # High align, Outcome
                "body": "Intent: Users can manage review bottlenecks under high agent PR volume.",
                "updatedAt": "2026-10-23T10:00:00Z",
            },
            {
                "number": 4,
                "title": "fix: crash in websocket ping",  # Activity
                "body": "Fix nil pointer exception.",
                "updatedAt": "2026-10-22T10:00:00Z",
            },
        ]

        summary = analyze_and_prioritize_issues(issues, repo_goals=goals, now=now)
        self.assertTrue(summary["has_goals"])

        # Verify P0 -> P1 -> P3 -> P4
        items_by_num = {it["number"]: it for it in summary["items"]}
        self.assertEqual(items_by_num[3]["priority_tier"], "P0")  # High + Outcome
        self.assertEqual(items_by_num[2]["priority_tier"], "P1")  # High + Output
        self.assertEqual(items_by_num[4]["priority_tier"], "P3")  # Activity
        self.assertEqual(items_by_num[1]["priority_tier"], "P4")  # Low align Output

        # Verify order: P0 (#3) comes first, then P1 (#2)
        ranked_numbers = [item["number"] for item in summary["items"]]
        self.assertEqual(ranked_numbers[0], 3)
        self.assertEqual(ranked_numbers[1], 2)

        # Check report formatting includes 2D sections
        report = format_prioritized_report(summary, repo_name="owner/repo")
        self.assertIn("P0: High-Leverage Strategic Value Drivers", report)
        self.assertIn("P1: Strategic Deliverables", report)
        self.assertIn("P4: Unanchored Outputs / Distractions", report)

    def test_analyze_and_prioritize_ordering_without_goals(self):
        now = datetime(2026, 10, 26, 12, 0, 0, tzinfo=timezone.utc)
        issues = [
            {
                "number": 101,
                "title": "Build user notification modal",
                "body": "Add a popup window.",
                "updatedAt": "2026-10-20T10:00:00Z",
                "createdAt": "2026-10-15T10:00:00Z",
                "labels": [{"name": "feature"}],
            },
            {
                "number": 102,
                "title": "Fix memory leak in websocket listener",
                "body": "Investigate heap dump.",
                "updatedAt": "2026-10-25T10:00:00Z",
                "createdAt": "2026-10-24T10:00:00Z",
                "labels": [{"name": "bug"}],
            },
            {
                "number": 103,
                "title": "Self-service team onboarding",
                "body": "Users can invite colleagues and get started in under 2 minutes.",
                "updatedAt": "2026-10-22T10:00:00Z",
                "createdAt": "2026-10-10T10:00:00Z",
                "labels": [{"name": "growth"}],
            },
            {
                "number": 104,
                "title": "Refactor legacy telemetry parser",
                "body": "Cleanup old functions.",
                "updatedAt": "2026-05-01T10:00:00Z",  # Stale (>90 days)
                "createdAt": "2026-04-01T10:00:00Z",
                "labels": [{"name": "tech-debt"}],
            },
        ]

        summary = analyze_and_prioritize_issues(issues, stale_days_threshold=90, repo_goals=None, now=now)
        self.assertEqual(summary["total_open_issues"], 4)
        self.assertEqual(summary["counts_by_level"]["Outcome"], 1)
        self.assertEqual(summary["counts_by_level"]["Output"], 1)
        self.assertEqual(summary["counts_by_level"]["Activity"], 2)
        self.assertEqual(summary["stale_count"], 1)

        # Priority ordering: #103 (Outcome) should come before #101 (Output) and #102/#104 (Activity)
        ranked_numbers = [item["number"] for item in summary["items"]]
        self.assertEqual(ranked_numbers[0], 103)
        self.assertEqual(ranked_numbers[1], 101)
        self.assertEqual(ranked_numbers[2], 102)
        self.assertEqual(ranked_numbers[3], 104)

    def test_format_prioritized_report_classic(self):
        now = datetime(2026, 10, 26, 12, 0, 0, tzinfo=timezone.utc)
        issues = [
            {
                "number": 10,
                "title": "Reduce user onboarding drop-off",
                "body": "Users can complete onboarding with zero support tickets.",
                "updatedAt": "2026-10-25T10:00:00Z",
            }
        ]
        summary = analyze_and_prioritize_issues(issues, repo_goals=None, now=now)
        report = format_prioritized_report(summary, repo_name="acme/platform")
        self.assertIn("Value Prioritization Report: acme/platform", report)
        self.assertIn("Tier 1: High-Leverage Value Drivers", report)
        self.assertIn("#10 [Outcome]: Reduce user onboarding drop-off", report)

    def test_fetch_open_issues_calls_gh_properly(self):
        fake_runner = MagicMock()
        fake_runner.return_value.returncode = 0
        fake_runner.return_value.stdout = json.dumps([
            {"number": 1, "title": "Test issue", "body": "details", "labels": []}
        ])

        results = fetch_open_issues(repo="owner/repo", limit=50, runner=fake_runner)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["number"], 1)

        called_cmd = fake_runner.call_args[0][0]
        self.assertIn("gh", called_cmd)
        self.assertIn("--limit", called_cmd)
        self.assertIn("50", called_cmd)
        self.assertIn("--repo", called_cmd)
        self.assertIn("owner/repo", called_cmd)

    def test_fetch_open_issues_error(self):
        fake_runner = MagicMock()
        fake_runner.return_value.returncode = 1
        fake_runner.return_value.stderr = "gh: command not found"

        with self.assertRaises(RuntimeError) as ctx:
            fetch_open_issues(repo="owner/repo", runner=fake_runner)
        self.assertIn("Failed to fetch issues", str(ctx.exception))

    @patch("scripts.prioritize_issues.fetch_open_issues")
    @patch("scripts.prioritize_issues.detect_repository")
    def test_main_cli_json_and_table(self, mock_detect, mock_fetch):
        mock_detect.return_value = "yyeret/ai-impact"
        mock_fetch.return_value = [
            {
                "number": 5,
                "title": "Improve team satisfaction through automated flow alerts",
                "body": "Users can see bottlenecks in slack.",
                "updatedAt": "2026-10-20T10:00:00Z",
                "labels": [],
            }
        ]

        # Test human-readable output
        with patch("builtins.print") as mock_print:
            code = main(["--repo", "yyeret/ai-impact", "--no-auto-goals"])
            self.assertEqual(code, 0)
            mock_print.assert_called()
            output_text = mock_print.call_args[0][0]
            self.assertIn("Value Prioritization Report: yyeret/ai-impact", output_text)

        # Test json output
        with patch("builtins.print") as mock_print:
            code = main(["--repo", "yyeret/ai-impact", "--json", "--no-auto-goals"])
            self.assertEqual(code, 0)
            mock_print.assert_called()
            json_output = json.loads(mock_print.call_args[0][0])
            self.assertEqual(json_output["repository"], "yyeret/ai-impact")
            self.assertEqual(json_output["total_open_issues"], 1)
            self.assertEqual(json_output["items"][0]["number"], 5)


if __name__ == "__main__":
    unittest.main()
