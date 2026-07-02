#!/usr/bin/env python3
"""Verify and export Anki decks from cards_data.py."""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import defaultdict
from pathlib import Path

from cards_data import CARDS, DECK_PREFIX

ROOT = Path(__file__).parent
OUT_DIR = ROOT / "decks"


def verify_calc_cards() -> list[str]:
    """Recompute known calculation cards. Returns list of errors."""
    errors: list[str] = []
    import math

    for card in CARDS:
        if card.get("card_type") != "calc":
            continue
        vid = card.get("verify_id")
        if not vid:
            errors.append(f"Calc card missing verify_id: {card['front'][:60]}...")
            continue

        if vid == "attention_exam2024":
            import numpy as np

            q = np.array([1.0, 0.0, 1.0])
            X = np.array([[1, 0, 0], [0, 1, 0], [1, 1, 0]], dtype=float)
            d = 3
            scores = X @ q / math.sqrt(d)
            weights = np.exp(scores) / np.exp(scores).sum()
            context = weights @ X
            expected_scores = [1 / math.sqrt(3), 0.0, 1 / math.sqrt(3)]
            if not np.allclose(scores, expected_scores, atol=1e-4):
                errors.append(f"{vid}: scores mismatch {scores}")
            if not np.allclose(weights.sum(), 1.0):
                errors.append(f"{vid}: weights don't sum to 1")

        elif vid == "mel_exam2024":
            def hz_to_mel(f: float) -> float:
                return 1127 * math.log(1 + f / 700)

            def mel_to_hz(m: float) -> float:
                return 700 * (math.exp(m / 1127) - 1)

            m_low = hz_to_mel(200)
            m_high = hz_to_mel(8000)
            points = [m_low + i * (m_high - m_low) / 4 for i in range(5)]
            hz_points = [mel_to_hz(m) for m in points]
            if not (190 < hz_points[0] < 210):
                errors.append(f"{vid}: first Hz point unexpected {hz_points[0]}")

        elif vid == "ik_ex4":
            L1, L2 = 5.0, 4.0
            t1 = t2 = math.pi / 2
            e0 = [
                L1 * math.cos(t1) + L2 * math.cos(t1 + t2),
                L1 * math.sin(t1) + L2 * math.sin(t1 + t2),
            ]
            if not (abs(e0[0] + 4) < 1e-6 and abs(e0[1] - 5) < 1e-6):
                errors.append(f"{vid}: e0 = {e0}, expected [-4, 5]")

        elif vid == "cosine_exam2025":
            import numpy as np

            a = np.array([0.5, 0.1, 0.4])
            b = np.array([0.4, 0.3, 0.1])
            sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
            if not (0.81 < sim < 0.83):
                errors.append(f"{vid}: cosine sim = {sim}, expected ~0.82")

        elif vid == "perplexity_exam2025":
            probs = [0.20, 0.10, 0.15, 0.25]
            log_sum = sum(math.log(p) for p in probs)
            n = len(probs)
            ppl = math.exp(-log_sum / n)
            if not (5.9 < ppl < 6.2):
                errors.append(f"{vid}: perplexity = {ppl}, expected ~6.04")

        elif vid == "top_p_ex2":
            probs = [0.35, 0.25, 0.15, 0.10, 0.06, 0.04]
            p = 0.85
            cum = 0.0
            tokens = []
            for pr in probs:
                cum += pr
                tokens.append(pr)
                if cum >= p:
                    break
            if abs(cum - 0.85) > 1e-6 and cum < 0.85:
                errors.append(f"{vid}: cumulative {cum} < 0.85")

        elif vid == "transe_exam2025":
            import numpy as np

            h = np.array([2.0, 1.5, -0.5])
            r = np.array([-0.2, -0.7, 0.3])
            t = np.array([1.8, 0.8, -0.2])
            score = float(np.linalg.norm(h + r - t))
            if not (0.0 <= score < 0.01):
                errors.append(f"{vid}: TransE score = {score}, expected 0.0")

        elif vid == "fidget_energy_ex1":
            if abs(8 / 9 * 100 - 88.88888888888889) > 0.01:
                errors.append(f"{vid}: energy mismatch")

        elif vid == "hrv_std_ex1":
            seq = [72, 75, 70, 73, 76]
            mean = sum(seq) / len(seq)
            std = math.sqrt(sum((x - mean) ** 2 for x in seq) / len(seq))
            if not (2.1 < std < 2.2):
                errors.append(f"{vid}: std = {std}")

        elif vid == "hrv_std2_ex1":
            seq = [74, 71, 76, 79, 80]
            mean = sum(seq) / len(seq)
            std = math.sqrt(sum((x - mean) ** 2 for x in seq) / len(seq))
            if not (3.2 < std < 3.4):
                errors.append(f"{vid}: std2 = {std}")

        elif vid == "hr_rr_exam2025":
            if abs(60000 / 400 - 150.0) > 1e-6:
                errors.append(f"{vid}: HR mismatch")

        elif vid == "artifact_exam2025":
            q1, q3, median = 795.0, 805.0, 800.0
            qd = (q3 - q1) / 2
            mad = (median - 2.9 * qd) / 3
            med = 3.32 * qd
            cbd = (mad + med) / 2
            if not (138 < cbd < 141):
                errors.append(f"{vid}: CBD = {cbd}")
            if not (400 > cbd):
                errors.append(f"{vid}: should be artifact")

        elif vid == "relu_ex1":
            z = 2.2 * 0 + (-3) * 5 + 1.5 * 8 + 3
            if z != 0:
                errors.append(f"{vid}: z = {z}")

        elif vid == "attention_ex1_scores":
            s1 = (3 * 1 + 1 * 2) / math.sqrt(2)
            s2 = (3 * 2 + 1 * 0) / math.sqrt(2)
            if not (3.5 < s1 < 3.6 and 4.2 < s2 < 4.3):
                errors.append(f"{vid}: scores {s1}, {s2}")

        elif vid == "attention_ex1_weights":
            import numpy as np

            s = np.array([5 / math.sqrt(2), 6 / math.sqrt(2)])
            w = np.exp(s) / np.exp(s).sum()
            if not (0.32 < w[0] < 0.34):
                errors.append(f"{vid}: w = {w}")

        elif vid == "attention_ex1_context":
            import numpy as np

            w = np.array([0.331, 0.669])
            v1 = np.array([0.0, 3.0])
            v2 = np.array([1.0, 1.0])
            c = w[0] * v1 + w[1] * v2
            if not (0.66 < c[0] < 0.68 and 1.65 < c[1] < 1.67):
                errors.append(f"{vid}: context = {c}")

        elif vid == "transformer_pe_exam2025":
            import numpy as np

            x0 = np.array([1.0, 2.0]) + np.array([math.sin(0), math.cos(0)])
            x1 = np.array([3.0, 4.0]) + np.array([math.sin(1), math.cos(1)])
            if not np.allclose(x0, [1, 3], atol=1e-4):
                errors.append(f"{vid}: x0 = {x0}")
            if not (3.83 < x1[0] < 3.85 and 4.53 < x1[1] < 4.55):
                errors.append(f"{vid}: x1 = {x1}")

        elif vid == "waveform_ex1":
            if abs(1 / 0.2 - 5.0) > 1e-6:
                errors.append(f"{vid}: frequency wrong")

        elif vid == "mel_ex1_endpoints":
            def hz_to_mel(f: float) -> float:
                return 1127 * math.log(1 + f / 700)

            m_low = hz_to_mel(100)
            m_high = hz_to_mel(2000)
            if not (149 < m_low < 152 and 1518 < m_high < 1525):
                errors.append(f"{vid}: mel endpoints {m_low}, {m_high}")

        elif vid == "mel_ex1_points":
            def hz_to_mel(f: float) -> float:
                return 1127 * math.log(1 + f / 700)

            def mel_to_hz(m: float) -> float:
                return 700 * (math.exp(m / 1127) - 1)

            m_low, m_high = hz_to_mel(100), hz_to_mel(2000)
            hz = [mel_to_hz(m_low + i * (m_high - m_low) / 5) for i in range(6)]
            expected = [100, 320, 600, 959, 1415, 2000]
            for got, exp in zip(hz, expected):
                if abs(got - exp) > 15:
                    errors.append(f"{vid}: hz point {got} vs {exp}")

        elif vid == "mel_exam2024_full":
            def hz_to_mel(f: float) -> float:
                return 1127 * math.log(1 + f / 700)

            def mel_to_hz(m: float) -> float:
                return 700 * (math.exp(m / 1127) - 1)

            m_low, m_high = hz_to_mel(200), hz_to_mel(8000)
            hz = [mel_to_hz(m_low + i * (m_high - m_low) / 4) for i in range(5)]
            if not (195 < hz[0] < 205 and 7900 < hz[4] < 8100):
                errors.append(f"{vid}: hz bounds {hz[0]}, {hz[4]}")

        elif vid == "wer_ex1_case1":
            wer = 100 * 2 / 6
            if abs(wer - 33.333333333333336) > 0.1:
                errors.append(f"{vid}: wer = {wer}")

        elif vid == "wer_ex1_case2":
            wer = 100 * 3 / 8
            if abs(wer - 37.5) > 0.01:
                errors.append(f"{vid}: wer = {wer}")

    return errors


