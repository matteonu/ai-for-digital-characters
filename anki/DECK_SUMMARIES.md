# Anki Deck Summaries

**Total: 201 cards** across 9 subdecks (Batches 1–2 complete).

| Deck | Cards | Types | Lectures / Sources |
|------|-------|-------|-------------------|
| `00_Exam_MC_Traps` | 79 | MC only | Exams 2024+2025, Exercises 1–5 |
| `01_Affective_Computing` | 35 | 30 basic, 5 calc | L02, Ex1 |
| `02_Attention_Deep_Learning` | 27 | 18 basic, 8 calc, 1 cloze | L03, Ex1, exam calc |
| `03_Speech_Recognition_Mel` | 27 | 19 basic, 8 calc | L04, Ex1, exam calc |
| `04_Chatbots_LLM` | 8 | 5 basic, 3 calc | L05–L07, Ex2 |
| `05_Speech_Synthesis` | 7 | 7 basic | L08–L09, Ex3 |
| `06_Knowledge_Graphs` | 6 | 5 basic, 1 calc | L12, Ex5 |
| `07_Reinforcement_Learning` | 4 | 4 basic | L14, Ex5 |
| `08_Animation` | 8 | 5 basic, 3 calc | L10–L11, Ex4 |

---

## 00 — Exam MC Traps (79 cards)

**Purpose:** Rapid-fire True/False practice for the scored MC block (−1 per wrong answer, floor 0).

**What's covered:**
- All 19 MC statements from Exam 2024 and 16 from Exam 2025
- All exercise MC questions (Exercises 1–5)
- Every card includes the correct answer **and** a one-line explanation of why

**High-yield traps to know cold:**
- Mel scale is logarithmic, not linear
- RNN-T supports streaming; pruning removes *least* important weights
- James-Lange is sequential; Cannon-Bard is simultaneous
- Dialogue trees = low flexibility; PEFT trains a subset of params (not fewer total)
- FastSpeech duration repeat → speech slows; RL reward is not differentiable
- LBS fails at large angles; Slow In/Out ≠ linear motion

**Study tip:** Run this deck before each mock exam. Tag misses as `leech` and review the explanation on the back.

---

## 01 — Affective Computing (35 cards)

**Purpose:** Emotion theory, biosignals, and video-based affect recognition — typically worth ~10–13 exam points.

**Key topics:**
- **Theories:** James-Lange, Cannon-Bard, Schachter-Singer, dimensional model (valence/arousal/dominance), Ekman's basic emotions
- **Video features:** Action Units (FACS), eye blinks (AU45), gaze, Mouth Aspect Ratio, fidgeting pipeline
- **Biosignals:** ECG, PPG, HRV (time-domain measures), skin conductance (phasic vs. tonic, cvxEDA)
- **SC response features:** amplitude, latency, rise time, half-recovery
- **Artifact detection:** QD → MAD → MED → CBD formulas (exam 2025)
- **Ground truth:** Self-Assessment Manikin (SAM)

**Calculation cards (5):** fidgeting energy %, HRV σ for two sequences, HR from R-R interval, full artifact CBD check

**Study tip:** Draw the phasic SC curve and label features 1–4 from memory. Practice the artifact algorithm once on paper.

---

## 02 — Attention & Deep Learning (27 cards)

**Purpose:** Neural nets, RNNs, attention, and Transformers — exam always includes an attention calculation (~10 pts).

**Key topics:**
- **Basics:** z = w·x + b, ReLU/softmax, cross-entropy loss, BPTT
- **RNNs:** hidden state, vanishing gradients, LSTM gates, bidirectional/stacked RNNs, sequence classification
- **Encoder-decoder:** context vector, teacher forcing vs. inference
- **Attention:** scaled dot-product (score → softmax → weighted sum), self- vs. cross-attention, multi-head, masked decoder attention
- **Transformers:** positional encoding formula, skip connections, layer norm

**Calculation cards (8):** ReLU unit, attention (exam 2024 vectors), attention exercise (q/k/v), transformer PE (exam 2025)

**Study tip:** Always write out the three attention steps (scores → weights → context) before looking at the answer. Know *why* masked attention exists.

---

## 03 — Speech Recognition & Mel (27 cards)

**Purpose:** ASR feature pipeline and Mel filter banks — exam includes a full Mel calculation (~12 pts).

**Key topics:**
- **Phonetics:** phones, F0 vs. pitch, Mel scale formula
- **Feature pipeline:** windowing (20–40 ms, Hamming) → DFT/FFT → power spectrum → Mel filter bank → log
- **Mel construction:** 5-step process, triangular overlapping filters
- **Evaluation:** WER (substitutions, insertions, deletions)
- **Architectures:** encoder-decoder subsampling, CTC (blank token), RNN-T (encoder + predictor + joiner, streaming), Whisper
- **Augmentation:** time warping, frequency masking, time masking
- **ADC:** sampling + quantization

