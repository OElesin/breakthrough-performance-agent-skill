# Runtime

A small engine that executes the skill defined by `skill.json` and the fact
files, following the control flow in `SKILL.md`: it walks the 12 facts in
order, carries findings forward from each fact to the facts that consume them,
and fires the four law-closing checkpoints plus the full-POD synthesis.

## Layout

```
runtime/
├── skill_runtime.py        LLM-agnostic core: loader, markdown parser,
│                           findings/state engine, session traversal
└── drivers/
    ├── manual_driver.py    Human plays the agent — zero dependencies
    └── bedrock_driver.py   LLM facilitates via Amazon Bedrock Converse API
```

The core knows nothing about any particular LLM. A **driver** supplies two
callables:

- a **facilitator** `(FactContext) -> finding_text` that runs one fact, and
- a **synthesiser** `(prompt, findings) -> headline` that runs a checkpoint.

`FactContext` gives the driver the current fact (with its parsed sections and
prompts), the full findings record so far, and `carried_in` — the subset of
findings this fact declared it consumes in `skill.json`.

## Run it

Manual driver (no dependencies — proves the flow end to end):

```bash
python -m runtime.drivers.manual_driver
```

Bedrock driver (requires `boto3` and AWS credentials with Bedrock access):

```bash
pip install boto3
python -m runtime.drivers.bedrock_driver --region us-east-1 \
    --model anthropic.claude-3-5-sonnet-20241022-v2:0
```

Both take an optional path to the skill root as the first argument; it
defaults to the repository root.

## How findings flow

Each fact declares `produces` and `consumes` in `skill.json`. After a fact's
facilitator returns a finding, the engine records it against every state
variable in that fact's `produces`. When a later fact runs, the engine hands
its facilitator the subset of findings whose keys match that fact's
`consumes`. This is the mechanism that turns twelve separate analyses into one
connected diagnosis — e.g. Fact 10 (Innovation Fulcrum) receives Fact 3's
`per_product_profitability`, and Fact 4 (ROA/RMS) receives the Law 1 cost
picture.

## Writing another driver

Implement the two callables and hand them to `DiagnosticSession`:

```python
from runtime.skill_runtime import load_skill, DiagnosticSession

skill = load_skill(".")

def facilitate(ctx):
    # ask ctx.fact.diagnostic_question, use ctx.carried_in, return a finding
    return "..."

def synthesise(prompt, findings):
    return "..."

result = DiagnosticSession(skill, facilitate, synthesise).run()
print(result.final_pod)
```
