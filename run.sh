"""
NAME:          Run.sh
AUTHOR:        Manuel Dominguez)
EMAIL:         manolo.biomero@gmail.comk
DATE:          02/07/2021
INSTITUTION:   NHS
DESCRIPTION:   A shell script to run third scripts to be able to compare
               the depth of coverage of specific region of sequences. The minimun coverage can be specify also here.
               This only works in the Linux terminal of Iridis 4.
	       
"""

#!/bin/sh

#  Load modules we need
module load bedtools
module load  python/3.8.0


filename="$1"    # input filename
bed_target="$2"  # A second file needed to specify the region we want to analyse.

min_coverage="20"# The minimus coverage

# Read the Bed file and take as a input for the python script with the 
# min_coverage, then with bedtools compare with the target file and count the depth of coverage
# Can be implement also  sum, min, max ... https://bedtools.readthedocs.io/en/latest/content/tools/map.html

cat  "${filename}" | \
  python3 vcf2cov_copy.py "${min_coverage}" | \
  bedtools map -a "${bed_target}"  -b stdin  -c 5 -o count

