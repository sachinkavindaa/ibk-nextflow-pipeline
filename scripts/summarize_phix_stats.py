#!/usr/bin/env python3

import sys
import csv
import re
from pathlib import Path

stats_files = [Path(x) for x in sys.argv[1:]]

rows = []

for file in stats_files:
    sample = file.name.replace("_phiX_stats.txt", "")

    input_reads = None
    matched_reads = 0
    matched_percent = 0.0

    text = file.read_text(errors="ignore").splitlines()

    for line in text:
        # BBduk stats usually include something like:
        # #Total    123456
        # #Matched  1234   1.00%
        if line.startswith("#Total"):
            parts = line.split()
            if len(parts) >= 2:
                input_reads = int(parts[1])

        if line.startswith("#Matched"):
            parts = line.split()
            if len(parts) >= 2:
                matched_reads = int(parts[1])
            if len(parts) >= 3:
                matched_percent = float(parts[2].replace("%", ""))

    clean_reads = None
    clean_percent = None

    if input_reads is not None:
        clean_reads = input_reads - matched_reads
        clean_percent = 100 - matched_percent

    rows.append({
        "sample_id": sample,
        "input_reads": input_reads,
        "phix_removed_reads": matched_reads,
        "phix_removed_percent": matched_percent,
        "clean_reads": clean_reads,
        "clean_percent": clean_percent
    })

summary_dir = Path("summary")
summary_dir.mkdir(exist_ok=True)

csv_file = summary_dir / "phix_summary.csv"

with csv_file.open("w", newline="") as out:
    writer = csv.DictWriter(out, fieldnames=[
        "sample_id",
        "input_reads",
        "phix_removed_reads",
        "phix_removed_percent",
        "clean_reads",
        "clean_percent"
    ])
    writer.writeheader()
    writer.writerows(rows)

avg_file = summary_dir / "phix_average_summary.txt"

valid = [r for r in rows if r["input_reads"] is not None]

with avg_file.open("w") as out:
    out.write("PhiX removal average summary\n")
    out.write("============================\n\n")
    out.write(f"Number of samples: {len(rows)}\n")

    if valid:
        avg_input = sum(r["input_reads"] for r in valid) / len(valid)
        avg_removed = sum(r["phix_removed_reads"] for r in valid) / len(valid)
        avg_removed_pct = sum(r["phix_removed_percent"] for r in valid) / len(valid)
        avg_clean = sum(r["clean_reads"] for r in valid) / len(valid)
        avg_clean_pct = sum(r["clean_percent"] for r in valid) / len(valid)

        out.write(f"Average input reads: {avg_input:.2f}\n")
        out.write(f"Average PhiX removed reads: {avg_removed:.2f}\n")
        out.write(f"Average PhiX removed percent: {avg_removed_pct:.4f}%\n")
        out.write(f"Average clean reads: {avg_clean:.2f}\n")
        out.write(f"Average clean percent: {avg_clean_pct:.4f}%\n")
    else:
        out.write("No valid BBduk stats parsed.\n")
