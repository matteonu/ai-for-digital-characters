#!/usr/bin/env python3
"""Generate randomized practice versions of the exam calculation recipes.

The past exams are your only two clean mock papers -- don't burn them on practice.
Drill with fresh numbers here instead.

    python3 drill.py                 # one problem from each recipe
    python3 drill.py attention ik    # only these recipes
    python3 drill.py --seed 7        # pin these exact numbers
    python3 drill.py --seed 7 --answers      # ... and check them

Every run prints the seed it used, plus the exact command to get the same
problems back with solutions. Re-running without that seed gives new numbers.
"""

from __future__ import annotations

import argparse
import math
import random

import numpy as np

R = lambda x, n=2: np.round(x, n)


def attention(rng):
    d = rng.choice([2, 3])
    # Reject degenerate draws: a zero query, a zero input vector, or inputs that all score the
    # same all collapse the softmax to uniform weights, which teaches nothing.
    for _ in range(100):
        q = np.array([rng.choice([0, 1, 2]) for _ in range(d)], dtype=float)
        X = np.array([[rng.choice([0, 1, 2]) for _ in range(d)] for _ in range(3)], dtype=float)
        s = X @ q / math.sqrt(d)
        if q.any() and all(row.any() for row in X) and len(set(np.round(s, 6))) > 1:
            break
    else:  # pragma: no cover - fall back to the 2024 exam vectors
        q = np.array([1.0, 0.0, 1.0])
        X = np.array([[1, 0, 0], [0, 1, 0], [1, 1, 0]], dtype=float)
        d = 3
        s = X @ q / math.sqrt(d)
    a = np.exp(s) / np.exp(s).sum()
    c = a @ X
    prob = (
        f"Scaled dot-product attention.\n"
        f"  q  = {q.tolist()}\n"
        f"  x1 = {X[0].tolist()}, x2 = {X[1].tolist()}, x3 = {X[2].tolist()}   (d = {d})\n"
        f"  Compute (a) similarity scores, (b) attention weights, (c) context vector."
    )
    ans = (
        f"  (a) scores = q.x_t / sqrt({d}) = {R(s, 3).tolist()}\n"
        f"  (b) weights = softmax = {R(a, 3).tolist()}  (sum = {a.sum():.3f})\n"
        f"  (c) context = sum a_t x_t = {R(c, 3).tolist()}"
    )
    return prob, ans


def positional_encoding(rng):
    x0 = np.array([rng.randint(1, 5), rng.randint(1, 5)], dtype=float)
    x1 = np.array([rng.randint(1, 5), rng.randint(1, 5)], dtype=float)
    pe0 = np.array([math.sin(0), math.cos(0)])
    pe1 = np.array([math.sin(1), math.cos(1)])
    prob = (
        f"Sinusoidal positional encoding, d = 2.\n"
        f"  x0 = {x0.tolist()} at pos 0,  x1 = {x1.tolist()} at pos 1\n"
        f"  PE(pos,0) = sin(pos/10000^(0/d)),  PE(pos,1) = cos(pos/10000^(0/d))\n"
        f"  Compute the encoded inputs."
    )
    ans = (
        f"  pos 0: PE = [sin 0, cos 0] = [0, 1]        -> x0 + PE = {R(x0 + pe0).tolist()}\n"
        f"  pos 1: PE = [sin 1, cos 1] = [0.84, 0.54]  -> x1 + PE = {R(x1 + pe1).tolist()}"
    )
    return prob, ans


def mel(rng):
    lo = rng.choice([100, 150, 200, 300])
    hi = rng.choice([4000, 6000, 8000])
    n = rng.choice([3, 4])
    npts = n + 2
    h2m = lambda f: 1127 * math.log(1 + f / 700)
    m2h = lambda m: 700 * (math.exp(m / 1127) - 1)
    ml, mh = h2m(lo), h2m(hi)
    pts = [ml + i * (mh - ml) / (npts - 1) for i in range(npts)]
    hz = [round(m2h(m)) for m in pts]
    prob = (
        f"Mel filter banks.  Lower bound {lo} Hz, upper bound {hi} Hz, {n} filters "
        f"({npts} points).\n"
        f"  Mel = 1127 ln(1 + f/700).  Give the start/peak/end in Hz for each filter."
    )
    ans = (
        f"  Mel bounds: {ml:.1f} .. {mh:.1f}, spacing {(mh - ml) / (npts - 1):.1f}\n"
        f"  Mel points: {[round(p, 1) for p in pts]}\n"
        f"  Hz points:  {hz}\n"
        + "\n".join(f"  filter {i+1}: ({hz[i]}, {hz[i+1]}, {hz[i+2]})" for i in range(n))
    )
    return prob, ans


