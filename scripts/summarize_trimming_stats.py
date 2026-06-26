#!/usr/bin/env python3

import sys
import csv
import re
from pathlib import Path

stats_files = [Path(x) for x in sys.argv[1:]]
rows = []

def get_number(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return int(m.group(1).replace(",", ""))
    return None

for file in stats_files:
    sample = file.name.replace("_trim_stats.txt", "")
    text = file.read_text(errors="ignore")

    # Sickle commonly reports records kept/discarded in stderr.
    paired_kept = get_number(r"FastQ records kept:\s+([0-9,]+)", text)
    singles_kept = get_number(r"FastQ singletons kept:\s+([0-9,]+)", text)
    discarded = get_number(r"FastQ records discarded:\s+([0-9,]+)", text)

    if paired_kept is None:
        paired_kept = 0
    if singles_kept is None:
        singles_kept = 0
    if discarded is None:
        discarded = 0

    total_after = paired_kept + singles_kept
    total_seen = paired_kept + singles_kept + discarded

    retention_percent = None
    discarded_percent = None

    if total_seen > 0:
        retention_percent = (total_after / total_seen) * 100
        discarded_percent = (discarded / total_seen) * 100

    rows.append({
        "sample_id": sample,
        "paired_reads_kept": paired_kept,
        "single_reads_kept": singles_kept,
        "discarded_reads": discarded,
        "total_reads_checked": total_seen,
        "retention_percent": round(retention_percent, 4) if retention_percent is not None else "",
        "discarded_percent": round(discarded_percent, 4) if discarded_percent is not None else ""
    })

summary_dir = Path("summary")
summary_dir.mkdir(exist_ok=True)

with (summary_dir / "trimming_summary.csv").open("w", newline="") as out:
    writer = csv.DictWriter(out, fieldnames=[
        "sample_id",
        "paired_reads_kept",
        "single_reads_kept",
        "discarded_reads",
        "total_reads_checked",
        "retention_percent",
        "discarded_percent"
    ])
    writer.writeheader()
    writer.writerows(rows)

valid = [r for r in rows if r["total_reads_checked"] > 0]

with (summary_dir / "trimming_average_summary.txt").open("w") as out:
    out.write("Trimming average summary\n")
    out.write("========================\n\n")
    out.write(f"Number of samples: {len(rows)}\n")

    if valid:
        avg_retention = sum(float(r["retention_percent"]) for r in valid) / len(valid)
        avg_discarded = sum(float(r["discarded_percent"]) for r in valid) / len(valid)
        avg_paired = sum(r["paired_reads_kept"] for r in valid) / len(valid)
        avg_single = sum(r["single_reads_kept"] for r in valid) / len(valid)
        avg_discarded_reads = sum(r["discarded_reads"] for r in valid) / len(valid)

        out.write(f"Average paired reads kept: {avg_paired:.2f}\n")
        out.write(f"Average single reads kept: {avg_single:.2f}\n")
        out.write(f"Average discarded reads: {avg_discarded_reads:.2f}\n")
        out.write(f"Average retention percent: {avg_retention:.4f}%\n")
        out.write(f"Average discarded percent: {avg_discarded:.4f}%\n")
    else:
        out.write("No valid trimming stats parsed.\n")
