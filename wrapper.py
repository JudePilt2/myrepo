#tools that must be installed: bowtie2(apt), spades.py, bedtools, samtools
#packages that must be installed: Biopython, build-essential
#bedtools is not available for windows, wrapper.py must be ran through linux
import sys, os, subprocess
from Bio import SeqIO

dpath='PipelineProject_Jude_Piltingsrud'
if os.path.exists(dpath) and os.path.isdir(dpath):
    os.chdir('PipelineProject_Jude_Piltingsrud') #moves into directory
else: #gives instructions for troubleshooting and exits, as the directory for generated results isn't found.
    print("Directory made by retrieve.py doesn't exist, please:\nMake sure wrapper.py and retrieve.py are in the same location and run retrieve.py, don't move the directory it creates\nOr create a directory named \"PipelineProject_Jude_Piltingsrud\" and name your files:\nSSR1_1.fastq\nSSR1_2.fastq\nSSR2_1.fastq\nSSR2_2.fastq")
    sys.exit()

#make sure bowtie2 is installed
check=os.system('bowtie2 --version')
if check!=0:
    print('bowtie2 is not installed, please install it using command:\nsudo apt install bowtie 2          (ubuntu)\nconda install -c bioconda bowtie2  (conda)\nOr follow installation guidelines from the website: https://bowtie-bio.sourceforge.net/bowtie2/index.shtml')

#building HCMV index
os.system('wget -q -O NC_006273.2.fasta "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_006273.2&rettype=fasta"') #calls the files, -O writes to file, -q quiet
os.system('bowtie2-build NC_006273.2.fasta HCMV_index') #builds the index
os.system('bowtie2 -x HCMV_index -1 SRR1_1.fastq -2 SRR1_2.fastq -S d1alligned.sam') #aligns paired reads to built index and saves it, -x is index, -S is save to output file
os.system('bowtie2 -x HCMV_index -1 SRR2_1.fastq -2 SRR2_2.fastq -S d2alligned.sam')

#convert sam file to bam file and sort/filter mapped reads
os.system('samtools view -Sb d1alligned.sam | samtools view -b -F 4 -o d1mapped.bam') #-Sb means input is sam and output is bam, -F 4 excludes(-F) unmapped reads(4), -o is output file
os.system('samtools view -Sb d2alligned.sam | samtools view -b -F 4 -o d2mapped.bam')

#uses subprocess b/c without using subprocess variables don't print to file properly
c1='grep "^@SRR" SRR1_1.fastq SRR1_2.fastq | wc -l' #lists all lines starting with @SRR and then counts the lines
bc=subprocess.check_output(c1, shell=True).decode('utf-8').strip()  #checks the output of c1 and prints it properly
c2='grep "^@SRR" SRR2_1.fastq SRR2_2.fastq | wc -l'
bz=subprocess.check_output(c2, shell=True).decode('utf-8').strip()
c3='samtools view -c d1mapped.bam'                                  #counts number of alignments
bg=subprocess.check_output(c3, shell=True).decode('utf-8').strip()
c4='samtools view -c d2mapped.bam'
be=subprocess.check_output(c4, shell=True).decode('utf-8').strip()
os.system('rm *.sam') #cleanup
output1=f"Donor 1 (2dpi) had {bc} read pairs before Bowtie2 filtering and {bg} read pairs after" #output formatting
output2=f"Donor 1 (6dpi) had {bz} read pairs before Bowtie2 filtering and {be} read pairs after"


#SPADES
os.system('bedtools bamtofastq -i d1mapped.bam -fq d1mapped.fastq') #spades requires fastq file as far as I can tell, and bedtools is the way to convert the bam files
os.system('bedtools bamtofastq -i d2mapped.bam -fq d2mapped.fastq')
#spades='spades.py --rna -s d1mapped.fastq -s d2mapped.fastq -k 99 -o spades_output' #not sure if I'm supposed to write the output to log or write the command used to log
#log='PipelineProject.log'
#with open(log, 'a') as log: #'a' for append (don't overwrite what I already have in the file)
#    subprocess.run(spades, shell=True, stdout=log, stderr=log)
os.system('spades.py --rna -s d1mapped.fastq -s d2mapped.fastq -k 99 -o spades_output') #-s for the differing lengths of reads, --rna b/c rna, -k for kmer count, -o for output file
output3=f"Bash command used to run SPAdes: spades.py --rna -s d1mapped.fastq -s d2mapped.fastq -k 99 -o spades_output"

outputfile='PipelineProject.log' #output printing
with open(outputfile, 'w') as out:
    out.write(output1+'\n'+output2+'\n\n'+output3+'\n')

#contig calculations
def ccalc(input_fasta, log_file):
    ccount = 0
    tlen = 0
    # Iterate over each contig in the input FASTA file
    for f in SeqIO.parse(input_fasta, "fasta"):
        clen = len(f.seq)
        if clen > 1000:
            ccount += 1
            tlen += clen
    # Write the results to the log file
    with open(log_file, 'a') as log:
        log.write(f'There are {ccount} contigs > 1000 bp in the assembly.\n')
        log.write(f'There are {tlen} bp in the assembly.\n')

# Replace 'spades_output/scaffolds.fasta' with the path to your SPAdes scaffolds file
input_fasta = 'spades_output/transcripts.fasta'
log_file = 'PipelineProject.log'
ccalc(input_fasta, log_file)

