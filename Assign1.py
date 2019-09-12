

import sys
import itertools
import math
import random
import operator
from collections import Counter

if len(sys.argv)>1:
	training_file=sys.argv[1]
	test_file=sys.argv[2]
	seed_file=sys.argv[3]
else:
   	print 'Please provide the training, test and seed files as arguments to execute this program'


#Reading the contents of the training file

with open(training_file, 'r') as inputFile:
	training_data = inputFile.readlines()


#################### TRAINING DATA PROCESSING #########################

unigrams_final_data=[]
bigrams_final_data=[]
bigrams_source_data=[]
bigrams_list=[]
bigrams=()

'''Counting the number of hashes as the number of lines since we assume every sentence would start with a hash'''

count_hash=len(training_data)
#print 'Number of lines in the file is :', len(training_data)



################ CONSTRUCTION OF UNIGRAMS ###############################

'''Converting all data in the file to lower-case and splitting based on space to store the words Removing the '\n' from each line and also removing the trailing space using strip()'''

for data in training_data:
	data1=data.lower().strip();
	data2=data1.replace("\n","")
	data3=data2.split(" ")
	unigrams_final_data.append(data3)

'''Unigrams is a list with all the words in the file split based on " " '''

vocabulary_repeated=[]
unigrams_table={}

'''Joining list of lists into a single list to get all words into a single list.'''

vocabulary_repeated=list(itertools.chain(*unigrams_final_data))

'''Creating dictionary of (word,count) key value pairs for the entire list or file of words'''

unigram_vocabulary=Counter(vocabulary_repeated)
unigrams_total_frequency=sum(unigram_vocabulary.values())

#print 'Total unigram frequency:', unigrams_total_frequency

bigrams_unigrams_vocabulary=Counter(vocabulary_repeated)

''' Adding the (hash,count) value to the dictionary so that it could be used for bigrams probability calculation'''

bigrams_unigrams_vocabulary['#']=count_hash

#print 'Vocabulary is :',bigrams_vocabulary
#print 'Number of times # occurs is :', bigrams_unigrams_vocabulary['#']


################ BIGRAM PROCESSING ########################################


''' List of lists where each list contains the content of each line '''
for data in training_data:
	data1=data.lower().strip();
	data2=data1.replace("\n","")
	bigrams_final_data.append(data2)

'''Looping through each line and then adding all the bigrams to a universal list '''
for data in bigrams_final_data:
	data1=data.split(" ");
	data1.insert(0,"#")
	for i in range(0, len(data1)-1):
		bigrams=(data1[i],data1[i+1])
		bigrams_source_data.append(bigrams);


bigrams_vocabulary=Counter(bigrams_source_data)

#print bigrams_vocabulary
#print bigrams_vocabulary[('#', 'i')]



################ UNIGRAM PROBABILITY FUNCTION ##########################

def unigrams_prob(sentence):

	prob_value=0
	''' Splitting the given sentence based on space to get the words and filtering/removing the trailing spaces in the sentence or line given to us '''
	data_array=sentence.split(" ")
	data_array = filter(lambda a: a != '', data_array)

	for i in range(0, len(data_array)):

		#print 'word is:',data_array[i]
		#print 'Freq count of word:', unigram_vocabulary[data_array[i]]
		#print 'Total frequency count:',unigrams_total_frequency

		a=unigram_vocabulary[data_array[i]]
		b=unigrams_total_frequency

		if  a == 0:
			return 'undefined'
			break;
		else:
			prob_value += math.log(a/float(b),2)

	return round(prob_value,4)





##################### BIGRAM PROBABILITY FUNCTION ##########################

def bigrams_prob(sentence):

	prob_value=0
	''' Splitting the given sentence based on space to get the words and filtering/removing the trailing spaces in the sentence or line given to us '''

	data_array=sentence.split(" ")
	data_array=filter(lambda a:a!='',data_array)

	#Inserting the start of sentence indicator as #

	data_array.insert(0,'#')

	for i in range(0, len(data_array)-1):


		#print 'word is:',(data_array[i],data_array[i+1])
		#print 'Freq count of word:', bigrams_vocabulary[(data_array[i],data_array[i+1])]
		#print 'Total frequency count:',unigram_vocabulary[data_array[i]]

		a=bigrams_vocabulary[(data_array[i],data_array[i+1])]
		b=bigrams_unigrams_vocabulary[data_array[i]]

		if  a == 0 :
			return 'undefined'
			break;
		else:
			prob_value += math.log(a/float(b),2)

	return round(prob_value,4)



##################### SMOOTHED BIGRAM PROBABILITY FUNCTION ##########################

def smoothed_bigrams_prob(sentence):
	prob_value=0
	data_array=sentence.split(" ")
	data_array=filter(lambda a:a!='',data_array)

	#Inserting the start of sentence indicator as #

	data_array.insert(0,'#')

	for i in range(0, len(data_array)-1):


		#print 'word is:',(data_array[i],data_array[i+1])
		#print 'Freq count of word:', bigrams_vocabulary[(data_array[i],data_array[i+1])]
		#print 'Total frequency count:',unigram_vocabulary[data_array[i]]

		'''Since V is the vocabulary size which refers to the number of unique terms, this count should not include the '#' which we added for computing the bigram probabilities'''

		V=len(unigram_vocabulary.keys())
		#print 'Value of V is :', V
		a=bigrams_vocabulary[(data_array[i],data_array[i+1])] + 1
		b=bigrams_unigrams_vocabulary[data_array[i]] + V

		prob_value += math.log(a/float(b),2)

	return round(prob_value,4)



