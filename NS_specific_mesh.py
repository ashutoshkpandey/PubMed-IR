import re,sys,fileinput

Argument = []
Argument = sys.argv[1:] 

Filepath = Argument[0]
Filepath1 = Argument[1]

Geneinfo = {}

for line in fileinput.input([Filepath]):
	rowlist = []
    	rowlist = (line.rstrip("\n")).split("\t")
	if int(rowlist[1]) > 100: 
    		Geneinfo[rowlist[0]] = int(rowlist[1])
     

newfile = open("Neuro_specific_keywords.txt","w")

NS = {}

for line1 in fileinput.input([Filepath1]):
        rowlist1 = []
        rowlist1 = (line1.rstrip("\n")).split("\t")

    	if int(rowlist1[1]) >= 95:
		if rowlist1[0] not in Geneinfo:
			NS[rowlist1[0]] = line1

for i in sorted(NS.keys()):
	newfile.write(str(NS[i]))
    	
newfile.close()
        
    

    

    
