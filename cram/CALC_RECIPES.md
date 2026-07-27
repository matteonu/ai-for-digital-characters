# Calculation Recipes — the pass-the-exam playbook

Every recipe below has appeared in a past exam. Numbers change year to year; the **procedure does not**.
Learn the procedures, not the theory. All worked numbers here were recomputed and verified.

> Math renders in Cursor/VS Code markdown preview (`⇧⌘V`) and on GitHub. Raw text in an editor pane
> will show the LaTeX source instead.

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

$$
s_t = \frac{\mathbf{q}^\top \mathbf{x}_t}{\sqrt{d}}
\qquad
a_t = \frac{e^{s_t}}{\sum_{i} e^{s_i}}
\qquad
\mathbf{c} = \sum_t a_t \mathbf{x}_t
$$

where $d$ is the dimension of the vectors.

**Worked (exam 2024 Q3):**

$$
\mathbf{q} = \begin{bmatrix}1\\0\\1\end{bmatrix},\quad
\mathbf{x}_1 = \begin{bmatrix}1\\0\\0\end{bmatrix},\quad
\mathbf{x}_2 = \begin{bmatrix}0\\1\\0\end{bmatrix},\quad
\mathbf{x}_3 = \begin{bmatrix}1\\1\\0\end{bmatrix},\quad d = 3
$$

**(a)** Dot products $\mathbf{q}^\top\mathbf{x}_t = 1,\,0,\,1$, divided by $\sqrt{3} = 1.732$:

$$s = \begin{bmatrix}0.577 & 0 & 0.577\end{bmatrix}$$

**(b)** Exponentiate: $e^{0.577} = 1.781,\; e^{0} = 1.000,\; e^{0.577} = 1.781$, sum $= 4.562$:

$$a = \begin{bmatrix}0.390 & 0.219 & 0.390\end{bmatrix}, \qquad \textstyle\sum_t a_t = 1 \;\checkmark$$

**(c)** Context vector:

$$
\mathbf{c} = 0.390\,\mathbf{x}_1 + 0.219\,\mathbf{x}_2 + 0.390\,\mathbf{x}_3
= \begin{bmatrix}0.781\\0.610\\0\end{bmatrix}
$$

**Traps:** divide by $\sqrt{d}$, not $d$. The weights must sum to $1$ — if they don't, you made an
arithmetic error; say so and continue. When keys and values aren't given separately, $X$ serves as both.

---

## 2. Sinusoidal positional encoding

