# AIDC Lecture Summary — Production Plan

**Target style:** [NetSec summary](https://github.com/ymerkli/eth-summaries) — prose lecture script, not bullet cheat sheet.

**Output:** `summaries/latex/AIDC_Lecture_Summary.pdf`

**Status:** Chapters 1–4 drafted (L01–L04). Awaiting review before L05–L14.

---

## Document structure

| Part | Chapters | Lectures | Est. pages | Status |
|------|----------|----------|------------|--------|
| Front matter | Abstract, TOC, pipeline overview | — | 4 | Planned |
| I — Perception & foundations | Ch 1–4 | L01–L04 | ~34 | **Draft** |
| II — Language & speech | Ch 5–9 | L05–L09 | ~44 | Pending review |
| III — Embodiment & agency | Ch 10–14 | L10–L14 | ~37 | Pending review |
| Appendix | Formulas, exam recipes, glossary | — | 8 | Pending |

---

## Writing rules (NetSec style)

1. **Prose first** — explain *why* before *what*; sections open with motivation or **Goal:**
2. **Terms inline** — define before use; maintain glossary consistency
3. **Trade-offs** — after major concepts: limitations, exam traps, **Problem:** / **Solution:**
4. **Calculations** — step-by-step in prose (attention, Mel, artifact detection, WER)
5. **Figures** — key diagrams from slides (to be added in later pass)
6. **Cross-refs** — link forward/back between chapters

---

## Chapter map

### Ch 1 — Introduction (L01)
Pipeline, course map, Digital Einstein, exam format.

### Ch 2 — Affective Computing (L02)
Theories, video features, biosensors, SC/HRV, artifact detection.

### Ch 3 — Deep Learning (L03)
Neural units, RNN/LSTM, encoder-decoder, attention, Transformers.

### Ch 4 — Speech Recognition (L04)
Phonetics, Mel pipeline, CTC/RNN-T/Whisper, WER.

### Ch 5 — Chatbot I (L05) — *pending*
Embeddings, sampling, fine-tuning, PEFT, RLHF.

### Ch 6 — Chatbot II (L06) — *pending*
RAG, retrieval, evaluation metrics.

### Ch 7 — Chatbot III (L07) — *pending*
Multimodal fusion, emotion, personality.

### Ch 8 — Speech Synthesis I (L08) — *pending*
Text normalization, prosody, unit selection.

### Ch 9 — Speech Synthesis II (L09) — *pending*
Tacotron/FastSpeech, vocoders, style transfer.

### Ch 10 — Animation I (L10) — *pending*
Disney principles, FK/IK, skinning.

### Ch 11 — Animation II (L11) — *pending*
DeepPhase, normalizing flows, datasets.

### Ch 12 — Autonomous Agents (L12) — *pending*
Agents, dialogue trees, knowledge graphs, TransE.

### Ch 13 — Applications (L13) — *pending*
Ethics, bias, case studies.

### Ch 14 — Reinforcement Learning (L14) — *pending*
MDP, PPO, behavior synthesis.

---

## Production workflow

| Phase | Task | Status |
|-------|------|--------|
| 1 | LaTeX template + plan | Done |
| 2 | Ch 1–4 prose draft | **Done** (18 pp., `summaries/AIDC_Summary_L01-L04.pdf`) |
| 3 | User review & corrections | **Waiting** |
| 4 | Ch 5–9 | Blocked on review |
| 5 | Ch 10–14 + appendix | Blocked on review |
| 6 | Figure extraction from slides | Later |
| 7 | Exam coverage audit | Later |

---

## File layout

```
summaries/
  PLAN.md                          ← this file
  latex/
    main.tex
    preamble.tex
    frontmatter.tex
    chapters/
      L01_introduction.tex
      L02_affective_computing.tex
      L03_deep_learning.tex
      L04_speech_recognition.tex
      (L05–L14 pending)
    figures/                       ← slide figures (later)
  pdfs/                            ← old bullet summaries (keep as quick review)
```

---

## Verification sources

1. Exercise solutions (`exercises/`)
2. Past exams (`AIChar_Exam_Spring_2024.pdf`, `2025`)
3. Lecture slides (`slides/L_*.pdf`)
4. Anki cards (`anki/cards_data.py`) for exam-critical facts

---

## Review checklist (for user)

- [ ] Tone: explanatory prose vs too dense/sparse?
- [ ] Depth: right level for exam prep?
- [ ] Structure: section numbering and flow?
- [ ] Math notation: clear enough?
- [ ] Missing topics from L01–L04?
- [ ] Figures: which diagrams to embed first?
