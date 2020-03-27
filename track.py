import re

class Track:
	def __init__(self, title, artist, startTime):
		self.title = title
		self.artist = artist
		self.startTime = startTime
		
	def filename(self):
		return self.title + ".m4a"
		
	def __repr__(self):
		return str(self)
		
	def __str__(self):
		artist = "<Not Found>" if self.artist == None else self.artist
		return f"Title: {self.title}; Artist: {artist}; Starting at: {self.startTime}s"
		
	def pretty(self):
		return f"{self.title} by {self.artist}" if self.artist != None else self.title

def crawl_timestamps(text, descriptionFormat):
	'''
		Returns a list of Track instances in order of appearance.
	'''
	
	lines = text.split("\n")
	lines = list(filter(lambda line: not re.search(r"[0-9]:[0-9][0-9]", line) == None, lines))
	lines = list(map(lambda line: line.strip(), lines))
	lines = list(map(lambda line: getTitleAndTimestamp(line), lines))
	lines = list(map(lambda line: makeTrack(line[1], descriptionFormat, getSeconds(line[0])), lines))
	
	return lines
	
def getTitleAndTimestamp(text):
	search = getTimeSearch(text)
	
	if search != None:
		time = text[search.span()[0] : search.span()[1]]
		
		remainder = text[search.span()[1] + 1:]
		i = getIndexOfFirstAlphaChar(remainder)
		if i == None:
			return (time, text)
		else:
			return (time, remainder[i:])
		
		
def getIndexOfFirstAlphaChar(text):
	for i in range(len(text)):
		c = ord(text[i])
		if ord('A') <= c <= ord('Z') or ord('a') <= c <= ord('z') or ord('0') <= c <= ord('9'):
			return i
	
def getTimeSearch(text):
	hourSearch = re.search(r"[0-9]?[0-9]:[0-9][0-9]:[0-9][0-9]", text)
	if hourSearch != None:
		return hourSearch
	
	return re.search(r"[0-9]?[0-9]:[0-9][0-9]", text)
		

def getSeconds(time):
	return sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":"))))

def makeTrack(description, descriptionFormat, seconds):
	'''
		Format is 'artist - track' or 'track | artist', etc.
	'''
	if descriptionFormat == None:
		return Track(description, None, seconds)
	
	artistSearch = re.search(r"artist", descriptionFormat)
	try:
		if artistSearch.start() == 0:
			separator = descriptionFormat.split("artist")[1].split("track")[0]
			components = description.split(separator)
			artist = components[0]
			track = components[1]
		else:
			separator = descriptionFormat.split("track")[1].split("artist")[0]
			components = description.split(separator)
			track = components[0]
			artist = components[1]
	except:
		artist = None
		track = description
		
	return Track(track, artist, seconds)	

if __name__ == "__main__":
	with open('test.description', 'r') as f:
		description = f.read()
		
	times = crawl_timestamps(description, "artist - track")
	print(times)
	print(times[3].pretty())
	
#	print(crawl_timestamps('''
#	A trip into the future. 
#
#	Please enjoy and subscribe for more.
#
#	Track List
#
#	0:00 HOME - Flood
#	3:33 A.L.I.S.O.N - Overflow
#	6:27 Forhill - Searching
#	11:25 Skykot - Timeform
#	16:37 A.L.I.S.O.N - Renaissance
#	20:17 Neydah - Night Sky
#	24:31 A.L.I.S.O.N & Rosentwig - Short Circuit
#	29:11 ＹＯＵＴＨ ８３ - Euphoria
#	33:37 Memorex Memories - Thanks for listening
#	01:11:02 A Random Song
#	''', "artist - track"))#"artist - track"))