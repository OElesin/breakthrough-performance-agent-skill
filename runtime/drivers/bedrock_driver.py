"""Bedrock-backed driver.

Facilitates the diagnostic with an LLM via the Amazon Bedrock Converse API.
The model plays the consultant described in SKILL.md: it opens each fact with
the diagnostic question, probes, accepts estimates, reflects a finding back,
and advances. A short interactive loop per fact lets the human (the business
being diagnosed) answer; the model decides when the fact's move-on signal is
met and emits a structured finding.

Requires: boto3, and AWS credentials with Bedrock access.

Usage:
    python -m runtime.drivers.bedrock_driver [path-to-skill-root] \
        [--model MODEL_ID] [--region REGION]

Default model: anthropic.claude-3-5-sonnet-20241022-v2:0
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from runtime.skill_runtime import (  # noqa: E402
    DiagnosticSession,
    FactContext,
    extract_labelled_prompt,
    load_skill,
)

DEFAULT_MODEL = "anthropic.claude-3-5-sonnet-20241022-v2:0"
DEFAULT_REGION = "us-east-1"

FINDING_SENTINEL = "FINDING:"

SYSTEM_PROMPT = """\
You are facilitating a structured point-of-departure (POD) business diagnostic
based on The Breakthrough Imperative. You are a thinking partner, not an
interrogator.

For the current fact you must:
1. Open with the fact's diagnostic question, adapted conversationally.
2. Probe with the fact's follow-up questions only if the user is vague or stuck.
3. Accept estimates. Never block waiting for perfect data; record assumptions
   explicitly and move on.
4. Reflect the finding back using the fact's synthesis prompt and get the
   user's confirmation or correction.
5. Advance only when the fact's "Signal to move on" condition is met.

Keep turns short and focused. Ask one thing at a time. Do not dump the whole
framework on the user.

When — and only when — the move-on condition is satisfied and the user has
confirmed your reflected finding, end your message with a final line of the
exact form:

FINDING: <one or two sentence synthesis of what was established for this fact>

