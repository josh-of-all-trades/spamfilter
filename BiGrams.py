from collections import defaultdict

def BiGramsTokenizer (string) :
	str = []
	for word in string[1].split():
		if word == 'JSNUM' or word == 'JSNUM3' or word == 'JSNUM6' or word == 'JSMONEY':
			str.append(word)
			if word.isalpha():
				str.append(word.tolower())
	return str

def createVocab (allStrings) :
	dir = {}
	for string in allStrings:
		string = BiGramsTokenizer(string)
		for i in range(len(string)-1):
			word1 = string[i]
			word2 = string[i+1]
			dir[(word1,word2)] += 1
	return dir

def biNaiveBayes (spamham) :
	vocab = defaultdict(int)
	for allStrings in spamham:
		vocab.update(createVocab(allStrings))
	classes = []
	i = 0
	for allStrings in spamham:
		countdict = defaultdict(int, vocab)
		countdict.update(createVocab(allStrings))
		m = 1
		total = len(countdict.keys())
		for ele in countdict:
			countdict[ele] = float(countdict[ele] + m) / float(len(allStrings) + total/m)
			classes.append((i,countdict))
		i += 1
	return classes
		
	
	
		