_REF = "the quick brown fox jumps over the lazy dog".split()


def align_wer(ref: list[str], hyp: list[str]) -> tuple[int, int, int, list[str]]:
    """Minimum-edit alignment of hyp against ref. Returns (S, I, D, per-word trace).

    WER is defined by the *minimum* edit distance between the two strings, so the counts must
    come from aligning the final texts -- not from whatever edits were used to build hyp. Those
    can cancel out (substitute a word, then delete it) and would overcount.
    """
    n, m = len(ref), len(hyp)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(
                d[i - 1][j] + 1,                                        # deletion
                d[i][j - 1] + 1,                                        # insertion
                d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]),           # match / substitution
            )

    s = ins = dele = 0
    trace: list[str] = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + (ref[i - 1] != hyp[j - 1]):
            if ref[i - 1] != hyp[j - 1]:
                s += 1
                trace.append(f"S: '{ref[i-1]}' -> '{hyp[j-1]}'")
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            dele += 1
            trace.append(f"D: '{ref[i-1]}' missing")
            i -= 1
        else:
            ins += 1
            trace.append(f"I: '{hyp[j-1]}' added")
            j -= 1
    return s, ins, dele, list(reversed(trace))


def wer(rng):
    ref = _REF[:]
    for _ in range(50):
        hyp = ref[:]
        for _ in range(rng.randint(2, 4)):
            kind = rng.choice(["S", "D", "I"])
            i = rng.randrange(len(hyp))
            if kind == "S":
                hyp[i] = hyp[i] + "s" if not hyp[i].endswith("s") else hyp[i][:-1]
            elif kind == "D" and len(hyp) > 3:
                hyp.pop(i)
            else:
                hyp.insert(i, "um")
        if hyp != ref:
            break

    s, ins, dele, trace = align_wer(ref, hyp)
    total = s + ins + dele
    prob = (
        f"Word Error Rate.\n"
        f"  Reference: {' '.join(ref)}\n"
        f"  Output:    {' '.join(hyp)}\n"
        f"  Give S, I, D and the WER."
    )
    ans = (
        f"  N = {len(ref)} (reference length)\n"
        + "".join(f"    {t}\n" for t in trace)
        + f"  S = {s}, I = {ins}, D = {dele}\n"
        f"  WER = (S+I+D)/N = {total}/{len(ref)} = {100*total/len(ref):.2f} %"
    )
    return prob, ans


def power_spectrum(rng):
    n = rng.choice([3, 4])
    X = np.array([rng.randint(0, 6) for _ in range(n)], dtype=float)
    prob = (
        f"Power spectrum.  DFT result X[n] = {X.tolist()} for a length-{n} signal.\n"
        f"  Compute P and state what it means."
    )
    ans = (
        f"  P(k) = |X(k)|^2 / N = {R(np.abs(X) ** 2 / n).tolist()}\n"
        f"  Meaning: energy contained in each frequency bin of the frame."
    )
    return prob, ans


def top_p(rng):
    raw = sorted([rng.random() for _ in range(6)], reverse=True)
    probs = [round(x / sum(raw), 2) for x in raw]
    probs[0] = round(probs[0] + (1 - sum(probs)), 2)
    probs = sorted(probs, reverse=True)
    p = rng.choice([0.7, 0.8, 0.85, 0.9])
    toks = ["cat", "dog", "runs", "fast", "tree", "blue"]
    cum, keep, lines = 0.0, [], []
    for t, pr in zip(toks, probs):
        cum += pr
        keep.append(t)
        lines.append(f"    +{t} ({pr}) -> cum {cum:.2f}")
        if cum >= p:
            break
    prob = (
        f"Top-p (nucleus) sampling with p = {p}.\n"
        + "\n".join(f"    {t}: {pr}" for t, pr in zip(toks, probs))
        + "\n  List the candidate tokens with all computation steps."
    )
    ans = "\n".join(lines) + f"\n  cum >= {p} -> candidates = {{{', '.join(keep)}}}, then renormalize."
    return prob, ans


