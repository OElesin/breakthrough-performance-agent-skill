# Fact 3: Product-Line Profitability Analysis
**Law:** Law 1 — Costs and prices always decline
**Position in Law:** Fact 3 of 3

---

## Purpose
Determine the true profitability of each product or service in your portfolio — going beyond conventional accounting to reveal which products are genuinely making money, which are destroying value, and where strategic action is required.

---

## Goal
Product-line profitability (PLP) analysis is a diagnostic tool that helps you determine the true profitability of each product in a multi-product portfolio. It answers a range of strategic and operational questions:
- Where should we focus our cost-reduction efforts?
- How can we optimise pricing?
- Which product lines should we drop?
- On which should we focus research-and-development efforts?
- Where should we change sales incentives?

---

## Diagnostic Question
> "Which of your products or services are making money (or not), and why?"

---

## Data Required

- **Direct costs for each product**
  - What it is: Materials, direct labour, packaging, and other costs directly attributable to each product
  - Where to get it: Cost accounting / manufacturing records; bill of materials

- **Indirect costs for each product**
  - What it is: Logistics, selling, G&A, and other overhead costs allocated to each product
  - Where to get it: Finance/management accounting; requires activity-based allocation (not standard accounting)

- **Major activities performed and cost drivers for each activity**
  - What it is: The operational activities that consume costs, and the metrics that drive those costs (e.g. cubic feet for warehouse labour, person-hours for delivery labour)
  - Where to get it: Operations team; process mapping; time-and-motion studies

---

## Analytical Approach

### Why conventional accounting is insufficient
PLP requires going beyond standard financial reports. There are three critical differences between standard accounting and PLP:

| Dimension | Standard Accounting | PLP Analysis |
|-----------|-------------------|--------------|
| **Cost collection** | Costs collected by function (e.g. R&D, advertising) | Costs collected by product |
| **Cost assigned to products** | COGS only — typically direct labour and materials | All costs including indirect (logistics, selling, G&A, HC costs) |
| **Cost allocation method** | Rules-based standard costing | Activity-based cost drivers (e.g. cubic feet for warehouse labour, person-hours for delivery labour) |

**Important:** Always account for fixed costs that would not go away if you eliminated a product. The key is to understand what the costs are and how they behave under different scenarios.

### Six-step PLP process (Figure A3.6)

| Step | Description | Key Success Factor |
|------|-------------|-------------------|
| 1. Understand current P&Ls and cost-collection systems | Identify people and systems that report financial data | Understand linkages and differences among the various sources of data |
| 2. Determine the major activities performed | Map your value chain from beginning to end | |
| 3. Identify costs and cost drivers for each activity | Assign costs to operational activities | Tie costs to activities, not accounting categories; focus on the largest cost elements |
| 4. Assign costs to each product | Quantify cost drivers for each product | |
| 5. Analyse profitability by product or group of products | Calculate over several years or periods | Eliminate seasonal or one-time effects; ensure absolute profit of product lines reconciles with total business profits |
| 6. Draw implications | Consider strategic and operational alternatives | |

### Reading the output (Figure A3.5)
The product-line profitability chart plots products as bars where:
- **Bar width = Revenue** (wider bar = more revenue)
- **Bar height = Profit margin** (above/below the axis)
- **Bar area = Absolute profit or loss**

This visual immediately reveals which products are the value creators and which are the destroyers — and at what scale. For each product, the point of arrival decision is: reduce costs, maintain as a loss leader, or drop altogether.

---

## Interpretation Guide

**Healthy signal:**
- High-revenue products are also high-margin — your volume leaders are driving profitability
- Indirect costs are genuinely understood and allocated, not hidden in overhead pools

**Warning signal:**
- High-revenue products have thin or negative margins when fully loaded with indirect costs — the business is cross-subsidising underperformers at scale
- A significant share of revenue comes from products that are loss-making on a fully-loaded basis

**Ambiguous result — probe further:**
- If a product appears loss-making, ask: is it a genuine loss, or an artefact of how costs are allocated?
- If fixed costs are large, ask: what would the cost structure look like if this product were dropped? Would fixed costs truly disappear?
- For loss-leaders: is there a deliberate strategic reason, and is it achieving its purpose?

---

## Connection to Adjacent Facts
- **Builds on:** Fact 2 (Relative Cost Position Analysis) — RCP established where costs are relative to competitors by element; PLP now reveals how those costs translate into profitability across the portfolio
- **Feeds into:** Law 2, Fact 1 — completing the cost picture across all three Law 1 facts enables the transition to the next law's diagnostic

---

## Additional Tools
- Activity-based costing
- Product-portfolio analysis

---

## Agent Prompting Guidance

**Opening question:**
> "The final piece of Law 1 is product-line profitability — do you know which of your products or services are actually making money once all costs, including indirect ones, are properly allocated? Or does your current accounting make it hard to see this clearly?"

**Follow-up probes if stuck:**
- "How does your finance system currently allocate costs — by function, or by product?"
- "Which product lines do you suspect are cross-subsidised by your stronger performers?"
- "If you had to rank your products by true profitability — fully loaded, including all indirect costs — what would the order look like?"
- "Are there any products you keep for strategic reasons even though you suspect they lose money?"

**Synthesising the finding:**
> "So on a fully-loaded basis, it looks like [products] are your genuine profit contributors, while [products] are either break-even or loss-making. The main driver of the gap appears to be [cost element]. Does that match your intuition — and does it change how you think about the portfolio?"

**Signal to move on:**
User has a working view of which products are genuinely profitable versus loss-making on a fully-loaded basis, understands the key cost drivers behind the differences, and has formed a view on what the implications are for the portfolio. This completes Law 1 — signal readiness to move to Law 2.

**Law 1 closing synthesis prompt:**
> "We've now completed the three facts of Law 1. You have a picture of your cost trajectory over time (experience curves), your cost position relative to competitors element by element (RCP), and the true profitability of your product portfolio (PLP). Before we move to Law 2, what's your headline finding from Law 1 — what is the single most important thing you've learned about your cost position?"
