#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example regression runner for the cases in cases/cases.jsonl.

This is a reference harness, not a copy of any production system.
Plug your own 4-state checker in as `check(gate_text) -> dict`
and it will print PASS/FAIL per case.

Design notes (the whole point of the repo):
- expected is a SET of acceptable states, never a single "correct" answer
- a case may pin the evidence source, so "right label, wrong evidence" fails
- `not_checked` is never accepted in place of `absent` unless listed
"""
import json
import pathlib
import sys

CASES = pathlib.Path(__file__).resolve().parent.parent / "cases" / "cases.jsonl"

# --- plug your checker here -------------------------------------------------
def check(text: str) -> dict:
    """Return {"state": ..., "evidence_source": ...} for the given input."""
    raise NotImplementedError("wire this to your own gate implementation")
# ---------------------------------------------------------------------------

EXPECTED = {
    # id: (allowed states, forbidden evidence sources)
    1: ({"absent", "suspected"}, {"pasted_document"}),
    2: ({"absent"}, {"question_itself"}),
    3: ({"absent", "not_checked"}, {"assistant_message"}),
    4: ({"blocked"}, set()),
    5: ({"not_checked"}, set()),
    6: ({"found", "suspected", "absent"}, set()),
    7: ({"blocked", "self_identified_fallback"}, set()),
    8: ({"delivered"}, set()),
    9: ({"not_checked"}, set()),
    10: ({"not_gating"}, set()),
}


def main() -> int:
    rows = [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines() if line.strip()]
    fails = 0
    for case in rows:
        want_states, forbidden = EXPECTED[case["id"]]
        try:
            got = check(case["input"])
        except NotImplementedError:
            print("harness not wired; showing case table only\n")
            for c in rows:
                print("#%-2d %-32s observed=%-12s expected=%s" % (c["id"], c["name"], c["observed"], ",".join(sorted(EXPECTED[c["id"]][0]))))
            return 0
        state = got.get("state")
        src = got.get("evidence_source")
        ok = state in want_states and src not in forbidden
        if not ok:
            fails += 1
        print("#%-2d %-32s %-12s %-14s %s" % (case["id"], case["name"], state, src or "-", "PASS" if ok else "FAIL"))
    print("\n%d/%d passed" % (len(rows) - fails, len(rows)))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