def cosine(rng):
    A = np.array([round(rng.uniform(0.1, 0.9), 1) for _ in range(3)])
    B = np.array([round(rng.uniform(0.1, 0.9), 1) for _ in range(3)])
    dot = float(A @ B)
    na, nb = float(np.linalg.norm(A)), float(np.linalg.norm(B))
    prob = f"Cosine similarity.  eA = {A.tolist()}, eB = {B.tolist()}"
    ans = (
        f"  dot  = {dot:.3f}\n"
        f"  |eA| = sqrt({float(A @ A):.2f}) = {na:.4f}\n"
        f"  |eB| = sqrt({float(B @ B):.2f}) = {nb:.4f}\n"
        f"  cos  = {dot:.3f} / ({na:.4f} x {nb:.4f}) = {dot / (na * nb):.4f}"
    )
    return prob, ans


def perplexity(rng):
    n = rng.randint(3, 5)
    probs = [round(rng.uniform(0.05, 0.4), 2) for _ in range(n)]
    prod = float(np.prod(probs))
    prob = f"Perplexity.  Token probabilities for the sentence: {probs}"
    ans = (
        f"  PPL = (prod p)^(-1/N),  N = {n}\n"
        f"  prod = {prod:.6f}\n"
        f"  PPL  = {prod:.6f}^(-1/{n}) = {prod ** (-1 / n):.3f}"
    )
    return prob, ans


def transe(rng):
    h = np.array([round(rng.uniform(-2, 3), 1) for _ in range(3)])
    r = np.array([round(rng.uniform(-1, 1), 1) for _ in range(3)])
    t = np.array([round(rng.uniform(-2, 3), 1) for _ in range(3)])
    v = h + r - t
    score = float(np.linalg.norm(v))
    prob = (
        f"TransE score for triple (h, r, t):\n"
        f"  h = {h.tolist()}, r = {r.tolist()}, t = {t.tolist()}\n"
        f"  Give the scoring function and the score; is it plausible against a threshold of 2.0?"
    )
    ans = (
        f"  score = ||h + r - t||\n"
        f"  h + r - t = {R(v, 2).tolist()}\n"
        f"  score = {score:.3f} -> {'plausible (< 2.0)' if score < 2 else 'not plausible (>= 2.0)'}"
    )
    return prob, ans


def heart_rate(rng):
    rr = rng.choice([400, 500, 600, 750, 800, 1000])
    return (
        f"Heart rate.  R-R interval = {rr} ms.  Give the heart rate in bpm.",
        f"  HR = 60000 / RR = 60000 / {rr} = {60000/rr:.2f} bpm",
    )


def artifact(rng):
    base = rng.choice([700, 800, 900])
    seq = [base + rng.randint(-10, 10) for _ in range(5)]
    bad = rng.choice([350, 400, 450, 1500])
    seq.insert(rng.randrange(len(seq)), bad)
    srt = sorted(seq)
    half = len(srt) // 2
    q1 = float(np.median(srt[:half]))
    q3 = float(np.median(srt[half:]))
    med = float(np.median(srt))
    qd = (q3 - q1) / 2
    mad = (med - 2.9 * qd) / 3
    medd = 3.32 * qd
    cbd = (mad + medd) / 2
    diff = abs(bad - base)
    prob = (
        f"Artifact detection.  R-R intervals (ms): {seq}\n"
        f"  Last valid R-R = {base} ms.  Is the {bad} ms beat an artifact?\n"
        f"  QD = (Q3-Q1)/2,  MAD = (Median - 2.9 QD)/3,  MED = 3.32 QD,  CBD = (MAD+MED)/2\n"
        f"  Valid range 300-2000 ms."
    )
    ans = (
        f"  sorted: {srt}\n"
        f"  Q1 = {q1}, Q3 = {q3}, Median = {med}\n"
        f"  QD  = {qd:.2f}\n"
        f"  MAD = ({med} - 2.9 x {qd:.2f})/3 = {mad:.2f}\n"
        f"  MED = 3.32 x {qd:.2f} = {medd:.2f}\n"
        f"  CBD = ({mad:.2f} + {medd:.2f})/2 = {cbd:.2f}\n"
        f"  |{bad} - {base}| = {diff} {'>' if diff > cbd else '<='} CBD -> "
        f"{'ARTIFACT' if diff > cbd else 'not an artifact'}"
    )
    return prob, ans