Do not emit the FINDING: line until the user has confirmed. Until then, keep
the conversation going normally with no FINDING: line.
"""


def _converse(client, model_id: str, system: str, messages: List[dict]) -> str:
    resp = client.converse(
        modelId=model_id,
        system=[{"text": system}],
        messages=messages,
        inferenceConfig={"maxTokens": 1024, "temperature": 0.4},
    )
    parts = resp["output"]["message"]["content"]
    return "".join(p.get("text", "") for p in parts).strip()


def _fact_briefing(ctx: FactContext) -> str:
    """Assemble the per-fact context the model needs, drawn from the fact file."""
    f = ctx.fact
    guidance = f.section("Agent Prompting Guidance")
    opening = (
        extract_labelled_prompt(guidance, "Opening question")
        or extract_labelled_prompt(guidance, "Opening question (Part 1)")
    )
    synth = (
        extract_labelled_prompt(guidance, "Synthesising the finding")
        or extract_labelled_prompt(guidance, "Synthesising the finding (Part 1)")
    )

    # Move-on signal (plain prose after a bold label).
    import re
    signal_lines, collecting = [], False
    for line in guidance.splitlines():
        m = re.match(r"^\*\*(.+?)\*\*\s*$", line.strip())
        if m:
            if collecting:
                break
            if m.group(1).strip().lower().rstrip(":") == "signal to move on":
                collecting = True
            continue
        if collecting and line.strip():
            signal_lines.append(line.strip())
    signal = " ".join(signal_lines)

    carried = ""
    if ctx.carried_in:
        carried = "\n".join(f"- {k}: {v}" for k, v in ctx.carried_in.items())

    parts = [
        f"CURRENT FACT: Fact {f.n} — {f.title}",
        f"LAW: {ctx.law.name}",
        f"\nDIAGNOSTIC QUESTION:\n{f.diagnostic_question}",
    ]
    if f.is_multi_part:
        parts.append(f"\nThis fact has two parts, run in order: {' then '.join(f.parts)}.")
    if carried:
        parts.append(f"\nFINDINGS CARRIED FORWARD (use these; reconcile any tension):\n{carried}")
    if opening:
        parts.append(f"\nOPENING PROMPT:\n{opening}")
    data_req = f.section_or_parts("Data Required")
    if data_req:
        parts.append(f"\nDATA REQUIRED:\n{data_req}")
    if synth:
        parts.append(f"\nSYNTHESIS PROMPT (use to reflect the finding back):\n{synth}")
    if signal:
        parts.append(f"\nSIGNAL TO MOVE ON:\n{signal}")
    return "\n".join(parts)


def make_facilitator(client, model_id: str):
    def facilitate(ctx: FactContext) -> str:
        briefing = _fact_briefing(ctx)
        system = SYSTEM_PROMPT + "\n\n" + briefing
        messages: List[dict] = []

        print("\n" + "=" * 72)
        print(f"FACT {ctx.fact.n}: {ctx.fact.title}  —  {ctx.law.name}")
        print("=" * 72)

        # Kick the model off; it should open with the diagnostic question.
        messages.append({"role": "user", "content": [{"text": "Begin this fact."}]})

        while True:
            reply = _converse(client, model_id, system, messages)
            messages.append({"role": "assistant", "content": [{"text": reply}]})

            finding = None
            display = reply
            if FINDING_SENTINEL in reply:
                idx = reply.rfind(FINDING_SENTINEL)
                display = reply[:idx].strip()
                finding = reply[idx + len(FINDING_SENTINEL):].strip()

            if display:
                print(f"\nAgent: {display}")

            if finding:
                print(f"\n  [finding recorded: {finding}]")
                return finding

            user = input("\nYou > ").strip()
            if user.lower() in {"/skip", "skip"}:
                return "(skipped by user)"
            messages.append({"role": "user", "content": [{"text": user}]})

    return facilitate


def make_synthesiser(client, model_id: str):
    def synthesise(prompt: str, findings: Dict[str, str]) -> str:
        print("\n" + "=" * 72)
        print("CHECKPOINT / SYNTHESIS")
        print("=" * 72)
        findings_block = "\n".join(f"- {k}: {v}" for k, v in findings.items())
        system = (
            "You are closing out a law (or the whole diagnostic) in a POD "
            "business analysis. Deliver the synthesis prompt to the user, then "
            "help them articulate a single headline finding. When they have, "
            "end with a line 'FINDING: <headline>'."
        )
        messages = [{
            "role": "user",
            "content": [{"text": (
                f"Findings so far:\n{findings_block}\n\n"
                f"Deliver this synthesis prompt to the user:\n{prompt}"
            )}],
        }]
        while True:
            reply = _converse(client, model_id, system, messages)
            messages.append({"role": "assistant", "content": [{"text": reply}]})
            finding = None
            display = reply
            if FINDING_SENTINEL in reply:
                idx = reply.rfind(FINDING_SENTINEL)
                display = reply[:idx].strip()
                finding = reply[idx + len(FINDING_SENTINEL):].strip()
            if display:
                print(f"\nAgent: {display}")
            if finding:
                print(f"\n  [headline recorded: {finding}]")
                return finding
            user = input("\nYou > ").strip()
            messages.append({"role": "user", "content": [{"text": user}]})

    return synthesise


def main(argv):
    parser = argparse.ArgumentParser(description="Bedrock driver for the POD diagnostic skill.")
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--region", default=DEFAULT_REGION)
    args = parser.parse_args(argv[1:])

    try:
        import boto3
    except ImportError:
        print("boto3 is required for the Bedrock driver: pip install boto3", file=sys.stderr)
        return 1

    client = boto3.client("bedrock-runtime", region_name=args.region)
    skill = load_skill(args.root)

    print("=" * 72)
    print(f"{skill.name} v{skill.version}  (model: {args.model})")
    print(f"{len(skill.laws)} laws, {len(skill.all_facts())} facts")
    print("Type /skip to force-advance a fact. Ctrl-C to quit.")
    print("=" * 72)

    session = DiagnosticSession(
        skill,
        make_facilitator(client, args.model),
        make_synthesiser(client, args.model),
    )
    result = session.run()

    print("\n" + "=" * 72)
    print("SESSION COMPLETE — POINT OF DEPARTURE")
    print("=" * 72)
    for law in skill.laws:
        hl = result.law_headlines.get(law.id)
        if hl:
            print(f"\n{law.name}:\n  {hl}")
    if result.final_pod:
        print(f"\nFull POD synthesis:\n  {result.final_pod}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
