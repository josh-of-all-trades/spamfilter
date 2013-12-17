from collections import defaultdict

def BiGramsTokenizer (string) :
	str = []
	for word in string:
		#print "word is ", word
		if word == 'JSNUM' or word == 'JSNUM3' or word == 'JSNUM6' or word == 'JSMONEY':
			str.append(word)
		if word.isalpha():
			str.append(word.lower())
	#print "printing str ", str
	return str

def createVocab (allStrings) :
	dir = {}
	for string in allStrings:
		#print "string ", string
		string = BiGramsTokenizer(string)
		for i in range(len(string)-1):
			word1 = string[i]
			word2 = string[i+1]
			#print word1, word2
			if (word1, word2) in dir:
				dir[(word1,word2)] += 1
			else :
				dir[(word1,word2)] = 0
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
			#print "printing countdict ", countdict[ele]
		classes.append((i,countdict))
		i += 1
	return classes
		
	
	
		