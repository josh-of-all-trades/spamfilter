import sys
import glob
import pickle

def tokenizer(filename):
	file = open(filename, 'r')
	viabletext = ""
	lines = file.readline()
	word = lines.split()[0]
	
	while ((not (word == "From:")) and not (word == "Subject:")):
		lines = file.readline()
		word = lines.split()[0]

		
	if (word == "From:"):
		viabletext = viabletext + lines
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
	return toks

	
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
	
	for c in classes:
		print "c =", c[0]
		print c[1]
	
if __name__ == '__main__':
    print 'argv', sys.argv
    print "Usage:", sys.argv[0], "classdir1 classdir2 [classdir3...] testfile"
    dirs = sys.argv[1:]
    tokenizedirs(dirs)