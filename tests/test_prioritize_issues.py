"""Tests for scripts/prioritize_issues.py."""

import json
import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

from scripts.prioritize_issues import (
    analyze_and_prioritize_issues,
    classify_issue_content,
    detect_repository,
    format_prioritized_report,
    main,
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
        # Outcome
        res = classify_issue_content(
            "Self-service onboarding flow",
            "Users can configure their own settings without engineering support.",
        )
        self.assertEqual(res["level"], "Outcome")
        self.assertFalse(res["defaulted"])

        # Impact
        res = classify_issue_content("Increase checkout conversion by 15%", "")
        self.assertEqual(res["level"], "Impact")

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

    def test_analyze_and_prioritize_ordering(self):
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

        summary = analyze_and_prioritize_issues(issues, stale_days_threshold=90, now=now)
        self.assertEqual(summary["total_open_issues"], 4)
        self.assertEqual(summary["counts_by_level"]["Outcome"], 1)
        self.assertEqual(summary["counts_by_level"]["Output"], 1)
        self.assertEqual(summary["counts_by_level"]["Activity"], 2)
        self.assertEqual(summary["stale_count"], 1)

        # Priority ordering: #103 (Outcome) should come before #101 (Output) and #102/#104 (Activity)
        ranked_numbers = [item["number"] for item in summary["items"]]
        self.assertEqual(ranked_numbers[0], 103)
        self.assertEqual(ranked_numbers[1], 101)
        # Active Activity #102 should come before stale Activity #104
        self.assertEqual(ranked_numbers[2], 102)
        self.assertEqual(ranked_numbers[3], 104)

        # Check grouped structure
        self.assertEqual(len(summary["grouped"]["value_drivers"]), 1)
        self.assertEqual(summary["grouped"]["value_drivers"][0]["number"], 103)
        self.assertEqual(len(summary["grouped"]["deliverables"]), 1)
        self.assertEqual(summary["grouped"]["deliverables"][0]["number"], 101)
        self.assertEqual(len(summary["grouped"]["tasks_and_maintenance"]), 2)

    def test_format_prioritized_report(self):
        now = datetime(2026, 10, 26, 12, 0, 0, tzinfo=timezone.utc)
        issues = [
            {
                "number": 10,
                "title": "Reduce user onboarding drop-off",
                "body": "Users can complete onboarding with zero support tickets.",
                "updatedAt": "2026-10-25T10:00:00Z",
            }
        ]
        summary = analyze_and_prioritize_issues(issues, now=now)
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
            code = main(["--repo", "yyeret/ai-impact"])
            self.assertEqual(code, 0)
            mock_print.assert_called()
            output_text = mock_print.call_args[0][0]
            self.assertIn("Value Prioritization Report: yyeret/ai-impact", output_text)

        # Test json output
        with patch("builtins.print") as mock_print:
            code = main(["--repo", "yyeret/ai-impact", "--json"])
            self.assertEqual(code, 0)
            mock_print.assert_called()
            json_output = json.loads(mock_print.call_args[0][0])
            self.assertEqual(json_output["repository"], "yyeret/ai-impact")
            self.assertEqual(json_output["total_open_issues"], 1)
            self.assertEqual(json_output["items"][0]["number"], 5)


if __name__ == "__main__":
    unittest.main()
