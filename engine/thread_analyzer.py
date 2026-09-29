"""Conversation-level scam progression analysis.

Single messages often look harmless. This module preserves no history; it
analyzes a user-supplied thread in memory and detects how identity, pressure,
secrecy, and extraction requests accumulate across turns.
"""

from __future__ import annotations

import math
import re

from .analyzer import analyze

STAGES = (
    ("identity", "Identity setup", {"identity"}, "A sender establishes authority or a familiar identity."),
    ("isolation", "Isolation and pressure", {"pressure"}, "The sender limits verification or creates urgency."),
    ("extraction", "Money or access request", {"payment", "credential", "link"}, "The conversation ends in a request for money, access, or secrets."),
)

SECRECY_RE = re.compile(r"\b(confidential|do not call|don't call|do not tell|don't tell|between us|private|secret)\b", re.I)
IDENTITY_RE = re.compile(r"\b(this is .{1,35} from|new number|manager|boss|finance head|police|officer|support agent)\b", re.I)


def analyze_thread(messages: list[dict | str]) -> dict:
    if not 2 <= len(messages) <= 20:
        raise ValueError("A conversation needs 2 to 20 messages")

    normalized = []
    for index, item in enumerate(messages):
        if isinstance(item, str):
            role, text = "sender", item.strip()
        else:
            role = str(item.get("role", "sender")).strip() or "sender"
            text = str(item.get("text", "")).strip()
        if not text:
            raise ValueError(f"Message {index + 1} is empty")
        normalized.append({"role": role[:30], "text": text})

    turns = []
    categories: set[str] = set()
    first_seen: dict[str, int] = {}
    peak = 0
    for index, item in enumerate(normalized):
        result = analyze(item["text"])
        turn_categories = {signal["category"] for signal in result["signals"]}
        if SECRECY_RE.search(item["text"]):
            turn_categories.add("pressure")
        if IDENTITY_RE.search(item["text"]):
            turn_categories.add("identity")
        for category in turn_categories:
            first_seen.setdefault(category, index)
        categories.update(turn_categories)
        peak = max(peak, result["score"])
        turns.append({
            "index": index + 1,
            "role": item["role"],
            "score": result["score"],
            "level": result["level"],
            "summary": result["summary"],
            "top_signal": result["signals"][0]["title"] if result["signals"] else "No strong indicator",
        })

    chain = []
    for key, title, required, detail in STAGES:
        matches = required & categories
        if matches:
            chain.append({
                "stage": key,
                "title": title,
                "detail": detail,
                "first_seen_at": min(first_seen[c] for c in matches) + 1,
            })

    chain.sort(key=lambda stage: stage["first_seen_at"])
    distinct_risk_categories = len(categories & {"identity", "pressure", "payment", "credential", "link", "semantic"})
    progression_bonus = max(0, (len(chain) - 1) * 8 + max(0, distinct_risk_categories - 2) * 4)
    aggregate = min(99, round(100 * (1 - math.exp(-(peak + progression_bonus) / 58))))
    if len(chain) == 3:
        aggregate = max(aggregate, 78)
    elif len(chain) == 2:
        aggregate = max(aggregate, 55)

    level = "high" if aggregate >= 70 else "medium" if aggregate >= 38 else "low"
    verdict = {
        "high": "Coordinated scam progression detected",
        "medium": "Conversation pattern needs independent verification",
        "low": "No coordinated scam progression found",
    }[level]

    intervention = [
        "Stop the conversation before sending money, codes, or documents.",
        "Verify the person through a number or app already known to you.",
        "Preserve the conversation and report the account if impersonation is confirmed.",
    ] if level == "high" else [
        "Verify unexpected identity claims through a separate channel.",
        "Treat any later request for money or secrecy as a reason to stop.",
    ]

    return {
        "score": aggregate,
        "level": level,
        "verdict": verdict,
        "turns": turns,
        "attack_chain": chain,
        "intervention": intervention,
        "meta": {
            "messages": len(turns),
            "peak_single_message_score": peak,
            "progression_bonus": progression_bonus,
            "raw_text_persisted": False,
            "network_calls": 0,
        },
    }
