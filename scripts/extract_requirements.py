#!/usr/bin/env python3
"""
Extract BIM validation requirements from a PDF file.
This script scans PDF documents for patterns like "Overdekning >= 75 mm" and
outputs a JSON list of rules. If no rules can be detected it falls back to a
default rule so downstream validation always has something to work with.
"""
import argparse
import os
import re
import json
import sys
from pypdf import PdfReader

def extract_text(pdf_path: str) -> str:
    """Read all pages of a PDF into a single string."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception:
                continue
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}", file=sys.stderr)
    return text

def parse_rules(text: str):
    """Parse rules from the provided text.

    Looks for patterns like "Property >= 75 mm". Returns a list of rule dicts.
    """
    rules = []
    # Pattern captures a property name, an operator, a numeric value and a unit
    pattern = re.compile(r"([A-Za-z\u00C0-\u017F\-_]{3,40})\s*(>=|<=|==|=|>|<)\s*(\d+(?:\.\d+)?)\s*(mm|cm|m|MPa|klasse|%)",
                         re.IGNORECASE)
    for match in pattern.finditer(text):
        prop = match.group(1).strip()
        oper = match.group(2)
        val = float(match.group(3))
        unit = match.group(4)
        rules.append({
            "scope": "Any",
            "property": prop,
            "operator": oper,
            "value": val,
            "unit": unit,
            "source": "pdf"
        })
    return rules

def main():
    parser = argparse.ArgumentParser(description="Extract BIM validation requirements from PDF")
    parser.add_argument('--input', required=True, help='Directory containing PDF files')
    parser.add_argument('--output', required=True, help='Path to output JSON file')
    args = parser.parse_args()

    # Locate PDF files in the input directory
    pdf_files = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.lower().endswith('.pdf')]
    pdf_files.sort()

    rules = []
    if pdf_files:
        # Use the last (lexicographically) PDF as the BIM instruction
        pdf_path = pdf_files[-1]
        text = extract_text(pdf_path)
        rules = parse_rules(text)
    else:
        print("No PDF files found in input directory", file=sys.stderr)

    # Fallback rule ensures validators still run
    if not rules:
        rules = [{
            "scope": "Any",
            "property": "dummy",
            "operator": ">=",
            "value": 0,
            "unit": "",
            "source": "default"
        }]

    with open(args.output, 'w', encoding='utf8') as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(rules)} rule(s)")


if __name__ == '__main__':
    main()
