
import sys
from collections import Counter

def unigrams(text_file):
    file1 = open(text_file,"r")
    str = file1.read()
    str = str.lower()
    print(str)
    words = str.split() #list of unigrams

#####frequency table of unigrams in dictionary
    unique_unigrams = Counter(words)
    a = unique_unigrams.keys()
    b = unique_unigrams.values()
    total_vocab = len(b)
    print(total_vocab)

####  Unigram smoothing
    unique_unigrams_probability= {}
    for i in unique_unigrams.keys():
        unique_unigrams_probability[i] = unique_unigrams[i]/total_vocab
    print(unique_unigrams_probability)


def bigrams(text_file):
    file1 = open(text_file,"r")
    str = file1.read()





def main():
    unigrams(sys.argv[1])
    print("cmd line arg:",sys.argv[1])
main()
