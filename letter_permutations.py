import math 
def anagram(word): #IDK if there's a strict definition of anagram where it only applies to words and not random characters. 
	out = [] 
	if(len(word)==1): 
		return [word]
	account_for_duplicate_letters = set() 
	for i in range(len(word)): 
		char = word[i]
		if(char in account_for_duplicate_letters):
			continue
		account_for_duplicate_letters.add(char)

		other_chars = word[i+1:] 
		if(i!=0): 
			other_chars+=word[:i] 
		for x in anagram(other_chars): 
			out.append(char+x) 
	return out 
x = anagram("learners")
print(len(x))
