#!/usr/bin/env python3
"""Prioritize repository open issues by value/outcome framing.

Can be run in any local git repository workspace with a GitHub origin,
or pointed at a remote repository with `--repo owner/name`.

Applies the Outcome Framing taxonomy (Input -> Activity -> Output -> Outcome -> Impact)
to classify open backlog items, identify prescriptive phrasing, and surface
high-leverage work.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

VERSION = "outcome-prioritize-1.0.0"
LEVELS = ["Impact", "Outcome", "Output", "Activity", "Input", "Unknown"]

QUARTERLY_BUCKET_RE = re.compile(
    r"^(FY\s*'?\d{2,4}\s*Q\d|Y\s*'?\d{2,4}\s*Q\d)",
    re.IGNORECASE,
)

INPUT_SIGNALS = [
    r"\bhiring\b",
    r"\bheadcount\b",
    r"\bstaffing\b",
    r"\bbudget\b",
    r"\bopex\b",
    r"\bcapex\b",
    r"\bresource allocation\b",
    r"\bonboarding\b",
]

ACTIVITY_SIGNALS = [
    r"\bbug\b",
    r"\bfix\b",
    r"\bfixes\b",
    r"\bfixed\b",
    r"\bqa\b",
    r"\bqat\b",
    r"\btest\b",
    r"\btesting\b",
    r"\bregression\b",
    r"\buat\b",
    r"\bspike\b",
    r"\bdiscovery\b",
    r"\bexplore\b",
    r"\bexploring\b",
    r"\btraining\b",
    r"\blearn\b",
    r"\bonboard\b",
    r"\bmaintenance\b",
    r"\bupgrade\b",
    r"\bupgrades\b",
    r"\bmigrate\b",
    r"\brefactor\b",
    r"\bdebug\b",
    r"\binvestigate\b",
    r"\breview\b",
    r"\bauditing\b",
    r"\bsupport\b",
    r"\bmeeting\b",
    r"\bgrooming\b",
    r"\bplanning\b",
    r"\bdeploy\b",
    r"\bdeployment\b",
    r"\bconfigure\b",
    r"\bsetup\b",
    r"\bset up\b",
    r"\bmonitor\b",
    r"\bmonitoring\b",
    r"\bscan\b",
    r"\bscanning\b",
    r"\bcleanup\b",
    r"\bcleaning\b",
    r"\bpatch\b",
    r"\bhardening\b",
    r"\bdevops\b",
    r"\bci\/cd\b",
    r"\bpipeline\b",
    r"\binfrastructure\b",
    r"\bsecurity\b",
    r"\bcompliance\b",
    r"\bingest\b",
    r"\bingestion\b",
    r"\bimport\b",
    r"\bexport\b",
    r"\bextract\b",
    r"\bparsing\b",
    r"\bprocessing\b",
    r"\bsync\b",
    r"\bscrape\b",
    r"\bcrawl\b",
]

OUTPUT_SIGNALS = [
    r"\bimplement\b",
    r"\bimplementation\b",
    r"\bbuild\b",
    r"\bbuildout\b",
    r"\bcreate\b",
    r"\bdevelop\b",
    r"\badd\b",
    r"\bintegrat\b",
    r"\blaunch\b",
    r"\brelease\b",
    r"\bship\b",
    r"\bdeploy\b",
    r"\bfeature\b",
    r"\benhancement\b",
    r"\bcomponent\b",
    r"\bendpoint\b",
    r"\bapi\b",
    r"\bui\b",
    r"\bpage\b",
    r"\bdashboard\b",
    r"\bmodal\b",
    r"\bmodule\b",
    r"\bservice\b",
    r"\btool\b",
    r"\bsystem\b",
    r"\bphase\b",
    r"\brollout\b",
    r"\bupdate\b",
    r"\bredesign\b",
    r"\brebuild\b",
    r"\bnew\b",
]

OUTCOME_SIGNALS = [
    r"\busers? can\b",
    r"\bability to\b",
    r"\bempower\b",
    r"\bimprove.{0,30}experience\b",
    r"\breduce.{0,30}time\b",
    r"\bfaster.{0,20}(for users?|workflow|process)\b",
    r"\beasier.{0,20}(for users?|to use|to access)\b",
    r"\bself.?serv\b",
    r"\bself.?service\b",
    r"\b(enable|allow)\b.{0,30}\busers?\b",
    r"\busers?.{0,30}\b(enable|allow|can|able to)\b",
]

IMPACT_SIGNALS = [
    r"\b(increase|improve|boost|grow|accelerate|maximise|maximize)\b.{0,60}\b(revenue|conversion|profit|nps|satisfaction|margin|ltv|roi|arr|mrr)\b",
    r"\b(increase|improve|reduce|boost|grow)\b.{0,40}\b(customer|user|subscriber|reader)\b.{0,40}\bretention\b",
    r"\bretention\b.{0,40}\b(customer|user|subscriber|reader)\b",
    r"\b(reduce|minimize|minimise|decrease|lower|cut|eliminate)\b.{0,60}\b(churn|cac|friction|dropout|attrition)\b",
    r"\b(reduce|cut|lower)\b.{0,30}\bcosts?\b.{0,20}\b(by|through|via|target|goal|objective)\b",
    r"\b(revenue|conversion|profit|nps|satisfaction|margin|ltv|roi|arr|mrr)\b.{0,60}\b(growth|increase|improvement|goal|target|objective|uplift|opportunity)\b",
    r"\bbusiness (result|objective|goal|kpi|impact|value proposition)\b",
    r"\b(unlock|drive|generate|capture)\b.{0,40}\b(revenue|value|growth|profit|market)\b",
    r"\breturn on investment\b",
    r"\bnet promoter\b",
    r"\b(cost|time)\b.{0,20}\b(savings?|reduction goal|reduction target)\b",
]

DATA_ARTIFACT_EXCLUSION_RE = re.compile(
    r"\b(revenue|conversion|retention|churn|profit|nps|satisfaction|cost|metric|kpi)\b"
    r".{0,50}"
    r"\b(report|dashboard|csv|file|table|dataset|feed|extract|ingest|import|export|"
    r"  tableau|bi|spreadsheet|data|query|schema|field|column|view|chart|graph|summary)\b"
    r"|"
    r"\b(report|dashboard|csv|file|table|dataset|feed|extract|ingest|import|export|"
    r"tableau|bi|spreadsheet|data|query|schema|field|column|view|chart|graph|summary)\b"
    r".{0,50}"
    r"\b(revenue|conversion|retention|churn|profit|nps|satisfaction|cost|metric|kpi)\b",
    re.IGNORECASE | re.VERBOSE,
)

PRESCRIPTIVE_VERBS_RE = re.compile(
    r"\b(build|create|implement|setup|set up|add|integrate|develop|launch|deploy|"
    r"configure|migrate|establish|introduce|rollout|release|redesign|rebuild|"
    r"buildout|build out)\b",
    re.IGNORECASE,
)


def _compile_patterns(signals: List[str]) -> List[re.Pattern]:
    return [re.compile(p, re.IGNORECASE) for p in signals]


INPUT_RE = _compile_patterns(INPUT_SIGNALS)
ACTIVITY_RE = _compile_patterns(ACTIVITY_SIGNALS)
OUTPUT_RE = _compile_patterns(OUTPUT_SIGNALS)
OUTCOME_RE = _compile_patterns(OUTCOME_SIGNALS)
IMPACT_RE = _compile_patterns(IMPACT_SIGNALS)


def _score(text: str, patterns: List[re.Pattern]) -> int:
    return sum(1 for p in patterns if p.search(text))


def _rationale(level: str, scores: Dict[str, int]) -> str:
    hits = [k for k, v in scores.items() if v > 0]
    signal_str = ", ".join(hits) if hits else "none"
    if level == "Activity":
        return f"Contains activity/task language (testing, maintenance, spike, bug-fix). Signal: {signal_str}"
    if level == "Output":
        return f"Describes deliverable artifact or feature. Signal: {signal_str}"
    if level == "Outcome":
        return f"References user behavior or observable experience change. Signal: {signal_str}"
    if level == "Impact":
        return f"References business metric or bottom-line result. Signal: {signal_str}"
    if level == "Input":
        return f"References resource, budget, or staffing allocation. Signal: {signal_str}"
    return ""


def classify_issue_content(title: str, body: Optional[str] = None) -> Dict[str, Any]:
    """Classify an issue's content using the outcome taxonomy."""
    clean_title = (title or "").strip()
    clean_body = (body or "").strip()
    content = f"{clean_title}\n{clean_body}".strip()

    prescriptive_verbs = sorted(set(v.lower() for v in PRESCRIPTIVE_VERBS_RE.findall(clean_title)))
    verbs_str = ", ".join(prescriptive_verbs)

    if not content:
        return {
            "level": "Unknown",
            "rationale": "No title or body available.",
            "prescriptive_verbs": verbs_str,
            "defaulted": False,
            "body_available": False,
        }

    if QUARTERLY_BUCKET_RE.match(clean_title):
        return {
            "level": "Activity",
            "rationale": "Quarterly bucket describes a time-box container for work, not an outcome.",
            "prescriptive_verbs": verbs_str,
            "defaulted": False,
            "body_available": bool(clean_body),
        }

    # Bug / fix override
    is_bug = bool(re.match(r"^(?:fix(?:es|ed)?|bug)(?:\b|\()", clean_title, re.I))
    if is_bug:
        return {
            "level": "Activity",
            "rationale": "Describes bug or defect repair work.",
            "prescriptive_verbs": verbs_str,
            "defaulted": False,
            "body_available": bool(clean_body),
        }

    s = content.lower()
    scores = {
        "Impact": _score(s, IMPACT_RE),
        "Outcome": _score(s, OUTCOME_RE),
        "Output": _score(s, OUTPUT_RE),
        "Activity": _score(s, ACTIVITY_RE),
        "Input": _score(s, INPUT_RE),
    }

    if scores["Impact"] > 0 and DATA_ARTIFACT_EXCLUSION_RE.search(s):
        scores["Impact"] = 0

    if scores["Impact"] > 0 and scores["Activity"] >= 2:
        scores["Impact"] = 0

    if scores["Output"] > 0 and scores["Activity"] > scores["Output"]:
        scores["Output"] = 0

    for level in ["Impact", "Outcome", "Output", "Activity", "Input"]:
        if scores[level] > 0:
            return {
                "level": level,
                "rationale": _rationale(level, scores),
                "prescriptive_verbs": verbs_str,
                "defaulted": False,
                "body_available": bool(clean_body),
            }

    return {
        "level": "Activity",
        "rationale": "No strong signal — defaulted to Activity (work item).",
        "prescriptive_verbs": verbs_str,
        "defaulted": True,
        "body_available": bool(clean_body),
    }


