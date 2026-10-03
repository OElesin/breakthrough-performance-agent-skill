"""Runtime core for the Breakthrough Performance diagnostic skill.

Dependency-free. Loads skill.json, parses the fact files into structured
sections, and drives the fact -> checkpoint -> final-synthesis flow while
maintaining the carry-forward findings record described in SKILL.md.

The core is LLM-agnostic. A *driver* supplies a `facilitator` callable that
turns a FactContext into one or more turns of conversation and returns the
captured finding. See drivers/ for a manual (human-in-the-loop) driver and a
Bedrock-backed driver.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass
class Fact:
    """A single diagnostic fact, as declared in skill.json plus parsed content."""

    id: str
    n: int
    title: str
    file: str
    diagnostic_question: str
    produces: List[str]
    consumes: List[str]
    parts: List[str] = field(default_factory=list)
    # Parsed from the markdown body:
    sections: Dict[str, str] = field(default_factory=dict)

    @property
    def is_multi_part(self) -> bool:
        return len(self.parts) > 1

    def section(self, name: str, default: str = "") -> str:
        """Fetch a parsed section body by its header text (case-insensitive)."""
        key = name.strip().lower()
        for header, body in self.sections.items():
            if header.strip().lower() == key:
                return body
        return default

    def section_or_parts(self, name: str, default: str = "") -> str:
        """Like section(), but for two-part facts fall back to concatenating the
        matching sub-content from Part 1 / Part 2.

        Two-part facts (7, 8, 11) nest Diagnostic Question / Data Required inside
        `## Part 1` / `## Part 2` as `### <name>` sub-headers rather than as a
        top-level `## <name>` section.
        """
        direct = self.section(name)
        if direct:
            return direct
        chunks: List[str] = []
        want = name.strip().lower()
        for header, body in self.sections.items():
            if not header.strip().lower().startswith("part"):
                continue
            # Pull a `### want` sub-section out of this Part body.
            sub = _extract_subsection(body, want)
            if sub:
                chunks.append(f"[{header}] {sub}")
        return "\n\n".join(chunks) if chunks else default


@dataclass
class Law:
    id: str
    name: str
    facts: List[Fact]
    closing_synthesis_source: Optional[str]
    closing_synthesis_section: Optional[str]
    final_synthesis_source: Optional[str] = None
    final_synthesis_section: Optional[str] = None


@dataclass
class FactContext:
    """Everything a facilitator needs to run one fact, including prior findings."""

    law: Law
    fact: Fact
    findings: Dict[str, str]        # state var -> finding text, accumulated so far
    carried_in: Dict[str, str]      # subset of findings this fact declares it consumes


@dataclass
class Skill:
    name: str
    version: str
    description: str
    facilitation: Dict[str, bool]
    laws: List[Law]
    root: Path

    def all_facts(self) -> List[Fact]:
        return [f for law in self.laws for f in law.facts]


# --------------------------------------------------------------------------- #
# Markdown parsing
# --------------------------------------------------------------------------- #

_H2 = re.compile(r"^##\s+(.*)$")
_H3 = re.compile(r"^###\s+(.*)$")


def _extract_subsection(body: str, want: str) -> str:
    """Return the text under a `### <want>` sub-header within a section body."""
    lines = body.splitlines()
    collecting = False
    out: List[str] = []
    for line in lines:
        m = _H3.match(line)
        if m:
            if collecting:
                break
            name = m.group(1).strip().lower()
            # Match leading header text, e.g. "Diagnostic Question" within
            # "### Diagnostic Question" or a numbered variant.
            if name == want or name.startswith(want):
                collecting = True
            continue
        if collecting:
            out.append(line)
    return "\n".join(out).strip()


def _parse_sections(markdown: str) -> Dict[str, str]:
    """Split a fact file into {h2 header: body} chunks.

    Nested ### and **bold** sub-headers are left inside the body verbatim so a
    facilitator can present them as-is.
    """
    sections: Dict[str, str] = {}
    current: Optional[str] = None
    buf: List[str] = []
    for line in markdown.splitlines():
        m = _H2.match(line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def extract_labelled_prompt(body: str, label: str) -> str:
    """Pull the blockquote(s) following a `**Label:**` marker within a section.

    Used for the law-closing and full-POD synthesis prompts, which live as
    bold-labelled blockquotes inside a section body.
    """
    lines = body.splitlines()
    want = label.strip().lower().rstrip(":")
    collecting = False
    out: List[str] = []
    for line in lines:
        stripped = line.strip()
        bold = re.match(r"^\*\*(.+?)\*\*\s*$", stripped)
        if bold:
            name = bold.group(1).strip().lower().rstrip(":")
            if collecting:
                break  # next bold label ends the capture
            if name == want:
                collecting = True
            continue
        if collecting:
            if stripped.startswith(">"):
                out.append(stripped.lstrip(">").strip())
            elif stripped == "":
                if out:
                    out.append("")  # preserve paragraph breaks
            elif out:
                break  # non-quote, non-blank line after content ends it
    return "\n".join(out).strip()


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #

def load_skill(root: str | Path) -> Skill:
    root = Path(root)
    manifest = json.loads((root / "skill.json").read_text(encoding="utf-8"))

    laws: List[Law] = []
    for lw in manifest["laws"]:
        facts: List[Fact] = []
        for fc in lw["facts"]:
            file_rel = fc["file"]
            body = (root / file_rel).read_text(encoding="utf-8")
            fact = Fact(
                id=fc["id"],
                n=fc["n"],
                title=fc["title"],
                file=file_rel,
                diagnostic_question=fc.get("diagnostic_question", ""),
                produces=fc.get("produces", []),
                consumes=fc.get("consumes", []),
                parts=fc.get("parts", []),
                sections=_parse_sections(body),
            )
            facts.append(fact)
        cs = lw.get("closing_synthesis") or {}
        fs = lw.get("final_synthesis") or {}
        laws.append(
            Law(
                id=lw["id"],
                name=lw["name"],
                facts=facts,
                closing_synthesis_source=cs.get("source"),
                closing_synthesis_section=cs.get("section"),
                final_synthesis_source=fs.get("source"),
                final_synthesis_section=fs.get("section"),
            )
        )

    return Skill(
        name=manifest["name"],
        version=manifest["version"],
        description=manifest["description"],
        facilitation=manifest.get("facilitation", {}),
        laws=laws,
        root=root,
    )


def read_synthesis_prompt(skill: Skill, source: Optional[str], section: Optional[str]) -> str:
    """Resolve a closing/final synthesis prompt referenced in the manifest."""
    if not source or not section:
        return ""
    body_sections = _parse_sections((skill.root / source).read_text(encoding="utf-8"))
    # The synthesis prompts live inside the fact's final H2 as bold-labelled
    # blockquotes; search every section body for the label.
    for sec_body in body_sections.values():
        prompt = extract_labelled_prompt(sec_body, section)
        if prompt:
            return prompt
    return ""


# --------------------------------------------------------------------------- #
# Session engine
# --------------------------------------------------------------------------- #

# A facilitator runs one fact and returns the finding text to record.
# Signature: facilitator(ctx: FactContext) -> str
Facilitator = Callable[[FactContext], str]

# A synthesiser runs a law-closing or final checkpoint given the prompt text
# and the findings so far. Signature: synthesiser(prompt, findings) -> str
Synthesiser = Callable[[str, Dict[str, str]], str]


@dataclass
class SessionResult:
    findings: Dict[str, str]
    law_headlines: Dict[str, str]
    final_pod: str


class DiagnosticSession:
    """Drives the full POD traversal defined by SKILL.md."""

    def __init__(self, skill: Skill, facilitator: Facilitator, synthesiser: Synthesiser):
        self.skill = skill
        self.facilitate = facilitator
        self.synthesise = synthesiser
        self.findings: Dict[str, str] = {}
        self.law_headlines: Dict[str, str] = {}

    def _carried_in(self, fact: Fact) -> Dict[str, str]:
        return {k: v for k, v in self.findings.items() if k in fact.consumes}

    def run(self) -> SessionResult:
        final_pod = ""
        for law in self.skill.laws:
            for fact in law.facts:
                ctx = FactContext(
                    law=law,
                    fact=fact,
                    findings=dict(self.findings),
                    carried_in=self._carried_in(fact),
                )
                finding = self.facilitate(ctx)
                # Record the finding against each state var this fact produces,
                # so later facts that consume those vars receive it.
                for var in fact.produces:
                    self.findings[var] = finding

            # Law checkpoint.
            closing = read_synthesis_prompt(
                self.skill, law.closing_synthesis_source, law.closing_synthesis_section
            )
            if closing:
                headline = self.synthesise(closing, dict(self.findings))
                self.law_headlines[law.id] = headline
                # Carry the headline forward so the next law's opening can use it.
                self.findings[f"{law.id}_headline"] = headline

            # Full-POD synthesis (declared on the final law only).
            if law.final_synthesis_source:
                final_prompt = read_synthesis_prompt(
                    self.skill, law.final_synthesis_source, law.final_synthesis_section
                )
                if final_prompt:
                    final_pod = self.synthesise(final_prompt, dict(self.findings))

        return SessionResult(
            findings=self.findings,
            law_headlines=self.law_headlines,
            final_pod=final_pod,
        )
