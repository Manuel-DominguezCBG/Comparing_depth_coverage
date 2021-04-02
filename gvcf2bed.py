

#!/usr/bin/env python3

import sys
import os

def process_line(line: str, MINDEPTH: int=20) -> None:
    """
    Extracts the depth of coverage for a position, and outputs it in BED format
    which will (externally) be merged with Bedtools.

    To override defaul MINDEPTH of 20, pass an integer as the second arg.
    """
    # Ignore comment/header lines
    if line.startswith("#"):
        return None
    # Regular nucleotide lines need processing.
    # Remove trailing newlines and split on tabs
    line = line.strip()
    line = line.split()
    # Assign the useful parameters
    chrom = line[0]
    pos = int(line[1])
    format_header = line[8]
    sample_format = line[9]
    sample_details = join_header_sample(format_header, sample_format)

    # Find the depth (DP) from the processed details. Asssume 0 depth if not found
    try:
        depth = int(sample_details['DP'])
    except KeyError:
        print(f"ERROR: DP field not found at chr{chrom}:{pos}. Assuming 0 depth.", file=sys.stderr)
        depth = 0

    # Print if depth at position is above MINDEPTH, otherwise do nothing
    if depth >= MINDEPTH:
        # Needs to be BED format, which is 0-indexed, rather than VCF which is 1-indexed
        # So we just subtract 1 from the start position, and leave the end unchanged
        # We include the optional name/score columns so we can calculate averages etc. if needed.
        # per UCSC BED format guide:
        # chrom    chromStart    chromEnd    name    score
        print(f"{chrom}\t{pos-1}\t{pos}\t.\t{depth}", file=sys.stdout)
    else:
        pass

def join_header_sample(format_header: str, sample_format: str) -> dict:
    """Join the format header and sample fields into a dictionary"""
    # DEV: This probably isn't strictly needed, but is a simple way to
    #      handle the fact that FORMAT isn't fixed between lines
    format_header = format_header.split(":")
    sample_format = sample_format.split(":")

    # simples way to combine is to use zip() and then cast to a dict()
    return dict(zip(format_header, sample_format))



if __name__ == "__main__":

    # Get command line arguments

    # If no arguemnts, use the default version

    # If arguments, check they are integer and then run process_line with that


    if  len(sys.argv) > 1:
        min_depth=sys.argv
        min_depth=int(min_depth[1])
    else:
        min_depth=10

    for line in sys.stdin:
        process_line(line, min_depth)


