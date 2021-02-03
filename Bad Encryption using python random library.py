#Bad Encryption using python random library.py



import random
key_to_char = {
	1:'a',
	2:'b',
	3:'c',
	4:'d',
	5:'e',	
	6:'f',	
	7:'g',		
	8:'h',	
	9:'i',	
	10:'j',
	11:'k',	
	12:'l',		
	13:'m',	
	14:'n',	
	15:'o',	
	16:'p',	
	17:'q',	
	18:'r',	
	19:'s',	
	20:'t',	
	21:'u',	
	22:'v',	
	23:'w',	
	24:'x',	
	25:'y',	
	26:'z',
	27:' ',
}
alphabet_length = len(key_to_char)
def zip2(l1,l2): #I made this just to learn yield, it's entirely useless.
	l1 = tuple(l1)
	l2 = tuple(l2)
	len_1 = len(l1)
	len_2 = len(l2)
	len_min = len_1 if len_1<len_2 else len_2
	for i in range(len_min):
		yield (l1[i],l2[i])

char_to_key = dict(zip2(key_to_char.values(),key_to_char.keys()))



def shift(char,amount):
	new = char_to_key[char]+amount
	while True: #if I actually cared I would use modulus and remainder stuff
		if(new>alphabet_length):
			new-=alphabet_length
		elif(new<1):
			new+=alphabet_length
		else:
			break
	#print(char, "shifted by: ", amount,"units")
	return key_to_char[new]
def crypt(text,seed,encrypt=True):
	if(encrypt==False):
		encrypt=-1
	random.seed(seed)
	text_2 = list(text)
	for i in range(len(text_2)):
		text_2[i]= shift(text_2[i],random.randint(0,26)*encrypt)
	text_3 = ""
	for i in text_2:
		text_3+=str(i)
	return text_3


	




























key = 10005
a = crypt("grandad said that papa ate a cow head",key,True)
print(a)
b = crypt(a,key,False)
print(b)
