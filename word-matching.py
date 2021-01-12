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
	combined = count1.copy()
	combined.update(count2)
	counter = 0
	#var: combined is every unique character found in either of them
	for char in combined:
		occurences1 = count1.get(char,0)
		occurences2 = count2.get(char,0)
		counter+= abs(occurences1-occurences2)
	worst_possible = (len(s1)+len(s2))
	counter_score = 1-(counter/worst_possible)
	return counter_score
def positional(s1,s2):
	'''Here, we account for position
		Position indexing and comparison
	For both words:
		find average index of each character, index is not quite desirable because the words may be of different lengths... we'll deal with this
	Now, for each unique character found in either:
		compare the difference of average position in word 1 to word 2

	create list of scores for each character which is the difference between the two average indexs, if one such index does not exist then the score is the length of word

	'''
	character_positions_1 = {}
	for i in range(len(s1)):
		position = (i)/len(s1)
		if(s1[i] in character_positions_1):
			character_positions_1[s1[i]].append(position)
		else:
			character_positions_1[s1[i]] = [position]
	for char in character_positions_1:
		avg = 0
		for index in character_positions_1[char]:
			avg+=index
		avg/=len(character_positions_1[char])
		character_positions_1[char] = avg
	character_positions_2 = {}
	for i in range(len(s2)):
		position = (i)/len(s2)
		if(s2[i] in character_positions_2):
			character_positions_2[s2[i]].append(position)
		else:
			character_positions_2[s2[i]] = [position]
	for char in character_positions_2:
		avg = 0
		for index in character_positions_2[char]:
			avg+=index
		avg/=len(character_positions_2[char])
		character_positions_2[char] = avg
	all_unique_chars = character_positions_1.copy()
	all_unique_chars.update(character_positions_2)
	worst_score_total = len(all_unique_chars)
	counter = 0

	for char in all_unique_chars:
		if(not char in character_positions_1 or not char in character_positions_2):
			counter+=1
		else:
			#worst score possible = 
			counter+=abs(character_positions_2[char]-character_positions_1[char])
	score = 1-(counter/worst_score_total)
	return score
	#return str(counter_score*100)+"%"
def robust(s1,s2):
	ana = anagram(s1,s2)
	pos = positional(s1,s2)
	return ((pos+ana)/2),ana,pos

#testing
def run_test():
	from english_words import english_words_set
	import random
	english_words_set = list(english_words_set)
	amount_of_words = len(english_words_set)
	while True:
		desired_score = input_ = input("Enter desired score, split with coma to specify range")
		desired_score = desired_score.split(",")
		try:
			for i in range(len(desired_score)):
				desired_score[i] = float(desired_score[i])
		except Exception as e:
			#print(e)
			if(robust("exit",input_)>0.7):
				exit()
			else:
				print('You\'ve done it wrong, try again or say "exit".')
				continue
		if(len(desired_score)==1):
			combos = 0
			while True:
				combos+=1
				i1 = random.randint(0,amount_of_words-1)
				i2 = random.randint(0,amount_of_words-1)
				w1 = english_words_set[i1]
				w2 = english_words_set[i2]
				score = robust(w1,w2)
				if(score[0]>=desired_score[0]):
					break
		else:
			combos = 0
			while True:
				combos+=1
				i1 = random.randint(0,amount_of_words-1)
				i2 = random.randint(0,amount_of_words-1)
				w1 = english_words_set[i1]
				w2 = english_words_set[i2]
				score = robust(w1,w2)
				if(score[0]>=desired_score[0] and score[0]<=desired_score[1]):
					break
		result = robust(w1,w2)
		print("anagram check:",result[1])
		print("position check:",result[2])
		print(w1,w2,result[0],"- tested",combos,"combinations")
run_test()


#An earlier attempt.
'''
def positional(s1,s2):
	character_positions_1 = {}
	for i in range(len(s1)):
		if(s1[i] in character_positions_1):
			character_positions_1[s1[i]].append(i)
		else:
			character_positions_1[s1[i]] = [i]
	for char in character_positions_1:
		avg = 0
		for index in character_positions_1[char]:
			avg+=index
		avg/=len(character_positions_1[char])
		character_positions_1[char] = avg
	character_positions_2 = {}
	for i in range(len(s2)):
		if(s2[i] in character_positions_2):
			character_positions_2[s2[i]].append(i)
		else:
			character_positions_2[s2[i]] = [i]
	for char in character_positions_2:
		avg = 0
		for index in character_positions_2[char]:
			avg+=index
		avg/=len(character_positions_2[char])
		character_positions_2[char] = avg
	all_unique_chars = character_positions_1.copy()
	all_unique_chars.update(character_positions_2)
	worst_individual_score = len(all_unique_chars)
	worst_score_total = worst_individual_score**2
	counter = 0
	for char in all_unique_chars:
		if(not char in character_positions_1 or not char in character_positions_2):
			counter+=worst_individual_score
		else:
			#worst score possible = 
			counter+=abs(character_positions_2[char]-character_positions_1[char])
	score = 1-(counter/worst_score_total)
	return score
'''
