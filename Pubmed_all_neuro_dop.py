import urllib
import sys
import re
from sets import Set
import time
import fileinput
from operator import itemgetter

Argument = []
Argument = sys.argv[1:]  # Reading the arguments

if len(Argument) < 6:
        print "Usage:python Program.py Nomenclature_file Stop_PMIDs English_genes Ambiguous_acronyms short_names junk_names Gene_keywords"
        sys.exit()

Filepath_name = Argument[0] # Nomenclature dictionary
Filepath_stop = Argument[1] # StopPMIDs
Filepath_english = Argument[2] # English words
Filepath_ambi = Argument[3] # Ambiguous acronyms
Filepath_short = Argument[4] #short names
Filepath_junk = Argument[5] #junk names
Filepath_keywords = Argument[6] # Gene specific tags
Filepath_neuro = Argument[7] # Neuroscience keywords
entrez_geneid = Argument[8] #Gene ID

English_words = {}
for line in fileinput.input([Filepath_english]):
        rowlist = []
        rowlist = (line.rstrip("\n")).split("\t")
        if len(rowlist[2:]) >= 1:
                English_words[rowlist[0]] = rowlist[2:]

#print English_words 
 
Ambi_words = {}
for line in fileinput.input([Filepath_ambi]):
        rowlist = []
        rowlist = (line.rstrip("\n")).split("\t")
        if len(rowlist[2:]) >= 1:
                Ambi_words[rowlist[0]] = rowlist[2:]

#print Ambi_words 
 
Short_words = {}
for line in fileinput.input([Filepath_short]):
        rowlist = []
        rowlist = (line.rstrip("\n")).split("\t")
        if len(rowlist[2:]) >= 1:
                Short_words[rowlist[0]] = rowlist[2:]

#print Short_words

junk_words = {}
for line in fileinput.input([Filepath_junk]):
        rowlist = []
        rowlist = (line.rstrip("\n")).split("\t")
        if len(rowlist[2:]) >= 1:
                junk_words[rowlist[0]] = rowlist[2:]

#print junk_words

Gene_keywords = {}
for line in fileinput.input([Filepath_keywords]):
        rowlist = []
        rowlist = (line.rstrip("\n")).split("\t")
        if len(rowlist[2:]) >= 1:
                Gene_keywords[rowlist[0]] = rowlist[2:]

#print Gene_keywords 

Stop_Pubmed = []
for line in fileinput.input([Filepath_stop]):
        Stop_Pubmed.append(line.rstrip("\n"))

Neuro_words = []
for line in fileinput.input([Filepath_neuro]):
        Neuro_words.append(line.rstrip("\n").split("\t")[0])

def unique(pmids,stoppmids):
	pubmed = []
	stoppubmed = []
	unique_pmids = []

	pubmed = pmids
	if len(pubmed) == 0:
		return unique_pmids

	pubmed[-1] = pubmed[-1].rstrip("</I")
	stoppubmed = stoppmids

	for i in pubmed:
		if i not in stoppubmed:
			unique_pmids.append(i)

	return unique_pmids

def pubmedcheck(genequery,geneid):

        PMIDSquery = []
        query = ""
        ambi = ""
        genearray =[]
        genearray = genequery 
       
        for name in genearray:
                if geneid in Short_words:
                        if name in Short_words[geneid]: 
                                continue

                if geneid in junk_words:
                        if name in junk_words[geneid]:
                                continue

                Isambiguous = "No"

                if geneid in English_words:
                        if name in English_words[geneid]:
                                Isambiguous = "Yes"

                if geneid in Ambi_words:
                        if name in Ambi_words[geneid]:
                                Isambiguous = "Yes"

                if Isambiguous == "Yes":
                        if geneid in Gene_keywords:
                                for keyword in Gene_keywords[geneid]:
                                        if ambi == "":
                                                ambi = "(\""+str(name)+"\"[TIAB] AND "+"\""+str(keyword)+"\"[TIAB]) OR "
                                        else:
                                                ambi =  ambi + "(\""+str(name)+"\"[TIAB] AND "+"\""+str(keyword)+"\"[TIAB]) OR "

                                continue
                        else:
                                continue


                if re.search('\W+',name):
                        queryarray = []
                        queryarray = re.split('\W+',name )
                        newquery = "+".join(queryarray)
                        if query == "":
                                query = "\""+str(newquery)+"\""
                        else:
                                query = query + "[TIAB] OR \""+str(newquery)+"\""

                else:    
                        if query == "":
                                query = "\""+str(name)+"\""
                        else:
                                query = query + "[TIAB] OR \""+str(name)+"\""

        query = "("+ambi+query+"[TIAB])"            
        
        url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="+query+"+ AND+ (Mus+Musculus OR Homo+Sapiens OR Rattus+Norvegicus)&retmax=10000"
        print url

        fp = urllib.urlopen(url)
        n = 0
        time.sleep(.30)
        while 1:
                s = fp.read(8192)
                if not s:
                    break
                n = n + len(s)

                PMIDarray = []
                PMIDarray = selectPMID(s)
		
                DifferenceSetP = []
                DifferenceSetP = unique(PMIDarray,Stop_Pubmed)		
	
                PMIDSquery = PMIDSquery + DifferenceSetP
		
        fp.close()

 	#print PMIDSquery 
        return PMIDSquery

