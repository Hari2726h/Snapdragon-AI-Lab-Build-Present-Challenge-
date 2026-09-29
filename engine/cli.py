"""Command-line interface for offline analysis."""

import argparse
import json

from .analyzer import analyze

parser = argparse.ArgumentParser(description="Analyze a suspicious message locally")
parser.add_argument("text", help="Message, URL, or QR payload")
args = parser.parse_args()
print(json.dumps(analyze(args.text), indent=2, ensure_ascii=False))