###################### TEST DATA PROCESSING ###############################

#Variable declarations

cleaned_data=[]


#Reading the contents of the test file

with open(test_file, 'r') as inputFile2:
	test_data = inputFile2.readlines()


for data in test_data:
	data1=data.lower();
	data2=data1.replace("\n","")
	cleaned_data.append(data2)

for i in range(0, len(cleaned_data)):
  print 'S = ',cleaned_data[i]
  print 'Unigrams:logprob(S) = ', unigrams_prob(cleaned_data[i])
  print 'Bigrams:logprob(S) = ', bigrams_prob(cleaned_data[i])
  print 'Smoothed Bigrams:logprob(S) =', smoothed_bigrams_prob(cleaned_data[i])



###################### CREATING an N-gram Language Generator ######################

iteration_counter=0
sentence=""
sent=[]
final_list=[]
x=bigrams_vocabulary.keys()


def n_gram_language_generator(seed_word,seed_counter,sentence_counter,iteration_counter):


	b_seed=[]
	#b_seed_count={}
	b_seed_count=[]
	total_freq=0

	if sentence_counter != 10:
		if iteration_counter==0:
			#print 'True'
			sent.append(seed_word)
		# First I find all the bi-grams which start with seed_word as the first word in the tuple

		for i in range(0, len(x)):
			if x[i][0]==seed_word:
				b_seed.append((x[i][0],x[i][1]))
				total_freq+=bigrams_vocabulary[(x[i][0],x[i][1])]

		#print b_seed
		#print total_freq



		# Bigrams and its corresponding probability values stored in a list of tuples where each tuple is of the form (bigram_tuple, probability_value)
		for i in range(0, len(b_seed)):
			b_seed_count.append((b_seed[i] ,bigrams_vocabulary[b_seed[i]] / float(total_freq)))


		#print 'Seed count with probability values is :',b_seed_count
		sorted_bseed=sorted(b_seed_count)

		#print sum(b_seed_count)

		#sorted_x = sorted(b_seed_count.items(), key=operator.itemgetter(1))

		#print sorted_bseed



		'''If no bigrams could be found for the given word, then stop it there. Using the delimiters to mimic the functionality.
		If the number of possible bigrams for the given seed word is just 1 then use that as the seed for the next iteration. No further processing is required '''
		if len(b_seed) == 0:
			w1='.'
			a=1
		elif(len(b_seed)==1):
			w1=b_seed[0][1]
			#print 'w1 is :', w1
			sent.append(w1);
		else:

			rand_no=random.random()
			cumulative_prob=0
			#print 'Random no generated is :', rand_no
			for i in range(0, len(sorted_bseed)):

				upper_limit=cumulative_prob + sorted_bseed[i][1]
				#print 'Upper limit now is :', upper_limit
				#print 'Lower limit is:', cumulative_prob
				#print 'Corresponding word in array:', sorted_bseed[i]
				if rand_no > cumulative_prob  and rand_no < upper_limit :
					w1=sorted_bseed[i][0][1]
					break
				else:
					cumulative_prob=cumulative_prob + sorted_bseed[i][1]

			#print 'w1 is :', w1
			sent.append(w1) ;

		#print 'Sentence at this point is :', sent

		if (w1 =='!' or w1=='.' or w1 =='?' or len(sent)== 41 or len(b_seed)==0):
			iteration_counter=0
			final_sent = ' '.join(sent)
			final_list.append(final_sent)
			#sentence_counter=sentence_counter + 1
			#print 'Sentence counter is now :', sentence_counter
			'''for i in range(1,len(final_list)+1):
				print 'Sentence %d'  %i, final_list[i-1]'''
			del sent[:]
			#print final_list
			#return final_list;

		else:
			iteration_counter=iteration_counter + 1
			n_gram_language_generator(w1,seed_counter,sentence_counter,iteration_counter)


	else:
		#print 'True'
		start=seed_counter*10
		end=start+10
		i=1
		for k in range(start,end):
				print 'Sentence %d :' %i, final_list[k]
				i=i+1
		#del final_list[:]
		return 1


####################### Seed Data Processing #########################
#Variable declaration area

seed_data=[]
sent_list=[]


#Reading the contents of the seed file

with open(seed_file, 'r') as inputFile3:
	seeds = inputFile3.readlines()

for data in seeds:
	data1=data.replace("\n","")
	data2=data1.lower().strip()
	seed_data.append(data2)

#print seed_data

for i in range(0, len(seed_data)):
	print '******************************************'
	print 'Seed =', seed_data[i]
	print '******************************************'

	for j in range(0, 11):
		n_gram_language_generator(seed_data[i],i,j,0)