def entrezcheck(geneid):

        PMIDSquery = []

        if geneid == "NA":
                return PMIDSquery

        fp = urllib.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&id="+geneid+"&Link&LinkName=gene_pubmed")
        n = 0

        time.sleep(.30)
        while 1:
                s = fp.read(8192)
                if not s:
                        break
                n = n + len(s)

                Entrezarray = []
                Entrezarray = selectPMID(s)

                DifferenceSet = []
                DifferenceSet = unique(Entrezarray[1:],Stop_Pubmed)

                PMIDSquery = PMIDSquery + DifferenceSet

        fp.close()
 
        return PMIDSquery

def neuropubmedcheck(genequery,geneid):

        PMIDSquery = []
        ambi = ""
        query = ""
        genearray =[]

        genearray = genequery
        
        for name in genearray:
                if geneid in Short_words:
                        if name in Short_words[geneid]:
                                continue

                if geneid in junk_words:
                        if name in junk_words[geneid]:
                                continue

                Isambiguous = "No"

                if geneid in English_words:
                        if name in English_words[geneid]:
                                Isambiguous = "Yes"

                if geneid in Ambi_words:
                        if name in Ambi_words[geneid]:
                                Isambiguous = "Yes"

                if Isambiguous == "Yes":
                        if geneid in Gene_keywords:
                                for keyword in Gene_keywords[geneid]:
                                        if ambi == "":
                                                ambi = "(\""+str(name)+"\"[TIAB] AND "+"\""+str(keyword)+"\"[TIAB]) OR "
                                        else:
                                                ambi =  ambi + "(\""+str(name)+"\"[TIAB] AND "+"\""+str(keyword)+"\"[TIAB]) OR "

                                continue
                        else:
                                continue

                if re.search('\W+',name):

                        queryarray = []
                        queryarray = re.split('\W+',name )
                        newquery = "+".join(queryarray)
                        if query == "":
                                query = "\""+str(newquery)+"\""
                        else:
                                query = query + "[TIAB] OR \""+str(newquery)+"\""
                else:
                        if query == "":
                                query = "\""+str(name)+"\""
                        else:
                                query = query + "[TIAB] OR \""+str(name)+"\""

        query = "("+ambi+query+"[TIAB])"
	
	neuro = ""
	
	for ns in Neuro_words:
		neuro = neuro+ns+"[TIAB] OR "
	
	neuro = neuro.rstrip(" OR ")

        #url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="+query+"+ AND+(Brain[TIAB] OR Brain's[TIAB] OR Nervous[TIAB] OR Neur*[TIAB] OR Neuro*[TIAB] OR Hippocamp*[TIAB] OR Cerebr*[TIAB] OR Synap*[TIAB] OR Cerebellum[TIAB] OR Medulla[TIAB] OR Hypothalamus[TIAB] OR Pituitary[TIAB] OR Thalamus*[TIAB] OR Neuron*[TIAB] OR Glial[TIAB] OR Nerve[TIAB] OR Cortex[TIAB] OR Amygdala[TIAB] OR Purkinje[TIAB] OR Substantia+Nigra[TIAB] OR Axon*[TIAB] OR Striatum[TIAB] OR Dendrit*[TIAB] OR neurodegenerati*[TIAB] OR Alzheimer*[TIAB] OR Autism[TIAB] OR Myelin[TIAB] OR Astrocyte*[TIAB] OR Oligodendrocytes[TIAB] OR Glial[TIAB] OR CNS[TIAB] OR Parkinson*[TIAB] OR Pallidum[TIAB] OR Seizure*[TIAB] OR Epilepsy[TIAB] OR Motor[TIAB] OR Cerelovascular[TIAB] OR Huntington*[TIAB] OR Aphasia[TIAB] OR Narcolepsy[TIAB] OR Neuromuscular[TIAB])+ AND+(Mus+Musculus OR Homo+Sapiens OR Rattus+Norvegicus)&retmax=10000"
       
	url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="+query+"+ AND+("+str(neuro)+")+ AND+(Mus+Musculus OR Homo+Sapiens OR Rattus+Norvegicus)&retmax=10000"
        print url 
        fp = urllib.urlopen(url)
        n = 0

	time.sleep(.90)
        
	while 1:
                s = fp.read(8192)
                if not s:
                    break
                n = n + len(s)

		PMIDarray = []
                PMIDarray = selectPMID(s)

                DifferenceSetP = []
                DifferenceSetP = unique(PMIDarray,Stop_Pubmed)

                PMIDSquery = PMIDSquery + DifferenceSetP

        fp.close()

	#print PMIDSquery 
        return PMIDSquery