$$
PE_{(pos,\,2i)} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right)
\qquad
PE_{(pos,\,2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right)
$$

Then **add** it to the token embedding (not concatenate): $\mathbf{x}'_{pos} = \mathbf{x}_{pos} + PE_{pos}$.

**Worked (exam 2025 Q3b i):** $\mathbf{x}_0 = [1, 2]^\top$, $\mathbf{x}_1 = [3, 4]^\top$, $d = 2$.

With $d = 2$ there is only $i = 0$, so the exponent is $2i/d = 0$ and $10000^0 = 1$:

$$
PE_0 = \begin{bmatrix}\sin 0\\ \cos 0\end{bmatrix} = \begin{bmatrix}0\\1\end{bmatrix}
\;\Longrightarrow\;
\mathbf{x}'_0 = \begin{bmatrix}1\\2\end{bmatrix} + \begin{bmatrix}0\\1\end{bmatrix} = \begin{bmatrix}1\\3\end{bmatrix}
$$

$$
PE_1 = \begin{bmatrix}\sin 1\\ \cos 1\end{bmatrix} = \begin{bmatrix}0.84\\0.54\end{bmatrix}
\;\Longrightarrow\;
\mathbf{x}'_1 = \begin{bmatrix}3\\4\end{bmatrix} + \begin{bmatrix}0.84\\0.54\end{bmatrix} = \begin{bmatrix}3.84\\4.54\end{bmatrix}
$$

**Trap:** $\sin$ and $\cos$ take **radians**. Set your calculator to RAD before the exam starts.

---

## 3. Mel filter banks

$$
m = 1127 \ln\!\left(1 + \frac{f}{700}\right)
\qquad\qquad
f = 700\left(e^{m/1127} - 1\right)
$$

**Five steps:**

1. Convert the lower and upper bound from Hz to Mel.
2. Space $n_\text{filters} + 2$ points **linearly in Mel**: $\;m_i = m_\text{low} + i\cdot\dfrac{m_\text{high} - m_\text{low}}{n+1}$
3. Convert every point back to Hz.
4. Each filter is $(\text{start},\,\text{peak},\,\text{end})$ of three consecutive points, **overlapping by one**.
5. Filters are triangular: $0$ at start, $1$ at peak, $0$ at end.

**Worked (exam 2024 Q4):** $200$–$8000$ Hz, $3$ filters, $5$ points.

**(1)** $m_\text{low} = 1127\ln(1 + \tfrac{200}{700}) = 1127\ln(1.2857) = 283.2$

  $m_\text{high} = 1127\ln(1 + \tfrac{8000}{700}) = 1127\ln(12.4286) = 2840.0$

**(2)** Spacing $= \dfrac{2840.0 - 283.2}{4} = 639.2$:

$$m = \begin{bmatrix}283.2 & 922.4 & 1561.6 & 2200.8 & 2840.0\end{bmatrix}$$

**(3)** Back to Hz via $f = 700(e^{m/1127} - 1)$:

$$f = \begin{bmatrix}200 & 887 & 2098 & 4234 & 8000\end{bmatrix}\ \text{Hz}$$

**(4)** $\text{Filter}_1 = (200,\,887,\,2098)$, $\text{Filter}_2 = (887,\,2098,\,4234)$, $\text{Filter}_3 = (2098,\,4234,\,8000)$

**Traps:** the spacing is linear in Mel and therefore *non-linear* in Hz — filters get wider at high
frequency, which is the whole point of the Mel scale. The first and last Hz points must come back out as
your original bounds; if they don't, you inverted the formula wrong.

---

## 4. Word Error Rate

$$
\text{WER} = \frac{S + I + D}{N}
$$

where $N$ is the number of words in the **reference**, and $S$, $I$, $D$ are substitutions, insertions
and deletions.

**Worked (exam 2025 Q4a):**

- Reference: `the quick brown fox jumps over the lazy dog` — so $N = 9$
- Output: `the quick brown fax jump over lazy dogs`

Aligning word by word: `fox`→`fax` (S), `jumps`→`jump` (S), `the` missing (D), `dog`→`dogs` (S).

$$S = 3,\quad I = 0,\quad D = 1 \qquad\Longrightarrow\qquad \text{WER} = \frac{4}{9} = 44.44\,\%$$

**Also asked (2 pts):** the minimum is $\text{WER} = 0$ (perfect transcription). The maximum is
**unbounded**, $\text{WER} > 100\,\%$, because $I$ is not capped by $N$ — the system can emit arbitrarily
many extra words.

**Trap:** divide by the reference length, never the hypothesis length. A word differing only by
inflection (`jump` vs `jumps`) is a substitution, not a match.

---

## 5. Power spectrum

$$
P(k) = \frac{|X(k)|^2}{N}
$$

where $N$ is the DFT length.

**Worked (exam 2025 Q4b i):** $X = [0,\,1,\,5]$, $N = 3$:

$$
P = \left[\frac{0^2}{3},\; \frac{1^2}{3},\; \frac{5^2}{3}\right] = [0,\; 0.33,\; 8.33]
$$

**Meaning (say this):** the power spectrum gives the energy at each frequency bin, i.e. how much of each
frequency is present in that frame.

**Part ii answer:** applied to **short-time frames** ($20$–$40$ ms), not the whole signal, because speech
is non-stationary — its frequency content changes over time, so a whole-signal DFT would smear all the
phonemes together.

---

## 6. Top-p (nucleus) and top-k sampling

**top-k:** keep the $k$ highest-probability tokens.
**top-p:** keep the smallest set $V^{(p)}$ such that

$$\sum_{t \in V^{(p)}} P(t) \;\ge\; p$$

so its size adapts to the shape of the distribution.

**Worked (exam 2025 Q5b ii):** $p = 0.85$.

| token | $P(t)$ | cumulative |
|---|---|---|
| cat | 0.35 | 0.35 |
| dog | 0.30 | 0.65 |
| runs | 0.15 | 0.80 |
| fast | 0.10 | $\mathbf{0.90 \ge 0.85}$ → stop |

Candidates $= \{\text{cat},\,\text{dog},\,\text{runs},\,\text{fast}\}$, then renormalize over those four and sample.

**Trap:** you include the token that *crosses* the threshold. Stopping at $0.80$ because $0.90$ overshoots
is the classic wrong answer.

---

## 7. Cosine similarity

$$
\cos(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|\,\|\mathbf{B}\|}
= \frac{\sum_i A_i B_i}{\sqrt{\sum_i A_i^2}\,\sqrt{\sum_i B_i^2}}
$$

**Worked (exam 2025 Q5c i):** $\mathbf{e}_A = [0.5,\,0.1,\,0.4]$, $\mathbf{e}_B = [0.4,\,0.3,\,0.1]$.

$$\mathbf{e}_A \cdot \mathbf{e}_B = (0.5)(0.4) + (0.1)(0.3) + (0.4)(0.1) = 0.20 + 0.03 + 0.04 = 0.27$$

$$\|\mathbf{e}_A\| = \sqrt{0.25 + 0.01 + 0.16} = \sqrt{0.42} = 0.6481$$

$$\|\mathbf{e}_B\| = \sqrt{0.16 + 0.09 + 0.01} = \sqrt{0.26} = 0.5099$$

$$\cos = \frac{0.27}{0.6481 \times 0.5099} = \frac{0.27}{0.3305} = \mathbf{0.82}$$

---

## 8. Perplexity

$$
\text{PPL} = \left(\prod_{i=1}^{N} p_i\right)^{-1/N}
= \exp\!\left(-\frac{1}{N}\sum_{i=1}^{N} \ln p_i\right)
$$

**Worked (exam 2025 Q5c ii):** $p = [0.20,\,0.10,\,0.15,\,0.25]$, $N = 4$.

$$\prod_i p_i = 0.20 \times 0.10 \times 0.15 \times 0.25 = 0.00075$$

$$\text{PPL} = 0.00075^{-1/4} = \mathbf{6.04}$$

**Trap:** the exponent is **negative** $1/N$. Lower perplexity means a better model.

---

## 9. TransE

$$
\text{score}(h, r, t) = \|\mathbf{h} + \mathbf{r} - \mathbf{t}\|
$$

using the $L_2$ norm — **lower is more plausible**, because a true triple should satisfy $\mathbf{h} + \mathbf{r} \approx \mathbf{t}$.

**Worked (exam 2025 Q7c i):**

$$
\underbrace{\begin{bmatrix}2.0\\1.5\\-0.5\end{bmatrix}}_{\text{Clark}}
+ \underbrace{\begin{bmatrix}-0.2\\-0.7\\0.3\end{bmatrix}}_{\text{supervise}}
- \underbrace{\begin{bmatrix}1.8\\0.8\\-0.2\end{bmatrix}}_{\text{Mark}}
= \begin{bmatrix}0\\0\\0\end{bmatrix}
\;\Longrightarrow\; \text{score} = 0.0
$$

a perfectly modelled triple.

**Part ii:** $\text{Mark} + \text{affiliatedWith} - \text{CS Dept} = [-0.2,\,-0.7,\,0.3]$, so

$$\text{score} = \sqrt{0.04 + 0.49 + 0.09} = 0.79 < 2.0 \;\Longrightarrow\; \textbf{likely true.}$$

**Part iii — the symmetry argument (write exactly this):** if $(h,r,t)$ and $(t,r,h)$ are both true, TransE requires

$$\mathbf{h} + \mathbf{r} \approx \mathbf{t} \qquad\text{and}\qquad \mathbf{t} + \mathbf{r} \approx \mathbf{h}$$

Adding the two equations gives $\mathbf{h} + \mathbf{t} + 2\mathbf{r} \approx \mathbf{t} + \mathbf{h}$, hence

$$2\mathbf{r} \approx \mathbf{0} \;\Longrightarrow\; \mathbf{r} \approx \mathbf{0} \;\Longrightarrow\; \mathbf{h} \approx \mathbf{t}$$

The relation collapses to the zero vector and the two entities collapse to the **same embedding**, becoming
indistinguishable. TransE therefore cannot represent symmetric relations.

---

## 10. SPARQL

Pattern for "find $X$ such that A **and** B **and** C" — one triple pattern per condition, sharing the variable:

```sparql
SELECT ?researcher WHERE {
  ?researcher uni:affiliatedWith "Computer Science Department" .
  ?researcher uni:published      ?paper .
  ?paper      uni:presentedAt    "ICML" .
  ?researcher uni:lead           ?project .
}
```

**Query type (1 free point):** three conditions AND-ed on one variable is a **conjunctive query**.
One relation hop is a one-hop query; chained relations form a path query.

**Traps:** every line ends with ` .`; the final one may too. Reuse the *same* variable name to express the AND.

---

## 11. Heart rate from R-R interval

$$
\text{HR}\;[\text{bpm}] = \frac{60000}{\text{RR}\;[\text{ms}]}
$$

**Worked:** $\text{RR} = 400$ ms $\Rightarrow \text{HR} = \dfrac{60000}{400} = \mathbf{150}$ bpm.
(Free point. Do not miss it.)

---

## 12. Artifact detection (Criterion Beat Difference)

The formulas are **given on the exam paper** — you only need the order of operations.

$$
QD = \frac{Q_3 - Q_1}{2}
\qquad
MAD = \frac{\text{Median} - 2.9\,QD}{3}
\qquad
MED = 3.32\,QD
$$

$$
CBD = \frac{MAD + MED}{2}
$$

A beat is an artifact if $\;|\text{RR} - \text{RR}_\text{last valid}| > CBD\;$ (or if it falls outside the
$300$–$2000$ ms validity range).

**Worked (exam 2025 Q2c ii):** R-R $= \{795,\,800,\,400,\,810,\,800,\,805\}$, last valid $= 800$ ms.

**(1)** Sort: $[400,\,795,\,800,\,800,\,805,\,810]$

**(2)** $Q_1 = \text{median}[400,795,800] = 795$, $\;Q_3 = \text{median}[800,805,810] = 805$, $\;\text{Median} = 800$

**(3)** $QD = \dfrac{805 - 795}{2} = 5.00$

**(4)** $MAD = \dfrac{800 - 2.9(5)}{3} = \dfrac{785.5}{3} = 261.83$

**(5)** $MED = 3.32 \times 5 = 16.60$

**(6)** $CBD = \dfrac{261.83 + 16.60}{2} = 139.22$

**(7)** $|400 - 800| = 400 > 139.22 \;\Longrightarrow\; \textbf{artifact.}$

Note that $400$ ms lies **inside** the $300$–$2000$ ms range, so the range check alone would not have
caught it — say this.

---

## 13. Inverse kinematics — one Jacobian step

**This is 10 points in both papers and the pseudoinverse is handed to you.** Five sub-steps:

$$
\text{(i)}\;\; \mathbf{e}^0 = F(\boldsymbol\theta)
\qquad
\text{(ii)}\;\; \Delta\mathbf{e} = \mathbf{e}^* - \mathbf{e}^0
\qquad
\text{(iii)}\;\; J = \frac{\partial \mathbf{e}}{\partial \boldsymbol\theta}
$$

$$
\text{(iv)}\;\; \Delta\boldsymbol\theta = \alpha\, J^{+} \Delta\mathbf{e}
\qquad
\text{(v)}\;\; \boldsymbol\theta^{1} = \boldsymbol\theta^{0} + \Delta\boldsymbol\theta
$$

For a planar arm, writing $c_1 = \cos\theta_1$, $c_{12} = \cos(\theta_1+\theta_2)$, $s_{12} = \sin(\theta_1+\theta_2)$, …

$$
\mathbf{e} = \begin{bmatrix}
L_1 c_1 + L_2 c_{12} + L_3 c_{123}\\
L_1 s_1 + L_2 s_{12} + L_3 s_{123}
\end{bmatrix}
$$

$$
J = \begin{bmatrix}
-L_1 s_1 - L_2 s_{12} - L_3 s_{123} & -L_2 s_{12} - L_3 s_{123} & -L_3 s_{123}\\
\phantom{-}L_1 c_1 + L_2 c_{12} + L_3 c_{123} & \phantom{-}L_2 c_{12} + L_3 c_{123} & \phantom{-}L_3 c_{123}
\end{bmatrix}
$$

**Column $j$ drops every term before joint $j$.** Row 1 is $\partial x/\partial\theta$ (sines, negative),
row 2 is $\partial y/\partial\theta$ (cosines, positive). That's the whole trick.

**Worked (exam 2025 Q9a):** $L = [2,\,2,\,1]$, $\;\theta_1 = \theta_2 = \theta_3 = \tfrac{\pi}{6}$,
$\;\mathbf{e}^* = [5,\,2]^\top$, $\;\alpha = 0.1$.

Cumulative angles: $\theta_1 = 30°$, $\theta_1 + \theta_2 = 60°$, $\theta_1+\theta_2+\theta_3 = 90°$.

**(i)** $\mathbf{e}^0 = \begin{bmatrix} 2(0.866) + 2(0.5) + 1(0) \\ 2(0.5) + 2(0.866) + 1(1)\end{bmatrix} = \begin{bmatrix}2.73\\3.73\end{bmatrix}$

**(ii)** $\Delta\mathbf{e} = \begin{bmatrix}5 - 2.73\\2 - 3.73\end{bmatrix} = \begin{bmatrix}2.27\\-1.73\end{bmatrix}$

**(iii)** $J = \begin{bmatrix}-3.73 & -2.73 & -1\\ \phantom{-}2.73 & \phantom{-}1.00 & \phantom{-}0\end{bmatrix}$

**(iv)** With the given $J^{+}$: $\;J^{+}\Delta\mathbf{e} = [-1.47,\,-0.76,\,-0.32]^\top$, so

$$\Delta\boldsymbol\theta = 0.1 \times \begin{bmatrix}-1.47\\-0.76\\-0.32\end{bmatrix} = \begin{bmatrix}-0.15\\-0.08\\-0.03\end{bmatrix}$$

**(v)** $\boldsymbol\theta^{1} = 0.524 + \Delta\boldsymbol\theta = [0.38,\,0.45,\,0.49]^\top$ rad

**Traps:** work in **radians** throughout. $\Delta\mathbf{e} = \text{target} - \text{current}$, not the
reverse. Don't forget to multiply by $\alpha$. The step (v) answer stays in radians — no conversion needed.

---

## 14. Neural network unit (ReLU)

$$
z = \mathbf{w}^\top\mathbf{x} + b
\qquad
\text{ReLU}(z) = \max(0,\, z)
$$

**Worked (Exercise 1, 3b):** $\mathbf{w} = [2.2,\,-3,\,1.5]$, $\mathbf{x} = [0,\,5,\,8]$, $b = 3$.

$$z = (2.2)(0) + (-3)(5) + (1.5)(8) + 3 = 0 - 15 + 12 + 3 = 0$$

$$\text{ReLU}(0) = \mathbf{0}$$

**Trap:** $\text{ReLU}(0) = 0$, and the exercise is built so $z$ lands exactly on $0$. Don't panic and
assume you made a mistake.

---

## 15. HRV as standard deviation

$$
\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}\left(x_i - \bar{x}\right)^2}
$$

