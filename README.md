# AI for Digital Characters — Exam Prep

Study materials for the ETH course **Artificial Intelligence for Digital Characters**.

> **Exam: Monday 17 August 2026.** Budget 2 h/day. Target 60/120 — a pass.
> **Start here → [`cram/PLAN.md`](cram/PLAN.md).** Track days in [`progress.md`](progress.md).

## Contents

| Path | Description |
|------|-------------|
| `cram/` | **The active plan** — 21-day schedule, calculation recipes, definitions, drill generator |
| `progress.md` | Daily checklist and recipe confidence tracker |
| `slides/` | Lecture slides (L01–L14) |
| `exercises/` | Exercise sheets and solutions |
| `AIChar_Exam_Spring_*.pdf` | Past exams (2024, 2025) — **keep sealed** until the mocks on Aug 8 / Aug 12 |
| `anki/` | Flashcards — only `decks/00_Exam_MC_Traps.csv` is in the plan |
| `archive/` | Shelved until after the exam ([why](archive/README.md)) |

## Cram materials

```bash
cd cram
python3 drill.py                       # one practice problem per recipe, fresh numbers
python3 drill.py ik mel --answers      # specific recipes, with worked solutions
python3 drill.py --seed 12             # reproducible set
```

- [`cram/CALC_RECIPES.md`](cram/CALC_RECIPES.md) — 13 exam procedures covering ~55 points, plus 4 exercise-only types; all numbers verified
- [`cram/DEFINITIONS.md`](cram/DEFINITIONS.md) — one-line answers to the recurring prose questions

## Anki

Import **one file**: `anki/decks/00_Exam_MC_Traps.csv` (Tab separator, HTML enabled). Its 79 true/false
statements cover the 16–19 point MC block, which is pure recall.

The topic decks `01`–`08` stay in the repo but are not in the plan — `cram/DEFINITIONS.md` and
`cram/CALC_RECIPES.md` cover the same material organized by exam question instead of by lecture.

```bash
cd anki && python3 export_decks.py --verify --export   # only if you edit cards_data.py
```

## Archived

The prose summary, bullet review PDFs, and the old 55-day Anki batch plan are in
[`archive/`](archive/README.md) — shelved on 2026-07-27, restorable in one command.

## Large files (not in repo)

These exceed GitHub's 100 MB limit and are listed in `.gitignore`:

- `Exercises-20260620.zip` — obtain from Moodle
- `exercises/Project/Unity Template.zip` — inside the exercises archive
