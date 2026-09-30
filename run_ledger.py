"""Run ledger for the 100-new-Accepted campaign on shailaendranms.

Single source for the daily counter + per-problem evidence. The runner
process appends/verifies rows; humans can read the JSON any time.
Schema: {target, start_solved, accepted: [rows], rejected: [rows]}
row: {slug, title, qid, source_bank, verdict, sid, ts, accepted_today}
"""
import json
import os
import time

# Campaign ledger path/name comes from LEDGER_FILE so several campaigns can run
# in parallel without trampling each other. Defaults to the 100-campaign ledger.
LEDGER = os.environ.get(
    "LEDGER_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_friend100.json"))
TARGET = int(os.environ.get("LEDGER_TARGET", "100"))
START_SOLVED = int(os.environ.get("LEDGER_START_SOLVED", "103"))


def load():
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            return json.load(f)
    return {"target": TARGET, "start_solved": START_SOLVED, "accepted": [], "rejected": []}


def save(doc):
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1)


def record(row, ok: bool):
    doc = load()
    key = "accepted" if ok else "rejected"
    if ok and any(r.get("slug") == row.get("slug") for r in doc["accepted"]):
        return doc  # never double-count
    row = dict(row)
    row["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
    row["accepted_today"] = ok
    doc[key].append(row)
    save(doc)
    return doc


def count(doc=None):
    doc = doc or load()
    return len({r.get("slug") for r in doc["accepted"]})


if __name__ == "__main__":
    doc = load()
    if not os.path.exists(LEDGER):
        save(doc)
    print("target:", doc["target"], "| start_solved:", doc["start_solved"],
          "| accepted_today:", count(doc))
