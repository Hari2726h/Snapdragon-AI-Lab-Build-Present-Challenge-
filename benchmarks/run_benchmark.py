"""Small reproducible latency and behavior benchmark."""

import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.analyzer import analyze

CASES = [
    ("low", "Your train ticket is confirmed for tomorrow morning."),
    ("high", "Urgent KYC update. Share OTP and pay Rs 10 at http://203.0.113.4/login"),
    ("high", "Digital arrest warning. Stay on the call and transfer ₹25,000 now."),
    ("medium", "You won a prize. Open bit.ly/example to claim it."),
    ("low", "Official security training: never share your OTP with anyone."),
]

if __name__ == "__main__":
    latencies = []
    correct = 0
    for expected, text in CASES * 200:
        start = time.perf_counter()
        result = analyze(text)
        latencies.append((time.perf_counter() - start) * 1000)
        correct += result["level"] == expected

    latencies.sort()
    print(f"cases={len(latencies)}")
    print(f"scenario_accuracy={correct / len(latencies):.3f}")
    print(f"median_ms={statistics.median(latencies):.3f}")
    print(f"p95_ms={latencies[int(len(latencies) * .95)]:.3f}")
