## VARIABLES PASSED TO PROGRAM IN THIS ORDER
##   synapseProjectId
##   projectPath
##   sampleName

import sys
import subprocess
from subprocess import call
import synapseclient
from synapseclient.entity import File
from synapseclient.entity import Folder

syn = synapseclient.Synapse()
syn.login()

synapseProjectId = sys.argv[2]
projectPath = sys.argv[3]
sampleName = sys.argv[4]

## CREATE A FOLDER FOR THIS SAMPLE IN THE PROJECT
sampleFolder = Folder(name=sampleName, parentId=synapseProjectId)
sampleFolder = syn.store(sampleFolder)

#####
## PUSH FASTQ FILE METADATA
#####
fastq1Path = projectPath + '/' + sampleName + '_R1_001.fastq.gz'
fastq2Path = projectPath + '/' + sampleName + '_R2_001.fastq.gz'

fastq1 = File(path=fastq1Path, parentId=synapseProjectId, synapseStore=False)
fastq1 = syn.store(fastq1)
fastq2 = File(path=fastq2Path, parentId=synapseProjectId, synapseStore=False)
fastq2 = syn.store(fastq2)

##################################################
call(projectPath + '/script1.sh', shell=True)
##################################################

#####
## PUSH TOPHAT FILE METADATA
#####
tophatPath = projectPath + '/tophat-version/tophat_' + sampleName + '_R1_001/accepted_hits.bam'

tophatFile = File(path=tophatPath, parentId=sampleFolder['id'], synapseStore=False)
tophatFile = syn.store(tophatFile, used=[fastq1, fastq2], activityName='tophat', activityDescription='tophat')

##################################################
call(projectPath + '/script2.sh', shell=True)
##################################################

#####
## PUSH CUFFLINKS FILE METADATA
#####
cufflinksPath = projectPath + '/tophat-version/cufflinks_' + sampleName + '_R1_001'

cufflinksFile = File(path=cufflinksPath, parentId=sampleFolder['id'], synapseStore=False)
cufflinksFile = syn.store(cufflinksFile, used=[tophatFile], activityName='cufflinks', activityDescription='cufflinks')

##################################################
call(projectPath + '/script3.sh', shell=True)
##################################################


#####
## PUSH HTSEQ FILE OUTPUT AND STORE IN SYNAPSE
#####
htseqPath = projectPath + '/tophat-version/tophat_' + sampleName + '_R1_001/accepted_hits.novosort.sam.ensembl.htseq'

htseqFile = File(path=htseqPath, parentId=sampleFolder['id'], synapseStore=True)
htseqFile = syn.store(htseqFile, used=[cufflinksFile], activityName='htseq', activityDescription='htseq')

