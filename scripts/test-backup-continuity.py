#!/usr/bin/env python3
"""Modeled backup admissibility and fixed-weight regression vectors, not runtime evidence."""
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
suite = json.loads((ROOT / 'specifications/conformance/missing-evidence-v1.json').read_text())
for case in suite['backup_admissibility_cases']:
    if not case['unique_observation_slots']:
        actual = 'reject_mapping'
    elif all(case[k] is True for k in ('current', 'independent', 'equivalent_population')):
        actual = 'populated'
    else:
        actual = 'unknown'
    assert actual == case['expected'], case['id']
for case in suite['weighted_average_cases']:
    slots = case['configuration']['aggregation_slots']
    alternatives = [feed for slot in slots for feed in slot['alternatives']]
    assert len(alternatives) == len(set(alternatives)), case['id']
    denominator = sum(Decimal(str(slot['weight'])) for slot in slots)
    for evaluation in case['evaluations']:
        selected = [next(feed for feed in slot['alternatives'] if feed in evaluation['current']) for slot in slots]
        assert selected == evaluation['selected'], case['id']
        total = sum(Decimal(str(slot['weight'])) * Decimal(str(case['normalized_values'][feed])) for slot, feed in zip(slots, selected))
        assert denominator == evaluation['denominator'], case['id']
        assert total / denominator == Decimal(str(evaluation['expected']['value'])), case['id']
print(f"Backup continuity: {len(suite['backup_admissibility_cases'])} admissibility cases and fixed-weight substitution pass")
