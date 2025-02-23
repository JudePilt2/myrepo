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
    getfile=('wget https://trace.ncbi.nlm.nih.gov/Traces/sra-reads-be/fastq?acc='+file[i]) #retrieves each SSR file in .gz format
    name=('mv fastq?acc='+file[i]+' '+file[i]) #renames default download name
    split=('fastq-dump --split-files '+file[i]) #splits .gz into two paired-end fastq files 
    os.system(getfile) #calling the commands
    os.system(name)
    os.system(split)
    i+=1

name1=('mv '+file[0]+'_1.fastq'+' SSR1_1.fastq') #renames processed .fastq files to work with wrapper.py
name2=('mv '+file[0]+'_2.fastq'+' SSR1_2.fastq')
name3=('mv '+file[1]+'_1.fastq'+' SSR2_1.fastq')
name4=('mv '+file[1]+'_2.fastq'+' SSR2_2.fastq')
os.system(name1) #calls commands
os.system(name2)
os.system(name3)
os.system(name4)