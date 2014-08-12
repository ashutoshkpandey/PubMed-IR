import re,sys

Argument = []
Argument = sys.argv[1:] 

Filepath = Argument[0] # Mouse Entrez	
Filepath1 = Argument[1] # Human Entrez
Filepath2 = Argument[2] # Rat Entrez
Filepath4 = Argument[3] # Bigfile

try:
    d = file(Filepath).read()
except IOError:                     
    print "The file does not exists."
    sys.exit()

rows = d.split('\n')
NRows = len(rows) # number of genes in the data file

MGeneinfo = {}

for i in range(1,NRows-1):
	rowlist = []
	rowlist = rows[i].split("\t") 
	sub1 = []
	#print rowlist[1]
	sub1 = rowlist[4].split("|")
	sub2 =[]
	sub2 = rowlist[13].split("|")
	
	subrowlist = []
	subrowlist.append(rowlist[2].lower())
	subrowlist.append(rowlist[8].lower())

	for a in sub1+sub2:
		subrowlist.append(a.lower())
		
	MGeneinfo[rowlist[1]] = subrowlist 

try:
    d1 = file(Filepath1).read()
except IOError:                     
    print "The file does not exists."
    sys.exit()

rows1 = d1.split('\n')
NRows1 = len(rows1) # number of genes in the data file

HGeneinfo = {}

for i in range(1,NRows1-1):
	rowlist = []
	rowlist = rows1[i].split("\t") 
	sub1 = []
	sub1 = rowlist[4].split("|")
	sub2 =[]
	sub2 = rowlist[13].split("|")
	
	subrowlist = []
	subrowlist.append(rowlist[2].lower())
	subrowlist.append(rowlist[8].lower())

	for a in sub1+sub2:
		subrowlist.append(a.lower())
		
	HGeneinfo[rowlist[1]] = subrowlist 

try:
    d2 = file(Filepath2).read()
except IOError:                     
    print "The file does not exists."
    sys.exit()

rows2 = d2.split('\n')
NRows2 = len(rows2) # number of genes in the data file

RGeneinfo = {}

for i in range(1,NRows2-1):
	rowlist = []
	rowlist = rows2[i].split("\t") 
	sub1 = []
	sub1 = rowlist[4].split("|")
	sub2 =[]
	sub2 = rowlist[13].split("|")
	
	subrowlist = []
	subrowlist.append(rowlist[2].lower())
	subrowlist.append(rowlist[8].lower())

	for a in sub1+sub2:
		subrowlist.append(a.lower())
		
	RGeneinfo[rowlist[1]] = subrowlist 


try:
    d4 = file(Filepath4).read()
except IOError:                     
    print "The file does not exists."
    sys.exit()

rows4 = d4.split('\n')
NRows4 = len(rows4) # number of genes in the data file

Genewords = {}
Homology = {}

for i in range(0,NRows4-1):
	rowlist = []
	rowlist = rows4[i].split('\t')
        Genewords[rowlist[0]] = []
        Homology[rowlist[0]] = "\t"+rowlist[1]+"\t"+rowlist[2]

        if rowlist[0] in MGeneinfo:
            for m in MGeneinfo[rowlist[0]]:
                if m not in Genewords[rowlist[0]]:
                    Genewords[rowlist[0]].append(m)
            
        if rowlist[1] in HGeneinfo:
            for m in HGeneinfo[rowlist[1]]:
                if m not in Genewords[rowlist[0]]:
                    Genewords[rowlist[0]].append(m)
            
        if rowlist[2] in RGeneinfo:
            for m in RGeneinfo[rowlist[2]]:
                if m not in Genewords[rowlist[0]]:
                    Genewords[rowlist[0]].append(m)
    
nfile = open('HCE_Gene_nomenclature.txt','w')

for c in Genewords.keys():
	nfile.write(str(c))
	nfile.write(str(Homology[c]))

    	for z in Genewords[c]:
        	nfile.write("\t"+str(z))
   	
	nfile.write("\n")
    
nfile.close()
    

    

    
