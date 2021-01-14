import math

def anagram(s1,s2):
	'''
	To Find how similar two strings are, first we start by comparing the amount of each character in one string to the other
	how this works is, for every unique character that resides in either of the two strings, we compare the amount of characters in string1 to the amount in string2. The difference is added to a variable of all the other differences found. We also need the worst possible score. This is where there are no shared characters,
	such as "tree" and "bunny". The worst possible score in this case would be 9 because there are 9 characters and zero matches between the two words. It doesn't matter that if the length of the strings are large enough it is impossible not to have matches. Then we divice the actual score by the worst possible score and subtract that from 1
	When this is done, the result is divided by the worst possib
	'''
	count1 = {}
	count2 = {}
	for char in list(s1):
		count1[char] = count1.get(char,0)+1
	for char in list(s2):
		count2[char] = count2.get(char,0)+1
	combined = list(count1.keys())+list(count2.keys())
	counter = 0
	#var: combined is every unique character found in either of them
	#print(combined)
	for char in combined:
		occurences1 = count1.get(char,0)
		occurences2 = count2.get(char,0)
		counter+= abs(occurences1-occurences2)
	worst_possible = (len(s1)+len(s2))
	counter_score = 1-(counter/worst_possible)
	return counter_score
def compute_average_index(word):
	word_length = len(word)
	#maybe try this as a tuple with the current sum and amount of tributes to that average, hehe, I've just realized I've been doing something really stupid for awhile
	#I don't know whether I should have two dictionaries, one for sums and the other for amount of tributes or one dictionary with tuples of length 2 for sum and tributes.
	#'''
	#'''
	storage = {}
	for i in range(word_length):
		position = i#/word_length
		char = word[i]
		#weights[char] = weights.get(char,0)+1
		old_values = storage.get(char, (0,0)) 
		storage[char] = (old_values[0]+position,old_values[1]+1)        #(storage[char][0]+position,storage[char][1]+1)
	for char in storage:
		storage[char] = storage[char][0]/storage[char][1]
	return storage
	'''
	sums = {}
	tributes = {}
	for i in range(word_length):
		position = i/word_length
		char = word[i]

		#weights[char] = weights.get(char,0)+1
		sums[char] = sums.get(char,0)+position
		tributes[char] = tributes.get(char,0)+1
	for char in sums:
		sums[char] = sums[char]/tributes[char]
	return sums
	'''
	#about 50% slower
	'''
	for i in range(len(word)):
		position = i/word_length
		char = word[i]
		weights[char] = weights.get(char,0)+1
		storage[char] = storage.get(char,[])+[position]
		if(char in storage):
			storage[char].append(position)
		else:
			storage[char] = [position]
	#
	for char in storage:
		avg = 0
		for index in storage[char]:
			avg+=index
		avg/=len(storage[char])
		storage[char] = avg
	'''
def positional(s1,s2):
	'''Here, we account for position
		Position indexing and comparison
	For both words:
		find average index of each character, index is not quite desirable because the words may be of different lengths... we'll deal with this
	Now, for each unique character found in either:
		compare the difference of average position in word 1 to word 2

	create list of scores for each character which is the difference between the two average indexs, if one such index does not exist then the score is the length of word

	'''
	#weights = {}#just how many times the character occurs in the two words combined
	character_positions_1 = compute_average_index(s1)
	character_positions_2 = compute_average_index(s2)
	'''
	for i in range(len(s1)):
		position = (i)/len(s1)
		if(s1[i] in character_positions_1):
			character_positions_1[s1[i]].append(position)
		else:
			character_positions_1[s1[i]] = [position]
	for i in range(len(s2)):
		position = (i)/len(s2)
		if(s2[i] in character_positions_2):
			character_positions_2[s2[i]].append(position)
		else:
			character_positions_2[s2[i]] = [position]
	for char in character_positions_1:
		avg = 0
		for index in character_positions_1[char]:
			avg+=index
		avg/=len(character_positions_1[char])
		character_positions_1[char] = avg
	for char in character_positions_2:
		avg = 0
		for index in character_positions_2[char]:
			avg+=index
		avg/=len(character_positions_2[char])
		character_positions_2[char] = avg
	'''
	all_unique_chars = list(character_positions_1.keys())+list(character_positions_2.keys())
	worst_score_total = len(all_unique_chars)*len(all_unique_chars)
	counter = 0
	for char in all_unique_chars:
		if(not char in character_positions_1 or not char in character_positions_2):
			counter+=len(all_unique_chars)
		else:
			#worst score possible =
			if(s2=="dancer"):
				print(character_positions_2[char],character_positions_1[char])
			counter+=abs(character_positions_2[char]-character_positions_1[char])
	score = 1-(counter/worst_score_total)
	return score
	#return str(counter_score*100)+"%"





#from english_words import english_words_set
#english_words = list(english_words_set)

def spellCheck(word,all_words,desired_results):
	word = word.lower()
	results_ordered = [(0,"")]*desired_results
	for compare_word in all_words:
		if(abs(len(word)-len(compare_word))>2):
			continue
		anagram_result = anagram(word,compare_word)
		if(anagram_result<0.5):
			continue
		match_rating = anagram_result*positional(word,compare_word)
		if(match_rating>results_ordered[0][0]):
			start = len(results_ordered)-1
			value_in_transit = (match_rating,compare_word)
			while start>-1:
				if(value_in_transit[0]>results_ordered[start][0]):
					#switch them
					results_ordered[start],value_in_transit = value_in_transit,results_ordered[start]
				start-=1
	results_ordered.reverse()
	return results_ordered

from datetime import datetime
with open("words_copy_paste.txt","r") as f:
	all_words = f.read().strip().split()
start = datetime.now()
x = spellCheck("gargantuane",all_words,13)
print(x)
print(datetime.now()-start)
