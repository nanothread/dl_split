from __future__ import unicode_literals

import ffmpeg
from timestamp import crawl_timestamps
import os 

def splitAudioFile(filename, tracks, outputFolder):
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)
		
	numTracks = len(tracks)
	for i in range(numTracks):
		startTime = tracks[i].startTime
		name = tracks[i].title
		endTime = timestamps[i + 1][0] if i + 1 < numTracks else None
		
		print(f" - Making Track ({i + 1}/{numTracks}): {name}")
		trimOne(filename, f"{outputFolder}/{name}.m4a", startTime, endTime)
		
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
		
	splitAudioFile("ASTRO - A Synthwave Mix [Chillwave - Retrowave - Synthwave]-XccPsuqAz4E.m4a", times)