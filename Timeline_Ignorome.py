import re,sys,fileinput

Argument = []
Argument = sys.argv[1:] 

Filepath = Argument[0]

Timeinfo = {}

for line in fileinput.input([Filepath]):

	rowlist = []
	if line.startswith("#"):
		continue

    	rowlist = (line.rstrip("\n")).split("\t")

    	Timeinfo[rowlist[0]] = rowlist[3:]
     

newfile = open("Ignorome_timeline.txt","w")

for year in range(1991,2013):
	count1 = 0
	count5 = 0
	count10 = 0

	per1 = 0
	per5 = 0
	per10 = 0

	year = int(year)

	for gene in Timeinfo:
		if Timeinfo[gene][0] != "NA":
			if year >= int(Timeinfo[gene][0]):
				count1 = count1 + 1
		if Timeinfo[gene][1] != "NA":
                        if year >= int(Timeinfo[gene][1]):
                                count5 = count5 + 1
		if Timeinfo[gene][2] != "NA":
                        if year >= int(Timeinfo[gene][2]):
                                count10 = count10 + 1
			
	per1 = float(count1)/648.0
	per5 = float(count5)/648.0
	per10 = float(count10)/648.0

    	newfile.write(str(year)+"\t"+str(count1)+"\t"+str(count5)+"\t"+str(count10)+"\t"+str(per1)+"\t"+str(per5)+"\t"+str(per10)+"\n")
    
newfile.close()
        
    

    

    
