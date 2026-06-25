process HOST_REMOVAL {

    module 'bowtie/2.5'

    tag "$sample_id"

    publishDir "${params.outdir}/03_Host_removal/final_clean_reads", pattern: "*_final_clean_*", mode: 'copy'
    publishDir "${params.outdir}/03_Host_removal/stats", pattern: "*.txt", mode: 'copy'

    input:
    tuple val(sample_id), path(read1), path(read2), path(single_reads), path(trim_stats)

    output:
    tuple val(sample_id),
          path("${sample_id}_final_clean_paired.1.fastq.gz"),
          path("${sample_id}_final_clean_paired.2.fastq.gz"),
          path("${sample_id}_human_paired.txt"),
          path("${sample_id}_bovine_paired.txt")

    script:
    """
    bowtie2 \\
        -x ${params.human_index} \\
        -1 ${read1} \\
        -2 ${read2} \\
        --un-conc-gz ${sample_id}_nonhuman_paired.%.fastq.gz \\
        -p ${task.cpus} \\
        --very-sensitive \\
        --no-unal \\
        -S /dev/null \\
        2> ${sample_id}_human_paired.txt

    bowtie2 \\
        -x ${params.bovine_index} \\
        -1 ${sample_id}_nonhuman_paired.1.fastq.gz \\
        -2 ${sample_id}_nonhuman_paired.2.fastq.gz \\
        --un-conc-gz ${sample_id}_final_clean_paired.%.fastq.gz \\
        -p ${task.cpus} \\
        --very-sensitive \\
        --no-unal \\
        -S /dev/null \\
        2> ${sample_id}_bovine_paired.txt
    """
}
