#!/usr/bin/env python3
"""Prioritize repository open issues by value/outcome framing and repo goals.

Can be run in any local git repository workspace with a GitHub origin,
or pointed at a remote repository with `--repo owner/name`.

Applies the Outcome Framing taxonomy (Input -> Activity -> Output -> Outcome -> Impact)
and compares detected outcomes/deliverables against repository strategic goals
to classify and rank open backlog items.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

VERSION = "outcome-prioritize-1.1.0"
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
    r"\bcleanup\b",
    r"\bcleaning\b",
    r"\bpatch\b",
    r"\bhardening\b",
    r"\bci\/cd\b",
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
    # Direct user/customer capability & behavior
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
    # Generic intent, JTBD, and observable delta signals
    r"\bjob to be done\b",
    r"\bjtbd\b",
    r"\bdesired outcome\b",
    r"\bobservable (?:change|delta|behavior|behaviour)\b",
    r"\b(?:behavior|behaviour|reader|user|team|developer) (?:change|delta)\b",
    r"\bintent\b\s*:",
    r"\bshiny dime\b",
    r"\bhypothesis\b\s*:",
    r"\bleading indicator\b\s*:",
    r"\bchanges? what (?:the|a|users?|readers?|teams?) does\b",
]

TITLE_INTENT_SIGNALS = [
    r"\?$",                                          # Direct question / dilemma hook
    r"\bnow what\b",                                # Dilemma / pivot point
    r"\bfrom \b.+\b to \b",                         # Paradigm / behavioral shift
    r"\b(?:doesn't|didn't|isn't|can't)\b.+\b(?:mean|require|fix|solve|scale)\b", # Belief reframing
    r"\b(?:why|how to|how do we|how i)\b",          # Direct inquiry / problem exploration
    r"\b(?:bottleneck|too late|too early)\b",       # Friction / flow constraint
    r"\b(?:before you|try this)\b",                 # Actionable decision gate
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
TITLE_INTENT_RE = _compile_patterns(TITLE_INTENT_SIGNALS)
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
        return f"References user/reader intent, observable behavioral change, or JTBD. Signal: {signal_str}"
    if level == "Impact":
        return f"References business metric or bottom-line result. Signal: {signal_str}"
    if level == "Input":
        return f"References resource, budget, or staffing allocation. Signal: {signal_str}"
    return ""


def classify_issue_content(title: str, body: Optional[str] = None) -> Dict[str, Any]:
    """Classify an issue's content using the outcome taxonomy and intent cues."""
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

    # Bug / fix override in title
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
    title_lower = clean_title.lower()

    title_intent_score = _score(title_lower, TITLE_INTENT_RE)
    scores = {
        "Impact": _score(s, IMPACT_RE),
        "Outcome": _score(s, OUTCOME_RE) + (2 if title_intent_score > 0 else 0),
        "Output": _score(s, OUTPUT_RE),
        "Activity": _score(s, ACTIVITY_RE),
        "Input": _score(s, INPUT_RE),
    }

    # Exclude data artifacts from Impact
    if scores["Impact"] > 0 and DATA_ARTIFACT_EXCLUSION_RE.search(s):
        scores["Impact"] = 0

    # If title itself is explicitly an activity/chore, don't let body make it Output
    is_activity_title = bool(
        re.match(r"^(?:chore|spike|investigate|debug|test|audit|cleanup|maintenance)\b", clean_title, re.I)
    )
    if is_activity_title and scores["Outcome"] == 0 and scores["Impact"] == 0:
        scores["Output"] = 0

    # Precedence: Impact -> Outcome -> Output -> Activity -> Input
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


