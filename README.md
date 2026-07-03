# AI for Digital Characters — Exam Prep

Study materials for the ETH course **Artificial Intelligence for Digital Characters**, including lecture slides, exercises, past exams, and Anki flashcards.

## Contents

| Path | Description |
|------|-------------|
| `slides/` | Lecture slides (L01–L14) |
| `exercises/` | Exercise sheets and solutions |
| `AIChar_Exam_Spring_*.pdf` | Past exams (2024, 2025) |
| `anki/` | Anki card source (`cards_data.py`) and importable decks |

## Anki decks

```bash
cd anki
python3 export_decks.py --verify --export
```

Import the CSV files from `anki/decks/` into Anki (Tab separator, HTML enabled).

See `anki/PROCESS.md`, `anki/SCHEDULE.md`, and `anki/DECK_SUMMARIES.md` for the study workflow and per-deck overviews.

## Slide summaries

**NetSec-style prose summary (recommended):**
- Part 1 (L01–L04): [`summaries/AIDC_Summary_L01-L04.pdf`](summaries/AIDC_Summary_L01-L04.pdf)
- LaTeX source: `summaries/latex/` — compile with `latexmk -pdf main.tex`
- Production plan: [`summaries/PLAN.md`](summaries/PLAN.md)

**Quick bullet review PDFs** (older format): `summaries/pdfs/`

```bash
cd summaries/latex && latexmk -pdf main.tex
```

## Large files (not in repo)

These exceed GitHub's 100 MB limit and are listed in `.gitignore`:

- `Exercises-20260620.zip` — obtain from Moodle
- `exercises/Project/Unity Template.zip` — inside the exercises archive