def ik(rng):
    n = rng.choice([2, 3])
    L = [float(rng.randint(1, 4)) for _ in range(n)]
    frac = rng.choice([6, 4, 3])
    th = np.array([math.pi / frac] * n)
    alpha = rng.choice([0.1, 0.2, 0.5])
    star = np.array([float(rng.randint(3, 6)), float(rng.randint(1, 4))])

    cum = np.cumsum(th)                       # cumulative angle at each joint
    deg = [math.degrees(c) for c in cum]

    e0 = np.array([sum(L[i] * math.cos(cum[i]) for i in range(n)),
                   sum(L[i] * math.sin(cum[i]) for i in range(n))])
    J = np.array([
        [-sum(L[i] * math.sin(cum[i]) for i in range(j, n)) for j in range(n)],
        [ sum(L[i] * math.cos(cum[i]) for i in range(j, n)) for j in range(n)],
    ])

    # Everything downstream is computed from the ROUNDED values the student actually sees --
    # notably the rounded J+ printed in the problem. Using the exact pseudoinverse here would
    # produce a key that cannot be reproduced from the given numbers.
    e0_r, J_r = np.round(e0, 2), np.round(J, 2)
    Jp_r = np.round(np.linalg.pinv(J), 2)
    de_r = np.round(star - e0_r, 2)
    Jpde = np.round(Jp_r @ de_r, 3)
    dth = np.round(alpha * Jpde, 3)
    th_new = np.round(th + dth, 3)

    ang = lambda i: "+".join(f"th{k+1}" for k in range(i + 1))   # th1, th1+th2, ...
    lengths = ", ".join(f"L{i+1} = {L[i]:g}" for i in range(n))
    # The exam hands you J+ (you can't invert a matrix by hand under time pressure), so do the same.
    jp_rows = "\n".join("        " + str(row.tolist()) for row in Jp_r)
    prob = (
        f"Inverse kinematics, one Jacobian step.  {n}-link planar arm, root at [0,0].\n"
        f"  {lengths};  all theta = pi/{frac};  target e* = {star.tolist()};  alpha = {alpha}\n"
        f"  You may use the Moore-Penrose pseudoinverse:\n"
        f"    J+ =\n{jp_rows}\n"
        f"  Compute (i) e0, (ii) delta-e, (iii) J, (iv) delta-theta, (v) updated angles."
    )

    out = ["  Cumulative angles (add up every angle out to that joint):"]
    for i in range(n):
        out.append(f"    {ang(i):<12} = {i+1}*pi/{frac} = {cum[i]:.3f} rad = {deg[i]:.1f} deg")

    out.append("")
    out.append("  (i) Forward kinematics   e0 = F(theta)")
    for axis, fn in (("x", math.cos), ("y", math.sin)):
        f_ = "cos" if axis == "x" else "sin"
        terms = [L[i] * fn(cum[i]) for i in range(n)]
        out.append(f"      e_{axis} = " + " + ".join(f"L{i+1}*{f_}({ang(i)})" for i in range(n)))
        out.append("          = " + " + ".join(f"{L[i]:g}*{f_}({deg[i]:.1f}deg)" for i in range(n)))
        out.append("          = " + " + ".join(f"{L[i]:g}*({fn(cum[i]):.4f})" for i in range(n)))
        out.append("          = " + " + ".join(f"{t:.3f}" for t in terms)
                   + f" = {sum(terms):.2f}")
    out.append(f"      e0 = {e0_r.tolist()}")

    out.append("")
    out.append("  (ii) Error   de = e* - e0      (target minus current, not the reverse)")
    out.append(f"      de = [{star[0]:g} - ({e0_r[0]:.2f}), {star[1]:g} - ({e0_r[1]:.2f})]"
               f" = {de_r.tolist()}")

    out.append("")
    out.append("  (iii) Jacobian   J = de/dtheta     (column j keeps only joints j..n)")
    out.append("      Row 1 = d(e_x)/d(theta) -- sines, negative:")
    for j in range(n):
        sym = " - ".join(f"L{i+1}*sin({ang(i)})" for i in range(j, n))
        num = " - ".join(f"{L[i]:g}({math.sin(cum[i]):.4f})" for i in range(j, n))
        out.append(f"        J[1,{j+1}] = -{sym} = -{num} = {J_r[0][j]:.2f}")
    out.append("      Row 2 = d(e_y)/d(theta) -- cosines, positive:")
    for j in range(n):
        sym = " + ".join(f"L{i+1}*cos({ang(i)})" for i in range(j, n))
        num = " + ".join(f"{L[i]:g}({math.cos(cum[i]):.4f})" for i in range(j, n))
        out.append(f"        J[2,{j+1}] =  {sym} =  {num} = {J_r[1][j]:.2f}")
    out.append(f"      J = {J_r.tolist()}")

    out.append("")
    out.append("  (iv) dtheta = alpha * J+ * de")
    out.append("      First J+ * de -- each row of J+ dotted with de:")
    for i in range(n):
        prod = " + ".join(f"({Jp_r[i][k]:g})({de_r[k]:g})" for k in range(2))
        parts = " + ".join(f"{Jp_r[i][k]*de_r[k]:.3f}" for k in range(2))
        out.append(f"        (J+de)_{i+1} = {prod} = {parts} = {Jpde[i]:.3f}")
    out.append(f"      Then scale by alpha = {alpha}:")
    out.append(f"        dtheta = {alpha} * {Jpde.tolist()} = {dth.tolist()}")

    out.append("")
    out.append("  (v) Update   theta_new = theta + dtheta")
    for i in range(n):
        out.append(f"      th{i+1}_new = {th[i]:.3f} + ({dth[i]:.3f}) = {th_new[i]:.3f}")
    out.append(f"      theta_new = {th_new.tolist()} rad   (stays in radians)")
    out.append("")
    out.append("  Rounding to 2 dp along the way can shift the last digit -- the exam marks the")
    out.append("  method. One step does not reach the target; a real solver iterates.")

    return prob, "\n".join(out)


