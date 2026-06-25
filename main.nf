#!/usr/bin/env nextflow

nextflow.enable.dsl=2

include { PHIX_REMOVAL } from './modules/phix_removal.nf'
include { PHIX_SUMMARY } from './modules/phix_summary.nf'
include { TRIMMING } from './modules/trimming.nf'
include { HOST_REMOVAL } from './modules/host_removal.nf'

workflow {

    reads_ch = Channel
        .fromPath(params.input)
        .splitCsv(header: true)
        .map { row ->
            tuple(row.sample_id, file(row.read1), file(row.read2))
        }

    // Step 1
    phix_out = PHIX_REMOVAL(reads_ch)

    // PhiX report
    phix_stats_ch = phix_out
        .map { sample_id, read1, read2, stats -> stats }
        .collect()

    PHIX_SUMMARY(phix_stats_ch)

    // Step 2
    trim_out = TRIMMING(phix_out)

    // Step 3
    host_out = HOST_REMOVAL(trim_out)
}
