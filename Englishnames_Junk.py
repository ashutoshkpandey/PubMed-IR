import re,sys,fileinput

Argument = []
Argument = sys.argv[1:] 

Filepath = Argument[0]
Filepath1 = Argument[1]

English_words = []

for line in fileinput.input([Filepath]):
	line = line.rstrip("\n")
	line = line.rstrip()
    	English_words.append(line)     

#print English_words 

count = 0
count1 = 0

newfile = open("Genes_English_names.txt","w")
newfile1 = open("Genes_Junk_names.txt","w")
newfile2 = open("Genes_short_names.txt","w")

for line1 in fileinput.input([Filepath1]):
        rowlist = []
        rowlist = (line1.rstrip("\n")).split("\t")
	
	newfile.write(str(rowlist[0])+"\t"+str(rowlist[3]))
	newfile1.write(str(rowlist[0])+"\t"+str(rowlist[3]))
	newfile2.write(str(rowlist[0])+"\t"+str(rowlist[3]))

    	for gene in rowlist[3:]:
		if gene in English_words:
			count = count + 1
			newfile.write("\t"+str(gene))

		if re.match("ottmus",gene)  or re.match("mgc",gene) or re.search("rik",gene) or re.match("ensmus",gene) or gene.startswith("rgd") or re.match("mgi",gene) or re.match("mkiaa",gene) or re.match("kiaa",gene) or re.match("ensembl",gene) or re.match("dkfz",gene) or re.match("otthum",gene) or gene == "-":
                        newfile1.write("\t"+str(gene))
			continue

		if len(gene) >=  10:
			continue

		if gene.find("-") != -1:
			if gene.split("-")[0] in English_words and gene.split("-")[1] in English_words:
				count = count + 1
				newfile.write("\t"+str(gene))
				

			if gene.split("-")[0] in English_words and (gene.split("-")[1]).isdigit():
                                count = count + 1
                                newfile.write("\t"+str(gene))
				
			if len(gene.split("-")[0]) <=2 and (gene.split("-")[1]).isdigit():
				count1 = count1 + 1
				newfile2.write("\t"+str(gene))
				continue

		if gene.find(" ") != -1:
			if gene.split(" ")[0] in English_words and gene.split(" ")[1] in English_words:
                        	count = count + 1
                                newfile.write("\t"+str(gene))
			

			if gene.split(" ")[0] in English_words and (gene.split(" ")[1]).isdigit():
                                count = count + 1
                                newfile.write("\t"+str(gene))
				
			
			if len(gene.split(" ")[0]) <=2 and (gene.split(" ")[1]).isdigit():
                        	count1 = count1 + 1
                                newfile2.write("\t"+str(gene))
				continue				

		if gene.isdigit() or isinstance(gene,float) or len(gene) <= 2:
			count1 = count1 + 1
			newfile2.write("\t"+str(gene))
			continue
			
		if len(gene) <=3 and len(gene) >= 1:
			if gene[0] in English_words:
				if gene[1:].isdigit():
					newfile2.write("\t"+str(gene))
					
	newfile.write("\n")
	newfile1.write("\n")
	newfile2.write("\n")

print count
print count1

newfile.close()
newfile1.close()        
newfile2.close()
    
