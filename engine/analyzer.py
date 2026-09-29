"""Explainable hybrid analyzer for social-engineering content."""

from __future__ import annotations

import hashlib
import ipaddress
import math
import re
import time
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from urllib.parse import parse_qs, urlparse

from .rules import BRAND_DOMAINS, HIGH_RISK_TLDS, IMPERSONATION, PAYMENT, PRESSURE, SAFE_CONTEXT, SECRETS, SHORTENERS, URGENCY
from .model import get_model

URL_RE = re.compile(r"(?:(?:https?://|www\.)[^\s<>'\"]+|(?:[a-z0-9-]+\.)+[a-z]{2,}(?:/[^\s<>'\"]*)?)", re.I)
UPI_RE = re.compile(r"\b[a-z0-9._-]{2,}@[a-z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+91[ -]?)?[6-9]\d{9}(?!\d)")
AMOUNT_RE = re.compile(r"(?:₹|rs\.?|inr)\s?([0-9][0-9,]*(?:\.\d{1,2})?)", re.I)


@dataclass
class Signal:
    title: str
    detail: str
    weight: int
    category: str
    evidence: str


def _terms(text: str, terms: set[str]) -> list[str]:
    return [term for term in sorted(terms, key=len, reverse=True) if term in text]


def _host(url: str) -> str:
    candidate = url if re.match(r"^[a-z]+://", url, re.I) else "https://" + url
    return (urlparse(candidate).hostname or "").lower().strip(".")


def _url_signals(raw_url: str) -> list[Signal]:
    signals: list[Signal] = []
    host = _host(raw_url)
    if not host:
        return signals
    try:
        ipaddress.ip_address(host)
        signals.append(Signal("Raw IP address", "Trusted services usually use a named domain, not a numeric address.", 22, "link", host))
    except ValueError:
        pass
    if host.startswith("xn--") or ".xn--" in host:
        signals.append(Signal("Encoded look-alike domain", "Punycode can hide characters that resemble a trusted brand.", 24, "link", host))
    if host in SHORTENERS or any(host.endswith("." + s) for s in SHORTENERS):
        signals.append(Signal("Destination hidden by short link", "Expand and verify the destination before opening it.", 15, "link", host))
    tld = host.rsplit(".", 1)[-1] if "." in host else ""
    if tld in HIGH_RISK_TLDS:
        signals.append(Signal("Unusual domain ending", f"The .{tld} ending needs extra verification for a sensitive request.", 10, "link", host))
    if host.count("-") >= 3 or len(host) > 45:
        signals.append(Signal("Deceptive domain structure", "Long or heavily hyphenated domains can imitate a legitimate sign-in page.", 11, "link", host))
    parsed = urlparse(raw_url if "://" in raw_url else "https://" + raw_url)
    risky_params = {"redirect", "url", "continue", "target", "dest"} & set(parse_qs(parsed.query))
    if risky_params:
        signals.append(Signal("Embedded redirect", "The link contains another destination and may send you somewhere unexpected.", 9, "link", ", ".join(sorted(risky_params))))
    for brand, official in BRAND_DOMAINS.items():
        compact = host.replace("-", "").replace(".", "")
        if brand in compact and not any(host == d or host.endswith("." + d) for d in official):
            closest = max(SequenceMatcher(None, host, d).ratio() for d in official)
            if closest > 0.35:
                signals.append(Signal("Possible brand impersonation", f"This host mentions {brand.title()} but is not one of its known domains.", 26, "identity", host))
                break
    return signals


def _add_term_signal(signals: list[Signal], matches: list[str], title: str, detail: str, weight: int, category: str) -> None:
    if matches:
        signals.append(Signal(title, detail, min(weight + 2 * (len(matches) - 1), weight + 8), category, ", ".join(matches[:4])))


