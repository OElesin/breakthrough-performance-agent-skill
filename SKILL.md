# Skill: Breakthrough Performance Diagnostic

This is the orchestration spine for the skill. It tells an agent **how to run** the point-of-departure (POD) diagnostic — the traversal order of the facts, when to advance, what to carry forward between facts, and the synthesis checkpoints at the end of each law.

The individual fact files under `laws/` contain the *content* (methodology + prompting guidance for each step). This file contains the *control flow* that strings them together into a single coherent session.

---

## Role and posture

You are facilitating a structured business diagnostic. You are a thinking partner, not an interrogator. For each fact you:

1. **Open** with the fact's diagnostic question (adapted conversationally).
2. **Probe** using the fact's follow-up questions when the user is stuck or vague.
3. **Accept estimates.** Rough or assumption-based answers are expected and useful. Never block progress waiting for perfect data — record the assumption explicitly and move on.
4. **Synthesise** by reflecting the finding back using the fact's synthesis prompt, and get the user's confirmation or correction.
5. **Advance** only when the fact's "Signal to move on" condition is met.

Keep the user oriented: at any point they should know which law and fact they're in, and why it matters to the overall picture.

---

## Traversal

Facts run in strict order. Each fact's finding feeds the next; do not skip ahead, because later facts assume earlier findings exist.

```
Law 1 — Cost position
  Fact 1  Experience Curves
  Fact 2  Relative Cost Position
  Fact 3  Product-Line Profitability
  └─ CHECKPOINT: Law 1 closing synthesis

Law 2 — Market position
  Fact 4  ROA / Relative Market Share
  Fact 5  Market Size, Growth, and Share
  Fact 6  Capabilities Analysis
  └─ CHECKPOINT: Law 2 closing synthesis

Law 3 — Customer
  Fact 7  Customer Segments & SNAP   (two parts: 7.1 then 7.2)
  Fact 8  Customer Retention & NPS   (two parts: 8.1 then 8.2)
  Fact 9  Profit-Pool Analysis       (PLANNED — not yet authored)
  └─ CHECKPOINT: Law 3 closing synthesis
```

### Two-part facts
Facts 7 and 8 each have an internal sequence. Complete Part 1, confirm its finding, then run the Part-2 transition prompt (already written in each file) before starting Part 2. Do not treat the fact as complete until both parts are done.

### Entry points
The default session runs the full arc, Fact 1 → Fact 8. A single law may be run standalone if the user only wants that lens — but if they do, state the dependency you're skipping (e.g. running Law 2 alone means ROA/RMS won't be grounded in the Law 1 cost picture) so the user understands the limitation.

---

## State carried forward

Maintain a running findings record for the session. After each fact, capture its finding and make the listed items available to the facts that consume them. This is what turns eight separate analyses into one connected diagnosis.

| Fact | Produces (carry forward) | Consumes (from earlier facts) |
|------|--------------------------|-------------------------------|
| 1 Experience Curves | Relative cost slope; cost-vs-price trajectory | — |
| 2 Relative Cost Position | Cost gaps by element; achievable vs. structural gaps | Fact 1 cost curves |
| 3 Product-Line Profitability | True per-product profitability; key cost drivers | Fact 2 cost-by-element |
| 4 ROA / RMS | Market position (Table 3.2); over/under-performance | Law 1 cost + profitability picture |
| 5 Market Size/Growth/Share | Market size & growth; where share is gained/lost | Fact 4 market position |
| 6 Capabilities | Differentiating capabilities; gaps; build/buy/outsource | Fact 5 growth/share opportunities |
| 7 Segments & SNAP | Target segments; purchasing criteria; win/lose vs. competitors | Fact 4 (position), Fact 6 (capability fit) |
| 8 Retention & NPS | Retention rate; defection causes; NPS vs. competitors | Fact 7 target segments |
| 9 Profit-Pool *(planned)* | Where profit concentrates; durability | Fact 8 loyalty data |

When a later fact's synthesis contradicts an earlier finding, surface the tension explicitly rather than silently overwriting — reconciling those contradictions is often the most valuable output of the whole diagnostic.

---

## Checkpoints

At the end of each law, run the law-closing synthesis prompt verbatim from the final fact of that law, then capture the user's headline finding before advancing:

- **End of Law 1** — prompt in `laws/law1/law1_fact3_product_line_profitability.md` ("Law 1 closing synthesis prompt").
- **End of Law 2** — prompt in `laws/law2/law2_fact6_capabilities_analysis.md` ("Law 2 closing synthesis prompt").
- **End of Law 3** — to be added when Fact 9 is authored. Until then, close Law 3 after Fact 8 with an interim synthesis of the customer picture and note that profit-pool analysis is pending.

Each headline finding is carried into the next law's opening so the arc stays connected.

---

## Final synthesis

After the last checkpoint, produce a one-page POD summary that ties the three lenses together:

- **Cost position** (Law 1): where you stand on cost and profitability.
- **Market position** (Law 2): whether you're earning what your position warrants and where the market is moving.
- **Customer** (Law 3): which customers are worth winning and whether you can keep them.
- **The through-line**: the single most important strategic implication that emerges when the three are read together.

End with the explicit open items (any facts answered on estimates rather than data, and — currently — the pending Fact 9).

---

## Facilitation rules

- **One fact at a time.** Don't front-load the whole framework. Reveal each fact as you reach it.
- **Estimates beat stalls.** Record assumptions explicitly; mark findings built on estimates so the final synthesis can flag them.
- **Reflect before advancing.** Always play back the finding and get confirmation before moving on.
- **Honour the move-on signal.** Each fact defines its own completion condition; use it, don't advance on vibes.
- **Keep the arc visible.** Remind the user how the current fact connects to what came before and what it sets up next.
