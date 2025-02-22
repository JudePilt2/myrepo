#Python Pipeline Project

#Retrieving SSR paired-end fastq files
To retrieve paired-end fastq files from NCBI, place the SSR numbers in a file with retrieve.py in this format:
>SSR123456
>SSR654321
To call retrieve.py, the format is: python retrieve.py --input <your input file here>
Remember not to include < or > in the command line