def strip(x):
    return x.lstrip().rstrip()

def selectDOP(data):
    year = ""
    rows = []
    rows = data.split('\n')
    for row in rows:
        if re.match("<Item Name=\"pubmed\" Type=\"Date\">",strip(row)):
            year = remove_html_tags(strip(row)).split("/")[0]
    return year

def dateofpub(Pubid):
        Pubmedid = ""
        Pubmedid = Pubid
        DateofPub = ""

        fp = urllib.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id="+Pubmedid+"+&retmode=xml")
        time.sleep(.30)
        s = fp.read(8192)

        DateofPub = selectDOP(s)
        fp.close()

        return DateofPub

def remove_html_tags(data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)

def selectPMID(data):

    Pubmedid = []
    rows = []
    count = 0
    total = 0
    rows = data.split('\n')
    for row in rows:
        if re.match("<Id>",strip(row)):
            count = count + 1
            Pubmedid.append(remove_html_tags(strip(row)))
    return Pubmedid

gene2pubmed = open("GeneID_G2P_Pubmed_t.txt","a")
dop = open("Date_publication_GeneID_t.txt","a")
ndop = open("Date_neuro_publication_GeneID_t.txt","a")
apmid = open("PMID_publication_GeneID_t.txt","a")
npmid = open("Neuro_PMID_publication_GeneID_t.txt","a")
allpmids = open("PMIDs_GeneID_neuro_t.txt","a")

Status = "False"

