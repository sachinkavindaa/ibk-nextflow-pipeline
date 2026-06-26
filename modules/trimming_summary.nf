process TRIMMING_SUMMARY {

    tag "Trimming summary"

    publishDir "${params.outdir}/02_Trimming", mode: 'copy'

    input:
    path stats_files

    output:
    path "summary/trimming_summary.csv"
    path "summary/trimming_average_summary.txt"

    script:
    """
    python3 ${projectDir}/scripts/summarize_trimming_stats.py ${stats_files}
    """
}
