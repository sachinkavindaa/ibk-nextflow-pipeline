process PHIX_REMOVAL {

    tag "$sample_id"

    publishDir "${params.outdir}/01_PhiX_contamination", mode: 'copy'

    input:
    tuple val(sample_id), path(read1), path(read2)

    output:
    tuple val(sample_id),
          path("${sample_id}_1_phiX_clean.fq.gz"),
          path("${sample_id}_2_phiX_clean.fq.gz"),
          path("${sample_id}_phiX_stats.txt")

    script:
    """
    bbduk.sh \\
        in1=${read1} \\
        in2=${read2} \\
        out1=${sample_id}_1_phiX_clean.fq.gz \\
        out2=${sample_id}_2_phiX_clean.fq.gz \\
        ref=artifacts,phix \\
        k=31 \\
        hdist=1 \\
        threads=${task.cpus} \\
        stats=${sample_id}_phiX_stats.txt
    """
}
