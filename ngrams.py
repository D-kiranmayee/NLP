
import sys
import math
from collections import Counter
# total uni =16641
import random


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
    list_sentence=[x.lower().strip().replace("\n","") for x in list_sentence]
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

    file_data = open(sys.argv[1],"r").read().strip().split("\n")
    #print(file_data)
    hash_len = len(file_data)
    #print(len(file_data))


    dict_unigram["#"]=hash_len
    #print("hash",hash_len)
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
                #print(w[i])
                #print(numer,"---",denom)
                bi_prob = bi_prob+ math.log2(numer/denom)
                #print(bi_prob)
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

    file_data = open(sys.argv[1],"r").read().strip().split("\n")
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

def lang_generator(bseed,count):
    #bseed='she'
    dict_bigrams = bigrams(sys.argv[1])
    list_words_1=[]
    list_words_2=[]
    prob_bi={}
    counter=0
    sum=0
    w=[]
    #list_keys = dict_bigrams.keys()
    #print(list_keys[0])
    for key in dict_bigrams:
        tup_words=key
        list_words_1.append(tup_words[0])
        list_words_2.append(tup_words[1])
        #if bseed in list_words_1:
            #print("yes")
    #print(list_words_1)
    b_seed = bseed.lower()
    #print("bseed",bseed)
    if b_seed in list_words_1:
        indices = [i for i, x in enumerate(list_words_1) if x == b_seed]

    for ix in indices:
        vals= dict_bigrams[(list_words_1[ix],list_words_2[ix])]
        counter+=vals
    for ix in indices:
        vals= dict_bigrams[(list_words_1[ix],list_words_2[ix])]
        #print(list_words_1[ix],"---",list_words_2[ix],"====",vals)
        freq = vals/counter
        prob_bi.update({(list_words_1[ix],list_words_2[ix]): freq})
        #prob_bi.update({'(list_words_1[ix],list_words_2[ix])','vals'})
#    print(prob_bi)

    #print(counter)
    #print(prob_bi)

    #for x in range(0,10):
    for i in range(0,1):
        rand_num=random.uniform(0,1)
        #print("rand-number",rand_num)
        for key in prob_bi:
            val= prob_bi[key]
            #print(key[1])
            sum+= val
            #print("n----",val)
            #print(w1)
            if(rand_num<sum):
                #w.append(key[0])
                print(key[0],end=" ")
                #print(key[0])
                break
        if(key[0]!='.' and key[0]!='?' and key[0]!='!' and count<10 and bseed!=""):
            count+=1
            #print(key[0],"--",key[1])
            lang_generator(key[1],count)
        else:
            return
    #print()


def seed_test_data():
    file_seed = open(sys.argv[3],"r").read()
    sent = file_seed.split("\n")
    #print(sent)
    for w in sent:
        print("Seed =",w)
        print()
        for i in range(0,10):
            print("Sentence",i+1,":",end=" ")
            lang_generator(w,0)
            print()
        print()

def main():
    file_main = open(sys.argv[3],"r").read()
    sent = file_main.split("\n")
    sen_len = len(sent)
    uni_probs_un=unigram_unsmooth(sys.argv[3])
    bi_probs_un=bigram_unsmooth(sys.argv[3])
    bi_probs_sm=bigram_smooth(sys.argv[3])
    if(sys.argv[2]=='-test'):
        for i in range(0,(sen_len)):
            print("S =", sent[i])
            print()
            print("Unsmoothed Unigrams, logprob(S) = {:.4f}".format(round(uni_probs_un[i],4)))

            if(bi_probs_un[i]=='undefined'):
                print("Unsmoothed Bigrams, logprob(S) = ",bi_probs_un[i])
            else:
                print("Unsmoothed Bigrams, logprob(S) = {:.4f} ".format(bi_probs_un[i]))

            print("Smoothed Bigrams, logprob(S) = {:.4f}".format(bi_probs_sm[i]))
            print()
    elif(sys.argv[2]=='-gen'):
        seed_test_data()
main()
