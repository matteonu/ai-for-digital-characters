# Calculation Recipes — the pass-the-exam playbook

Every recipe below has appeared in a past exam. Numbers change year to year; the **procedure does not**.
Learn the procedures, not the theory. All worked numbers here were recomputed and verified.

**Rule for the exam:** always write the formula down first, even if you botch the arithmetic. Both papers
say "write down all formulas and intermediate steps" — partial credit is generous and formula lines are free points.

| # | Recipe | 2024 | 2025 | Points |
|---|--------|------|------|--------|
| 1 | Scaled dot-product attention | Q3 | Q3b ii | 9–10 |
| 2 | Sinusoidal positional encoding | — | Q3b i | 3 |
| 3 | Mel filter banks | Q4 | — | 12 |
| 4 | Word Error Rate | — | Q4a | 5 |
| 5 | Power spectrum | — | Q4b i | 4 |
| 6 | Top-p / top-k sampling | Q5a | Q5b ii | 2–3 |
| 7 | Cosine similarity | — | Q5c i | 4 |
| 8 | Perplexity | — | Q5c ii | 2 |
| 9 | TransE score | — | Q7c | 3 |
| 10 | SPARQL query | Q7c | Q7b ii | 3–5 |
| 11 | Heart rate from R-R | — | Q2c i | 1 |
| 12 | Artifact detection (CBD) | — | Q2c ii | 5 |
| 13 | Inverse kinematics, one Jacobian step | Q9a | Q9a | 10 |

**Exercise-only types** — never yet on an exam, but same format and same lecturer. Cheap insurance;
drill them once each in week 3, not before.

| # | Recipe | Source |
|---|--------|--------|
| 14 | Neural network unit (ReLU) | Ex 1, 3b |
| 15 | HRV standard deviation | Ex 1, 2d |
| 16 | Fidgeting / motion energy | Ex 1, 2c |
| 17 | tf-idf retrieval scoring | Ex 2, 3b |

---

## 1. Scaled dot-product attention

**Three steps, always the same:** scores → softmax → weighted sum.

```
score_t = (q · x_t) / sqrt(d)          d = dimension of the vectors
a_t     = exp(score_t) / Σ exp(score_i)
c       = Σ a_t · x_t
```

**Worked (exam 2024 Q3):** q = [1,0,1], x₁ = [1,0,0], x₂ = [0,1,0], x₃ = [1,1,0], d = 3.

1. Dot products: q·x₁ = 1, q·x₂ = 0, q·x₃ = 1. Divide by √3 = 1.732:
   **scores = [0.577, 0, 0.577]**
2. exp: [1.781, 1.000, 1.781], sum = 4.562:
   **weights = [0.390, 0.219, 0.390]** (check: sums to 1)
3. c = 0.390·x₁ + 0.219·x₂ + 0.390·x₃ = **[0.781, 0.610, 0]**

**Traps:** divide by √d, not d. Weights must sum to 1 — if they don't, you made an arithmetic error, say so and continue. When keys and values aren't given separately, X serves as both.

---

