# Breakthrough Performance Agent Skill

A structured knowledge base for an AI agent that guides users through a point-of-departure (POD) business diagnostic, based on the framework in *The Breakthrough Imperative* by Mark Gottfredson and Steve Schaubert.

The skill walks a user through a sequence of **facts** — self-contained diagnostic analyses — organized under four **laws**. Each fact combines an analytical methodology (what to construct, what data is needed, how to interpret it) with agent prompting guidance (how to facilitate the analysis conversationally).

## How it runs

- **[`SKILL.md`](SKILL.md)** is the orchestration spine: traversal order, when to advance, what state carries forward between facts, and the per-law synthesis checkpoints. Start here to understand how a session flows.
- **[`skill.json`](skill.json)** is the machine-readable companion encoding the same traversal, produces/consumes dependencies, and checkpoints — for driving the session programmatically.
- The files under `laws/` hold the *content* for each step; `SKILL.md` holds the *control flow* that strings them together.

## Structure

Each fact builds on the previous one and feeds into the next, forming a single diagnostic arc from cost position, through market position and the customer, to organisational execution.

```
laws/
├── law1/   Cost position
│   ├── law1_fact1_experience_curves.md
│   ├── law1_fact2_relative_cost_position.md
│   └── law1_fact3_product_line_profitability.md
├── law2/   Market position
│   ├── law2_fact4_roa_rms.md
│   ├── law2_fact5_market_size_growth_share.md
│   └── law2_fact6_capabilities_analysis.md
├── law3/   Customer
│   ├── law3_fact7_customer_segments_snap.md
│   ├── law3_fact8_retention_nps.md
│   └── law3_fact9_profit_pool_analysis.md
└── law4/   Organisational capability / execution
    ├── law4_fact10_innovation_fulcrum.md
    ├── law4_fact11_decision_making_org.md
    └── law4_fact12_process_mapping.md
SKILL.md       Orchestration spine (traversal, state, checkpoints)
skill.json     Machine-readable traversal manifest
templates/
└── _TEMPLATE_fact.md   Blank template for authoring new facts
```

## The facts

| # | Fact | Law | Diagnostic question |
|---|------|-----|---------------------|
| 1 | Experience Curves | 1 — Cost position | How does your cost slope compare with competitors and industry price? |
| 2 | Relative Cost Position | 1 — Cost position | What are your costs compared with competitors, element by element? |
| 3 | Product-Line Profitability | 1 — Cost position | Which products are making money (or not), and why? |
| 4 | Return on Assets / Relative Market Share | 2 — Market position | Where do you and competitors fall on the ROA/RMS chart? |
| 5 | Market Size, Growth, and Share | 2 — Market position | How big is your market, what's growing, where are you gaining/losing share? |
| 6 | Capabilities Analysis | 2 — Market position | Which capabilities create competitive advantage, and where are the gaps? |
| 7 | Customer Segments & SNAP | 3 — Customer | Which segments are most attractive, and can you win them? |
| 8 | Customer Retention & NPS | 3 — Customer | What proportion of customers are you retaining, and how does your NPS track? |
| 9 | Profit-Pool Analysis | 3 — Customer | Where is profit concentrated across the value chain, and how durable is it? |
| 10 | Innovation Fulcrum (Model T) | 4 — Execution | How complex are your offerings, what is that costing you, and where is your fulcrum? |
| 11 | Decision-Making & Org Complexity | 4 — Execution | How complex are your decisions and structure, and what is the impact? |
| 12 | Process Mapping | 4 — Execution | Where does complexity reside in your processes, and what is it costing you? |

> **Note:** Law names are currently placeholders pending confirmation. Fact 12 carries the full point-of-departure (POD) synthesis across all four laws.

## Fact file format

Every fact follows a consistent template (see `templates/_TEMPLATE_fact.md`):

- **Purpose** — what the fact establishes and why it matters
- **Goal** — what the analyst constructs or determines
- **Diagnostic Question** — the framing question the agent opens with
- **Data Required** — inputs, sources, and fallbacks
- **Analytical Approach** — step-by-step methodology, formulas, frameworks
- **Interpretation Guide** — healthy vs. warning vs. ambiguous signals
- **Connection to Adjacent Facts** — what it builds on and feeds into
- **Additional Tools** — supplementary frameworks
- **Agent Prompting Guidance** — opening questions, probes, synthesis, and move-on signals

## Source

Framework adapted from *The Breakthrough Imperative: How the Best Managers Get Outstanding Results* by Mark Gottfredson and Steven Schaubert (HarperCollins, 2008). This repository contains original diagnostic and agent-facilitation material derived from that framework; it is not a reproduction of the book.

## License

See [LICENSE](LICENSE).
