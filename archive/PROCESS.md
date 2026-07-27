# Anki Card Production Process — AI for Digital Characters

## Goal
Produce exam-ready Anki cards that are **traceable to course materials** and **independently verifiable**.

## Source hierarchy (highest → lowest trust)
1. **Exercise solutions** (`exercises/Exercise N/*solution*.pdf`) — worked answers with reasoning
2. **Past exams** (`AIChar_Exam_Spring_2024.pdf`, `AIChar_Exam_Spring_2025.pdf`) — defines what is tested
3. **Lecture slides** (`slides/L_*.pdf`) — definitions, formulas, diagrams
4. **Exercise questions** (without solution) — only for card fronts; answers must come from (1) or (3)

Never use external web sources unless cross-checking a formula already present in slides.

## Card creation pipeline (per batch)

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│ Pick topic  │───▶│ Extract from │───▶│ Write card  │───▶│ Verify card  │
│ + batch #   │    │ PDF sources  │    │ in cards.py │    │ (checklist)  │
└─────────────┘    └──────────────┘    └─────────────┘    └──────┬───────┘
                                                                  │
                    ┌──────────────┐    ┌─────────────┐           │
                    │ You import   │◀───│ Export CSV  │◀──────────┘
                    │ into Anki    │    │ per deck    │
                    └──────────────┘    └─────────────┘
```

### Step 1 — Extract
For each batch, read only the relevant PDFs. Log page numbers in the card `sources` field.

### Step 2 — Write (`anki/cards_data.py`)
Each card is a dict:
```python
{
    "deck": "00_Exam_MC_Traps",
    "front": "...",
    "back": "...",
    "tags": ["exam2024", "priority:high"],
    "sources": ["exam2024:Q1a", "solution_ex1:a"],
    "card_type": "mc",  # mc | basic | cloze | calc
}
```

### Step 3 — Verify (mandatory before export)

| Check | Rule |
|-------|------|
| **Source tag** | Every card has ≥1 `sources` entry |
| **MC cards** | Answer matches solution PDF or exam logic; include "Why" on back |
| **Calc cards** | Numbers recomputed independently (Python/numpy); match solution steps |
| **Cloze cards** | One fact per cloze; max 3 clozes per note |
| **No orphan facts** | If a claim appears in slides only, cite `L0N:topic` |
| **Conflicts** | If exam MC contradicts a slide, card back notes both; exam wins |

Run verification:
```bash
cd anki && python3 export_decks.py --verify
```

### Step 4 — Export
```bash
cd anki && python3 export_decks.py
```
Outputs one tab-separated CSV per subdeck in `anki/decks/`.

### Step 5 — Import into Anki
1. File → Import → pick `anki/decks/00_Exam_MC_Traps.csv`
2. Type: **Basic** (or Cloze for `{{c1::...}}` notes)
3. Field separator: Tab
4. Allow HTML in fields: ✓
5. Deck override: use deck name from file header
6. Repeat for each CSV

## Batches (55-day plan)

| Batch | Days | Decks | ~Cards | Primary sources |
|-------|------|-------|--------|-----------------|
| 1 | 1–10 | 00, 01 (partial), 02 (partial) | 120 | Exams MC + Ex1 MC + key concepts |
| 2 | 11–18 | 01, 02, 03 | 80 | Ex1 solutions, L02–L04 |
| 3 | 19–26 | 04, 05 (partial) | 80 | Ex2–Ex3, L05–L09 |
| 4 | 27–34 | 05, 06 | 70 | Ex3–Ex5, L12 |
| 5 | 35–42 | 07, 08 | 70 | Ex4–Ex5, L10–L14 |
| 6 | 43–48 | All (calc drill) | 40 | Exam calc problems |
| — | 49–55 | Review only | 0 new | Filter `priority:high` + `type:calc` |

**New cards:** ~6/day average → ~460 total  
**Daily review target:** start at 20/day, ramp to 80/day by week 6

## Card templates

### MC (exam-style)
- **Front:** Statement exactly as in exam/exercise
- **Back:** `FALSE — [one-line reason]` + optional detail
- **Tag:** `type:mc`

### Basic concept
- **Front:** Question
- **Back:** Answer (2–4 bullet points max) + source line
- **Tag:** `type:basic`

### Calculation
- **Front:** Problem setup with given values
- **Back:** Numbered steps + final answer
- **Tag:** `type:calc`

### Cloze
- **Front:** `Formula: {{c1::1127·ln(1+f/700)}} where f is Hz`
- **Tag:** `type:cloze`

## Quality gates per batch
- [ ] All MC from batch have solution or exam cross-check
- [ ] All calc cards pass `--verify` recomputation
- [ ] No duplicate fronts within same deck
- [ ] Tags include `batch:N` and `source:*`

## File layout
```
anki/
  PROCESS.md          ← this file
  SCHEDULE.md         ← 55-day calendar
  cards_data.py       ← all card definitions (grows per batch)
  export_decks.py     ← verify + export to CSV
  decks/              ← generated CSVs for Anki import
```