def analyze(message: str) -> dict:
    started = time.perf_counter()
    clean = re.sub(r"\s+", " ", message.strip())
    lower = clean.casefold()
    signals: list[Signal] = []

    _add_term_signal(signals, _terms(lower, URGENCY), "Artificial urgency", "Pressure reduces the time available to verify the request.", 16, "pressure")
    _add_term_signal(signals, _terms(lower, SECRETS), "Sensitive information requested", "Legitimate organisations do not ask for passwords, PINs, CVVs, or OTPs in a message.", 30, "credential")
    _add_term_signal(signals, _terms(lower, PAYMENT), "Payment or reward language", "Unexpected fees, refunds, collect requests, and prizes deserve independent verification.", 17, "payment")
    _add_term_signal(signals, _terms(lower, IMPERSONATION), "Authority or brand claim", "Scammers often borrow trusted roles to make a request feel official.", 14, "identity")
    _add_term_signal(signals, _terms(lower, PRESSURE), "Coercive instruction", "Secrecy, threats, or forced call control are strong social-engineering patterns.", 24, "pressure")

    urls = list(dict.fromkeys(URL_RE.findall(clean)))
    for url in urls[:5]:
        signals.extend(_url_signals(url.rstrip(".,);]")))

    upi = list(dict.fromkeys(UPI_RE.findall(clean)))
    phones = list(dict.fromkeys(PHONE_RE.findall(clean)))
    amounts = [m.group(1) for m in AMOUNT_RE.finditer(clean)]
    if upi:
        signals.append(Signal("UPI payment destination", "Confirm the payee inside the payment app and contact the person through a known channel.", 10, "payment", ", ".join(upi[:3])))
    if amounts and (upi or _terms(lower, PAYMENT)):
        signals.append(Signal("Specific financial ask", "A precise amount can make a fabricated request feel routine.", 8, "payment", "₹" + ", ₹".join(amounts[:3])))

    semantic = get_model().predict(clean)
    if semantic["label"] == "high" and semantic["confidence"] >= 0.48:
        signals.append(Signal("Semantic scam pattern", "The local language model recognizes a high-risk request even without relying on a malicious link.", round(16 + semantic["confidence"] * 12), "semantic", f"{semantic['confidence'] * 100:.1f}% model confidence"))
    elif semantic["label"] == "medium" and semantic["confidence"] >= 0.46:
        signals.append(Signal("Uncertain sender intent", "The local language model found a suspicious request pattern that deserves verification.", round(7 + semantic["confidence"] * 8), "semantic", f"{semantic['confidence'] * 100:.1f}% model confidence"))

    safe_discount = 20 if _terms(lower, SAFE_CONTEXT) else 0
    raw = sum(item.weight for item in signals)
    score = max(0, min(99, round(100 * (1 - math.exp(-raw / 65)) - safe_discount)))
    if semantic["label"] == "high" and semantic["confidence"] >= 0.92:
        score = max(score, 72)
    elif semantic["label"] == "high" and semantic["confidence"] >= 0.60:
        score = max(score, 55)
    elif semantic["label"] == "medium" and semantic["confidence"] >= 0.60:
        score = max(score, 42)
    if any(s.category == "credential" for s in signals) and any(s.category in {"payment", "link"} for s in signals):
        score = min(99, score + 8)
    if {"pressure", "payment", "identity"}.issubset({s.category for s in signals}):
        score = min(99, score + 10)

    if score >= 70:
        level, verdict = "high", "High risk: stop and verify independently"
    elif score >= 38:
        level, verdict = "medium", "Suspicious: verify before taking action"
    else:
        level, verdict = "low", "No strong scam pattern found"

    actions = [
        "Do not reply, pay, share a code, or open the link yet.",
        "Contact the organisation using the number or app you already trust.",
        "If money or credentials were shared, call the bank and report the incident immediately.",
    ] if level == "high" else [
        "Verify the sender through a separate, trusted channel.",
        "Open the official app or type the known website address yourself.",
        "Never share an OTP, PIN, CVV, password, or remote-access code.",
    ]

    elapsed_ms = (time.perf_counter() - started) * 1000
    return {
        "id": hashlib.sha256(clean.encode()).hexdigest()[:10],
        "score": score,
        "level": level,
        "verdict": verdict,
        "summary": _summary(signals, urls, upi),
        "signals": [asdict(s) for s in sorted(signals, key=lambda x: x.weight, reverse=True)[:8]],
        "entities": {"links": urls[:5], "upi_ids": upi[:5], "phone_numbers": phones[:5], "amounts_inr": amounts[:5]},
        "actions": actions,
        "model": semantic,
        "meta": {"latency_ms": round(elapsed_ms, 2), "backend": "Rules + local semantic n-gram model", "privacy": "Processed locally. Nothing uploaded."},
    }


def _summary(signals: list[Signal], urls: list[str], upi: list[str]) -> str:
    if not signals:
        return "The message contains no strong indicators in the current rule set. That does not prove the sender is genuine."
    categories = {s.category for s in signals}
    parts = []
    if "credential" in categories:
        parts.append("asks for sensitive credentials")
    if "pressure" in categories:
        parts.append("uses urgency or pressure")
    if "payment" in categories or upi:
        parts.append("includes a financial request")
    if "link" in categories or urls:
        parts.append("contains a link that needs verification")
    if "identity" in categories:
        parts.append("claims a trusted identity")
    if not parts:
        parts.append("matches known social-engineering language")
    return "The message " + ", ".join(parts[:3]) + "."