def relu_unit(rng):
    """Exercise 1, 3b -- single neuron forward pass."""
    w = np.array([round(rng.uniform(-3, 3), 1) for _ in range(3)])
    x = np.array([float(rng.randint(0, 9)) for _ in range(3)])
    b = float(rng.randint(-4, 5))
    z = float(w @ x + b)
    prob = (
        f"Neural network unit.  w = {w.tolist()}, x = {x.tolist()}, b = {b:g}\n"
        f"  Activation is ReLU.  Compute the output of the unit."
    )
    terms = " + ".join(f"({w[i]:g} x {x[i]:g})" for i in range(3))
    ans = (
        f"  z = w^T x + b = {terms} + {b:g} = {z:.2f}\n"
        f"  ReLU(z) = max(0, {z:.2f}) = {max(0.0, z):.2f}"
    )
    return prob, ans


def hrv(rng):
    """Exercise 1, 2d -- HRV as the standard deviation of a heart-rate sequence."""
    seqs = []
    for spread in (rng.randint(2, 4), rng.randint(5, 9)):
        base = rng.randint(65, 80)
        seqs.append([base + rng.randint(-spread, spread) for _ in range(5)])
    prob = (
        f"HRV indicator.  Two heart-rate sequences:\n"
        f"  seq1 = {seqs[0]}\n  seq2 = {seqs[1]}\n"
        f"  Compute the standard deviation of each (population, divide by N) and say which\n"
        f"  indicates the more relaxed state."
    )
    lines, sds = [], []
    for k, s in enumerate(seqs, 1):
        m = sum(s) / len(s)
        sq = [(v - m) ** 2 for v in s]
        sd = math.sqrt(sum(sq) / len(s))
        sds.append(sd)
        lines.append(
            f"  seq{k}: mean = {sum(s)}/{len(s)} = {m:.2f}\n"
            f"         sum sq dev = {' + '.join(f'{v:.2f}' for v in sq)} = {sum(sq):.2f}\n"
            f"         sigma{k} = sqrt({sum(sq):.2f}/{len(s)}) = {sd:.2f}"
        )
    hi = 1 if sds[0] > sds[1] else 2
    ans = (
        "\n".join(lines)
        + f"\n  seq{hi} has the higher HRV -> more relaxed / adaptive; "
        f"lower HRV is associated with stress."
    )
    return prob, ans


