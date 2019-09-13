
import sys
import math
from collections import Counter
# total uni =16641



def unigrams(text_file):
    file1 = open(sys.argv[1],"r")
    str1 = file1.readlines()
    list_unigrams=[]
    list_sentence=[]
    dict_uni={}
         ####### sending each sen into list
    for i in str1:
        list_sentence.append(i)
        ###### changing into lower
    list_sentence=[x.lower().strip().replace("\n","") for x in list_sentence]
    total_sen = len(list_sentence)
    for li in list_sentence:
        words = li.split() #list of unigrams
        #print(words)
        for i in words:
            #val=words.count(i)
            #print(i,"--",val)
            list_unigrams.append(i)
            if(i in dict_uni.keys()):
                dict_uni[i]+=1
            elif(i not in dict_uni.keys()):
                dict_uni[i]=1

    #print(dict_uni)
    freq2 = len(dict_uni)
    total_vocab2 = sum(dict_uni.values())
#    print("lines:",freq2,"vocab:",total_vocab2)

    return dict_uni


def unigram_unsmooth(test_file):
####  Unigram smoothing
    probs=[]
    file2 = open(test_file,"r")
    str2 = file2.readlines()
    list_sentence2=[]
    dict_unigram = unigrams(sys.argv[1])
    total_vocab=sum(dict_unigram.values())
 ####### sending each sen into list
    for i in str2:
        list_sentence2.append(i)
###### changing into lower
    list_sentence2=[x.lower().strip() for x in list_sentence2]
    for li in list_sentence2:
        #print("S =",li)
        words = li.split(" ")
        uni_prob = 0
        for i in words:
            val=dict_unigram[i]
            uni_prob = uni_prob+math.log2(val/total_vocab)
        probs.append(uni_prob)
        #print("\n unigram unsmoothed probability of",li,"is",uni_prob)
    return probs

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
        l1=l.split();
        #print(l1)
        for i in range(0, len(l1)-1):
            bigrams=(l1[i],l1[i+1])
            list_bigrams.append(bigrams);

    dict_bigrams=Counter(list_bigrams)
    #print(list_bigrams)
    #print(dict_bigrams)

    return dict_bigrams

def bigram_unsmooth(test_file):
    probs=[]
    file3 = open(test_file,"r")
    str3 = file3.readlines()
    list_sentence3=[]
 ####### sending each sen into list
    for i in str3:
        list_sentence3.append(i)
###### changing into lower
    dict_unigram = unigrams(sys.argv[1])
    total_vocab=sum(dict_unigram.values())

    file_data = open(sys.argv[1],"r").read().split("\n")
    hash_len = len(file_data)



    dict_unigram["#"]=hash_len

    dict_bigrams = bigrams(sys.argv[1])
    #print(dict_bigrams)
    list_sentence3=[x.lower().strip().replace("\n","") for x in list_sentence3]
    list_sentence3 = ["# "+li for li in list_sentence3]


    for l in list_sentence3:
        bi_prob=0
        #print("S=",l)
        w = l.split()
        #print(w)
        for i in range(0,len(w)-1):
#            print("kiran")
            #print(i,"--",i+1)
            numer = dict_bigrams[(w[i],w[i+1])]
            #print("numerator",numer)
            #print("words:",w[i],w[i+1])
            denom = dict_unigram[w[i]]
            #print("denom:",denom)
            if(numer == 0):
                bi_prob="undefined"
                break
            else:
                bi_prob = bi_prob+ math.log(numer/denom,2)
        probs.append(bi_prob)
        #print("bigram unsmooth:",bi_prob)
    return probs

def bigram_smooth(test_file):
    probs=[]
    file3 = open(test_file,"r")
    str3 = file3.readlines()
    list_sentence3=[]
 ####### sending each sen into list
    for i in str3:
        list_sentence3.append(i)
###### changing into lower
    dict_unigram = unigrams(sys.argv[1])
    total_vocab=len(dict_unigram)

    file_data = open(sys.argv[1],"r").read().split("\n")
    hash_len = len(file_data)



    dict_unigram["#"]=hash_len

    dict_bigrams = bigrams(sys.argv[1])
    #print(dict_bigrams)
    list_sentence3=[x.lower().strip().replace("\n","") for x in list_sentence3]
    list_sentence3 = ["# "+li for li in list_sentence3]

    #total_vocab = total_vocab - len(list_sentence3)
    for l in list_sentence3:
        bi_prob=0
        #print("S=",l)
        w = l.split()
        #print(w)
        for i in range(0,len(w)-1):
            numer = dict_bigrams[(w[i],w[i+1])]
            if(w[i] not in dict_unigram):
                bi_prob =bi_prob+math.log2(1/total_vocab)
            elif(w[i+1] not in dict_unigram):
                bi_prob = bi_prob+math.log2(1/(dict_unigram[w[i]]+total_vocab))
            else:
                bi_prob = bi_prob+ math.log2((numer+1)/(dict_unigram[w[i]]+total_vocab))
        probs.append(bi_prob)
        #print("bigram smooth:",bi_prob)
    return probs


def main():
    file_main = open(sys.argv[3],"r").read()
    sent = file_main.split("\n")
    sen_len = len(sent)
    uni_probs_un=unigram_unsmooth(sys.argv[3])
    bi_probs_un=bigram_unsmooth(sys.argv[3])
    bi_probs_sm=bigram_smooth(sys.argv[3])
    for i in range(0,(sen_len)):
        print("S =", sent[i])
        print("\n")
        print("Unsmoothed Unigrams, logprob(S){:+.4f}".format(round(uni_probs_un[i],4)))

        if(bi_probs_un[i]=='undefined'):
            print("Unsmoothed Bigrams, logprob(S)",bi_probs_un[i])
        else:
            print("Unsmoothed Bigrams, logprob(S){:+.4f}".format(bi_probs_un[i]))

        print("Smoothed Bigrams, logprob(S){:+.4f}".format(bi_probs_sm[i]))
        print("\n")

main()
