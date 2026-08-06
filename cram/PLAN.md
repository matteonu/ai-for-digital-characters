# 21-Day Pass Plan — exam Monday 17 August 2026

**Budget:** 2 h/day × 21 days = **42 hours.** That is the entire budget. Nothing outside this plan.

**Goal:** 60/120. Not a good grade — a pass.

**Strategy:** the exam is ~55 points of mechanical calculation plus a 16–19 point MC block. Drill those
to reflex, memorize a short list of one-line definitions, and ignore everything else. Do not read the
lecture slides cover to cover; you do not have time and it is not how the points are earned.

**Explicitly dropped:** the LaTeX prose summary (chapters 5–14), the bullet review PDFs, figure
extraction, expanding Anki decks `01`–`08`, and deep understanding of any topic. Removed from the
working tree on 2026-08-06 but still in git history — see "Removed material" in the [README](../README.md).

**On Anki:** only deck `00_Exam_MC_Traps` survives. Its 79 true/false statements map directly onto the
16–19 point MC block, which is pure recall and the format's natural fit. The topic decks `01`–`08` are
superseded by `DEFINITIONS.md` and `CALC_RECIPES.md`, which cover the same ground organized by exam
question rather than by lecture. Ignore the old spaced-repetition ramp (20 → 100 reviews/day) — over
21 days you want repeated full passes, not an SRS schedule tuned for months.

---

## Week 1 (Jul 27 – Aug 2) — calculations only

The highest-value week. Everything here is worth points on both past papers.

| Day | Date | 2 hours |
|-----|------|---------|
| 1 | Mon Jul 27 | Read `CALC_RECIPES.md` start to finish (30 min). Then recipes **1 & 2** (attention, positional encoding) by hand: `python3 drill.py attention pe` ×3 rounds. |
| 2 | Tue Jul 28 | Recipes **3, 4, 5** (Mel, WER, power spectrum). Mel is 12 pts on the 2024 paper — do it until the Hz endpoints come back out correctly every time. |
| 3 | Wed Jul 29 | Recipe **13 (IK Jacobian)** — 10 pts on *both* papers, the single biggest item. `python3 drill.py ik` ×4. Learn the "column j drops every term before joint j" rule. |
| 4 | Thu Jul 30 | Recipes **6, 7, 8** (top-p, cosine, perplexity) + **9, 10** (TransE, SPARQL): `python3 drill.py topp cosine perplexity transe sparql`. All short, all cheap points. |
| 5 | Fri Jul 31 | Recipes **11, 12** (heart rate, artifact CBD). Then a full mixed set: `python3 drill.py`. |
| 6 | Sat Aug 1 | Full mixed drill, **timed at 1 min/point**. Redo every one you got wrong. |
| 7 | Sun Aug 2 | Light. First pass through Anki deck `00_Exam_MC_Traps` only. Stop after 30 min. |

**Week 1 exit test:** you can do all 13 recipes from a blank sheet without opening the playbook.

---

## Week 2 (Aug 3 – 9) — MC block + one-line definitions

Each definition day pairs with a short calc drill so Week 1's recipes don't decay.

| Day | Date | 2 hours |
|-----|------|---------|
| 8 | Mon Aug 3 | Anki deck `00_Exam_MC_Traps` (79 cards). 16–19 exam points, pure memorization. **The only deck you need to import.** |
| 9 | Tue Aug 4 | `DEFINITIONS.md` Q2–Q4 (affective, deep learning, speech recognition) + `drill.py attention mel wer`. |
| 10 | Wed Aug 5 | `DEFINITIONS.md` Q5–Q6 (LLMs, speech synthesis) + `drill.py topp cosine perplexity`. |
| 11 | Thu Aug 6 | `DEFINITIONS.md` Q7–Q9 (knowledge graphs, RL, animation) + `drill.py transe sparql ik`. |
| 12 | Fri Aug 7 | Full mixed calc drill + full MC deck pass. |
| 13 | **Sat Aug 8** | **MOCK 1: Exam 2024. 2 hours, closed book, calculator in RAD.** |
| 14 | Sun Aug 9 | Grade mock 1 against the point table. Write down every lost point. Nothing else. |

---

## Week 3 (Aug 10 – 16) — fix and rehearse

| Day | Date | 2 hours |
|-----|------|---------|
| 15 | Mon Aug 10 | Fix the biggest gaps from mock 1, highest-point-value first. |
| 16 | Tue Aug 11 | Definition drill — the recurring one-liners (see `DEFINITIONS.md`). |
| 17 | **Wed Aug 12** | **MOCK 2: Exam 2025. 2 hours, closed book.** |
| 18 | Thu Aug 13 | Grade mock 2. Fix gaps. |
| 19 | Fri Aug 14 | Every calc recipe once, timed — **including the four exercise-only ones**: `python3 drill.py relu hrv fidget tfidf`. |
| 20 | Sat Aug 15 | Full MC deck + definitions. |
| 21 | Sun Aug 16 | Light skim of `CALC_RECIPES.md` only. Pack calculator (**RAD mode**), ID. Sleep. |
| — | **Mon Aug 17** | **EXAM.** |

---

## Why drills use fresh numbers

You only have two past papers and they are your only honest measurement of where you stand. If you
practise on them directly, you will memorize their answers and your mock score will overstate your
readiness — dangerous when the target is a bare pass.

So: **`drill.py` generates the same problems with new numbers**; the two real papers stay sealed until
Aug 8 and Aug 12.

```bash
cd cram
python3 drill.py                 # one problem per recipe
python3 drill.py ik mel          # just these
python3 drill.py --seed 12       # reproducible set
python3 drill.py --seed 12 --answers   # same set, with solutions
```

---

## Exam-day rules

- **1 minute per point.** 120 points, 120 minutes. Check the clock at the halfway mark.
- **Answer the calculations first**, in any order you like — they are the reliable points. Prose answers last.
- **Write the formula before every calculation.** Both papers award partial credit for method.
- **MC block: blank beats a guess.** −1 for wrong, 0 for blank, block floors at 0.
- Calculator in **radians**. Non-programmable only; a neutral dictionary is permitted.

---

## Honest risks

1. **The 2026 paper may swap in a calculation neither past paper used.** Partly covered now: the four
   exercise-only types (ReLU unit, HRV σ, fidgeting energy, tf-idf) are in the drill and scheduled for
   day 19. The exercises and exams share a format and an author, so an exercise calculation is the most
   likely source of a surprise question.
2. **Prose answers are ~40 % of the paper** and this plan largely writes them off. That is the deliberate
   trade for a 42-hour budget — it is why the target is 60, not 80.
3. **Missing a mock is not recoverable.** Aug 8 and Aug 12 are the two immovable dates in this plan.