## 2. Sinusoidal positional encoding

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```
Then **add** it to the token embedding (not concatenate).

**Worked (exam 2025 Q3b i):** x₀ = [1,2], x₁ = [3,4], d = 2.

- pos 0: exponent 2i/d = 0 → 10000⁰ = 1. PE = [sin(0), cos(0)] = [0, 1] → x₀ + PE = **[1, 3]**
- pos 1: PE = [sin(1), cos(1)] = [0.84, 0.54] → x₁ + PE = **[3.84, 4.54]**

**Trap:** sin/cos take **radians**. Set your calculator to RAD before the exam starts.

---

## 3. Mel filter banks

```
Mel  = 1127 · ln(1 + f/700)
Hz   = 700 · (e^(m/1127) − 1)
```

**Five steps:**
1. Convert lower and upper bound Hz → Mel.
2. Space (n_filters + 2) points **linearly in Mel**.
3. Convert every point back → Hz.
4. Each filter = (start, peak, end) of three consecutive points, **overlapping by one**.
5. Filters are triangular: 0 at start, 1 at peak, 0 at end.

**Worked (exam 2024 Q4):** 200–8000 Hz, 3 filters, 5 points.

1. Mel(200) = 1127·ln(1.2857) = **283.2**; Mel(8000) = 1127·ln(12.4286) = **2840.0**
2. Spacing = (2840.0 − 283.2)/4 = 639.2 → [283.2, 922.4, 1561.6, 2200.8, 2840.0]
3. Back to Hz → **[200, 887, 2098, 4234, 8000]**
4. Filter 1 = (200, 887, 2098), Filter 2 = (887, 2098, 4234), Filter 3 = (2098, 4234, 8000)

**Traps:** the spacing is linear in Mel and therefore *non-linear* in Hz — the filters get wider at high frequency. That's the whole point of the Mel scale. First and last Hz points must come back out as your original bounds; if they don't, you inverted the formula wrong.

---

## 4. Word Error Rate

```
WER = (S + I + D) / N     N = number of words in the REFERENCE
```

**Worked (exam 2025 Q4a):**
- Reference: `the quick brown fox jumps over the lazy dog` (N = 9)
- Output: `the quick brown fax jump over lazy dogs`

Align word by word: `fox→fax` (S), `jumps→jump` (S), `the` missing (D), `dog→dogs` (S).
**S = 3, I = 0, D = 1** → WER = 4/9 = **44.44 %**

**Also asked (2 pts):** min WER = 0 (perfect). Max is **unbounded / > 100 %**, because insertions are not capped by N — the system can output arbitrarily many extra words.

**Trap:** divide by the reference length, never the hypothesis length. A word that differs only by an inflection (`jump` vs `jumps`) is a substitution, not a match.

---

## 5. Power spectrum

```
P(k) = |X(k)|² / N        N = DFT length
```

**Worked (exam 2025 Q4b i):** X = [0, 1, 5], N = 3 → P = [0²/3, 1²/3, 5²/3] = **[0, 0.33, 8.33]**

**Meaning (say this):** the power spectrum gives the energy at each frequency bin, i.e. how much of each frequency is present in that frame.

**Part ii answer:** applied to **short-time frames** (20–40 ms), not the whole signal, because speech is non-stationary — its frequency content changes over time, so a whole-signal DFT would smear all the phonemes together.

---

## 6. Top-p (nucleus) and top-k sampling

**top-k:** keep the k highest-probability tokens. **top-p:** keep the smallest set whose cumulative probability **≥ p** — the size varies with the shape of the distribution.

**Worked (exam 2025 Q5b ii):** p = 0.85, probs cat 0.35, dog 0.30, runs 0.15, fast 0.10, tree 0.06, blue 0.04.

| token | p | cumulative |
|---|---|---|
| cat | 0.35 | 0.35 |
| dog | 0.30 | 0.65 |
| runs | 0.15 | 0.80 |
| fast | 0.10 | **0.90 ≥ 0.85 → stop** |

**Candidates = {cat, dog, runs, fast}.** Then renormalize over those four and sample.

**Trap:** you include the token that *crosses* the threshold. Stopping at 0.80 because "0.90 overshoots" is the classic wrong answer.

---

## 7. Cosine similarity

```
cos(A,B) = (A · B) / (‖A‖ · ‖B‖)
```

**Worked (exam 2025 Q5c i):** eA = [0.5, 0.1, 0.4], eB = [0.4, 0.3, 0.1].

1. Dot: 0.5·0.4 + 0.1·0.3 + 0.4·0.1 = 0.20 + 0.03 + 0.04 = **0.27**
2. ‖eA‖ = √(0.25+0.01+0.16) = √0.42 = **0.6481**
3. ‖eB‖ = √(0.16+0.09+0.01) = √0.26 = **0.5099**
4. cos = 0.27 / (0.6481 · 0.5099) = 0.27 / 0.3305 = **0.82**

---

## 8. Perplexity

```
PPL = (Π p_i)^(−1/N)   =   exp( −(1/N) Σ ln p_i )
```

**Worked (exam 2025 Q5c ii):** p = [0.20, 0.10, 0.15, 0.25], N = 4.

Product = 0.20·0.10·0.15·0.25 = 0.00075 → PPL = 0.00075^(−1/4) = **6.04**

**Trap:** the exponent is *negative* 1/N. Lower perplexity = better model.

---

## 9. TransE

```
score(h, r, t) = ‖h + r − t‖     (L2 norm; lower = more plausible)
```

**Worked (exam 2025 Q7c i):** Clark [2.0, 1.5, −0.5] + supervise [−0.2, −0.7, 0.3] − Mark [1.8, 0.8, −0.2]
= [0, 0, 0] → score = **0.0** (a perfectly modelled triple).

**Part ii:** Mark [1.8,0.8,−0.2] + affiliatedWith [1.2,0.6,0.8] − CS Dept [3.2,2.1,0.3] = [−0.2,−0.7,0.3] → ‖·‖ = **0.79 < 2.0 → likely true.**

**Part iii — the symmetry argument (write exactly this):** if (h,r,t) and (t,r,h) are both true, TransE requires h + r ≈ t **and** t + r ≈ h. Adding them gives 2r ≈ 0, so r ≈ 0, which then forces h ≈ t — the two entities collapse to the same embedding and become indistinguishable. TransE therefore cannot represent symmetric relations.

---

## 10. SPARQL

Pattern for "find X such that A **and** B **and** C" — one triple pattern per condition, sharing the variable:

```sparql
SELECT ?researcher WHERE {
  ?researcher uni:affiliatedWith "Computer Science Department" .
  ?researcher uni:published      ?paper .
  ?paper      uni:presentedAt    "ICML" .
  ?researcher uni:lead           ?project .
}
```

**Query type (1 free point):** three conditions joined by AND on one variable = a **conjunctive query**.
One relation hop = one-hop query; chained relations = path query.

**Traps:** every line ends with ` .`; the final one may too. Reuse the *same* variable name to express the AND.

---

## 11. Heart rate from R-R interval

```
HR (bpm) = 60000 / RR(ms)
```
**Worked:** RR = 400 ms → 60000/400 = **150 bpm**. (Free point. Do not miss it.)

---

## 12. Artifact detection (Criterion Beat Difference)

Formulas are **given on the exam paper** — you only need the order of operations.

```
QD  = (Q3 − Q1) / 2
MAD = (Median − 2.9 × QD) / 3
MED = 3.32 × QD
CBD = (MAD + MED) / 2
```
Then: the beat is an artifact if **|RR − last valid RR| > CBD** (or if it falls outside the 300–2000 ms validity range).

**Worked (exam 2025 Q2c ii):** R-R = {795, 800, 400, 810, 800, 805}, last valid = 800.

1. Sort: [400, 795, 800, 800, 805, 810]
2. Q1 = median of lower half [400,795,800] = **795**; Q3 = median of upper half [800,805,810] = **805**; Median = **800**
3. QD = (805 − 795)/2 = **5.00**
4. MAD = (800 − 2.9·5)/3 = 785.5/3 = **261.83**
5. MED = 3.32 · 5 = **16.60**
6. CBD = (261.83 + 16.60)/2 = **139.22**
7. |400 − 800| = 400 > 139.22 → **artifact.** (400 ms is inside the 300–2000 range, so the range check alone would not have caught it — say this.)

---

## 13. Inverse kinematics — one Jacobian step

**This is 10 points in both papers and the pseudoinverse is handed to you.** Five sub-steps:

```
i)   e⁰ = F(θ)                    forward kinematics
ii)  Δe = e* − e⁰                 error to target
iii) J                            partial derivatives
iv)  Δθ = α · J⁺ · Δe
v)   θ_new = θ + Δθ
```

For an n-link planar arm, with c₁ = cos θ₁, c₁₂ = cos(θ₁+θ₂), …:

```
e = [ L₁c₁ + L₂c₁₂ + L₃c₁₂₃ ,  L₁s₁ + L₂s₁₂ + L₃s₁₂₃ ]

      ⎡ −L₁s₁ − L₂s₁₂ − L₃s₁₂₃   −L₂s₁₂ − L₃s₁₂₃   −L₃s₁₂₃ ⎤
