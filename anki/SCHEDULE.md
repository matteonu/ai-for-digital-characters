# 55-Day Study Schedule — AI for Digital Characters

**Assumption:** ~6 new cards/day, ramping reviews from 20 → 100/day.

## Phase overview

| Phase | Days | Focus | New cards | Daily reviews |
|-------|------|-------|-----------|---------------|
| 1 | 1–10 | Batch 1 import + MC mastery | 130 (done) | 20→40 |
| 2 | 11–18 | Batch 2: affective, DL, speech rec | +80 | 40→60 |
| 3 | 19–26 | Batch 3: chatbots, TTS deep dive | +80 | 60→70 |
| 4 | 27–34 | Batch 4: KG, agents, SPARQL | +70 | 70→80 |
| 5 | 35–42 | Batch 5: RL, animation calcs | +70 | 80→90 |
| 6 | 43–48 | Batch 6: remaining calcs + gaps | +40 | 90 |
| 7 | 49–55 | Exam simulation + weak-card drill | 0 | 100 |

---

## Week-by-week

### Week 1 (Days 1–7) — Foundation
- **Day 1:** Import `anki/decks/*.csv`. Study deck `00_Exam_MC_Traps` (exam 2024 MC only).
- **Day 2:** Finish `00` (exam 2025 + exercise MC). Tag any card you miss `leech`.
- **Day 3:** Deck `01_Affective_Computing` + re-read L02 slides (phasic/tonic SC).
- **Day 4:** Deck `02_Attention_Deep_Learning` — redo attention calc cards by hand.
- **Day 5:** Deck `03_Speech_Recognition_Mel` — practice Mel conversion on paper.
- **Day 6:** Deck `04_Chatbots_LLM` (sampling, prompt engineering).
- **Day 7:** **Rest / light review only** — filter `priority:high`, max 30 cards.

### Week 2 (Days 8–14) — Consolidate Batch 1
- **Day 8:** Deck `05_Speech_Synthesis` + Exercise 3 solutions.
- **Day 9:** Deck `06_Knowledge_Graphs` + Exercise 5 KG section.
- **Day 10:** Decks `07` + `08`. Import Batch 2 when ready.
- **Day 11–14:** Batch 2 new cards (~10/day) + 40 reviews. Re-do Exercise 1 fully timed.

### Week 3 (Days 15–21) — Speech + Chatbots depth
- **Days 15–17:** Batch 2 completion. L04 + L05–L07 slide review for gaps.
- **Day 18:** Exercise 2 timed (LLM section).
- **Days 19–21:** Batch 3 start (~10/day). Focus top-p, perplexity, RAG, Tacotron/FastSpeech.

### Week 4 (Days 22–28) — Midpoint exam
- **Day 22:** **Timed mock:** Exam 2024 (2 h, closed book). Score MC + note weak sections.
- **Days 23–25:** Batch 3 completion. Add cards only for mock gaps.
- **Day 26:** Exercise 3 timed.
- **Days 27–28:** Batch 4 start (KG, SPARQL, TransE).

### Week 5 (Days 29–35) — Agents + RL
- **Days 29–31:** Batch 4 completion. L12 autonomous agents slides.
- **Day 32:** Exercise 5 timed.
- **Days 33–35:** Batch 5 (RL formulation, PPO, IK Jacobian full walkthrough).

### Week 6 (Days 36–42) — Animation + calc drill
- **Days 36–38:** Batch 5 completion. L10–L11 animation. Exercise 4 timed.
- **Days 39–42:** Batch 6 calc cards. Daily: 1 attention, 1 Mel, 1 IK, 1 TransE problem by hand.

### Week 7 (Days 43–48) — Second mock
- **Day 43:** **Timed mock:** Exam 2025 (2 h).
- **Days 44–46:** Fix all leeches. Re-study missed mock questions → new cards if needed.
- **Days 47–48:** Mixed review: `tag:priority:high` + `tag:type:calc`.

### Week 8 (Days 49–55) — Exam week
- **Day 49:** Full deck review (split across 2 days if needed).
- **Day 50:** MC only — both exams, 30 min timed.
- **Day 51:** Calculation sprint — all `type:calc` cards.
- **Day 52:** Concept maps: draw pipeline diagrams from memory (TTS, chatbot, agent).
- **Day 53:** Light review of `leech` + `priority:high` only.
- **Day 54:** Read exam MC traps once; no new material.
- **Day 55 (exam eve):** 20-card warm-up max. Sleep.

---

## Weekly habits
1. **After each exercise:** add cards for anything you couldn't explain without notes.
2. **After each mock exam:** 30 min card creation for gaps only.
3. **Saturdays:** one timed exercise or half-exam.
4. **Anki settings:** new cards/day = 8 (weeks 1–4), 4 (weeks 5–6), 0 (week 7–8).

## Import reminder
```bash
cd "AI for Digital Characters/anki"
python3 export_decks.py --verify --export
```
Then import each file in `decks/` into Anki (File → Import, Tab separator, HTML on).