def discover_repo_goals(cwd: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Attempt to discover declared goals and mission from local repo context."""
    root = cwd or os.getcwd()
    candidate_files = [
        "AGENTS.md",
        "README.md",
        "GOALS.md",
        "docs/goals.md",
    ]

    for rel in candidate_files:
        path = os.path.join(root, rel)
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                goals = parse_goals_text(content, source_name=rel)
                if goals and goals["keywords"]:
                    return goals
            except Exception:
                continue
    return None


def parse_goals_text(text: str, source_name: str = "custom") -> Dict[str, Any]:
    """Extract key themes, positive keywords, and anti-goal terms from goals text."""
    clean_text = text.strip()
    if not clean_text:
        return {"source": source_name, "raw": "", "keywords": set(), "anti_keywords": set(), "themes": []}

    # Separate positive goal sections from anti-goal/de-emphasized sections
    pos_lines = []
    anti_lines = []
    current_target = pos_lines
    in_any_section = False

    for line in clean_text.splitlines():
        if re.match(r"^#{1,3}\s+.*(?:anti-goal|de-emphasiz|out of scope|non-goal)", line, re.I):
            current_target = anti_lines
            in_any_section = True
            current_target.append(line)
        elif re.match(r"^#{1,3}\s+.*(?:goal|mission|outcome|purpose|intent|pillar|priority|priorities|focus)", line, re.I):
            current_target = pos_lines
            in_any_section = True
            current_target.append(line)
        elif in_any_section and re.match(r"^#{1,2}\s+", line):
            # A new major section that isn't explicitly goal/anti-goal
            in_any_section = False
            current_target = pos_lines
        elif in_any_section or not re.match(r"^#{1,3}\s+", line):
            current_target.append(line)

    pos_text = "\n".join(pos_lines) if pos_lines else clean_text
    anti_text = "\n".join(anti_lines)

    # Comprehensive stopwords (filter out prepositions, conjunctions, pronouns, and web artifacts)
    stop_words = {
        "this", "that", "with", "from", "have", "more", "will", "your", "what", "when",
        "where", "which", "about", "into", "over", "after", "before", "their", "there",
        "should", "would", "could", "these", "those", "other", "using", "under", "while",
        "also", "than", "then", "them", "they", "been", "being", "were", "does", "done",
        "doing", "some", "such", "only", "same", "just", "very", "much", "even", "most",
        "here", "both", "each", "well", "down", "once", "such", "through", "across",
        "between", "without", "again", "further", "because", "cannot", "above", "below",
        "during", "always", "every", "many", "ours", "yours", "theirs", "whose", "and",
        "for", "the", "are", "not", "but", "all", "can", "out", "was", "has", "had",
        "its", "etc", "com", "http", "https", "www", "you", "our", "one", "get", "make",
        "set", "see", "run", "let", "via", "per", "any", "how", "why", "who", "whom",
    }

    pos_tokens = re.findall(r"\b[a-zA-Z0-9_\-]{4,}\b", pos_text.lower())
    keywords = {t for t in pos_tokens if t not in stop_words and not t.isdigit()}

    anti_tokens = re.findall(r"\b[a-zA-Z0-9_\-]{4,}\b", anti_text.lower())
    anti_keywords = {t for t in anti_tokens if t not in stop_words and not t.isdigit()}

    # Extract short theme phrases (from positive sections only)
    themes = []
    for line in pos_lines:
        m = re.match(r"^\s*[-*•\d.]+\s+\*{0,2}([^:*]+?)\*{0,2}(?::|\s*[-—])\s*(.*)", line)
        if m:
            theme_title = m.group(1).strip()
            if 3 < len(theme_title) < 50:
                themes.append(theme_title)

    return {
        "source": source_name,
        "raw": clean_text[:2000],
        "distilled": pos_text[:2000],
        "keywords": keywords,
        "anti_keywords": anti_keywords,
        "themes": themes[:10],
    }


def load_repo_goals(
    goals_input: Optional[str] = None,
    cwd: Optional[str] = None,
    auto_discover: bool = True,
) -> Optional[Dict[str, Any]]:
    """Load repo goals from explicit string, file path, or auto-discovery."""
    if goals_input:
        arg_path = goals_input.strip()
        if os.path.isfile(arg_path):
            with open(arg_path, "r", encoding="utf-8", errors="ignore") as f:
                return parse_goals_text(f.read(), source_name=os.path.basename(arg_path))
        return parse_goals_text(goals_input, source_name="command-line")

    if auto_discover:
        return discover_repo_goals(cwd=cwd)

    return None


def assess_goal_alignment(
    title: str,
    body: str,
    repo_goals: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Score how well an issue aligns with declared repository goals vs anti-goals."""
    if not repo_goals or not repo_goals.get("keywords"):
        return {
            "alignment": "Unspecified",
            "score": 0,
            "matched_terms": [],
            "matched_anti_terms": [],
        }

    issue_text = f"{title}\n{body}".lower()
    issue_tokens = set(re.findall(r"\b[a-zA-Z0-9_\-]{4,}\b", issue_text))
    goal_keywords: Set[str] = repo_goals["keywords"]
    anti_keywords: Set[str] = repo_goals.get("anti_keywords", set())

    # Match positive tokens
    matched = sorted(issue_tokens.intersection(goal_keywords))
    
    # Check title matches specifically (title matches have higher weight)
    title_tokens = set(re.findall(r"\b[a-zA-Z0-9_\-]{4,}\b", title.lower()))
    title_matched = sorted(title_tokens.intersection(goal_keywords))

    pos_score = len(matched) + (len(title_matched) * 2)

    # Match anti-goal tokens
    matched_anti = sorted(issue_tokens.intersection(anti_keywords))
    title_anti = sorted(title_tokens.intersection(anti_keywords))
    anti_score = len(matched_anti) + (len(title_anti) * 2)

    # If strongly matched against anti-goals / de-emphasized scope without strong positive goal alignment
    if anti_score > 0 and anti_score >= pos_score:
        alignment = "Low"
    elif pos_score >= 3 or len(title_matched) >= 2:
        alignment = "High"
    elif pos_score >= 2 or len(title_matched) >= 1:
        alignment = "Medium"
    else:
        alignment = "Low"

    return {
        "alignment": alignment,
        "score": pos_score,
        "matched_terms": matched[:8],
        "matched_anti_terms": matched_anti[:5],
    }

    return {
        "alignment": alignment,
        "score": score,
        "matched_terms": matched[:8],
    }


def parse_repo_from_remote(remote_url: str) -> Optional[str]:
    """Extract owner/repo from a git remote URL (HTTPS or SSH)."""
    if not remote_url:
        return None
    url = remote_url.strip()
    m = re.search(r"github\.com[:/]([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?$", url)
    if m:
        return m.group(1)
    return None


def detect_repository(cwd: Optional[str] = None) -> Optional[str]:
    """Detect GitHub owner/repo from current workspace."""
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
    repo_goals: Optional[Dict[str, Any]] = None,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Classify issues and group them into prioritized tiers based on outcome and goals."""
    now = now or datetime.now(timezone.utc)
    items = []
    level_counts = dict.fromkeys(LEVELS, 0)
    stale_count = 0
    smell_count = 0

    has_goals = bool(repo_goals and repo_goals.get("keywords"))

    # Priority rank mapping:
    # 2D Grid if goals present:
    # P0: High Alignment + Impact/Outcome
    # P1: High Alignment + Output
    # P2: Medium Alignment (Outcome/Output) OR High Alignment Activity (Critical Enabler)
    # P3: Routine Maintenance & Chores
    # P4: Low Alignment / Unanchored
    tier_rank_with_goals = {
        "P0": 1,
        "P1": 2,
        "P2": 3,
        "P3": 4,
        "P4": 5,
    }

    # 1D Altitude fallback:
    tier_rank_1d = {
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

        # Goal alignment evaluation
        goal_eval = assess_goal_alignment(title, body, repo_goals)
        alignment = goal_eval["alignment"]
        matched_terms = goal_eval["matched_terms"]

        # Determine Tier
        if has_goals:
            if alignment == "High" and level in ("Impact", "Outcome"):
                priority_tier = "P0"
                tier_label = "P0: Strategic Value Driver"
                coaching = "Core strategic driver aligned to repo goals. Ensure falsifiable metric or acceptance delta is defined."
            elif alignment == "High" and level == "Output":
                priority_tier = "P1"
                tier_label = "P1: Strategic Deliverable"
                coaching = f"Aligned to repo goals, but framed as output ({classification['prescriptive_verbs'] or 'artifact'}). Reframe to clarify user outcome before pulling."
            elif (alignment == "Medium" and level in ("Impact", "Outcome", "Output")) or (alignment == "High" and level == "Activity"):
                priority_tier = "P2"
                tier_label = "P2: Supporting & Operational Runway"
                coaching = "Supporting outcome or critical enabling runway. Pull after P0/P1 items or when unblocking flow."
            elif level in ("Activity", "Input"):
                priority_tier = "P3"
                tier_label = "P3: Routine Maintenance & Chores"
                coaching = "Routine maintenance or defect repair. Group into cohesive maintenance blocks."
            else:
                priority_tier = "P4"
                tier_label = "P4: Unanchored / Distraction"
                coaching = "Low alignment to declared repo goals. Review whether to close, archive, or reframe."
            sort_rank = tier_rank_with_goals.get(priority_tier, 99)
        else:
            priority_tier = None
            tier_label = None
            sort_rank = tier_rank_1d.get(level, 99)
            if level in ("Output", "Activity") and has_smell:
                coaching = f"Reframe away from '{classification['prescriptive_verbs']}': What observable user behavior change does this deliver?"
            elif level == "Output" and not classification["body_available"]:
                coaching = "Add an outcome hypothesis: Who uses this and how will their behavior change?"
            elif level in ("Outcome", "Impact"):
                coaching = "High-leverage value driver. Ensure measurable KPI or leading indicator is defined."
            else:
                coaching = None

        items.append({
            "number": num,
            "title": title,
            "url": url,
            "level": level,
            "tier_rank": sort_rank,
            "priority_tier": priority_tier,
            "priority_tier_label": tier_label,
            "goal_alignment": alignment,
            "matched_terms": matched_terms,
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
    # 1. Tier rank (P0 -> P4 or Tier 1 -> Tier 3)
    # 2. Staleness (active before stale)
    # 3. Recency of update (days_since_update ascending)
    items.sort(key=lambda x: (x["tier_rank"], 1 if x["is_stale"] else 0, x["days_since_update"]))

    if has_goals:
        grouped = {
            "p0_strategic_drivers": [i for i in items if i["priority_tier"] == "P0"],
            "p1_strategic_deliverables": [i for i in items if i["priority_tier"] == "P1"],
            "p2_supporting_operations": [i for i in items if i["priority_tier"] == "P2"],
            "p3_maintenance_chores": [i for i in items if i["priority_tier"] == "P3"],
            "p4_unanchored_distractions": [i for i in items if i["priority_tier"] == "P4"],
        }
    else:
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
        "repo_goals_source": repo_goals.get("source") if repo_goals else None,
        "repo_goals_themes": repo_goals.get("themes") if repo_goals else [],
        "has_goals": has_goals,
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

    if summary.get("has_goals"):
        src = summary.get("repo_goals_source", "custom")
        themes = summary.get("repo_goals_themes", [])
        theme_str = f" | Themes: {', '.join(themes[:4])}" if themes else ""
        lines.append(f"Strategic Alignment Context: Goals loaded from '{src}'{theme_str}")
    lines.append("")

    grouped = summary["grouped"]

    def _render_item(item: Dict[str, Any]):
        stale_tag = " [STALE]" if item["is_stale"] else ""
        verbs_tag = f" [Smell: {item['prescriptive_verbs']}]" if item["prescriptive_verbs"] else ""
        align_tag = f" [Align: {item['goal_alignment']}]" if item.get("goal_alignment") and item["goal_alignment"] != "Unspecified" else ""
        lines.append(f"  • #{item['number']} [{item['level']}]{align_tag}{stale_tag}{verbs_tag}: {item['title']}")
        lines.append(f"    Reason: {item['rationale']}")
        if item.get("matched_terms"):
            lines.append(f"    Matched Goals: {', '.join(item['matched_terms'])}")
        if item.get("coaching_hint"):
            lines.append(f"    -> Coaching: {item['coaching_hint']}")
        if item.get("labels"):
            lines.append(f"    Labels: {', '.join(item['labels'])}")
        lines.append("")

    if summary.get("has_goals"):
        sections = [
            ("P0: High-Leverage Strategic Value Drivers", grouped.get("p0_strategic_drivers", []),
             "Top investment priority: Direct alignment with repo goals expressed as observable outcomes."),
            ("P1: Strategic Deliverables (Needs Outcome Hypothesis)", grouped.get("p1_strategic_deliverables", []),
             "Core repo deliverables: Reframe from solution output to user outcome before pulling into work."),
            ("P2: Supporting Outcomes & Operational Runway", grouped.get("p2_supporting_operations", []),
             "Secondary scope: Supporting deliverables, adjacent outcomes, or critical enabler runway."),
            ("P3: Routine Maintenance & Chores", grouped.get("p3_maintenance_chores", []),
             "Operational health: Fixes and chores. Keep batch-sized and prevent starvation of P0."),
            ("P4: Unanchored Outputs / Distractions", grouped.get("p4_unanchored_distractions", []),
             "Strategic drift: Low alignment to declared repo goals. Review for parking, closing, or reframing."),
        ]
    else:
        sections = [
            ("Tier 1: High-Leverage Value Drivers (Impact & Outcome)", grouped.get("value_drivers", []),
             "Highest priority for work: Expresses clear user behavioral changes or measurable business metrics."),
            ("Tier 2: Output Deliverables (Features & Artifacts)", grouped.get("deliverables", []),
             "Secondary priority: Expresses a deliverable. Reframe to clarify who uses it and what behavior changes."),
            ("Tier 3: Maintenance, Bugs & Chores (Activity & Input)", grouped.get("tasks_and_maintenance", []),
             "Operational work: Fixes, chores, and maintenance. Triage and prevent unbounded growth."),
        ]

    for title, sec_items, explanation in sections:
        lines.append(f"### {title} ({len(sec_items)})")
        lines.append(f"    {explanation}")
        lines.append("-" * 72)
        if not sec_items:
            lines.append("    (No items in this category)")
            lines.append("")
            continue
        for it in sec_items:
            _render_item(it)

    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze and prioritize GitHub open issues by value/outcome framing and repo goals."
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
        "--goals",
        "-g",
        help="Repository goals text or path to a goals file (e.g. README.md, AGENTS.md, or custom goals)",
    )
    parser.add_argument(
        "--no-auto-goals",
        action="store_true",
        help="Disable automatic discovery of goals from local README.md/AGENTS.md",
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

    # Load repo goals if provided or discoverable
    repo_goals = load_repo_goals(
        goals_input=args.goals,
        auto_discover=not args.no_auto_goals,
    )

    analysis = analyze_and_prioritize_issues(
        raw_issues,
        stale_days_threshold=args.stale_days,
        repo_goals=repo_goals,
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
