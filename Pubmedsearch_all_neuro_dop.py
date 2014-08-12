import urllib
import sys
import re
from sets import Set
import time
from operator import itemgetter

Argument = []
Argument = sys.argv[1:]  # Reading the arguments

Filepath = Argument[0] # Nomenclature dictionary
Filepath_stop = Argument[1] # StopPMIDs
Filepath_english = Argument[2] # English words
Filepath_amb = Argument[3] # Ambiguous acronyms
Filepath_keywords = Argument[4] # Gene specific tags

Genenum = Argument[5]

try:
	d = file(Filepath).read()
except IOError:                     
	print "The file does not exists."
	sys.exit()

rows = d.split('\n')
NRows = len(rows)

try:
	d1 = file(Filepath_stop).read()
except IOError:                     
	print "The file does not exists."
	sys.exit()

rows1 = d1.split('\n')
NRows1 = len(rows1)

Stoppmids = []
for stoppmid in rows1:
	stoppmid.lstrip()
	Stoppmids.append(stoppmid)
	
try:
	d2 = file(Filepath_english).read()
except IOError:                     
	print "The file does not exists."
	sys.exit()

rows2 = d2.split('\n')
NRows2 = len(rows2)

Englishwords = []
for word in rows2:
	word = word.lstrip()
	Englishwords.append(word.lower())
	
try:
	d3 = file(Filepath_amb).read()
except IOError:                     
	print "The file does not exists."
	sys.exit()

rows3 = d3.split('\n')
Ambiwords = []
for aword in rows3:
	aword = aword.lstrip()
	Ambiwords.append(aword.lower())

try:
	d4 = file(Filepath_keywords).read()
except IOError:                     
	print "The file does not exists."
	sys.exit()

rows4 = d4.split('\n')
IDgenetag = {}
for geneidn in rows4:
	tag = ""
	listg = []
	listg = geneidn.split("\t")
	if listg[0] not in IDgenetag:
		IDgenetag[listg[0]] = listg[1]
		
def isTrue(x):
	if x: 
		return 1
	return 0

def remove_html_tags(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)

def is_not_number(s):
    try:
        float(s)
        return False
    except ValueError:
        return True

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
            
def strip(x):
    return x.lstrip().rstrip()
    
def Differencen(list1,list2):
	lista = []
	listb = []
	listn = []
	lista = list1
	listb = list2
	
	for a in lista:
		if a not in listb:
			if a not in listn:
				listn.append(a)
	return listn

def pubmedcheck(genearray,geneidf1):
	PMIDSquery = []
	query = ""
	ambi = ""

	for name in genearray:
		if name in Ambiwords or name in Ambiwords2:
			if geneidf1 in IDgenetag:
				if ambi == "":
					ambi = "(\""+str(name)+"\"[TIAB] AND "+"\""+str(IDgenetag[geneidf1])+"\"[TIAB]) OR "
				else:
					ambi =  ambi + "(\""+str(name)+"\"[TIAB] AND "+"\""+str(IDgenetag[geneidf1])+"\"[TIAB]) OR "
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

	url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="+query+"+ AND+ (Mus+Musculus OR Homo+Sapiens OR Rattus+Norvegicus)&retmax=100000"
	#print url

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
		DifferenceSetP = Differencen(PMIDarray,Stoppmids)

		PMIDSquery = PMIDSquery + DifferenceSetP
		
	fp.close()
	return PMIDSquery

def entrezcheck(geneid):
	
	PMIDSquery = []	
	if geneid == "":
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

		DifferenceSet = Set([])
		DifferenceSet = Set(Entrezarray[1:]).difference(Set(Stoppmids))
		
		PMIDSquery = PMIDSquery + list(DifferenceSet)
	
	fp.close()
	return PMIDSquery
 
