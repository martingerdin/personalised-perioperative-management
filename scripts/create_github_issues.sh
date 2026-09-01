#!/usr/bin/env bash
# Create GitHub issues from the research documents plan.
# Idempotent: skips titles that already exist as open issues.

set -euo pipefail
REPO="${1:-martingerdin/personalised-perioperative-management}"

exists() {
  local title="$1"
  gh issue list --repo "$REPO" --state all --search "in:title \"$title\"" --json title --jq '.[].title' | grep -Fxq "$title"
}

create() {
  local title="$1"
  local body="$2"
  local labels="${3:-}"
  if exists "$title"; then
    echo "SKIP (exists): $title"
    return 0
  fi
  if [[ -n "$labels" ]]; then
    gh issue create --repo "$REPO" --title "$title" --body "$body" --label "$labels"
  else
    gh issue create --repo "$REPO" --title "$title" --body "$body"
  fi
  echo "CREATED: $title"
}

create "Design note: lock population, data source, and primary outcome" "$(cat <<'EOF'
## Goal
Write a one-page design note before drafting protocols or Ethix answers.

## Deliverable
`docs/design-note.qmd` (or `.md`) covering:

- Population and setting (Sweden; perioperative / anaesthesia context)
- Data sources (registers, journals — name access route when known)
- Primary design: observational (SPIROS) vs interventional (SPIRIT contingency)
- Primary and secondary outcome *families*
- AI processing boundary (assistive only; no autonomous clinical decisions)

## Acceptance
- [ ] Signed off by responsible researcher
- [ ] Referenced from umbrella and detailed research plans

## References
- `docs/plan-research-documents.qmd`
- `docs/two-research-plans.md`
EOF
)"

create "Draft umbrella research plan for Ethix" "$(cat <<'EOF'
## Goal
Draft the stable, broad protocol annexed to the Ethix Grundansökan.

## Deliverable
`docs/research-plan-umbrella.qmd` — SPIROS-aligned, Swedish where required for annex.

## Must include
- Aims and research questions (programme level)
- Observational design bounds; SPIRIT noted only as future contingency
- Population, data categories, consent/legal basis options
- AI processing principles, human oversight, risk classes
- Dissemination and AI-writing transparency (link `meta/ai-attribution-summary.md`)

## Must avoid locking
Exact model names, prompts, package versions, sprint details.

## Acceptance
- [ ] SPIROS checklist (`checklists/spiros-checklist.md`) completed with section refs
- [ ] Consistent with design note
- [ ] Detailed plan can fit inside these bounds

## References
- `docs/plan-research-documents.qmd`
- `docs/ethix/ethix-template.md`
EOF
)"

create "Draft detailed research plan" "$(cat <<'EOF'
## Goal
Write the living internal plan that guides day-to-day research work.

## Deliverable
`docs/research-plan-detailed.qmd`

## Must include
- Workstreams and milestones
- Architecture (agents, tools, retrieval, audit logs)
- Model shortlist and evaluation protocol
- Traceability matrix: each workstream → umbrella aim

## Rule
Stay **inside** umbrella bounds. Flag anything that would need an Ethix ändringsansökan.

## Acceptance
- [ ] Every workstream maps to an umbrella aim
- [ ] No wider population, data route, or purpose than umbrella plan

## References
- `docs/two-research-plans.md`
- Blocked on: umbrella plan draft (can start in parallel with explicit assumptions)
EOF
)"

create "Build search strategy and seed bibliography" "$(cat <<'EOF'
## Goal
Set up systematic search and expand `references/project.bib`.

## Deliverables
- Search strings in `scripts/README.md` (refined for PubMed/Scopus syntax)
- Screening log schema / starter CSV
- `references/project.bib` with methods guidelines + first perioperative/LLM hits

## Tasks
- [ ] Refine perioperative and clinical-LLM search strings
- [ ] Export results to BibTeX
- [ ] Deduplicate and verify DOIs
- [ ] Optional: `scripts/bibliography_check.py`

## References
- `docs/plan-research-documents.qmd` § literature review method
EOF
)"

create "Run literature screening and evidence tables" "$(cat <<'EOF'
## Goal
Screen titles/abstracts and build structured evidence tables.

## Deliverables
- Machine-readable screening table (R or Python)
- Theme tags aligned with the five literature-review scope questions

## Tasks
- [ ] Title/abstract inclusion decisions with reasons
- [ ] Full-text screen where needed
- [ ] Extract: design, population, exposure, outcomes, limitations

## References
- Depends on: search strategy issue
- `docs/plan-research-documents.qmd` § literature review
EOF
)"

create "Draft short literature review" "$(cat <<'EOF'
## Goal
Write `docs/literature-review.qmd` (1,500–2,500 words).

