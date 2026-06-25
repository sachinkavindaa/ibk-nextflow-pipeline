process TRIMMING {

    module 'sickle'

    tag "$sample_id"

    publishDir "${params.outdir}/02_Trimming/paired_reads", pattern: "*_trimmed.fq", mode: 'copy'
    publishDir "${params.outdir}/02_Trimming/single_reads", pattern: "*_trimmed_single.fq", mode: 'copy'
    publishDir "${params.outdir}/02_Trimming/stats", pattern: "*_trim_stats.txt", mode: 'copy'

    input:
    tuple val(sample_id), path(read1), path(read2), path(phix_stats)

    output:
    tuple val(sample_id),
          path("${sample_id}_1_trimmed.fq"),
          path("${sample_id}_2_trimmed.fq"),
          path("${sample_id}_trimmed_single.fq"),
          path("${sample_id}_trim_stats.txt")

    script:
    """
    zcat ${read1} > ${sample_id}_1_tmp.fq
    zcat ${read2} > ${sample_id}_2_tmp.fq

    sickle pe -t sanger \\
        -f ${sample_id}_1_tmp.fq \\
        -r ${sample_id}_2_tmp.fq \\
        -o ${sample_id}_1_trimmed.fq \\
        -p ${sample_id}_2_trimmed.fq \\
        -s ${sample_id}_trimmed_single.fq \\
        -q 30 \\
        -l 50 \\
        2> ${sample_id}_trim_stats.txt

    rm ${sample_id}_1_tmp.fq ${sample_id}_2_tmp.fq
    """
}