Divide by $N$, **not** $N-1$.

**Worked (Exercise 1, 2d):** $\text{seq}_1 = \{72,\,75,\,70,\,73,\,76\}$.

$$\bar{x}_1 = \frac{366}{5} = 73.2$$

$$\sum_i (x_i - \bar{x})^2 = 1.44 + 3.24 + 10.24 + 0.04 + 7.84 = 22.8$$

$$\sigma_1 = \sqrt{\frac{22.8}{5}} = \mathbf{2.14}$$

For $\text{seq}_2 = \{74,\,71,\,76,\,79,\,80\}$: $\bar{x}_2 = 76$, $\sum = 54$, $\sigma_2 = \sqrt{54/5} = \mathbf{3.29}$.

**Interpretation (they always ask):** **higher** HRV means relaxed, adaptive, a resilient autonomic
system; **lower** HRV means stress, anxiety, reduced flexibility.

---

## 16. Fidgeting / motion energy

Four steps on a frame $f$ against a running background $b$:

$$
\text{(1)}\;\; f_\text{temp} = f - b
\qquad
\text{(2)}\;\; f_\text{binary}^{(i,j)} = \begin{cases}1 & \text{if } |f_\text{temp}^{(i,j)}| > t\\[2pt] 0 & \text{otherwise}\end{cases}
$$

