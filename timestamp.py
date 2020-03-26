import re

def crawl_timestamps(text):
	'''
		Returns a dictionary of {int: string} where int is the
		number of seconds into the video the song starts and
		the string is the name of the song.
	'''
	
#	for line in text.split("\n"):
#		print("Testing " + line)
#		print(" -> " + str(re.search(r"[0-9]:[0-9][0-9]", line)))
	
	lines = text.split("\n")
	lines = list(filter(lambda line: not re.search(r"[0-9]:[0-9][0-9]", line) == None, lines))
	lines = list(map(lambda line: line.strip(), lines))
	lines = list(map(lambda line: getTitleAndTimestamp(line), lines))
	return lines
	
def getTitleAndTimestamp(text):
	search = getTimeSearch(text)
	
	if search != None:
		time = text[search.span()[0] : search.span()[1]]
		
		remainder = text[search.span()[1] :]
		nameSearch = re.findall(r"[:alpha:]", remainder) # [^([:digit:]|[:punct:]|[:space:])]
		if nameSearch == None:
			return (time, remainder)
		
		name = remainder[nameSearch[0].span()[0] :]
		return(time, name)
		
def getIndexOfFirstAlphaChar(text):
	for i in range(len(text)):
		c = ord(text[i])
		if ord(A) <= c <= ord(Z) or ord('a') <= c <= ord('z'):
			return i
	
def getTimeSearch(text):
	hourSearch = re.search(r"[0-9]?[0-9]:[0-9][0-9]:[0-9][0-9]", text)
	if hourSearch != None:
		return hourSearch
	
	return re.search(r"[0-9]?[0-9]:[0-9][0-9]", text)
		

if __name__ == "__main__":
	print(ord('a'))
	print(ord('z'))
	print(ord('A'))
	print(ord('Z'))
	print(chr(94))
	# TODO: Testing
	print(crawl_timestamps('''
	A trip into the future. 

	Please enjoy and subscribe for more.

	Track List

	0:00 HOME - Flood
	3:33 A.L.I.S.O.N - Overflow
	6:27 Forhill - Searching
	11:25 Skykot - Timeform
	16:37 A.L.I.S.O.N - Renaissance
	20:17 Neydah - Night Sky
	24:31 A.L.I.S.O.N & Rosentwig - Short Circuit
	29:11 ＹＯＵＴＨ ８３ - Euphoria
	33:37 Memorex Memories - Thanks for listening
	01:11:02 A Random Song
	'''))