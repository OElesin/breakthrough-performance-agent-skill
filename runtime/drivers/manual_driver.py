"""Manual (human-in-the-loop) driver.

Runs the full diagnostic in the terminal with no external dependencies. For
each fact it prints the diagnostic question, data required, and the opening
prompt, then lets you type the finding — you (or a test script) stand in for
the LLM facilitator. This proves the traversal, state carry-forward, and
checkpoint flow end to end.

Usage:
    python -m runtime.drivers.manual_driver [path-to-skill-root]

Default skill root is the repository root (parent of runtime/).
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

# Allow running as a script or module.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from runtime.skill_runtime import (  # noqa: E402
    DiagnosticSession,
    FactContext,
    Skill,
    load_skill,
)

RULE = "=" * 72
SUB = "-" * 72


def _wrap(text: str, indent: str = "    ") -> str:
    out = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        out.append(textwrap.fill(para, width=72, initial_indent=indent,
                                 subsequent_indent=indent))
    return "\n".join(out)


def _opening_question(fact) -> str:
    guidance = fact.section("Agent Prompting Guidance")
    from runtime.skill_runtime import extract_labelled_prompt
    opening = extract_labelled_prompt(guidance, "Opening question")
    if opening:
        return opening
    # Fall back to the opening question for a part-1 of a two-part fact.
    return extract_labelled_prompt(guidance, "Opening question (Part 1)") or fact.diagnostic_question


def _move_on_signal(fact) -> str:
    guidance = fact.section("Agent Prompting Guidance")
    from runtime.skill_runtime import extract_labelled_prompt
    # "Signal to move on" is a bold label whose body is plain prose, not a
    # blockquote, so pull the lines after it directly.
    lines = guidance.splitlines()
    collecting = False
    out = []
    import re
    for line in lines:
        m = re.match(r"^\*\*(.+?)\*\*\s*$", line.strip())
        if m:
            if collecting:
                break
            if m.group(1).strip().lower().rstrip(":") == "signal to move on":
                collecting = True
            continue
        if collecting and line.strip():
            out.append(line.strip())
    return " ".join(out)


def make_facilitator():
    def facilitate(ctx: FactContext) -> str:
        fact = ctx.fact
        print("\n" + RULE)
        print(f"LAW {fact.n and ''}{ctx.law.name}")
        print(f"FACT {fact.n}: {fact.title}")
        if fact.is_multi_part:
            print(f"  (two parts: {' / '.join(fact.parts)})")
        print(RULE)

        if ctx.carried_in:
            print("\nCarried forward from earlier facts:")
            for var, val in ctx.carried_in.items():
                print(_wrap(f"- {var}: {val}"))

        print("\nDiagnostic question:")
        print(_wrap(fact.diagnostic_question))

        data_req = fact.section_or_parts("Data Required")
        if data_req:
            print("\nData required:")
            # Show only the bold "what it is" headers to keep it scannable.
            for line in data_req.splitlines():
                s = line.strip()
                if s.startswith("- **") or s.startswith("**"):
                    print(_wrap(s.replace("**", "")))

        print("\nOpening prompt (ask the user):")
        print(_wrap(_opening_question(fact)))

        signal = _move_on_signal(fact)
        if signal:
            print("\nAdvance only when:")
            print(_wrap(signal))

        print(SUB)
        finding = input(f"Finding for Fact {fact.n} > ").strip()
        return finding or "(no finding recorded)"

    return facilitate


def make_synthesiser():
    def synthesise(prompt: str, findings) -> str:
        print("\n" + RULE)
        print("CHECKPOINT / SYNTHESIS")
        print(RULE)
        print("\nSynthesis prompt (ask the user):")
        print(_wrap(prompt))
        print(SUB)
        return input("Headline / POD finding > ").strip() or "(none)"

    return synthesise


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[2]
    skill: Skill = load_skill(root)

    print(RULE)
    print(f"{skill.name}  v{skill.version}")
    print(_wrap(skill.description, indent=""))
    print(f"\n{len(skill.laws)} laws, {len(skill.all_facts())} facts")
    print(RULE)

    session = DiagnosticSession(skill, make_facilitator(), make_synthesiser())
    result = session.run()

    print("\n" + RULE)
    print("SESSION COMPLETE — POINT OF DEPARTURE")
    print(RULE)
    for law in skill.laws:
        headline = result.law_headlines.get(law.id)
        if headline:
            print(f"\n{law.name}:")
            print(_wrap(headline))
    if result.final_pod:
        print("\nFull POD synthesis:")
        print(_wrap(result.final_pod))
    print()


if __name__ == "__main__":
    main(sys.argv)
