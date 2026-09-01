#!/usr/bin/env python3
"""Convert Ethix Grundansökan PDF export to structured markdown and YAML."""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber
import yaml

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "docs" / "ethix" / "ethix-template.pdf"
TXT = ROOT / "docs" / "ethix" / "ethix-template.raw.txt"
MD = ROOT / "docs" / "ethix" / "ethix-template.md"
YAML_OUT = ROOT / "docs" / "ethix" / "ethix-template-fields.yaml"

# Common PDF ligature / encoding fixes from this export
FIXES = {
    "perioperave": "perioperativa",
    "Marn": "Martin",
    "uppgier": "uppgifter",
    "Instuon": "Institution",
    "Innefaar": "Innefattar",
    "personuppgier": "personuppgifter",
    "iniala": "initiala",
    "omfaas": "omfattas",
    "ekprövningslagen": "etikprövningslagen",
    "Innefaar": "Innefattar",
    "yrande": "yttrande",
    "Cirkulaonsorganens": "Cirkulationsorganens",
    "Observaon": "Observation",
    "donaon": "donation",
    "förginingar": "förgiftningar",
    "yre": "yttre",
    " ll ": " till ",
    "Sye": "Syfte",
    "sammanfaning": "sammanfattning",
    "syet": "syftet",
    "avsni": "avsnitt",
    "digare": "tidigare",
    "moverar": "motiverar",
    "Eska": "Etiska",
    "e ": "ett ",
    "nyan": "nyttan",
    "uormats": "utformats",
    "Idenfiera": "Identifiera",
    "eska": "etiska",
    "perspekv": "perspektiv",
    "relaon": "relation",
    "Informaon": "Information",
    "llfrågas": "tillfrågas",
    "hälsollstånd": "hälsotillstånd",
    "ll ": "till ",
    "llt": "till",
    "llgång": "tillgång",
    "skrilig": "skriftlig",
    "rä ll": "rätt till",
    "företagsinierad": "företagsinitierad",
    "selse": "stiftelse",
}


def clean_line(text: str) -> str:
    text = text.replace("\x00", "")
    for bad, good in FIXES.items():
        text = text.replace(bad, good)
    return re.sub(r"\s+", " ", text).strip()


def clean_block(text: str) -> str:
    lines = [clean_line(ln) for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def extract_pdf() -> str:
    parts: list[str] = []
    with pdfplumber.open(PDF) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            t = page.extract_text() or ""
            parts.append(f"--- Page {i} ---\n{t}")
    return "\n\n".join(parts)


def parse_fields(text: str) -> list[dict]:
    """Parse numbered Ethix questions from cleaned text."""
    text = clean_block(text)
    # Drop page markers
    text = re.sub(r"--- Page \d+ ---", "\n", text)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    fields: list[dict] = []
    current_section = ""
    i = 0
    section_re = re.compile(r"^(\d+)\.\s+(.+)$")
    question_re = re.compile(r"^(\d+(?:\.\d+)+(?:\.\d+)?)\s+(.+)$")

    while i < len(lines):
        line = lines[i]
        sec = section_re.match(line)
        if sec and not question_re.match(line):
            current_section = f"{sec.group(1)}. {sec.group(2)}"
            i += 1
            continue

        q = question_re.match(line)
        if q:
            qid = q.group(1)
            prompt = q.group(2)
            # Collect answer lines until next question/section
            answers: list[str] = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if section_re.match(nxt) and not question_re.match(nxt):
                    break
                if question_re.match(nxt):
                    break
                if nxt in {"Signaturer"}:
                    break
                answers.append(nxt)
                i += 1
            answer = clean_line(" ".join(answers)) if answers else ""
            status = "todo"
            if answer in {"", "-"}:
                answer = ""
            elif answer.startswith("✓"):
                status = "prefilled"
            elif answer in {"Ja", "Nej"}:
                status = "prefilled"
            elif re.fullmatch(r"\d+", answer.replace(" ", "")):
                status = "prefilled"
            elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", answer):
                status = "placeholder"
            else:
                status = "prefilled" if answer else "todo"

            fields.append(
                {
                    "id": qid,
                    "section": current_section,
                    "prompt_sv": prompt,
                    "answer": answer,
                    "status": status,
                    "draft_sv": "",
                    "source_doc": "",
                }
            )
            continue
        i += 1

    return fields


def write_markdown(meta: dict, fields: list[dict]) -> None:
    lines = [
        "# Ethix Grundansökan — field map",
        "",
        "Converted from `ethix-template.pdf` for offline drafting. Paste answers into Ethix manually.",
        "",
        "## Application metadata",
        "",
        f"- **Title:** {meta.get('title', '')}",
        f"- **Type:** {meta.get('type', '')}",
        f"- **Subject area:** {meta.get('subject_area', '')}",
        f"- **Status:** {meta.get('status', '')}",
        f"- **Principal investigator:** {meta.get('pi', '')}",
        "",
        "## Sections",
        "",
    ]

    by_section: dict[str, list[dict]] = {}
    for f in fields:
        by_section.setdefault(f["section"], []).append(f)

    for section, items in by_section.items():
        if not section:
            continue
        lines.append(f"### {section}")
        lines.append("")
        for f in items:
            flag = {"todo": "🔲", "prefilled": "✅", "placeholder": "⚠️"}.get(
                f["status"], "🔲"
            )
            lines.append(f"#### {flag} {f['id']} {f['prompt_sv']}")
            lines.append("")
            if f["answer"]:
                lines.append(f"**Current Ethix value:** {f['answer']}")
                lines.append("")
            lines.append("**Draft answer (sv):**")
            lines.append("")
            lines.append("_To write._")
            lines.append("")
            lines.append(f"**Maps to:** `{f.get('source_doc', '') or 'TBD'}`")
            lines.append("")

    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    raw = extract_pdf()
    TXT.write_text(raw, encoding="utf-8")
    fields = parse_fields(raw)

    meta = {
        "title": "Personalised perioperative medicine",
        "type": "Grundansökan",
        "subject_area": "Medicin och hälsovetenskap",
        "status": "Påbörjad ansökan",
        "pi": "Martin Knut Erik Filippus Gerdin Wärnberg",
        "source_pdf": "docs/ethix/ethix-template.pdf",
    }

    payload = {"meta": meta, "fields": fields}
    YAML_OUT.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    write_markdown(meta, fields)
    todo = sum(1 for f in fields if f["status"] == "todo")
    print(f"Wrote {len(fields)} fields ({todo} need draft answers)")
    print(f"  {MD.relative_to(ROOT)}")
    print(f"  {YAML_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
