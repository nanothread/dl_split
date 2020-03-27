from __future__ import unicode_literals

import ffmpeg
from timestamp import crawl_timestamps
import os 

def splitAudioFile(filename, timestamps):
	if not os.path.exists("./tracks"):
		os.makedirs("./tracks")
		
	numTracks = len(timestamps)
	for i in range(numTracks):
		startTime, name = timestamps[i]
		endTime = timestamps[i + 1][0] if i + 1 < len(timestamps) else None
		
		print(f"Making Track ({i}/{numTracks}): {name};")
		trimOne(filename, f"./tracks/{name}.m4a", startTime, endTime)
		
def trimOne(inputFile, outputFile, startTime, endTime):
	inputArgs = {
		"ss": startTime,
		"loglevel": "warning"
	}
	
	if endTime != None:
		inputArgs["t"] = endTime - startTime
	
	stream = ffmpeg.input(inputFile, **inputArgs)
	stream = ffmpeg.output(stream, outputFile)
	ffmpeg.run(stream);
		
if __name__ == "__main__":
	with open("ASTRO - A Synthwave Mix [Chillwave - Retrowave - Synthwave]-XccPsuqAz4E.description", "r") as f:
		times = crawl_timestamps(f.read())
		
#	trimOne("ASTRO - A Synthwave Mix [Chillwave - Retrowave - Synthwave]-XccPsuqAz4E.m4a", "out.m4a", 0, 65)
	splitAudioFile("ASTRO - A Synthwave Mix [Chillwave - Retrowave - Synthwave]-XccPsuqAz4E.m4a", times)