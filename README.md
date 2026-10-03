# Breakthrough Performance Agent Skill

A structured knowledge base for an AI agent that guides users through a point-of-departure (POD) business diagnostic, based on the framework in *The Breakthrough Imperative* by Mark Gottfredson and Steve Schaubert.

The skill walks a user through a sequence of **facts** — self-contained diagnostic analyses — organized under three **laws**. Each fact combines an analytical methodology (what to construct, what data is needed, how to interpret it) with agent prompting guidance (how to facilitate the analysis conversationally).

## Structure

Each fact builds on the previous one and feeds into the next, forming a single diagnostic arc from cost position through market position to the customer.

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
└── law3/   Customer
    ├── law3_fact7_customer_segments_snap.md
    └── law3_fact8_retention_nps.md
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

> **Note:** Fact 9 (Profit-Pool Analysis) is planned and referenced by the Law 3 facts but not yet written. Law names are currently placeholders pending confirmation.

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