J  =  ⎣  L₁c₁ + L₂c₁₂ + L₃c₁₂₃    L₂c₁₂ + L₃c₁₂₃    L₃c₁₂₃ ⎦
```
**Column j drops every term before joint j.** Row 1 = ∂x/∂θ (sines, negative), row 2 = ∂y/∂θ (cosines, positive). That's the whole trick.

**Worked (exam 2025 Q9a):** L = [2,2,1], θ = [π/6, π/6, π/6], e* = [5,2], α = 0.1.
Angles: θ₁ = 30°, θ₁+θ₂ = 60°, θ₁+θ₂+θ₃ = 90°.

1. e⁰ = [2(0.866) + 2(0.5) + 1(0), 2(0.5) + 2(0.866) + 1(1)] = **[2.73, 3.73]**
2. Δe = [5 − 2.73, 2 − 3.73] = **[2.27, −1.73]**
3. J = ⎡ −3.73  −2.73  −1 ⎤
       ⎣  2.73   1.00   0 ⎦
4. J⁺Δe with the given J⁺ = [−1.47, −0.76, −0.32]; × α = 0.1 → **Δθ = [−0.15, −0.08, −0.03]**
5. θ_new = 0.524 + Δθ = **[0.38, 0.45, 0.49]** rad

**Traps:** work in **radians** throughout. Δe = target − current, not the reverse. Don't forget to multiply by α. In step v the answer stays in radians — no need to convert.

---

## 14. Neural network unit (ReLU)

```
z = wᵀx + b        output = ReLU(z) = max(0, z)
```

**Worked (Exercise 1, 3b):** w = [2.2, −3, 1.5], x = [0, 5, 8], b = 3.
z = (2.2·0) + (−3·5) + (1.5·8) + 3 = 0 − 15 + 12 + 3 = **0** → ReLU(0) = **0**.

**Trap:** ReLU(0) = 0, and the exercise is built so z lands exactly on 0. Don't panic and assume you erred.

---

## 15. HRV as standard deviation

```
σ = sqrt( (1/N) · Σ(xᵢ − x̄)² )      ← divide by N, not N−1
```

**Worked (Exercise 1, 2d):** seq = {72, 75, 70, 73, 76}.
1. Mean = 366/5 = **73.2**
2. Squared deviations: 1.44 + 3.24 + 10.24 + 0.04 + 7.84 = **22.8**
3. σ = √(22.8/5) = **2.14**

For {74, 71, 76, 79, 80}: mean 76, Σ = 54, σ = √(54/5) = **3.29**.

**Interpretation (they always ask):** **higher** HRV = relaxed, adaptive, resilient autonomic system.
**Lower** HRV = stress, anxiety, reduced flexibility.

---

## 16. Fidgeting / motion energy

Four steps on a frame `f` against a running background `b`:

```
1. f_temp = f − b
2. binarize: 1 where |f_temp| > t, else 0
3. E = (surviving pixels / total pixels) × 100 %
4. update background: b' = (1 − α)·b + α·f
```

**Worked (Exercise 1, 2c):** with t = 5, one pixel of the 3×3 difference fell at or below threshold,
giving 8 survivors → E = 8/9 × 100 = **88.89 %**. With α = 0.2, b' = 0.8·b + 0.2·f elementwise.

**Traps:** the comparison is **strictly greater than** t — a difference of exactly t is *not* counted.
Use the absolute value: motion is movement in either direction.

---

## 17. tf-idf retrieval scoring

```
tf(t,d)  = 1 + log₁₀ count(t,d)   if the term occurs, else 0
idf(t)   = log₁₀( N / df(t) )      N = number of documents, df = docs containing t
tf-idf   = tf · idf
score(q,d) = cosine between the tf-idf vectors of q and d
```

**Worked (Exercise 2, 3b):** query *"deep learning transformers"*, 3 documents.

- "deep" appears in all 3 → idf = log₁₀(3/3) = **0** — a term in every document carries **no**
  discriminative information.
- "learning" in 2 → idf = log₁₀(1.5) = **0.176**
- "transformers" in 1 → idf = log₁₀(3) = **0.477**

Each count is 1, so every tf = 1 + log₁₀(1) = 1 and tf-idf = idf. Query vector norm =
√(0² + 0.176² + 0.477²) = **0.509**. Normalize each document over **all** its terms (not just query
terms) — Doc 1's norm came to 1.194 — then take the cosine.

**Traps:** tf is **1 + log₁₀(count)**, not the raw count. A term present in every document scores zero.
Document normalization runs over every term in the document.

---

## Exam-day checklist

- Calculator in **RAD** mode. Non-programmable only; a neutral dictionary is allowed.
- Write the formula on its own line before every calculation. Free partial credit.
- 120 points in 120 minutes → **1 minute per point.** The IK question is worth 10 — don't spend 25 minutes on it.
- MC block: **−1 for wrong, 0 for blank**, floor of 0 for the block. If you genuinely don't know, leave it blank; a coin flip has zero expected value.
- If you run out of time on a calculation, write the remaining *steps* in words. Method earns points.
