import math
import sys
import glob
import pickle
from collections import defaultdict

def separatefromsection(dirs):

	for dir in dirs:    	
        vocab.update(files2countemails(dir)
    	# Set all counts to 0
   	 	vocab = defaultdict(int, zip(vocab.iterkeys(), [0 for i in vocab.values()]))
	
	classes = []
	for dir in dirs:
		tokendic = defaultdict(int, vocab)
		
		
	
def files2countemails(dir):
	tokenizedtext = tokenizedirs(dir)
	email = tokenizedtext[1][0]
	#separate everything before and after the @ sign
	toks = email.split('@')
	fronttoks = toks[0].split()
	username = fronttoks[-1]
	backtoks = toks[1].split('.')
	website = backtoks[0]
	extension = backtoks[1]
	d = defaultdict(int)
	
	