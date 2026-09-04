# A worked `wip-limit-configuration-coach` run

**Made-up team, made-up numbers.** No client, no real board. It exists because
this is the longest skill in the library — fifteen interview questions before it
computes anything — and nobody should pay that price without seeing what comes
out the other end.

The point of reading it is the shape of the reasoning, especially where the skill
refuses to give a number. Your team will produce different numbers.

---

## The setup

Six engineers on an internal platform team. Everyone drives Claude Code; one
staff engineer does effectively all the review. The board says "9 in progress"
and the team lead cannot tell whether that is a fire or a Tuesday.

The opening message:

> Use the wip-limit-configuration-coach skill. Six engineers, all using coding
> agents, one reviewer. Jira board attached. Our "in progress" count is 9 and I
> don't know if that's bad.

**Budget about 35 minutes.** It is an interview, and the questions are the
product — several of them are ones a team typically has not asked itself.

---

## The interview, compressed

The parts that changed the answer:

- **Q2, workflow states.** The board had `In Progress → In Review → Done`. Asking
  which states were queues rather than work surfaced an unnamed one: items sat
  "in review" for days before the reviewer opened them. That is a queue, and it
  was invisible because the board had no column for it.
- **Q6, independent pods.** The lead's first answer was "six — everyone works
  independently." Pushed on *"without repeatedly borrowing the same human
  constraint,"* it became **two**. Everything crosses the one reviewer.
- **Q7, guided vs. autonomous.** Agents run genuinely unattended for 20-40
  minutes at a stretch, a few times a day. Not the multi-hour autonomous loops
  that would license a second concurrent feature per person.
- **Q11, fan-out.** This is the finding. Each feature lands as **4 to 7 pull
  requests** across separate worktrees — a number most teams have never counted.

---

## What came back

### 1. Workflow, restated

| Stage | Type |
|---|---|
| Backlog | funnel |
| Ready | Ready queue |
| In Progress | active |
| **Ready for Review** | **downstream queue (was invisible)** |
| In Review | active |
| Done | done |

### 2. Intent

Change the pattern, not preserve it. The lead's stated goal was "stop feeling
spread thin," which means the limit has to bite.

### 3. Topology and the constraint

Two independent pods. **The constraint is the single reviewer**, and it is not
close. Agent capacity is irrelevant to the limit — six people driving agents can
generate work far faster than one person can review it, so the review stage sets
the pace for the whole system.

### 4. Candidates, with arithmetic

| Candidate | Number | What it answers |
|---|---|---|
| One guided feature per pod | **2** | What can actually move without contention |
| Pods +1 | 3 | Buffer for one blocked item |
| Pods ×1.5 | 3 | Moderate variability |
| Pods ×2 | 4 | High variability or slow blocker recovery |
| Half current WIP | 4-5 | Aggressive brownfield experiment |
| Historical p50 | 8 | The level half the observed days sat at or below |
| Historical p85 | 12 | The level 85% of observed days sat at or below |

### 5. Recommendation

**Active features: 2. Ready-to-start: 2. Combined `Ready for Review + In Review`:
2 — counted in pull requests, not features.**

The Ready-to-start limit comes from the replenishment answer, not from the
constraint: the team replenishes roughly weekly and starts about two features a
week, so two on the shelf reaches the next realistic trip.

That second half is the part that matters, and it is where the skill contradicted
its own default. The counting rule says count a feature once. But review capacity
is consumed in the artifacts the reviewer opens, and at 4-7 PRs per feature, a
two-*feature* review cap is a ten-PR queue. So the review stage gets its limit in
PRs.

It then said the fan-out is the actual problem: *a feature that arrives as seven
review artifacts is a batch-size problem upstream, not a limit to raise.* The
recommended first move was to cut PRs per feature toward two or three, and it was
explicit that if that works, the review limit should be revisited rather than
left where it is.

### 6. Why not the others

**The percentiles (8 and 12) were rejected, but not for the reason you might
expect.** A limit of 8 sits *below* today's WIP of 9, and half the observed days
were at or above 8 — so it would genuinely bind, on roughly half of them. It is
not a no-op. (The trap in the skill's scenario 11 is a limit at or *above* current
WIP; that is a different case and it does not apply here.)

It was rejected because of what it measures. Historical WIP is a record of what
the board accumulated, not evidence of what the system can sustain — the skill is
explicit that *"historical WIP can include old queues and is not proof of human
capacity."* With one reviewer, eight concurrent features is inventory piled in
front of the constraint. Setting the limit there would ratify the pile. The p85 of
12 is the same objection, further from the constraint.

**The buffer multipliers (3, 3, 4)** were rejected for a related reason: `+1`,
`×1.5` and `×2` protect a constraint against variability by holding more work near
it. Here the constraint is one person's attention, and extra work near it does not
protect it — it lengthens the queue it has to look at.

**Half-WIP (4-5)** is the closest runner-up and would be a defensible first move
on a team without such a stark single-point constraint. It is derived from
history rather than from the topology, so it was compared and set aside, not
dismissed.

### 7. Pull policy

When you cannot start a new feature: progress the same feature; then work
right-to-left on existing WIP — review, test, split, integrate, release; then, and
only then, consider pulling new work, and only if an existing feature is in a
genuinely autonomous loop rather than merely waiting on you.

**Blocked items keep their slot.** The team asked about exempting them. The skill
declined and explained why: exempt blocked work and the limit stops binding, and
in six weeks everyone concludes WIP limits do not work.

### 8. Sensitivity check

- **Normal week:** two features active, review queue rarely empty. The limit binds
  a few times a week, which is the point — each time is a prompt to finish rather
  than start.
- **Reviewer absent:** the system stalls at 2 within a day or so. That is correct
  and visible, rather than six people quietly starting a seventh thing.
- **Agents generating 2×:** nothing changes. The constraint is downstream of
  generation, which is the whole argument for not multiplying limits by agents.
- **Review gets slower** (bigger changes, more context to reload): the PR-denominated
  review cap binds harder and sooner. Tighten the fan-out before loosening it.
- **Replenishment changes** to twice-weekly grooming: the Ready-to-start limit
  drops from 2 to 1 — a shorter trip needs less on the shelf. The active and review
  limits are unaffected, because they come from the constraint, not the cadence.

### 9. The experiment

Four weeks. **Tighten** if work-item age or the review queue grows. **Loosen**
only if throughput rises while age and rework stay flat. **Redesign** if the
reviewer keeps overriding every local limit — that means the constraint is
structural and no number fixes it.

---

## What a run like this is for

Again: constructed team, so no claim about what it changed for anyone. What the
example is meant to show is that the number is not the point. The interview
surfaces the things that actually cap the system — one reviewer, an unnamed queue,
five-PR features — none of which a WIP limit fixes, and all of which the WIP
conversation is unusually good at dragging into view.

If a run ends with a number and no structural finding, you have paid 35 minutes
for something you could have guessed.

## Where a run like this goes wrong

- It can treat two pods as symmetric when one of them works on a legacy service
  where review takes twice as long. The interview asks about *shared* constraints,
  not asymmetric ones — you have to raise that yourself.
- It computes a Ready queue limit from your replenishment answer. If "we groom
  weekly" actually means "we groom when someone remembers," the arithmetic is fine
  and the answer is wrong. It takes the input at face value.

Both are the same lesson as everywhere else in this library: it reasons well over
what you tell it, and it cannot tell when what you told it is optimistic.