## Answer these five questions only
1. Preoperative risk assessment and personalised perioperative planning
2. Chart review / structured data for fitness-for-anaesthesia
3. LLM/agent evidence in clinical documentation, triage, care planning
4. Safety, bias, privacy, accountability gaps
5. Gap this project addresses

## Rules
- First person, short sentences, no AI hype
- Every claim cited from `references/project.bib`
- Mark confidence: strong / limited / speculation

## Acceptance
- [ ] Renders via Quarto to HTML/PDF
- [ ] Human review of all citations

## References
- Depends on: screening issue
EOF
)"

create "Draft Ethix answers: syfte, metod, tidsplan, data (§3–§6)" "$(cat <<'EOF'
## Goal
Draft Swedish paste-ready answers for Ethix sections 3–6.

## Fields (see `docs/ethix/ethix-template-fields.yaml`)
- 3.1–3.3 Populärvetenskaplig sammanfattning, syfte, frågeställningar
- 4.1–4.3 Metod
- 5.3 Tidsplan
- 6.1–6.4 Datainsamling

## Deliverables
- Draft text in `docs/ethics-application.qmd` and/or `docs/ethix/ethix-template.md`
- `source_doc` links in YAML updated

## Must align with
- Umbrella research plan (not detailed-only details that widen scope)

## References
- `docs/ethix/ethix-template.md`
EOF
)"

create "Draft Ethix answers: etik och forskningspersoner (§7–§8)" "$(cat <<'EOF'
## Goal
Draft Swedish answers for ethical considerations and participants.

## Fields
- 7.1–7.5 Risker, nytta, risk–nytta, riskminimering, långsiktiga etiska frågor
- 8.1–8.9 Urval, N, kriterier, relation, försäkring, oväntade fynd

## AI-specific content
- No autonomous decisions; clinician accountable
- OpenRouter / open-weight model processing boundaries
- Bias, equity, failure modes, incident reporting

## Deliverables
- `docs/ethics-application.qmd` sections
- Updates to `docs/ethix/ethix-template.md`

## References
- Umbrella plan + `docs/ai-transparency.md`
EOF
)"

create "Draft Ethix answers: information, register, resultat (§9–§12)" "$(cat <<'EOF'
## Goal
Draft Swedish answers for consent model, registers, and dissemination.

## Fields
- 9.1.2, 9.3.1–9.3.2 (no direct contact; includes persons unable to consent)
- 10.1.1–10.1.2 Register/journal data
- 12.1–12.4 Data access, analysis responsibility, publication, integrity

## Deliverables
- Ethix draft answers
- Annex list for upload (umbrella plan PDF, data flow, risk register)

## References
- Official stödmallar for FPI/samtycke (authority website)
- `docs/ethix/ethix-template.md`
EOF
)"

create "Draft annexes: FPI, samtycke, and Ethix uploads" "$(cat <<'EOF'
## Goal
Prepare bilagor referenced in the Ethix application.

## Deliverables
- Forskningspersonsinformation (from official stödmall, adapted)
- Samtycke or waiver documentation as applicable
- Umbrella research plan PDF for upload
- Data flow diagram
- Risk register (AI + chart review)

## Note
Prefilled Ethix answers indicate no direct participant information (9.1 Nej) but includes persons unable to consent (9.3 Ja) — align annexes with that model.

## Acceptance
- [ ] Plain Swedish, lay-readable where required
- [ ] Consistent with §7–§10 answers
EOF
)"

create "Consistency pass: plans, Ethix, SPIROS, AI disclosure" "$(cat <<'EOF'
## Goal
Final internal review before Ethix paste and external review.

## Checks
- [ ] Detailed plan ⊆ umbrella plan
- [ ] Ethix answers match umbrella plan (aims, data, consent, AI processing)
- [ ] SPIROS checklist complete with section/page refs
- [ ] `python scripts/ai_attribution.py refresh` — weighted AI % cited in umbrella plan
- [ ] Quarto renders: literature review, both plans, ethics draft
- [ ] All 18 open Ethix fields have draft text

## Deliverable
Issue checklist closed; submission-ready PDF pack in `docs/`

## References
- `docs/plan-research-documents.qmd` acceptance criteria
EOF
)"

create "Complete Ethix admin fields and paste into portal" "$(cat <<'EOF'
## Goal
Fill remaining prefilled/placeholder admin fields and submit via Ethix.

## Tasks
- [ ] 1.5, 1.6.1 Hemvist / institution
- [ ] 5.1–5.2 Start/slutdatum
- [ ] 8.2 Antal forskningspersoner
- [ ] 13.3–13.4 Finansiering and conflicts detail
- [ ] Invite signatories in Ethix
- [ ] Upload bilagor
- [ ] Manual paste of all draft answers from `docs/ethix/ethix-template.md`

## Human-only
Requires Ethix login and BankID/signing workflow.

## References
- `docs/ethix/ethix-template.pdf`
EOF
)"

echo "Done."
