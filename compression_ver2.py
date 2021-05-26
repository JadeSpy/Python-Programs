






lookup_table = [[],{}] #first is a list for faster lookups while unencrypting
lookup_table[0] = ["hello","hell","beep"]
lookup_table[1] = {  lookup_table[0][index]:index for index in range(len(lookup_table[0]))    }

def populate_lookup_table(file_name):
	lookup_table = [[],{}] #first is a list for faster lookups while unencrypting
	
	with open(file_name,'r') as f:
		line = f.readline()
		line_num = 0
		while(line):
			word = line.strip()
			line_num+=1
			if(len(word)>1): #For one algorithm type, words of length 2 are marginally smaller than two chars
				if(len(lookup_table[0])>65278):
					print("Too many words were uploaded for aliasing!", len(lookup_table[0]),"words are already in use. Failed at",line_number)
					break
				lookup_table[0].append(word)
				lookup_table[0].append(word[0].upper()+word[1:])


			line = f.readline()
	lookup_table[1] = {  lookup_table[0][index]:index for index in range(len(lookup_table[0]))    }
	return lookup_table
lookup_table = populate_lookup_table("most_common_word_list.txt")



empty_node = {}
empty_node["word"] = False
def create_empty_node():
	return empty_node.copy()
#returns a list of tuples, inner tuples will be of the form (starting_index,ending_index,word_residing_in_index)



def recursive_func(look_through:str, current_layer:list, starting_index:int, current_index):
	pass
	

def find_all_occurences(look_through:str,look_for:list):
	#create the lookup structure
	#in each layer, the keys are individual characters (alphabetical or otherwise) that map to another layer. 
	#There is also a key, "word", which indicates whether the characters traversed in the lower branches represent a word.
	#Index 26 (or the 27th index) is a boolean value indicating whether a word has been completed.
	first_layer = create_empty_node()
	for word in look_for:
		current_layer = first_layer
		for char in word:
			current_layer[char] = current_layer.get(char,create_empty_node())
			current_layer = current_layer[char]
		current_layer["word"] = True

	#print(first_layer)
	words_found = []
	i = -1
	while(True):
		i+=1
		if(i>=len(look_through)):
			break


	i = -1
	while(True):
		i+=1
		if(i>=len(look_through)):
			break
		current_layer = first_layer
		longest_word_starting_at_index = (0,-1)
		for i2 in range(i,len(look_through)+1):
			if(i2==len(look_through)):
				current_layer=None
			else:
				current_layer  = current_layer.get(look_through[i2])
			
			if(current_layer==None):#No more word possibilities exist for this set of chars.
				if(longest_word_starting_at_index!=(0,-1)):
					i = longest_word_starting_at_index[1]
					words_found.append(longest_word_starting_at_index)
				break
			if(current_layer["word"]==True):
				if(i2-i>longest_word_starting_at_index[1]-longest_word_starting_at_index[0]):
					longest_word_starting_at_index = (i,i2)
					#print("word found:",longest_word_starting_at_index)
	return words_found
def calculate_compression_strength(word_segments:list,input_text:str):
	last_index = -1
	word_chars = 0
	lone_chars = 0
	temp_segs = [(0,-1)]+word_segments
	for part in temp_segs:
		
		lone_chars+=(part[0]-last_index)-1
		word_chars+=part[1]-part[0]+1
		last_index = part[1]

	lone_chars+=len(input_text)-temp_segs[-1][1]-1
	



	non_compressed_bits_used = len(input_text)*8
	compressed_bits_used = (len(word_segments)*17+lone_chars*9)
	compressed_bits_used += 8-(compressed_bits_used%8) if compressed_bits_used%8!=0 else 0
	compression_strength = compressed_bits_used/non_compressed_bits_used

	compressed_bits_used_ver2 = len(word_segments)*25+lone_chars*8
	compressed_strength_ver2 = compressed_bits_used_ver2/non_compressed_bits_used
	#non_compressed_bits_used_2
	#return {"compressed_type_1":compression_strength,"compress_type_2":compressed_strength_ver2}
	print("Compressed version 1 is:", compression_strength*100,"% the size of the non-compressed version.")
	print("Compressed version 2 is:", compressed_strength_ver2*100,"% the size of the non-compressed version.")
from bitarray import bitarray

def compress(input_text:str):
	if(not input_text.isascii()):
		raise Exception("The input cannot be compressed because it is not an anscii string.")
	word_segments = find_all_occurences(input_text,lookup_table[0])

	
	#for word in word_segments:
	#	print(input_text[word[0]:word[1]+1])
	x = calculate_compression_strength(word_segments,input_text)
	word_segments.append((len(input_text),-1))

	output = bitarray()
	i = -1
	while True:
		i+=1
		if(i>=len(input_text)):
			break
		if(i==word_segments[0][0]):
			output.append(1)
			word = input_text[word_segments[0][0]:word_segments[0][1]+1]
			x = lookup_table[1][word]
			#print(word)
			as_2_bytes = x.to_bytes(2,'big')
			output.frombytes(as_2_bytes)
			i=word_segments[0][1]
			word_segments.pop(0)
		else:
			#print(input_text[i])
			output.append(0)
			output.frombytes(input_text[i].encode())
			

		#loop body
	if(len(output)%8)!=0: 
		for i in range(8-len(output)%8): output.append(0)
	return output.tobytes()
	#in the future, if both algorithms are built, there should be a condition here dictating which to use.
