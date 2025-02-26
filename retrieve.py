import sys, argparse, os

#Function to parse command line arguments
def check_arg(args=None):
    parser = argparse.ArgumentParser(
    description="Retrieve and process SSR information")
    parser.add_argument("-i", "--input",
    help="input file",
    required=True)
    return parser.parse_args(args)

#retrieve command line arguments
arguments = check_arg(sys.argv[1:])
infile = arguments.input

with open (infile, 'r') as f:
    file=f.read().split() #reads in lines removing spaces and \n values


dpath='PipelineProject_Jude_Piltingsrud' 
if os.path.exists(dpath) and os.path.isdir(dpath): #checks for directory used to store generated files
    os.chdir('PipelineProject_Jude_Piltingsrud')   #moves to directory, existing files will be written over
else:
    os.system('mkdir PipelineProject_Jude_Piltingsrud') #Makes directory for generated files
    os.chdir('PipelineProject_Jude_Piltingsrud')        #moves into created directory


i=0 #empty counter for file
while i<2:
    os.system('wget https://trace.ncbi.nlm.nih.gov/Traces/sra-reads-be/fastq?acc='+file[i]) #retrieves each SSR file in .gz format
    os.system('mv fastq?acc='+file[i]+' '+file[i]) #renames default download name
    os.system('fasterq-dump --split-files '+file[i]) #splits .gz into two paired-end fastq files
    i+=1

os.system('mv '+file[0]+'_1.fastq'+' SRR1_1.fastq') #renames processed .fastq files to work with wrapper.py
os.system('mv '+file[0]+'_2.fastq'+' SRR1_2.fastq')
os.system('mv '+file[1]+'_1.fastq'+' SRR2_1.fastq')
os.system('mv '+file[1]+'_2.fastq'+' SRR2_2.fastq')