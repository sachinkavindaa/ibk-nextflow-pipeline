#!/usr/bin/env python3

import sys, csv, re
from pathlib import Path

files = [Path(x) for x in sys.argv[1:]]
samples = {}

def parse_bowtie2_log(path):
    text = path.read_text(errors="ignore")

    total = None
    overall_pct = None

    m = re.search(r"(\d+)\s+reads; of these:", text)
    if m:
        total = int(m.group(1))

    m = re.search(r"([0-9.]+)%\s+overall alignment rate", text)
    if m:
        overall_pct = float(m.group(1))

    if total is not None and overall_pct is not None:
        aligned = round(total * overall_pct / 100)
        unaligned = total - aligned
    else:
        aligned = ""
        unaligned = ""

    return total, aligned, unaligned, overall_pct

for f in files:
    name = f.name

    sample = name
    for suffix in ["_human_paired.txt", "_bovine_paired.txt", "_human_single.txt", "_bovine_single.txt"]:
        sample = sample.replace(suffix, "")

    samples.setdefault(sample, {"sample_id": sample})

    total, aligned, unaligned, pct = parse_bowtie2_log(f)

    if name.endswith("_human_paired.txt"):
        prefix = "human_paired"
    elif name.endswith("_bovine_paired.txt"):
        prefix = "bovine_paired"
    elif name.endswith("_human_single.txt"):
        prefix = "human_single"
    elif name.endswith("_bovine_single.txt"):
        prefix = "bovine_single"
    else:
        continue

    samples[sample][f"{prefix}_input_reads"] = total if total is not None else ""
    samples[sample][f"{prefix}_removed_reads"] = aligned
    samples[sample][f"{prefix}_clean_reads"] = unaligned
    samples[sample][f"{prefix}_removed_percent"] = pct if pct is not None else ""

rows = list(samples.values())

fields = [
    "sample_id",
    "human_paired_input_reads", "human_paired_removed_reads", "human_paired_clean_reads", "human_paired_removed_percent",
    "bovine_paired_input_reads", "bovine_paired_removed_reads", "bovine_paired_clean_reads", "bovine_paired_removed_percent",
    "human_single_input_reads", "human_single_removed_reads", "human_single_clean_reads", "human_single_removed_percent",
    "bovine_single_input_reads", "bovine_single_removed_reads", "bovine_single_clean_reads", "bovine_single_removed_percent"
]

summary_dir = Path("summary")
summary_dir.mkdir(exist_ok=True)

with (summary_dir / "host_summary.csv").open("w", newline="") as out:
    writer = csv.DictWriter(out, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

def avg(field):
    vals = []
    for r in rows:
        v = r.get(field, "")
        if v != "":
            vals.append(float(v))
    return sum(vals) / len(vals) if vals else None

with (summary_dir / "host_average_summary.txt").open("w") as out:
    out.write("Host removal average summary\n")
    out.write("============================\n\n")
    out.write(f"Number of samples: {len(rows)}\n\n")

    for field in [
        "human_paired_removed_percent",
        "bovine_paired_removed_percent",
        "human_single_removed_percent",
        "bovine_single_removed_percent"
    ]:
        value = avg(field)
        if value is not None:
            out.write(f"Average {field}: {value:.4f}%\n")
        else:
            out.write(f"Average {field}: NA\n")
