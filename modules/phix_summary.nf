process PHIX_SUMMARY {

    tag "PhiX summary"

    publishDir "${params.outdir}/01_PhiX_contamination", mode: 'copy'

    input:
    path stats_files

    output:
    path "summary/phix_summary.csv"
    path "summary/phix_average_summary.txt"

    script:
    """
    python3 ${projectDir}/scripts/summarize_phix_stats.py ${stats_files}
    """
}