def fidget(rng):
    """Exercise 1, 2c -- fidgeting/motion energy from frame differencing."""
    t = rng.choice([5, 10, 20])
    f = np.array([[rng.randint(0, 200) for _ in range(3)] for _ in range(3)])
    # b is a running background model, so it tracks f closely -- deltas must straddle the
    # threshold, otherwise every pixel survives and the energy is trivially 100%.
    delta = np.array([[rng.choice([0, 1, t - 1, t, t + 1, 2 * t, 3 * t]) * rng.choice([1, -1])
                       for _ in range(3)] for _ in range(3)])
    b = np.clip(f - delta, 0, 255)
    alpha = rng.choice([0.1, 0.2, 0.5])
    ftemp = f - b
    binary = (np.abs(ftemp) > t).astype(int)
    energy = binary.sum() / binary.size * 100
    bnew = (1 - alpha) * b + alpha * f
    ind = lambda m: str(m).replace("\n", "\n       ")
    prob = (
        f"Fidgeting / motion energy.  Frame f and background b:\n"
        f"  f = {ind(f)}\n  b = {ind(b)}\n"
        f"  Threshold t = {t}, background update rate alpha = {alpha}.\n"
        f"  Compute (1) f_temp, (2) the binarized frame, (3) the energy %, (4) the updated background."
    )
    ans = (
        f"  (1) f_temp = f - b =\n       {ind(ftemp)}\n"
        f"  (2) binarize |f_temp| > {t} ->\n       {ind(binary)}\n"
        f"  (3) E = surviving/total x 100 = {binary.sum()}/{binary.size} x 100 = {energy:.2f} %\n"
        f"  (4) b' = (1-{alpha})b + {alpha}f =\n       {ind(np.round(bnew, 1))}"
    )
    return prob, ans


def _match(triples, patterns):
    """Evaluate a list of triple patterns against a triple store. Returns list of bindings.

    Lets the drill *execute* the SPARQL it generates, so the stated answer is verified against
    the graph rather than assumed.  Anything starting with '?' is a variable.
    """
    results = [{}]
    for ps, pp, po in patterns:
        nxt = []
        for binding in results:
            for s, p, o in triples:
                b = dict(binding)
                ok = True
                for pat, val in ((ps, s), (pp, p), (po, o)):
                    if pat.startswith("?"):
                        if b.setdefault(pat, val) != val:
                            ok = False
                            break
                    elif pat != val:
                        ok = False
                        break
                if ok:
                    nxt.append(b)
        results = nxt
    return results


_PEOPLE = ["Dr. Sarah Clark", "Dr. Liu Wei", "Dr. Ana Rossi", "Dr. Elena Fischer"]
_STUDENTS = ["Mark Thompson", "Jonas Weber", "Priya Nair"]
_DEPTS = ["Computer Science Department", "Physics Department", "Biology Department"]
_UNIS = ["ETH Zurich", "EPFL"]
_CONFS = ["ICML", "NeurIPS", "CVPR"]
_PROJECTS = ["AI for Healthcare", "Quantum Sensing", "Protein Folding"]


