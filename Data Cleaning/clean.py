from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string


with open('TripAdviser Reviews.csv','r') as inFile, open('outputFile.csv','w') as outFile:
	for line in inFile.readlines():
	    print(" ".join([word for word in line.lower().translate(str.maketrans('', '', string.punctuation)).split()
        	if len(word) >=4 and word not in stopwords.words('english')]), file=outFile)