for line in fileinput.input([Filepath_name]):
        genearray = []
        genearray = (line.rstrip("\n")).split("\t")

	if genearray[0] == entrez_geneid:
		Status = "True"

	if Status != "True":
		continue

        GeneID = ""
        GeneIDh = ""
        GeneIDr = ""

        PMIDquery = []
        NPMIDquery = []

        MouseG2P = []
        HumanG2P = []
        RatG2P = []

        GeneID = genearray[0]
        GeneIDh = genearray[1]
        GeneIDr = genearray[2]

        print GeneID

	firstpubdate = ""
        firstneuropubdate = ""

        lastpubdate = ""
        lastneuropubdate = ""

        MouseG2P = entrezcheck(GeneID)
        HumanG2P = entrezcheck(GeneIDh)
        RatG2P = entrezcheck(GeneIDr)

        PMIDquery = pubmedcheck(genearray[3:],GeneID)
        NPMIDquery = neuropubmedcheck(genearray[3:],GeneID)

        dop.write(str(GeneID)+"\t"+str(GeneIDh)+"\t"+str(GeneIDr))
	ndop.write(str(GeneID)+"\t"+str(GeneIDh)+"\t"+str(GeneIDr))
	apmid.write(str(GeneID)+"\t"+str(GeneIDh)+"\t"+str(GeneIDr))
	npmid.write(str(GeneID)+"\t"+str(GeneIDh)+"\t"+str(GeneIDr))
	
	for paper in NPMIDquery:
		allpmids.write(str(GeneID)+"\t"+str(paper)+"\n")

        gene2pubmed.write(str(GeneID)+"\t"+str(GeneIDh)+"\t"+str(GeneIDr)+"\t"+str(len(MouseG2P))+"\t"+str(len(HumanG2P))+"\t"+str(len(RatG2P))+"\t"+str(len(PMIDquery))+"\t"+str(len(NPMIDquery))+"\n")

        if len(PMIDquery) >= 2:
                firstpubdate = dateofpub(PMIDquery[-1])
                lastpubdate = dateofpub(PMIDquery[0])

        elif len(PMIDquery) == 1:
                lastpubdate = dateofpub(PMIDquery[0])
                firstpubdate = lastpubdate
        else:
                firstpubdate = "NA"
		lastpubdate = "NA"


	if len(PMIDquery) >= 10:
                dop.write("\t"+str(firstpubdate)+"\t"+str(dateofpub(PMIDquery[-5]))+"\t"+str(dateofpub(PMIDquery[-10]))+"\t"+str(lastpubdate)+"\n")
		apmid.write("\t"+str(PMIDquery[-1])+"\t"+str(PMIDquery[-5])+"\t"+str(PMIDquery[-10])+"\t"+str(PMIDquery[0])+"\n")        
	elif len(PMIDquery) >= 5 and len(PMIDquery) < 10:
                dop.write("\t"+str(firstpubdate)+"\t"+str(dateofpub(PMIDquery[-5]))+"\tNA\t"+str(lastpubdate)+"\n")    
		apmid.write("\t"+str(PMIDquery[-1])+"\t"+str(PMIDquery[-5])+"\tNA\t"+str(PMIDquery[0])+"\n")
	elif len(PMIDquery) >= 1 and len(PMIDquery) < 5:                
		dop.write("\t"+str(firstpubdate)+"\tNA\tNA\t"+str(lastpubdate)+"\n")
		apmid.write("\t"+str(PMIDquery[-1])+"\tNA\tNA\t"+str(PMIDquery[0])+"\n")
        else:
                dop.write("\tNA\tNA\tNA\tNA\n")
		apmid.write("\tNA\tNA\tNA\tNA\n")

        if len(NPMIDquery) >= 2:
                firstneuropubdate = dateofpub(NPMIDquery[-1])
                lastneuropubdate = dateofpub(NPMIDquery[0])
               
        elif len(NPMIDquery) == 1:
                lastneuropubdate = dateofpub(NPMIDquery[0])
                firstneuropubdate = lastneuropubdate
               
        else:
                firstneuropubdate = "NA"
		lastneuropubdate = "NA"

        if len(NPMIDquery) >= 10:
                ndop.write("\t"+str(firstneuropubdate)+"\t"+str(dateofpub(NPMIDquery[-5]))+"\t"+str(dateofpub(NPMIDquery[-10]))+"\t"+str(lastneuropubdate)+"\n")
		npmid.write("\t"+str(NPMIDquery[-1])+"\t"+str(NPMIDquery[-5])+"\t"+str(NPMIDquery[-10])+"\t"+str(NPMIDquery[0])+"\n")
        elif len(NPMIDquery) >= 5 and len(NPMIDquery) < 10:
                ndop.write("\t"+str(firstneuropubdate)+"\t"+str(dateofpub(NPMIDquery[-5]))+"\tNA"+"\t"+str(lastneuropubdate)+"\n")
		npmid.write("\t"+str(NPMIDquery[-1])+"\t"+str(NPMIDquery[-5])+"\tNA\t"+str(NPMIDquery[0])+"\n")
        elif len(NPMIDquery) >= 1 and len(NPMIDquery) < 5:
                ndop.write("\t"+str(firstneuropubdate)+"\tNA\tNA"+"\t"+str(lastpubdate)+"\n")
		npmid.write("\t"+str(NPMIDquery[-1])+"\tNA\tNA\t"+str(NPMIDquery[0])+"\n")
        else:
        	ndop.write("\tNA\tNA\tNA\tNA\n")
		npmid.write("\tNA\tNA\tNA\tNA\n")
       
        gene2pubmed.flush()
        dop.flush()
	ndop.flush()
	apmid.flush()
	npmid.flush()
	allpmids.flush()

gene2pubmed.close()
dop.close()
ndop.close()
apmid.close()
npmid.close()
allpmids.close()
