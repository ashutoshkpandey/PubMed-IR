import re,sys,fileinput

Argument = []
Argument = sys.argv[1:] 

Filepath = Argument[0]
Filepath_eng = Argument[1]

English_words = []

for line in fileinput.input([Filepath_eng]):
	English_words.append(line.rstrip("\r\n"))

Meshfreq = {}

regex = re.compile(r'[\s+,/]')

for line in fileinput.input([Filepath]):
	
	if not line.startswith("MH  -") and not line.startswith("TI  -"):
		continue

	line = (line[6:]).rstrip("\n")
	
	rowlist = []
    	rowlist = regex.split(line)
	rowlist = [(i.lstrip()).rstrip() for i in rowlist]

	for term in rowlist:
		if term.lower() not in English_words and not term.startswith("*") and len(term) >= 5 and term.isalpha():
			if term.lower() not in Meshfreq:
				Meshfreq[term.lower()] = 1
			else:
				Meshfreq[term.lower()] = Meshfreq[term.lower()] + 1		
		
newfile = open("Mesh_keywords_short.txt","w")

for term in sorted(Meshfreq, key=Meshfreq.get, reverse=True):
	newfile.write(str(term)+"\t"+str(Meshfreq[term])+"\n")
newfile.close()