$$
\text{(3)}\;\; E = \frac{\sum f_\text{binary}}{\text{total pixels}} \times 100\,\%
\qquad
\text{(4)}\;\; b' = (1-\alpha)\,b + \alpha\,f
$$

**Worked (Exercise 1, 2c):** with $t = 5$, one pixel of the $3\times3$ difference fell at or below
threshold, leaving $8$ survivors:

$$E = \frac{8}{9} \times 100 = \mathbf{88.89\,\%}$$

With $\alpha = 0.2$, the background update is $b' = 0.8\,b + 0.2\,f$ elementwise.

**Traps:** the comparison is **strictly** greater than $t$ — a difference of exactly $t$ is *not* counted.
Use the absolute value: motion counts in either direction.

---

## 17. tf-idf retrieval scoring

$$
\text{tf}_{t,d} = \begin{cases}1 + \log_{10}\text{count}(t,d) & \text{if } \text{count}(t,d) > 0\\[2pt] 0 & \text{otherwise}\end{cases}
\qquad
\text{idf}_t = \log_{10}\frac{N}{\text{df}_t}
$$

$$
\text{tf-idf}(t,d) = \text{tf}_{t,d} \cdot \text{idf}_t
\qquad
\text{score}(q,d) = \sum_{t \in q} \frac{\text{tf-idf}(t,q)}{\sqrt{\sum_{q_i \in q}\text{tf-idf}^2(q_i,q)}} \cdot \frac{\text{tf-idf}(t,d)}{\sqrt{\sum_{d_i \in d}\text{tf-idf}^2(d_i,d)}}
$$

