import time
import glob
import random
import sys
import os
import pickle
import math
from collections import defaultdict


class Predictor:
    '''
    Predictor which will do prediction on emails
    '''
    def __init__(self, spamFolder, hamFolder):
        self.__createdAt = time.strftime("%d %b %H:%M:%S", time.gmtime())
        self.__spamFolder = spamFolder
        self.__hamFolder = hamFolder
        self.__spamFrequency = 0

        # do training on spam and ham
        self.__trained = []
        self.__naivedic = {}
        
        [self.__trained, self.__naivedic] = self.__train__()

    def __train__(self):
        '''train model on spam and ham'''
        # the following code is only an naive example,
        # implement your own training methond here
        spamCount = len(glob.glob(self.__spamFolder+'/*'))
        hamCount = len(glob.glob(self.__hamFolder+'/*'))
        #self.__spamFrequency = 1.0*spamCount/(spamCount+hamCount)
        toks = tokenizedirs([self.__spamFolder, self.__hamFolder])
        nb = naivebayes([self.__spamFolder, self.__hamFolder])
        return [biNaiveBayes(toks[:][1]), nb]
        
    def getTrained(self):
    	return self.__trained

    def predict(self, filename):
        '''Take in a filename, return whether this file is spam
        return value:
        True - filename is spam
        False - filename is not spam (is ham)
        '''
        
        unians = classify(self.__naivedic, filename)
        
        # do prediction on filename
        answers = []
        bigrams = bigramify(filename)
        for i in range(len(self.__trained)):
        	#print "i: ", i
        	score = 0
        	for j in range(len(bigrams) - 1):

        		tempscore = self.__trained[i][1][(bigrams[j], bigrams[j+1])]
        		#sorry for this really bad smoothing technique but it's late
        		if tempscore == 0:
        			tempscore = 0.000000000000000001
				#why is it trained[i][1] not trained[i][bigram tuple thing]
        		score = score + math.log(tempscore)
        	answers.append((score, i))
        
        
        
        
        answers.sort()
        answers.reverse()
        
        realanswers = []
        
        for val in unians:
        	if val[1] == self.__spamFolder:
        		for ans in answers:
        			if ans[1] == 0:
        				realanswers.append(((ans[0]+val[0]*2), 0))
        	else:
        		for ans in answers:
        			if ans[1] == 1:
        				realanswers.append(((ans[0]+val[0]*2), 1))
        				
        realanswers.sort()
        realanswers.reverse()
        
        if (realanswers[0][1] == 0):
        	return True
        else :
        	return False


def bigramify(filename):
	toks = tokenizer(filename)
	bigrams = BiGramsTokenizer(toks)
	return bigrams

def tokenizer(filename):
	print filename
	file = open(filename, 'r')
	viabletext = ""
	lines = file.readline()
	word = lines.split()[0]
	
	while (not (word == "Subject:")):
		lines = file.readline()
		word = lines.split()[0]	
	if (word == "Subject:"):
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
	return classes
		
		
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
	#print "spam ham in beNaiveBaives", spamham
	vocab = defaultdict(int)
	for allStrings in spamham:
		vocab.update(createVocab(allStrings))
	classes = []
	i = 0
	#print "vocab", vocab
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
	
def naivebayes (dirs):
    """Train and return a naive Bayes classifier.  
    The datastructure returned is an array of tuples, one tuple per
    class; each tuple contains the class name (same as dir name)
    and the multinomial distribution over words associated with
    the class"""
    # Set up the vocabulary for all files in the training set
    vocab = defaultdict(int)

    for dir in dirs:    
    	
        vocab.update(files2countdict(glob.glob(dir+"/*")))
    # Set all counts to 0
    vocab = defaultdict(int, zip(vocab.iterkeys(), [0 for i in vocab.values()]))
    
    #this is the tokenizer that I was working on implementing however
    #I noticed that when I removed it I had a better percentage correct so I 
    #decided to leave it out
    
    classes = []
    for dir in dirs:
        print dir
        # Initialize to zero counts   
        countdict = defaultdict(int, vocab)
        # Add in counts from this class
        countdict.update(files2countdict(glob.glob(dir+"/*")))

       
        #***
        # Here turn the "countdict" dictionary of word counts into
        # into a dictionary of smoothed word probabilities
        #***
        
        for key in countdict:
        	countdict[key] = (countdict[key] + 1.0) / (len(dirs) + len(vocab))
        
        classes.append((dir,countdict))
    return classes

def classify (classes, filename):
    """Given a trained naive Bayes classifier returned by naivebayes(), and
    the filename of a test document, d, return an array of tuples, each
    containing a class label; the array is sorted by log-probability 
    of the class, log p(c|d)"""
    answers = []
    #print 'Classifying', filename
    for c in classes:
        score = 0
        #***
        # Here, compute the naive bayes score for a file for a given class by:
        # 1. Reading in each word, and converting it to lower case (see code below)
        f = open(filename, 'r')
        str = f.read().lower()
        tok = str.split()
        # 2. Adding  the log probability of that word for that class
        #***
        for el in tok:
        	score = score + math.log(c[1].get(el,1))
        	
        answers.append((score,c[0]))
        f.close()
    answers.sort()
    answers.reverse()
    return answers

def files2countdict (files):
    """Given an array of filenames, return a dictionary with keys
    being the space-separated, lower-cased words, and the values being
    the number of times that word occurred in the files."""
    d = defaultdict(int)
    for file in files:
        for word in open(file).read().split():
            d[word.lower()] += 1
    return d

		
if __name__ == '__main__':
	print "time to train"
	if not (len(sys.argv) == 4):
		print "incorrect arguments given"
	else:
		if (os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2])):
			print "training"
			#predictor = Predictor(sys.argv[1], sys.argv[2])
			#files = glob.glob(sys.argv[3]+"/*")
			#for file in files:
			#	print predictor.predict(file)
			# save to pickle
			#print 'saving predictor to pickle'
			#pickle.dump(predictor, open("predictor.pickle", 'w'))
		else:
			print "you can't train on this :( sorry qq"