def crawl_timestamps(text):
	'''
		Returns a dictionary of {int: string} where int is the
		number of seconds into the video the song starts and
		the string is the name of the song.
	'''
	
	

if __name__ == "__main__":
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
	'''))