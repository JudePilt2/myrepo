# Python Pipeline Project

## Retrieving SSR paired-end fastq files
>[!WARNING]
>SRA Toolkit must be installed to run retrieve.py
To retrieve paired-end fastq files from NCBI, place the SSR numbers in a file with retrieve.py in this format:
>SSR123456<br />
>SSR654321

To call retrieve.py, the format is: python retrieve.py --input (your input file here)<br /><br />
Remember not to include "(" or ")" in the command<br /><br />
An example using SSREX.txt: $\color{green}{\textsf{python retrieve.py --input SSREX.txt}}$<br /><br />

## Wrapper.py
>[!WARNING]
>tools that must be installed: Biopython, bowtie2, SPAdes.py, samtools, BLAST+, ncbi-datasets-cli, and unzip<br />


