# Ethix Grundansökan template

Offline working copy of the in-progress Ethix application.

| File | Purpose |
|------|---------|
| `ethix-template.pdf` | Source export from Ethix (from `main`) |
| `ethix-template.raw.txt` | Raw PDF text extraction |
| `ethix-template.md` | Human-editable field map with draft slots |
| `ethix-template-fields.yaml` | Machine-readable fields for scripts |

## Regenerate from PDF

```bash
python scripts/convert_ethix_template.py
```

## Draft workflow

1. Write content in Swedish in `ethix-template.md` or linked Quarto docs
2. Map umbrella plan sections → Ethix fields (`source_doc` in YAML)
3. Paste final answers into Ethix portal manually

## Field counts

After conversion: **68** fields; **18** need draft text (others prefilled or placeholders).

Key open sections:

- §3 Syfte och frågeställningar (3.1–3.3)
- §4 Metod (4.1–4.3)
- §5 Tidsplan (5.3)
- §6 Datainsamling (6.1–6.4)
- §7 Etiska överväganden (7.1–7.5)
- §8 Forskningspersoner (8.1–8.9)
- §9 Information och samtycke (9.1.2, 9.3.1–9.3.2)
- §10 Register (10.1.1–10.1.2)
- §12 Redovisning (12.1–12.4)
- §13 Ekonomi (13.3–13.4)

Prefilled highlights: observational study, sensitive health data, register/journal data, no direct participant contact (9.1 Nej), includes persons unable to consent (9.3 Ja).