where $N$ is the number of documents and $\text{df}_t$ the number containing term $t$.

**Worked (Exercise 2, 3b):** query *"deep learning transformers"*, $N = 3$ documents.

- "deep" appears in all 3: $\;\text{idf} = \log_{10}(3/3) = \mathbf{0}$ — a term in *every* document
  carries no discriminative information.
- "learning" in 2: $\;\text{idf} = \log_{10}(1.5) = 0.176$
- "transformers" in 1: $\;\text{idf} = \log_{10}(3) = 0.477$

Every count is $1$, so each $\text{tf} = 1 + \log_{10}(1) = 1$ and $\text{tf-idf} = \text{idf}$. The query
normalization factor is

$$\sqrt{0^2 + 0.176^2 + 0.477^2} = \sqrt{0.259} = 0.509$$

Normalize each document over **all** its terms, not just the query terms — Doc 1's factor came to $1.194$
— then take the cosine.

**Traps:** $\text{tf}$ is $1 + \log_{10}(\text{count})$, not the raw count. A term present in every
document scores zero. Document normalization runs over every term in the document.

---

## Exam-day checklist

- Calculator in **RAD** mode. Non-programmable only; a neutral dictionary is allowed.
- Write the formula on its own line before every calculation. Free partial credit.
- 120 points in 120 minutes → **1 minute per point.** The IK question is worth 10 — don't spend 25 minutes on it.
- MC block: $-1$ for wrong, $0$ for blank, floor of $0$ for the block. If you genuinely don't know, leave
  it blank; a coin flip has zero expected value.
- If you run out of time on a calculation, write the remaining *steps* in words. Method earns points.
