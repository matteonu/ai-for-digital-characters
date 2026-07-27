# Archive — not part of the 21-day plan

Everything here was built for a longer runway than exists. Archived **2026-07-27**, when the plan
changed to a 21-day, 2 h/day push at the 17 August 2026 exam (see [`../cram/PLAN.md`](../cram/PLAN.md)).

Nothing is deleted — it's all recoverable, and worth revisiting after the exam.

| Path | What it was | Why it's here |
|------|-------------|---------------|
| `summaries/latex/` | NetSec-style prose summary, chapters 1–4 of a planned 14 | ~80 pages of prose is the wrong tool for a closed-book exam on a 42-hour budget |
| `summaries/AIDC_Summary_L01-L04.pdf` | Compiled output of the above (18 pp.) | Still readable if you want L01–L04 in prose; not in the plan |
| `summaries/AIDC_Summary_L01-L04_annotated.pdf` | Your annotated copy (2 questions, pp. 11–12) | Both questions are answered in `cram/DEFINITIONS.md` |
| `summaries/pdfs/` | Bullet review PDFs, all 14 lectures | Superseded by `cram/DEFINITIONS.md`, which is exam-question-shaped |
| `summaries/generate_slide_summary_pdfs.py` | Generator for the above (729 lines, content hardcoded) | Only useful if regenerating the bullet PDFs |
| `summaries/PLAN.md` | Production plan for the prose summary | Shelved; chapters 5–14 cancelled |
| `PROCESS.md` | Anki card production pipeline, 6 batches | Batches 3–6 will never be written |
| `SCHEDULE.md` | 55-day study calendar | The runway is 21 days |
| `DECK_SUMMARIES.md` | Per-deck overviews | Only deck `00` is still in use. **Note:** this file credits PPO with a "clipped surrogate objective," which the L14 slides never mention — don't revive it without checking |

LaTeX build artifacts (`main.aux`, `.log`, `.fls`, `.fdb_latexmk`, `.out`, `.toc`) were deleted and
added to `.gitignore`; `latexmk` regenerates them.

## To restore

```bash
git mv archive/summaries summaries
cd summaries/latex && latexmk -pdf main.tex
```
