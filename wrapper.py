import sys, os, subprocess
from Bio import SeqIO

dpath='PipelineProject_Jude_Piltingsrud'
if os.path.exists(dpath) and os.path.isdir(dpath):
    os.chdir('PipelineProject_Jude_Piltingsrud') #moves into directory
else: #gives instructions for troubleshooting and exits, as the directory for generated results isn't found.
    print("Directory made by retrieve.py doesn't exist, please:\nMake sure wrapper.py and retrieve.py are in the same location and run retrieve.py, don't move the directory it creates\nOr create a directory named \"PipelineProject_Jude_Piltingsrud\" and name your files:\nSSR1_1.fastq\nSSR1_2.fastq\nSSR2_1.fastq\nSSR2_2.fastq")
    sys.exit()

#building HCMV index
os.system('wget -O NC_006273.2.fasta "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_006273.2&rettype=fasta"') #calls the files, -O writes to file
os.system('bowtie2-build NC_006273.2.fasta HCMV_index') #builds the index
os.system('bowtie2 -x HCMV_index -1 SRR1_1.fastq -2 SRR1_2.fastq -S d1alligned.sam') #aligns paired reads to built index and saves it, -x is index, -S is save to output file
os.system('bowtie2 -x HCMV_index -1 SRR2_1.fastq -2 SRR2_2.fastq -S d2alligned.sam')

#convert sam file to bam file and sort/filter mapped reads
os.system('samtools view -Sb d1alligned.sam | samtools view -b -F 4 -o d1mapped.bam') #filter -Sb means input is sam and output is bam, -F 4 excludes(-F) unmapped reads(4), -o is output file
os.system('samtools view -Sb d2alligned.sam | samtools view -b -F 4 -o d2mapped.bam')
os.system('samtools sort -n d1mapped.bam -o d1sort.bam') #sort
os.system('samtools sort -n d2mapped.bam -o d2sort.bam')

#uses subprocess b/c without using subprocess variables don't print to file properly
c1='grep "^@SRR" SRR1_1.fastq SRR1_2.fastq | wc -l' #lists all lines starting with @SRR and then counts the lines
bc=subprocess.check_output(c1, shell=True).decode('utf-8').strip()  #checks the output of c1 and prints it properly
c2='grep "^@SRR" SRR2_1.fastq SRR2_2.fastq | wc -l'
bz=subprocess.check_output(c2, shell=True).decode('utf-8').strip()
c3='samtools view -c d1sort.bam'                                  #counts number of alignments
bg=subprocess.check_output(c3, shell=True).decode('utf-8').strip()
c4='samtools view -c d2sort.bam'
be=subprocess.check_output(c4, shell=True).decode('utf-8').strip()

output1=f"Donor 1 (2dpi) had {bc} read pairs before Bowtie2 filtering and {bg} read pairs after" #output formatting, f"" for variable use
output2=f"Donor 1 (6dpi) had {bz} read pairs before Bowtie2 filtering and {be} read pairs after"


#SPADES
os.system('samtools fastq -@ 8 d1sort.bam \-1 d1for.fastq \-2 d1rev.fastq \-0 /dev/null -s /dev/null -n') #splits filtered/sorted bam files into fastq files for SPAdes
os.system('samtools fastq -@ 8 d2sort.bam \-1 d2for.fastq \-2 d2rev.fastq \-0 /dev/null -s /dev/null -n')
os.system('spades.py --rna -1 d1for.fastq -2 d1rev.fastq -1 d2for.fastq -2 d2rev.fastq -k 99 -o spades_output') #runs spades, --rna for type of info, -k 99 for kmers, -o for output
output3=f"Bash command used to run SPAdes: spades.py --rna -1 d1for.fastq -2 d1rev.fastq -1 d2for.fastq -2 d2rev.fastq -k 99 -o spades_output" #output formatting


outputfile='PipelineProject.log' #output printing
with open(outputfile, 'w') as out:
    out.write(output1+'\n'+output2+'\n\n'+output3+'\n')


def ccalc(input_fasta, log_file): #contig calculations for part 4&5
    ccount = 0 #contig count
    tlen = 0   #total length of assembly
    maxlen=0   #longest length counter
    long_cont='' #longest contig saver

    for f in SeqIO.parse(input_fasta, "fasta"): #reading fasta file 1 contig at a time
        clen = len(f.seq) #current length 
        if clen > maxlen:
            maxlen=clen #saves length value of longest contig
            long_cont=f #saves string value of longest contig
        if clen > 1000: #counts contigs longer than 1000
            ccount += 1
            tlen += clen #counts total bp length 
    with open(log_file, 'a') as log: #writes number of good contigs found in assembly and total bp in assembly. 'a' for appending (don't write over other log lines)
        log.write(f'There are {ccount} contigs > 1000 bp in the assembly.\n')
        log.write(f'There are {tlen} bp in the assembly.\n\n')
    return long_cont #returns longest conting (string) for part 5

input_fasta = 'spades_output/contigs.fasta' #var for calling ccalc, SPAdes output
log_file = 'PipelineProject.log'                #var for calling ccalc, outfile

long_cont=ccalc(input_fasta, log_file)          #call ccalc and save longest contig string to var

SeqIO.write(long_cont, "long_cont.fasta", "fasta") #Saves longest contig to fasta file

#BLAST
os.system('datasets download virus genome taxon betaherpesvirinae --refseq --include genome')   #download betaherpesvirinae
os.system('unzip ncbi_dataset.zip')                                                             #unzip file
os.system('mv ncbi_dataset/data/genomic.fna betaherpesvirinae.fna')                             #renaming and moving target file
os.system('makeblastdb -in betaherpesvirinae.fna -out betaherpesvirinae -title betaherpesvirinae -dbtype nucl') #create database    
os.system('echo "sacc\tpident\tlength\tqstart\tqend\tsstart\tsend\tbitscore\tevalue\tstitle" >> PipelineProject.log') #write header
os.system('blastn -query long_cont.fasta -db betaherpesvirinae -outfmt "6 sacc pident length qstart qend sstart send bitscore evalue stitle" -max_target_seqs 10 -max_hsps 1 >> PipelineProject.log') #blast command, returns (up to) top 10 hits, -max_hsps 1 makes sure only one hit per sequence

os.system('rm *.fna *.ndb *.nhr *.nin *.not *.nsq *.ntf *.nto *.bam *.sam *.bt2 *.txt *.zip *.md d1for.fastq d1rev.fastq d2for.fastq d2rev.fastq long_cont.fasta NC_006273.2.fasta') #cleanup files that aren't input/output
os.system('rm -r ncbi_dataset spades_output')