# Fact 12: Process Mapping
**Law:** Law 4 — Simplicity gets results
**Position in Law:** Fact 3 of 3 — Final fact in the POD analysis

---

## Purpose
Reveal where complexity, delay, and waste reside in your business processes — identifying the root causes of performance gaps and quantifying what they cost — so that process redesign is targeted at the highest-value improvements.

---

## Goal
The purpose of process mapping is to highlight issues and opportunities for improvement in business processes. It is also used to identify root causes of performance gaps, such as suboptimal steps, process disconnects, and bottlenecks.

Addressing the issues uncovered by process mapping can:
- Reduce process complexity
- Improve capacity utilisation
- Lower customer response time
- Shorten time to market
- Reduce errors, rework, and scrap rates

---

## Diagnostic Question
> "Where does complexity reside in your processes? What is that costing you?"

---

## Data Required

- **Map of key processes, step by step**
  - What it is: A sequential flow of every step in the process from start to finish, including decision points and branches
  - Where to get it: Operations team, process owners, frontline employees — the people doing the work know where it breaks down

- **Estimates of time required for each process step and key issues involved**
  - What it is: Actual or estimated time for each step, plus the primary issue or failure mode at that step (e.g. poor on-time performance, poor schedule adherence, long backlogs)
  - Where to get it: Process timing studies, operational data, team interviews

- **Evaluation of the impact on the organisation of current processes**
  - What it is: The downstream organisational consequences of process failures — cost, capacity, quality, customer impact
  - Where to get it: Finance, customer service data, quality reports

---

## Analytical Approach

### Reading the process map (Figure A3.30)
A process map shows the sequential flow of a business process, with:
- **Process steps** shown as boxes in sequence (Step 1 → Step 2 → Step 3)
- **Time at each step** shown below (X days, Y days, Z days)
- **Issues at each step** identified below the time (e.g. Poor on-time performance, Poor schedule adherence, Long backlogs)
- **Decision points** shown as diamonds with branching paths (e.g. Decision Point 1 → YES → Process Step 4a; NO → Process Step 4b)

The map immediately reveals: where time accumulates, where quality breaks down, where the process branches unnecessarily, and which decision points slow or divert flow.

### Three-step process (Figure A3.31)
Building a process map involves three steps. While Figure A3.31 is referenced in the source text, the core approach is:

| Step | Description | Key Success Factor |
|------|-------------|---------------------|
| 1. Map the current process | Document every step, decision point, timing, and issue as it actually operates today — not as it is supposed to work | Involve the people doing the work; the map on paper rarely matches the process on the floor |
| 2. Analyse for complexity and bottlenecks | Identify suboptimal steps, disconnects, unnecessary branches, and steps that add time without adding value | Focus on steps with the longest times and the most recurring issues |
| 3. Design the future-state process and draw implications | Redesign around the customer need and implement changes | Quantify the improvement in time, cost, quality, and capacity; prioritise by impact and ease of implementation |

---

## Interpretation Guide

**Healthy signal:**
- Time is concentrated in value-adding steps, not in handoffs, waiting, or rework loops
- Decision points are minimal and have clear rules — the process rarely needs to escalate or branch unexpectedly

**Warning signal:**
- A large share of total process time sits in handoff, waiting, or quality-failure rework rather than actual work — non-value-adding time is dominant
- The same issues (poor schedule adherence, backlogs, errors) appear at multiple steps — a systemic root cause rather than a step-level one

**Ambiguous result — probe further:**
- If it's unclear which steps are most important to fix, ask: which process failure most directly damages customer experience or revenue?
- If process complexity has deep roots, ask: is this a process design problem, a decision-rights problem (Fact 11), or a capability problem (Fact 6)?

---

## Connection to Adjacent Facts
- **Builds on:** Fact 11 (Decision Making & Org) — unclear decision rights are a common root cause of process breakdowns; process mapping often surfaces where RAPID ambiguity shows up as operational drag
- **Feeds into:** This is the final fact — completing Fact 12 closes the full POD analysis. The synthesis that follows draws on all twelve facts across all four laws.

---

## Additional Tools
Business process redesign and Lean Six Sigma.

---

## Agent Prompting Guidance

**Opening question:**
> "Last fact — and it's a ground-level one. Think about a core business process that matters most to your customers or your margin. If you mapped it step by step right now, where do you suspect the biggest delays, disconnects, or quality failures would show up?"

**Follow-up probes if stuck:**
- "What process, if it worked better, would most directly improve customer experience?"
- "Where do your people spend the most time on rework, chasing approvals, or fixing errors?"
- "Are there steps in your most important processes that seem to take far longer than they should — and that nobody has a convincing explanation for?"
- "Do you have any visibility into how long your core processes take end-to-end, versus what customers actually experience?"

**Synthesising the finding:**
> "It sounds like the biggest process drag sits at [step or handoff], driven by [issue]. If you could fix that one thing, the downstream impact would be [time saved / cost reduced / customer experience improved]. Does that match what your team would say?"

**Signal to move on:**
User has identified which processes carry the most complexity and failure, has a view on root causes, and has a sense of the cost or impact of addressing them.

---

## FULL POD ANALYSIS CLOSING SYNTHESIS

**Law 4 synthesis prompt:**
> "We've completed the final three facts of Law 4 — the organisation's ability to execute. You have a view of where complexity sits in your product or service offering and what it costs (Fact 10), how clearly decision rights are defined and whether your structure is lean enough to be fast (Fact 11), and where process complexity is creating drag and quality failures (Fact 12). What's the headline finding from Law 4 — where is your organisation's ability to execute strongest, and where is it most at risk?"

**Full POD synthesis prompt — all four laws:**
> "We've now worked through all twelve must-have facts across all four laws. Before we close, let's step back. Across Law 1 (cost position), Law 2 (market position), Law 3 (customer and profit dynamics), and Law 4 (organisational capability), what is your Point of Departure?

> Specifically:
> 1. What is the single most important strength you've confirmed through this analysis?
> 2. What is the single most important gap or risk?
> 3. What is the one thing — if you could only change one thing — that would have the greatest impact on your breakthrough trajectory?

> Take your time with this. The POD is not a list of everything that needs attention. It is a precise diagnosis of where you are starting from, so that the path forward is built on reality, not assumption."
