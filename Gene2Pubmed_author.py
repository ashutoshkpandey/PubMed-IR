
# This programs needs following modules from Biopython 

from Bio import Medline
from Bio import Entrez
Entrez.email = 'ashutoshmits@gmail.com'

import os, sys, math, fileinput

Argument = []
Argument = sys.argv[1:]

if (len(Argument)) < 3:
	print "Usage: python Program.py Gene2Pubmed Old_Pubmed_file Outputfile"
	sys.exit()

# wget ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz
# Old_Pubmed_file in case the purpose of this program is to update otherwise a blank file can be provided

Pubmed2gene = {}
Old_Pubmedids = {}
 
for line in fileinput.input(Argument[1]):
        if line.startswith("#"):
                continue

        line = line.rstrip("\n")
        array = []
        array = line.split("\t")
	Old_Pubmedids[array[1]] = ""
	

for line in fileinput.input(Argument[0]):
	if line.startswith("#"):
		continue

        line = line.rstrip("\n")
        array = []
        array = line.split("\t")

	if array[0] == "10090" or array[0] == "9606" or array[0] == "10116" or array[0] == "7227": # Tax id for mouse, human, rat and drosophilla. More species can be added.
		if array[2] not in Pubmed2gene:
			Pubmed2gene[array[2]] = []
			Pubmed2gene[array[2]].append(array[1])
		else:
			Pubmed2gene[array[2]].append(array[1])

print "Gene2Pubmed read"

def Pubmedsearch(PMID):
	pmid = ""
	pmid = PMID

    	handle = Entrez.efetch(db="pubmed", id= pmid, rettype="medline",retmode="text")
    	records = Medline.parse(handle)
    	records = list(records)
    	for record in records:
        	return (str(pmid)+"\t"+str(record.get("TI", "?"))+"\t"+str(record.get("FAU", "?"))+"\t"+str(record.get("AU", "?"))+"\t"+str(record.get("AD", "?")))
		# TI >Title, FAU > Full Author Name, AU > Author name, AD > Affiliation (More tags can be added)

output = open(str(Argument[2]),"a")

for pmid in Pubmed2gene:
	if pmid in Old_Pubmedids:
		continue 

	if len(Pubmed2gene[pmid]) >= 50:# Pubmed2gene directory links a PMID to number of genes associated with it. We ignore articles (PMID) related to more than 50 genes.
		continue
	
	info = ""
	info = Pubmedsearch(pmid)

	for geneid in Pubmed2gene[pmid]:
		output.write(str(geneid)+"\t"+str(info)+"\n")
		output.flush()

output.close()
