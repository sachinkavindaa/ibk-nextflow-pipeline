process HOST_SUMMARY {

    tag "Host summary"

    publishDir "${params.outdir}/03_Host_removal", mode: 'copy'

    input:
    path stats_files

    output:
    path "summary/host_summary.csv"
    path "summary/host_average_summary.txt"

    script:
    """
    python3 ${projectDir}/scripts/summarize_host_stats.py ${stats_files}
    """
}