def sparql(rng):
    """Exam 2025 Q7b / 2024 Q7c -- classify the query type and write the SPARQL."""
    people = rng.sample(_PEOPLE, 3)
    student = rng.choice(_STUDENTS)
    depts = rng.sample(_DEPTS, 2)
    uni = rng.choice(_UNIS)
    confs = rng.sample(_CONFS, 2)
    projects = rng.sample(_PROJECTS, 2)

    triples = []
    for i, person in enumerate(people):
        triples.append((person, "affiliatedWith", depts[i % 2]))
    for d in depts:
        triples.append((d, "partOf", uni))
    # person 0 and person 2 publish; only person 0 also leads a project
    papers = {people[0]: "Advanced ML Algorithms", people[2]: "Sensor Fusion Methods"}
    for person, paper in papers.items():
        triples.append((person, "published", paper))
    triples.append((papers[people[0]], "presentedAt", confs[0]))
    triples.append((papers[people[2]], "presentedAt", confs[1]))
    triples.append((people[0], "lead", projects[0]))
    triples.append((people[1], "lead", projects[1]))
    triples.append((people[0], "supervise", student))
    triples.append((student, "affiliatedWith", depts[0]))
    rng.shuffle(triples)

    kind = rng.choice(["one-hop", "path", "conjunctive"])
    if kind == "one-hop":
        question = f'"Which department is {people[0]} affiliated with?"'
        patterns = [(people[0], "affiliatedWith", "?dept")]
        select = "?dept"
        why = "a single relation from a known entity -> one hop"
    elif kind == "path":
        question = f'"Which university is the department of {people[0]} part of?"'
        patterns = [(people[0], "affiliatedWith", "?dept"), ("?dept", "partOf", "?uni")]
        select = "?uni"
        why = "two relations chained through an intermediate variable -> path query"
    else:
        question = (f'"Find all researchers affiliated with the {depts[0]} AND who published a paper '
                    f'presented at {confs[0]} AND who lead a research project."')
        patterns = [
            ("?researcher", "affiliatedWith", depts[0]),
            ("?researcher", "published", "?paper"),
            ("?paper", "presentedAt", confs[0]),
            ("?researcher", "lead", "?project"),
        ]
        select = "?researcher"
        why = "several conditions AND-ed on the same variable -> conjunctive query"

    answers = sorted({b[select] for b in _match(triples, patterns)})

    kg = "\n".join(f"    ({s}, {p}, {o})" for s, p, o in triples)
    prob = (
        f"SPARQL.  Knowledge graph:\n{kg}\n\n"
        f"  Query: {question}\n"
        f"  (a) Classify the query type as discussed in the lecture.\n"
        f"  (b) Write a SPARQL query that retrieves it. Use the uni: prefix for relations."
    )

    body = "\n".join(f"      {s if s.startswith('?') else repr(s)} uni:{p} "
                     f"{o if o.startswith('?') else repr(o)} ." for s, p, o in patterns)
    body = body.replace("'", '"')
    ans = (
        f"  (a) {kind.upper()} query -- {why}\n\n"
        f"  (b) SELECT {select} WHERE {{\n{body}\n      }}\n\n"
        f"  Returns: {', '.join(answers) if answers else '(no match)'}\n"
        f"  Note: entity names may be written unquoted; the marks are for the triple patterns.\n"
        f"  Every pattern line ends with a period, and the shared variable is what expresses the AND."
    )
    return prob, ans


_VOCAB = ["deep", "learning", "transformers", "neural", "networks", "models", "speech", "chatbots"]