def newpubmedcheck(genearray,geneidf2):

	PMIDSquery = []
	ambi = ""
	query = ""
	
	for name in genearray:
		if name in Ambiwords or name in Ambiwords2:
			if geneidf2 in IDgenetag:
				if ambi == "":
					ambi = "(\""+str(name)+"\"[TIAB] AND "+"\""+str(IDgenetag[geneidf2])+"\"[TIAB]) OR "
				else:
					ambi =  ambi + "(\""+str(name)+"\"[TIAB] AND "+"\""+str(IDgenetag[geneidf2])+"\"[TIAB]) OR "
				continue
		
		test = ""
		test = name.replace("-","")
		if len(test)>2:
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
	
	#print query

	url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="+query+"+ AND (Brain[TIAB] OR Brain's[TIAB] OR Nervous[TIAB] OR Neur*[TIAB] OR Neuro*[TIAB] OR Hippocamp*[TIAB] OR Cerebr*[TIAB] OR Synap*[TIAB] OR Cerebellum[TIAB] OR Medulla[TIAB] OR Hypothalamus[TIAB] OR Pituitary[TIAB] OR Thalamus*[TIAB] OR Neuron*[TIAB] OR Glial[TIAB] OR Nerve[TIAB] OR Cortex[TIAB] OR Amygdala[TIAB] OR Purkinje[TIAB] OR Substantia+Nigra[TIAB] OR Axon*[TIAB] OR Striatum[TIAB] OR Dendrit*[TIAB] OR neurodegenerati*[TIAB] OR Alzheimer*[TIAB] OR Autism[TIAB] OR Myelin[TIAB] OR Astrocyte*[TIAB] OR Oligodendrocytes[TIAB] OR Glial[TIAB] OR CNS[TIAB] OR Parkinson*[TIAB] OR Pallidum[TIAB] OR Seizure*[TIAB] OR Epilepsy[TIAB] OR Motor[TIAB] OR Cerebovascular[TIAB] OR Huntington*[TIAB] OR Aphasia[TIAB] OR Narcolepsy[TIAB] OR Neuromuscular[TIAB])+ AND (Mus+Musculus OR Homo+Sapiens OR Rattus+Norvegicus)&retmax=100000"
	#print url	
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
		DifferenceSetP = Differencen(PMIDarray,Stoppmids)
		PMIDSquery = PMIDSquery + DifferenceSetP

	fp.close()
	return PMIDSquery
	
def selectDOP(data):
    year = ""
    rows = []
    rows = data.split('\n')
    for row in rows:
        if re.match("<Item Name=\"pubmed\" Type=\"Date\">",strip(row)):
            year = remove_html_tags(strip(row)).split("/")[0]
    return year
    
def dateofpub(Pubid):
	Pubmid = ""
	Pubmid = Pubid
	DateofPub = ""
	
	fp = urllib.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id="+Pubmid+"+&retmode=xml")
	time.sleep(.30)
	s = fp.read(8192)
	
	DateofPub = selectDOP(s)
	fp.close()
	
	return DateofPub
	
ambifile =  open("KGN_gids-ambiwords1.txt", "w")
Geneinfo2d3 = []

p = re.compile(r'^\d+')
q = re.compile(r'\d+$')

Ambiwords2 = []

for i in range(0,NRows):
	rowlist = []
	nrowlist = []
	rowlist = rows[i].split("\t")
	nrowlist.append(rowlist[0])
	nrowlist.append(rowlist[1])
	nrowlist.append(rowlist[2])
	
	for a in rowlist[3:]:
		if a == "-" or a == " ":
			continue
		
		subrowlist = []
		subrowlist = a.split("|")
		for b in subrowlist:
			if b.lower() not in nrowlist and b.lower() != "-" and b.find(":") == -1 and not b.isdigit():
				# Filtering1
				test1 = ""
				test2 = ""
				test1 = b.replace("-","")
				test2 = test1.replace(" ","")
					
				#Filtering2
				if b.lower() not in Englishwords and len(test2) > 2 and is_not_number(b):
					if b.find("-") != -1 or b.find(" ") != -1:
						if len(p.sub('',test2)) == 2 or len(q.sub('',test2)) == 2 and b.find("-") != -1:
							Ambiwords2.append(b.lower())
						if len(p.sub('',test2)) == 2 or len(q.sub('',test2)) == 2 and b.find(" ") != -1:
							Ambiwords2.append(b.lower())
						x = []
						x = re.findall(r"\d+",b)
						if x != []:
							if int(x[-1]) <= 10:	
								tempn = []
								temps = []
								tempn = b.split("-")
								temps = b.split(" ")
								
								if len(temps) > 2:
									nrowlist.append(b.lower())
									continue
								
								#print tempn
								#print temps
								
								#Filtering 3 
								if not tempn[-1].isdigit() or tempn[0].lower() not in Englishwords:
									nrowlist.append(b.lower())
								else:
									ambifile.write(str(rowlist[0]+"\t"+str(b))+"\n")
					
									
								if not temps[-1].isdigit() or temps[0].lower() not in Englishwords :
									nrowlist.append(b.lower())
								else:
									ambifile.write(str(rowlist[0]+"\t"+str(b))+"\n")
							else:
								nrowlist.append(b.lower())
							
						else:
							nrowlist.append(b.lower())
						
					else:
						nrowlist.append(b.lower())
					
				else:
					ambifile.write(str(rowlist[0]+"\t"+str(b))+"\n")
	
	Geneinfo2d3.append(nrowlist)
	#print nrowlist

#print Ambiwords2

Geneinfo2d4 = [] 
    
for m in range(0,len(Geneinfo2d3)):
	subarray = []
	subarray.append(Geneinfo2d3[m][0])
	subarray.append(Geneinfo2d3[m][1])
	subarray.append(Geneinfo2d3[m][2])
	for n in range(3,len(Geneinfo2d3[m])):
		if Geneinfo2d3[m][n].lower() not in subarray:
			subarray.append(Geneinfo2d3[m][n].lower())
	#print subarray
	Geneinfo2d4.append(subarray)    

maxfmeanfile = open('KGN_HSE_GeneID,G2P,Pubmed-All1.txt','a') 
litpub = open('KGN_First-Last_publ1.txt','a')
firstpubmedid = open("KGN_pubmedid_first1.txt","a")
diffignorome =  open("KGN_diff-ignorome1.txt","a")

Status = "No"

#print Ambiwords2
for genearray1 in Geneinfo2d4:
	GeneID = ""
	GeneIDh = ""
	GeneIDr = ""
	
	if len(genearray1) != 0 and genearray1[0] != "-":
		GeneID = genearray1[0]
		if GeneID == Genenum:
			Status = "Yes"
			
	if Status == "No": 
		continue

	print GeneID
		
	if len(genearray1[3:]) <= 0:
		nogeneinfo.write(str(GeneID)+"\n")
		maxfmeanfile.write(str(GeneID)+"\t\t\t\t\t\t\n")
		maxfmeanfile.flush()
		continue

	PMIDquery = []
	Entrezarray = []
	NPMIDquery = []
	HumanG2P = []
	RatG2P = []
	
	GeneIDh = genearray1[1]
	GeneIDr = genearray1[2]
	#print genearray1[3:]
	
	firstpubdate = ""
	firstneuropubdate = ""
	lastpubdate = ""
	lastneuropubdate = ""
	
	diffignorome.write(str(GeneID))

	Entrezarray = entrezcheck(GeneID)
	HumanG2P = entrezcheck(GeneIDh)
	RatG2P = entrezcheck(GeneIDr)
	
	PMIDquery = pubmedcheck(genearray1[3:],GeneID)
	NPMIDquery = newpubmedcheck(genearray1[3:],GeneID)
	
	if len(PMIDquery) >= 2:
		firstpubdate = dateofpub(PMIDquery[-1])
		lastpubdate = dateofpub(PMIDquery[0])
	elif len(PMIDquery) == 1:
		lastpubdate = dateofpub(PMIDquery[0])
		firstpubdate = lastpubdate
	else:
		pass
		
	if len(NPMIDquery) >= 2:
		firstneuropubdate = dateofpub(NPMIDquery[-1])
		lastneuropubdate = dateofpub(NPMIDquery[0])
		firstpubmedid.write(str(GeneID)+"\t"+str(NPMIDquery[-1])+"\n")
	
	elif len(NPMIDquery) == 1:
		lastneuropubdate = dateofpub(NPMIDquery[0])
		firstneuropubdate = lastneuropubdate
		firstpubmedid.write(str(GeneID)+"\t"+str(NPMIDquery[-1])+"\n")
		
	else:
		pass
	
	if len(NPMIDquery) >= 15:
		diffignorome.write("\t"+str(firstneuropubdate)+"\t"+str(dateofpub(NPMIDquery[-5]))+"\t"+str(dateofpub(NPMIDquery[-10]))+"\t"+str(dateofpub(NPMIDquery[-15])))
	elif len(NPMIDquery) >= 10 and len(NPMIDquery) < 15:
		diffignorome.write("\t"+str(firstneuropubdate)+"\t"+str(dateofpub(NPMIDquery[-5]))+"\t"+str(dateofpub(NPMIDquery[-10])))
	elif len(NPMIDquery) >= 5 and len(NPMIDquery) < 10:
		diffignorome.write("\t"+str(firstneuropubdate)+"\t"+str(dateofpub(NPMIDquery[-5])))
	elif len(NPMIDquery) >= 1 and len(NPMIDquery) < 5:
		diffignorome.write("\t"+str(firstneuropubdate))
	else:
		pass
			
	maxfmeanfile.write(str(GeneID)+"\t"+str(len(Entrezarray))+"\t"+str(len(HumanG2P))+"\t"+str(len(RatG2P))+"\t"+str(len(PMIDquery))+"\t"+str(len(NPMIDquery))+"\n")
	diffignorome.write("\n")
	maxfmeanfile.flush()
	diffignorome.flush()
		
	litpub.write(str(GeneID)+"\t"+str(firstpubdate)+"\t"+str(lastpubdate)+"\t"+str(firstneuropubdate)+"\t"+str(lastneuropubdate)+"\n")
	litpub.flush()

maxfmeanfile.close()
litpub.close()
ambifile.close()
firstpubmedid.close()
diffignorome.close()

