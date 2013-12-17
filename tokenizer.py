import sys
import glob
import pickle
from collections import defaultdict
import BiGrams


def tokenizer(filename):
	file = open(filename, 'r')
	viabletext = ""
	lines = file.readline()
	word = lines.split()[0]
	fromsec = ""
	
	while ((not (word == "From:")) and not (word == "Subject:")):
		lines = file.readline()
		word = lines.split()[0]

		
	if (word == "From:"):
		fromsec = lines
		while (not (word == "Subject:")):
			lines = file.readline()
			word = lines.split()[0]
		
		while (not (lines == "")):
			viabletext = viabletext + lines
			lines = file.readline()
		
	elif (word == "Subject:"):
		while (not (lines == "")):
			viabletext = viabletext + lines
			lines = file.readline()
	else :
		print "you dun goofed"

	toks = viabletext.split()
	for i in range(len(toks)):
		if (toks[i].isdigit()):
			if (len(toks[i]) == 6):
				toks[i] = "JSNUM6"
			elif (len(toks[i]) == 3):
				toks[i] = "JSNUM3"
			else:
				toks[i] = "JSNUM"
		if (toks[i][0] == "$"):
			toks[i] = "JSMONEY"
		if (not(toks[i].find("http") == -1) or not(toks[i].find("www") == -1)):
			toks[i] = "JSWEBSITE"
	return (fromsec, toks)

	
def tokenizedirs(dirs):
	print dirs
	classes = []
	for dir in dirs:
		dirclass = []
		files = glob.glob(dir+"/*")
		for file in files:
			print file
			dirclass.append(tokenizer(file))
		
		classes.append((dir, dirclass))
	
	"""for c in classes:
		print "c =", c[0]
		print c[1]
	"""
	return classes
		
	
if __name__ == '__main__':
    print 'argv', sys.argv
    print "Usage:", sys.argv[0], "classdir1 classdir2 [classdir3...] testfile"
    dirs = sys.argv[1:]
    tk = tokenizedirs(dirs)
<<<<<<< HEAD
    print "tk is : ", tk[0][1]
    print "bigrams hurray ", BiGrams.biNaiveBayes(tk[0][1])
=======
    #print "tk is : ", tk
    print tk
    print "bigrams hurray "
    bla = BiGrams.biNaiveBayes(tk[0][1])
    print bla
>>>>>>> b36124d4ccf9ea674a28897fc236b607c18cd076