**Calculation cards (8):** waveform f/A, Mel endpoints (exercise + exam), full filter definitions, WER (33.3% / 37.5%)

**Study tip:** Practice one complete Mel problem (Hz → Mel → spaced points → Hz → filter triples) without notes. This is the most formula-heavy deck.

---

## 04 — Chatbots & LLM (8 cards)

**Purpose:** LLM adaptation, sampling, and evaluation — worth ~17 exam points but only partially covered so far (Batch 3 will expand).

**Key topics:**
- **Sampling:** greedy, top-k, top-p/nucleus (with numeric example)
- **Adaptation:** fine-tuning disadvantages vs. prompt engineering; PEFT, RAG (mentioned in MC deck)
- **Prompt engineering:** zero-shot CoT, few-shot, self-ask; few-shot format mimicry failure
- **Metrics:** perplexity formula, cosine similarity between sentence embeddings

**Calculation cards (3):** top-p candidate set (p=0.85), cosine similarity, perplexity

**Study tip:** Be able to compute top-p by cumulative sum. Know three fine-tuning disadvantages and three prompt strategies for open-ended exam questions.

---

## 05 — Speech Synthesis (7 cards)

**Purpose:** TTS pipeline and vocoders — worth ~13–18 exam points (Batch 3 will expand).

**Key topics:**
- **Pipeline:** text normalization → phonetic analysis → prosody → acoustic model → vocoder
- **Unit selection:** diphones, target cost vs. join cost
- **Acoustic models:** Tacotron 2 (autoregressive + attention) vs. FastSpeech (duration predictor, parallel)
- **Vocoders:** Griffin-Lim, WaveNet, HiFi-GAN, DiffWave (forward/reverse diffusion, mel conditioning)
- **Multi-speaker:** learned speaker embeddings vs. one-hot

**Calculation cards:** none yet

**Study tip:** Always compare Tacotron vs. FastSpeech in terms of speed *and* architecture. Know what DiffWave conditions on.

---

## 06 — Knowledge Graphs (6 cards)

**Purpose:** RDF triples, SPARQL, and embeddings — growing exam weight (10–13 pts in 2025).

**Key topics:**
- **Representation:** RDF triples (subject, predicate, object)
- **Querying:** SPARQL for structured queries; KGE (TransE) for large/incomplete graphs
- **TransE:** score = ‖h + r − t‖; symmetric relation limitation
- **Link prediction** and query types (one-hop, path, conjunctive)

**Calculation cards (1):** TransE score with given embeddings

**Study tip:** Practice writing a simple SPARQL SELECT query. Know why TransE fails on symmetric relations mathematically.

---

## 07 — Reinforcement Learning (4 cards)

**Purpose:** MDP formulation and PPO — worth ~10–13 exam points (Batch 5 will expand).

**Key topics:**
- **MDP:** state, action, reward, policy, return
- **Value functions:** Q(s,a) and V(s) relationship
- **PPO + Actor-Critic:** critic baseline, clipped surrogate, sample efficiency
- **Why RL:** non-differentiable simulators (can't backprop through physics)

**Calculation cards:** none yet

**Study tip:** Be ready to define state/action/reward/policy for a word problem (robot navigation, soccer dribbling). Reward does *not* need to be differentiable.

---

## 08 — Animation (8 cards)

**Purpose:** Classical and learning-based animation — includes Jacobian IK calculation (~14 pts).

**Key topics:**
- **FK vs. IK:** forward = angles → position; inverse = target → angles
- **Jacobian IK:** Δθ = α · J⁺ · Δe
- **LBS:** candy-wrapper artifact at large joint angles
- **Modern:** DeepPhase (phase-aware motion manifolds), normalizing flows (invertible maps, Jacobian determinant)

**Calculation cards (3):** full one-step IK update (e₀, Δe, Δθ) from exam 2024 / Exercise 4

**Study tip:** Work through the IK calculation by hand at least twice. Know Disney's Slow In/Out (ease in/out, not linear).

---

## Suggested review order

1. `00_Exam_MC_Traps` — highest ROI per minute
2. `type:calc` across decks 02, 03, 08 — exam always tests calculations here
3. `priority:high` tag across all decks
4. Decks 04–07 — expand as Batches 3–5 are added

Regenerate decks after card updates:
```bash
cd anki && python3 export_decks.py --verify --export
```
