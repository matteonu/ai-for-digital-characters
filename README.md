# AI for Digital Characters — Exam Prep

Study materials for the ETH course **Artificial Intelligence for Digital Characters**.

> **Exam: Monday 17 August 2026.** Budget 2 h/day. Target 60/120 — a pass.
> **Start here → [`cram/PLAN.md`](cram/PLAN.md).** Track days in [`progress.md`](progress.md).

The repo holds two things and nothing else: the **study material for the plan**, and the **sources**
it was built from.

## Study material

| Path | Description |
|------|-------------|
| [`cram/PLAN.md`](cram/PLAN.md) | The 21-day schedule, 2 h/day |
| [`cram/CALC_RECIPES.md`](cram/CALC_RECIPES.md) | 13 exam calculations (~55 points) + 4 exercise-only types, every number verified |
| [`cram/DEFINITIONS.md`](cram/DEFINITIONS.md) | One-line answers to the recurring prose questions |
| [`cram/drill.py`](cram/drill.py) | Practice problems with fresh numbers and worked solutions |
| [`progress.md`](progress.md) | Daily checklist and recipe confidence tracker |
| `anki/decks/00_Exam_MC_Traps.csv` | 79 true/false cards for the MC block |

## Sources

| Path | Description |
|------|-------------|
| `slides/` | Lecture slides (L01–L14) |
| `exercises/` | Exercise sheets and solutions |
| `AIChar_Exam_Spring_*.pdf` | Past exams — **keep sealed** until the mocks on Aug 8 and Aug 12 |

## Drilling

```bash
cd cram
python3 drill.py                        # one problem per recipe, fresh numbers
python3 drill.py ik mel                  # just these two
python3 drill.py --seed 12 --answers     # a pinned set, with worked solutions
```

Every run prints its seed and the command to get the same problems back with answers. The two past
papers stay sealed for the mocks, so practice always uses generated numbers.

Recipes: `attention pe mel wer power topp cosine perplexity transe sparql hr artifact ik`
plus the exercise-only `relu hrv fidget tfidf`.

## Anki

Import **one file**: `anki/decks/00_Exam_MC_Traps.csv` (Tab separator, HTML enabled). Its 79 true/false
statements cover the 16–19 point MC block, which is pure recall — the one place flashcards beat a document.

The topic decks `01`–`08` were removed: `cram/DEFINITIONS.md` and `cram/CALC_RECIPES.md` cover the same
ground organized by exam question rather than by lecture. `cards_data.py` still holds all 201 cards, so
`python3 export_decks.py --verify --export` regenerates every deck if you want them back.

## Removed material

Cleared out of the working tree on 2026-08-06 to leave only what the plan uses. All of it is still in
git history — nothing is lost:

- the NetSec-style LaTeX prose summary (chapters 1–4) and its compiled PDFs
- the bullet review PDFs for all 14 lectures, and their generator
- the 55-day Anki batch plan (`PROCESS.md`, `SCHEDULE.md`, `DECK_SUMMARIES.md`)
- Anki decks `01`–`08`

```bash
git log --diff-filter=D --oneline        # find the commit that removed a file
git checkout <commit>^ -- archive/       # restore the whole archive
```

## Large files (not in repo)

Exceed GitHub's 100 MB limit, listed in `.gitignore`:

- `Exercises-20260620.zip` — obtain from Moodle
- `exercises/Project/Unity Template.zip` — inside the exercises archive
