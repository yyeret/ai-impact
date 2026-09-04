# Running these against real data

These skills are most useful pointed at your actual portfolio — your Jira, your
Confluence, your repos. That is the whole design. It also means the sensible
question before you install anything is: *what leaves my building?*

## What this repo does

Nothing. These are Markdown files. There is no code that runs, no service, no
telemetry, no analytics, no callback, no dependency to install. Nothing here
phones home, because nothing here runs on your machine. The repo does contain two
pieces of automation, and both run in this project's own CI rather than on your
side: `scripts/validate_skills.py`, which checks this repo's own files for
structural problems, and an inline link check in `.github/workflows/validate.yml`
which makes outbound requests to the URLs this repo cites. Neither is invoked by
installing or running a skill, and neither reads anything of yours.

Neither Yuval nor anyone else can see what you point a skill at, what it returns,
or that you ran it at all.

## What your agent does

That is the part that matters, and it is entirely between you and your AI
vendor. When a skill says *"point me at your Confluence space and I'll ingest
what's there,"* your agent reads that content and sends it to whichever model
you are running — Anthropic, OpenAI, or something self-hosted. **The skill is
instructions; your harness and your model provider decide where the data goes.**

So before running any of these against something confidential:

- **Check your provider's terms**, particularly around training on your inputs.
  Enterprise and zero-retention agreements differ substantially from consumer
  tiers, and that difference is the whole question.
- **Check what your harness is allowed to read.** "Run this in the folder where
  the initiative lives" is a broad grant. Some initiative folders contain
  customer data, salary information, or M&A material that has no business in a
  model context, whatever your agreement says.
- **A skill will use whatever you give it.** None of them ask whether the
  material is sensitive, and none of them should be trusted to notice. That
  judgment is yours and cannot be delegated to a Markdown file.

## If you cannot send the data anywhere

Every skill works as an interview. You can run any of them without giving your
agent access to anything, by answering its questions yourself from material it
never sees. You lose the stage-verification step in `sniff-test` — which is the
part that reads git history and ticket transitions to catch a stale status label,
and it is genuinely the most valuable thing that skill does — but the rest of the
read still works.

For a regulated or NDA-bound initiative, that is the mode to use.

## Reporting a problem

If you find something in this repo that leaks information, misdirects an agent,
or would cause harm if followed — a private path that survived review, an
instruction that would send data somewhere unexpected — please
[open an issue](https://github.com/yyeret/ai-activity-to-impact/issues), or
[contact Yuval directly](https://yuvalyeret.com/contact/) if it is not something
to discuss in public.

There is no bug bounty and no formal SLA. It is a Markdown repo maintained by one
person, and it will be fixed as fast as one person can fix it.