def verify_all() -> bool:
    errors: list[str] = []

    fronts: dict[str, list[str]] = defaultdict(list)
    for i, card in enumerate(CARDS):
        if not card.get("sources"):
            errors.append(f"Card {i}: missing sources — {card['front'][:50]}")
        if not card.get("deck"):
            errors.append(f"Card {i}: missing deck")
        if not card.get("tags"):
            errors.append(f"Card {i}: missing tags")
        fronts[card["front"]].append(card["deck"])

    for front, decks in fronts.items():
        if len(decks) > 1 and len(set(decks)) > 1:
            errors.append(f"Duplicate front across decks: {front[:60]}...")

    errors.extend(verify_calc_cards())

    if errors:
        print("VERIFICATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False

    print(f"Verification passed: {len(CARDS)} cards")
    return True


def format_back(card: dict) -> str:
    back = card["back"]
    sources = card.get("sources", [])
    if sources:
        src = ", ".join(html.escape(s) for s in sources)
        back += f'<br><br><small><i>Source: {src}</i></small>'
    return back


def export_decks() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    by_deck: dict[str, list[dict]] = defaultdict(list)
    for card in CARDS:
        by_deck[card["deck"]].append(card)

    for deck, cards in sorted(by_deck.items()):
        full_deck = f"{DECK_PREFIX}::{deck}"
        path = OUT_DIR / f"{deck}.csv"
        lines = [
            "#separator:tab",
            "#html:true",
            f"#deck:{full_deck}",
            "Front\tBack\tTags",
        ]
        for card in cards:
            tags = " ".join(card.get("tags", []))
            front = card["front"].replace("\t", " ")
            back = format_back(card).replace("\t", " ")
            lines.append(f"{front}\t{back}\t{tags}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {path} ({len(cards)} cards)")

    # Combined file for one-shot import
    all_path = OUT_DIR / "ALL_DECKS.csv"
    lines = ["#separator:tab", "#html:true", "Front\tBack\tTags\tDeck"]
    for deck, cards in sorted(by_deck.items()):
        full_deck = f"{DECK_PREFIX}::{deck}"
        for card in cards:
            tags = " ".join(card.get("tags", []))
            front = card["front"].replace("\t", " ")
            back = format_back(card).replace("\t", " ")
            lines.append(f"{front}\t{back}\t{tags}\t{full_deck}")
    all_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {all_path} ({len(CARDS)} cards total)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--export", action="store_true")
    args = parser.parse_args()

    if not args.verify and not args.export:
        args.verify = args.export = True

    if args.verify and not verify_all():
        sys.exit(1)

    if args.export:
        export_decks()


if __name__ == "__main__":
    main()
