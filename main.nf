#!/usr/bin/env nextflow

nextflow.enable.dsl=2

include { PHIX_REMOVAL } from './modules/phix_removal.nf'

workflow {

    reads_ch = Channel
        .fromPath(params.input)
        .splitCsv(header: true)
        .map { row ->
            tuple(row.sample_id, file(row.read1), file(row.read2))
        }

    PHIX_REMOVAL(reads_ch)
}