def tfidf(rng):
    """Exercise 2, 3b -- tf-idf retrieval scoring with cosine normalization."""
    query = rng.sample(_VOCAB[:3], 2)
    docs = [rng.sample(_VOCAB, rng.randint(3, 4)) for _ in range(3)]
    # Every query term must appear in at least one document, otherwise df = 0 and idf is
    # undefined. (In the exercise all query terms occur somewhere.)
    for term in query:
        if not any(term in d for d in docs):
            d = docs[rng.randrange(len(docs))]
            d[rng.randrange(len(d))] = term
    N = len(docs)

    tf = lambda term, doc: 1 + math.log10(doc.count(term)) if term in doc else 0.0
    df = lambda term: sum(1 for d in docs if term in d)
    idf = lambda term: math.log10(N / df(term)) if df(term) else 0.0

    lines = [f"  N = {N} documents.  Query terms: {query}", "  idf:"]
    for t in query:
        lines.append(f"    idf({t}) = log10({N}/{df(t)}) = {idf(t):.3f}")

    qvec = [tf(t, query) * idf(t) for t in query]
    qnorm = math.hypot(*qvec) if len(qvec) > 1 else abs(qvec[0])
    lines.append(f"  query tf-idf = {[round(v,3) for v in qvec]}, norm = {qnorm:.3f}")

    scores = []
    for i, d in enumerate(docs, 1):
        terms = sorted(set(d))
        dvec_all = [tf(t, d) * idf(t) for t in terms]
        dnorm = math.sqrt(sum(v * v for v in dvec_all))
        dot = sum(tf(t, query) * idf(t) * tf(t, d) * idf(t) for t in query)
        sc = dot / (qnorm * dnorm) if qnorm and dnorm else 0.0
        scores.append((sc, i))
        lines.append(
            f"  Doc{i} {d}\n"
            f"    tf-idf over all doc terms {terms} = {[round(v,3) for v in dvec_all]}\n"
            f"    norm = {dnorm:.3f}, dot with query = {dot:.3f}, score = {sc:.4f}"
        )
    best = max(scores)[1]
    lines.append(f"  Ranking -> Doc{best} is most relevant.")

    prob = (
        f"tf-idf retrieval.  Query: {' '.join(query)}\n"
        + "\n".join(f"  Document {i}: {' '.join(d)}" for i, d in enumerate(docs, 1))
        + "\n  tf = 1 + log10(count) if present else 0;  idf = log10(N/df);  tf-idf = tf x idf."
        "\n  Score each document by cosine similarity with the query and rank them."
    )
    return prob, "\n".join(lines)


RECIPES = {
    "attention": attention,
    "pe": positional_encoding,
    "mel": mel,
    "wer": wer,
    "power": power_spectrum,
    "topp": top_p,
    "cosine": cosine,
    "perplexity": perplexity,
    "transe": transe,
    "sparql": sparql,
    "hr": heart_rate,
    "artifact": artifact,
    "ik": ik,
    # exercise-only types (not yet seen on a past exam, but same format)
    "relu": relu_unit,
    "hrv": hrv,
    "fidget": fidget,
    "tfidf": tfidf,
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recipes", nargs="*", help=f"any of: {', '.join(RECIPES)}")
    ap.add_argument("--answers", action="store_true", help="print worked solutions")
    ap.add_argument("--seed", type=int, metavar="NUM",
                    help="pin the random numbers, e.g. --seed 7 (any integer)")
    args = ap.parse_args()

    names = args.recipes or list(RECIPES)
    unknown = [n for n in names if n not in RECIPES]
    if unknown:
        ap.error(f"unknown recipe(s): {', '.join(unknown)}. Choose from: {', '.join(RECIPES)}")

    # Always pin a seed, even when the user didn't give one, and report it. Otherwise re-running
    # with --answers would silently produce a different problem set than the one just worked on.
    seed = args.seed if args.seed is not None else random.randrange(10000)

    print(f"\nseed {seed}")
    for i, name in enumerate(names, 1):
        # Each recipe gets its own RNG derived from (seed, name). With one shared RNG a recipe's
        # numbers depended on which recipes ran before it, so `drill.py wer --seed 7` and
        # `drill.py attention wer --seed 7` produced different WER problems.
        prob, ans = RECIPES[name](random.Random(f"{seed}:{name}"))
        print(f"\n{'='*66}\n[{i}] {name.upper()}   (seed {seed})\n{'='*66}\n{prob}")
        if args.answers:
            print(f"\n  --- solution ---\n{ans}")

    if not args.answers:
        cmd = f"python3 drill.py {' '.join(names)} --seed {seed} --answers"
        print(f"\n{'='*66}\nCheck with:  {cmd}")


if __name__ == "__main__":
    main()
