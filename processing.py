from __future__ import unicode_literals

import ffmpeg
from timestamp import crawl_timestamps
import os 

def splitAudioFile(filename, tracks, outputFolder = "./Tracks"):
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)
		
	numTracks = len(tracks)
	for i in range(numTracks):
		track = tracks[i]
		startTime = track.startTime
		name = track.title

		endTime = tracks[i + 1].startTime if i + 1 < numTracks else None
		
		t = track.pretty()
		print(f" - Making Track ({i + 1}/{numTracks}): {t}")
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
	with open("test.description", "r") as f:
		times = crawl_timestamps(f.read(), "artist - track")
		
	splitAudioFile("test.m4a", times)