def decompress(input_bytes:bytes):
	if(input_bytes.isascii()):
		raise Exception("Text is already decompressed.")
	input_bitarray = bitarray()
	input_bitarray.frombytes(input_bytes)
	as_text = str()
	i = 0
	while True:
		if(i+8>len(input_bitarray)):
			break
		if(input_bitarray[i]==1):
			as_text+=lookup_table[0][int.from_bytes(input_bitarray[i+1:i+17].tobytes(),'big')]
			i=i+17

		else:
			#print(i)
			#print(input_bitarray[i+1:i+9])
			
			as_text+=input_bitarray[i+1:i+9].tobytes().decode()
			i = i+9
	#print(as_text)
	return as_text




#with open("corp_original.txt") as f: print(decompress(compress(f.read())))
#with open("rom.txt") as f: decompress(compress(f.read()))
#compress("eweeeeeeeeeeee")











def one_num_as_two_bytes(inp:int):#Unefficient, but clear.
	if(inp<0 or inp>65535):
		raise Exception("Input: "+str(inp) +"cannot be represented as two bytes.")
	out = bytearray((0,0))
	div = 1
	for i in range(16):
		div = div*2
		bit = inp%div
		inp-=bit
		#print(int(not bit==0)) representing as a 1 or a 0 
		if(i<=7):
			out[0]+=bit
		else:
			out[1]+=int(bit/256)
	return out
def two_bytes_to_one_num(inp):
	div = 1
	total = 0
	for i in range(8):

		div*=2
		bit= inp[0]%div
		inp[0]-=bit
		total+=bit
	div = 1
	for i in range(8):
		div*=2
		bit = inp[1]%div
		inp[1]-=bit
		total+=256*bit
	return total
'''
def compress(str_to_enc:str,list_of_word_shortcuts:list):
	compressed_value = bytearray()
	places_to_replace = find_all_occurences(str_to_enc,list_of_word_shortcuts[0])
	i = -1
	while(True):
		i+=1
		if(i>=len(str_to_enc)):
			break
		if(len(places_to_replace)!=0 and i==places_to_replace[0][0]):
			word = str_to_enc[places_to_replace[0][0]:places_to_replace[0][1]+1]
			#print(word)
			compressed_value+=one_num_as_two_bytes(list_of_word_shortcuts[1][word]+256)
			i=places_to_replace[0][1]
			places_to_replace.pop(0)
		else:
			as_int = None
			try:
				as_int = ord(str_to_enc[i])
			except:
				raise Exception("This text cannot be compressed, value: "+str_to_enc[i]+" is not supported")
			compressed_value+=one_num_as_two_bytes(as_int)
	return compressed_value
def decompress(data:bytearray,list_of_word_shortcuts:list):
	out = str()
	for raw_i in range(int(len(data)/2)):
		byte1_index = raw_i*2
		byte2_index = byte1_index+1
		byte1 = data[byte1_index]
		byte2 = data[byte2_index]
		num = two_bytes_to_one_num(bytearray((byte1,byte2)))
		if(num<256):
			out+=chr(num)
		else:
			out+=list_of_word_shortcuts[0][num-256]
	return out
'''
def compress_file(file_name,lookup_table):
	with open(file_name,'r') as f:
		text = f.read()
	comp = compress(text)
	with open(file_name,'wb') as f:
		f.write(bytes(comp))
def decompress_file(file_name,lookup_table):
	with open(file_name,'rb') as f:
		comp = f.read()
	text = decompress(comp)
	with open(file_name,'w') as f:
		f.write(text)
#compress_file('test.txt',lookup_table)
def to_anscii(file_name):
	with open(file_name,'r') as f:
		text = f.read()
		if(text.isascii()):
			raise Exception("File is already in anscii")
		text = text.encode("ascii", "ignore").decode()
	with open(file_name,'w') as f:
		f.write(text)
def start_user_interface():
	while(True):
		print("Type /a %file_name% to to convert a file to anscii")
		print("Type /c %file_name% to select and compress a file")
		print("Type /d %file_name% to select and decompress a file")
		print("Type /s %command% to have python evaluate the proceeding text.")
		inp = input("")
		#inp = "/c test.txt"
		parts = inp.split(" ")
		if(parts[0]=='/a'):
			try:
				to_anscii(parts[1])
				print("convert to anscii")
			except Exception as e:
				print(e)

		elif(parts[0]=='/c'):
			try:
				with open(parts[1],'rb') as f:
					starting_size = len(bytearray(f.read()))#conversion to bytearray probably is not necessary
				compress_file(parts[1],lookup_table)
				with open(parts[1],'rb') as f:
					ending_size = len(bytearray(f.read()))
				print("The compressed file is", str((ending_size/starting_size*100))+"% of the original size!")
			except Exception as e:
				print("Error:",e)
		elif(parts[0]=='/d'):
			try:
				decompress_file(parts[1],lookup_table)
				print("decompressed!")
			except Exception as e:
				print("Error:",e)
		elif(parts[0]=='/s'):
			cmd = ""
			for i in range(1,len(parts)):
				cmd+=parts[i]
			try:
				eval(cmd)
			except Exception as e:
				print(e)

		else:
			print("No command begins with:",parts[0])
start_user_interface()