def parse_repo_from_remote(remote_url: str) -> Optional[str]:
    """Extract owner/repo from a git remote URL (HTTPS or SSH)."""
    if not remote_url:
        return None
    url = remote_url.strip()
    # SSH: git@github.com:owner/repo.git
    m = re.search(r"github\.com[:/]([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?$", url)
    if m:
        return m.group(1)
    return None


def detect_repository(cwd: Optional[str] = None) -> Optional[str]:
    """Detect GitHub owner/repo from current workspace."""
    # 1. Try git remote origin url
    try:
        res = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            repo = parse_repo_from_remote(res.stdout.strip())
            if repo:
                return repo
    except Exception:
        pass

    # 2. Try gh repo view
    try:
        res = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass

    return None


def fetch_open_issues(
    repo: Optional[str] = None,
    limit: int = 100,
    runner=subprocess.run,
    cwd: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch open issues using the gh CLI."""
    cmd = [
        "gh", "issue", "list",
        "--state", "open",
        "--limit", str(limit),
        "--json", "number,title,body,labels,createdAt,updatedAt,url",
    ]
    if repo:
        cmd.extend(["--repo", repo])

    res = runner(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        err = res.stderr.strip() if res.stderr else "Unknown error running gh command."
        raise RuntimeError(f"Failed to fetch issues: {err}")

    try:
        return json.loads(res.stdout)
    except Exception as e:
        raise RuntimeError(f"Failed to parse gh output: {e}")


def calculate_days_ago(date_str: Optional[str], now: Optional[datetime] = None) -> int:
    """Calculate elapsed days from an ISO-8601 timestamp string."""
    if not date_str:
        return 0
    now = now or datetime.now(timezone.utc)
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return max(0, (now - dt).days)
    except Exception:
        return 0


def analyze_and_prioritize_issues(
    raw_issues: List[Dict[str, Any]],
    stale_days_threshold: int = 90,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Classify issues and group them into prioritized tiers."""
    now = now or datetime.now(timezone.utc)
    items = []
    level_counts = dict.fromkeys(LEVELS, 0)
    stale_count = 0
    smell_count = 0

    # Weighting rank for sorting: Impact > Outcome > Output > Activity > Input > Unknown
    tier_rank = {
        "Impact": 1,
        "Outcome": 2,
        "Output": 3,
        "Activity": 4,
        "Input": 5,
        "Unknown": 6,
    }

    for issue in raw_issues:
        num = issue.get("number")
        title = issue.get("title", "")
        body = issue.get("body", "")
        url = issue.get("url", "")
        updated_at = issue.get("updatedAt")
        created_at = issue.get("createdAt")
        labels = [l.get("name", "") if isinstance(l, dict) else str(l) for l in issue.get("labels", [])]

        classification = classify_issue_content(title, body)
        level = classification["level"]
        level_counts[level] += 1

        days_since_update = calculate_days_ago(updated_at, now)
        is_stale = days_since_update >= stale_days_threshold
        if is_stale:
            stale_count += 1

        has_smell = bool(classification["prescriptive_verbs"])
        if has_smell:
            smell_count += 1

        coaching = None
        if level in ("Output", "Activity") and has_smell:
            coaching = f"Reframe away from '{classification['prescriptive_verbs']}': What observable user behavior change does this deliver?"
        elif level == "Output" and not classification["body_available"]:
            coaching = "Add an outcome hypothesis: Who uses this and how will their behavior change?"
        elif level in ("Outcome", "Impact"):
            coaching = "High-leverage value driver. Ensure measurable KPI or leading indicator is defined."

        items.append({
            "number": num,
            "title": title,
            "url": url,
            "level": level,
            "tier_rank": tier_rank.get(level, 99),
            "rationale": classification["rationale"],
            "prescriptive_verbs": classification["prescriptive_verbs"],
            "body_available": classification["body_available"],
            "defaulted": classification["defaulted"],
            "labels": labels,
            "days_since_update": days_since_update,
            "is_stale": is_stale,
            "created_at": created_at,
            "updated_at": updated_at,
            "coaching_hint": coaching,
        })

    # Sort prioritized backlog:
    # 1. Tier (Impact, Outcome, Output, Activity...)
    # 2. Staleness (active first: not stale before stale)
    # 3. Recency of update (days_since_update ascending)
    items.sort(key=lambda x: (x["tier_rank"], 1 if x["is_stale"] else 0, x["days_since_update"]))

    grouped = {
        "value_drivers": [i for i in items if i["level"] in ("Impact", "Outcome")],
        "deliverables": [i for i in items if i["level"] == "Output"],
        "tasks_and_maintenance": [i for i in items if i["level"] in ("Activity", "Input", "Unknown")],
    }

    return {
        "version": VERSION,
        "total_open_issues": len(items),
        "counts_by_level": level_counts,
        "stale_count": stale_count,
        "stale_days_threshold": stale_days_threshold,
        "prescriptive_smell_count": smell_count,
        "items": items,
        "grouped": grouped,
    }


def format_prioritized_report(summary: Dict[str, Any], repo_name: Optional[str] = None) -> str:
    """Format prioritization results as a readable terminal report."""
    lines = []
    header = f"Value Prioritization Report: {repo_name or 'Current Repository'}"
    lines.append("=" * len(header))
    lines.append(header)
    lines.append("=" * len(header))
    lines.append("")

    total = summary["total_open_issues"]
    counts = summary["counts_by_level"]
    lines.append(f"Total Open Issues Analyzed: {total}")
    lines.append(
        f"Taxonomy Breakdown: Impact={counts['Impact']} | Outcome={counts['Outcome']} | "
        f"Output={counts['Output']} | Activity={counts['Activity']} | Input={counts['Input']}"
    )
    lines.append(
        f"Signals: {summary['prescriptive_smell_count']} prescriptive wording smells | "
        f"{summary['stale_count']} stale issues (>= {summary['stale_days_threshold']} days untouched)"
    )
    lines.append("")

    grouped = summary["grouped"]

    def _render_section(title: str, items: List[Dict[str, Any]], explanation: str):
        lines.append(f"### {title} ({len(items)})")
        lines.append(f"    {explanation}")
        lines.append("-" * 72)
        if not items:
            lines.append("    (No items in this category)")
            lines.append("")
            return

        for item in items:
            stale_tag = " [STALE]" if item["is_stale"] else ""
            verbs_tag = f" [Smell: {item['prescriptive_verbs']}]" if item["prescriptive_verbs"] else ""
            lines.append(f"  • #{item['number']} [{item['level']}]{stale_tag}{verbs_tag}: {item['title']}")
            lines.append(f"    Reason: {item['rationale']}")
            if item.get("coaching_hint"):
                lines.append(f"    -> Coaching: {item['coaching_hint']}")
            if item.get("labels"):
                lines.append(f"    Labels: {', '.join(item['labels'])}")
            lines.append("")

    _render_section(
        "Tier 1: High-Leverage Value Drivers (Impact & Outcome)",
        grouped["value_drivers"],
        "Highest priority for work: Expresses clear user behavioral changes or measurable business metrics.",
    )

    _render_section(
        "Tier 2: Output Deliverables (Features & Artifacts)",
        grouped["deliverables"],
        "Secondary priority: Expresses a deliverable. Reframe to clarify who uses it and what behavior changes.",
    )

    _render_section(
        "Tier 3: Maintenance, Bugs & Chores (Activity & Input)",
        grouped["tasks_and_maintenance"],
        "Operational work: Fixes, chores, and maintenance. Triage and prevent unbounded growth.",
    )

    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze and prioritize GitHub open issues by value/outcome framing."
    )
    parser.add_argument(
        "--repo",
        "-r",
        help="GitHub repository in owner/repo format (defaults to current git workspace)",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=100,
        help="Maximum open issues to fetch (default: 100)",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=90,
        help="Days since last update to consider an issue stale (default: 90)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output structured JSON instead of human-readable report",
    )

    args = parser.parse_args(argv)

    repo = args.repo
    if not repo:
        repo = detect_repository()
        if not repo:
            sys.stderr.write(
                "Error: Could not detect GitHub repository from current working directory.\n"
                "Provide `--repo owner/name` or run from inside a git clone with a GitHub remote.\n"
            )
            return 1

    try:
        raw_issues = fetch_open_issues(repo=repo, limit=args.limit)
    except Exception as e:
        sys.stderr.write(f"Error fetching issues: {e}\n")
        return 1

    analysis = analyze_and_prioritize_issues(
        raw_issues,
        stale_days_threshold=args.stale_days,
    )

    if args.json:
        payload = {
            "repository": repo,
            **analysis,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_prioritized_report(analysis, repo_name=repo))

    return 0


if __name__ == "__main__":
    sys.exit(main())
