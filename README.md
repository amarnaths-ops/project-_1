
README.md

Overview

This project provides a Python utility for sorting BED-formatted genomic data according to a predefined chromosome order.
The ordering rules are read from a separate file (e.g., standard_selection.tsv), and only the chromosomes listed in that rule file are included in the final output.

The tool accepts BED data from standard input (stdin) and prints the sorted result to standard output (stdout).


---

Features

Reads a chromosome priority list from a selection file.

Filters input BED records so only allowed chromosomes are processed.

Buckets entries by chromosome for efficient sorting.

Sorts each chromosome’s entries by:

1. Start position


2. End position (used as tie-breaker)



Outputs records in the exact chromosome order defined in the selection file.



---

Input Requirements

1. Rule File (e.g., standard_selection.tsv)

A plain text file containing chromosome names, one per line:

chr1
chr2
chr3
...

The order in this file determines the order of chromosomes in the output.

2. BED Input via stdin

The script expects BED-like tab-separated lines with at least:

chrom   start   end

Comments (#...) and empty lines are ignored.

Examples of valid lines:

chr1    120     400
chr2    50      80


---

Usage

Command-line Example

You can use the script in a Unix-style pipeline:

cat input.bed | python Project_1.py > sorted_output.bed

File Dependencies

The script expects the chromosome order file to be named:


standard_selection.tsv

Place this file in the same directory as the script or provide an absolute path (modify code if needed).


---

Program Structure

1. BedSorter Class

Handles rule loading, data processing, and output.

load_rules()
Reads chromosome names from the rule file and stores:

chrom_order → preserves the original order

chrom_set → quick membership lookup


process_input(input_stream)
Reads input BED lines, validates coordinates, and groups entries by chromosome using buckets.

write_output(output_stream)
Sorts each chromosome’s bucket and prints the original lines in order.


2. main()

Coordinates the overall workflow:

1. Initialize sorter with the selection file.


2. Load chromosome rules.


3. Read BED entries from stdin.


4. Output sorted result.




---

Output

The program writes all sorted BED lines to stdout.
Chromosomes appear only if present in the rule file, and in the exact order defined there.

Within each chromosome group, entries are sorted numerically by:

1. Start coordinate


2. End coordinate




---

Example

Rule File

chr2
chr1

Input

chr1    200   300
chr2    10    20
chr1    100   150

Output

chr2    10    20
chr1    100   150
chr1    200   300
