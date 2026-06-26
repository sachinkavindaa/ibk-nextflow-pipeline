#!/usr/bin/env nextflow

nextflow.enable.dsl=2

include { PHIX_REMOVAL } from './modules/phix_removal.nf'
include { PHIX_SUMMARY } from './modules/phix_summary.nf'

include { TRIMMING } from './modules/trimming.nf'
include { TRIMMING_SUMMARY } from './modules/trimming_summary.nf'

include { HOST_REMOVAL } from './modules/host_removal.nf'
include { HOST_SUMMARY } from './modules/host_summary.nf'

workflow {

    reads_ch = Channel
        .fromPath(params.input)
        .splitCsv(header: true)
        .map { row ->
            tuple(row.sample_id, file(row.read1), file(row.read2))
        }

    phix_out = PHIX_REMOVAL(reads_ch)

    phix_stats_ch = phix_out
        .map { sample_id, read1, read2, phix_stats -> phix_stats }
        .collect()

    PHIX_SUMMARY(phix_stats_ch)

    trim_out = TRIMMING(phix_out)

    trim_stats_ch = trim_out
        .map { sample_id, read1, read2, single_reads, trim_stats -> trim_stats }
        .collect()

    TRIMMING_SUMMARY(trim_stats_ch)

    host_out = HOST_REMOVAL(trim_out)

    host_stats_ch = host_out
        .map { sample_id, r1, r2, single, human_paired, bovine_paired, human_single, bovine_single ->
            [human_paired, bovine_paired, human_single, bovine_single]
        }
        .flatten()
        .collect()

    HOST_SUMMARY(host_stats_ch)
}
