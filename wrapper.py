import sys, os
#from Bio import SeqIO

with open('SSR1_1.fastq', 'r') as f:
    lines1 = f.readline().split()

with open('SSR1_2.fastq', 'r') as f:
    lines2 = f.readline().split()

with open('SSR2_1.fastq', 'r') as f:
    lines3 = f.readline().split()

with open('SSR2_2.fastq', 'r') as f:
    lines4 = f.readline().split()




#format needs to be named "PipelineProject.log" in directory named "PipelineProject_Jude_Piltingsrud"
#"easiest way: create directory using os.system() call and then move into it via os.chdir()"
outputfile='PipelineProject.log'
with open(outputfile, 'w') as out:
    out.write("test")