
import sys
import math
from collections import Counter
# total uni =16641



#def unigrams(text_file):
file1 = open(sys.argv[1],"r")
str1 = file1.readlines()
list_unigrams=[]
list_sentence=[]
     ####### sending each sen into list
for i in str1:
    list_sentence.append(i)
    ###### changing into lower
list_sentence=[x.lower().strip().replace("\n","") for x in list_sentence]
total_sen = len(list_sentence)
for li in list_sentence:
    words = li.split(" ") #list of unigrams
    print(words)
    for i in words:
        #val=words.count(i)
        #print(i,"--",val)
        list_unigrams.append(i)

freq=Counter(list_unigrams)
#print(freq.keys())
total_vocab = sum(freq.values())
#print("total sen",total_sen)
#print(sum(list_dict.values()))

#print(total_vocab)
#print(list_dict)

#####frequency table of unigrams in dictionary
     #unique_unigrams = len(words)
    # a = unique_unigrams.keys()
    # b = unique_unigrams.values()
#     total_vocab = len(b) #total no of unique words
#     print(total_vocab)

#     unique_unigrams_freq= {}
#     for i in unique_unigrams.keys():
#         unique_unigrams_freq[i] = unique_unigrams[i]
#         print(i,unique_unigrams[i])
#     print(unique_unigrams_freq)


def unigram_unsmooth(test_file):
####  Unigram smoothing
    file2 = open(test_file,"r")
    str2 = file2.readlines()
    list_sentence2=[]
 ####### sending each sen into list
    for i in str2:
        list_sentence2.append(i)
###### changing into lower
    list_sentence2=[x.lower().strip() for x in list_sentence2]
    for li in list_sentence2:
        print("S =",li)
        words = li.split(" ")
        uni_prob = 0
        for i in words:
            val=freq[i]
            uni_prob = uni_prob+math.log(val/total_vocab,2)
        print("\n unigram unsmoothed probability of",li,"is",uni_prob)


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
    print(dict_bigrams)


#def bigram_unsmooth(sentence):

unigram_unsmooth(sys.argv[3])

#def main():
    #unigram_unsmooth(sys.argv[3])
#    unigrams(sys.argv[1])
#    unigram_unsmooth(sys.argv[3])
    #unigram_smooth(test1.txt)
    #bigrams(sys.argv[1])
    #bigrams(sys.argv[1])
    #print("cmd line arg:",sys.argv[1])


#main()
