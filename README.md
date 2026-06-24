# IBK Shotgun Metagenomics Nextflow Pipeline

This repository contains a Nextflow pipeline for shotgun metagenomics analysis of IBK samples.

## Current step

1. PhiX contamination removal using BBduk

## Run on HCC

```bash
module load nextflow
module load bbmap/39.06

nextflow run main.nf -profile hcc
