# Screening log (placeholder)

Use R or Python to maintain a machine-readable screening table. Keep decisions auditable.

Suggested columns:

- `id`
- `bib_key`
- `title`
- `year`
- `source`
- `include_title_abstract` (yes/no/maybe)
- `include_full_text` (yes/no)
- `exclusion_reason`
- `theme_tags`
- `notes`

## Search strings (draft)

### Perioperative assessment

`(perioperative OR preoperative OR "pre-operative" OR anaesthesia OR anesthesia) AND (risk OR fitness OR "functional assessment" OR "chart review" OR personalis* OR personaliz*)`

### Clinical LLM / agents

`(LLM OR "large language model" OR "AI agent" OR "clinical decision support") AND (perioperative OR preoperative OR anaesthesia OR anesthesia OR surgery)`

Refine by database syntax before running formal searches.
