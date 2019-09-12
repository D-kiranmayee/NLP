
import sys
from collections import Counter

def unigrams(train_file):
    file1 = open(train_file,"r")
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
    str1 = file1.readlines()
    list_sentence = []
    list_bigrams=[]
     ####### sending each sen into list
    for i in str1:
        list_sentence.append(i)

    ###### changing into lower
    list_sentence=[x.lower().strip() for x in list_sentence]
    ###### adding # to start of each sentence
    list_sentence = ["# "+li for li in list_sentence]


    for l in list_sentence:
        l1=l.split(" ");
        print(l1)
        for i in range(0, len(l1)-1):
            bigrams=(l1[i],l1[i+1])
            list_bigrams.append(bigrams);


    dict_bigrams=Counter(list_bigrams)
    #print(list_bigrams)
    #print(dict_bigrams)

def main():
#    unigrams(sys.argv[1])
    #bigrams(sys.argv[1])
    bigrams(sys.argv[1])
    print("cmd line arg:",sys.argv[1])
main()
