from __future__ import unicode_literals

import ffmpeg
import os 
from track import crawl_timestamps
from configure import configure_tracks

def splitAudioFile(filename, tracks, outputFolder = "./Tracks"):
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)
		
	numTracks = len(tracks)
	for i in range(numTracks):
		track = tracks[i]
		startTime = track.startTime
		name = track.filename()

		endTime = tracks[i + 1].startTime if i + 1 < numTracks else None
		
		t = track.pretty()
		print(f" - Making Track ({i + 1}/{numTracks}): {t}")
		trimOne(filename, f"{outputFolder}/{name}", startTime, endTime)
		
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
		
		
def splitUpTrack(track, desc_path, desc_format, outputFolder, metadata):
	with open(desc_path, "r") as f:
		description = f.read()
		
		tracks = crawl_timestamps(description, desc_format)
		
		print()
		for t in tracks:
			print(t.pretty())
		
		if metadata["artist"] == None:
			i = input("\nAre these track names & artists correct? [y/n, f=flip] ")
				
			if i == 'f':
				print("Ok, flipping artists and tracks for new tracklist:\n")
				separator = desc_format.split("artist")[1].split("track")[0]
				comps = desc_format.split(separator)
				rev = comps[1] + separator + comps[0]
				tracks = crawl_timestamps(description, rev)
				for t in tracks:
					print(t.pretty())
			elif i != 'y':
				print("Ok, ignoring artists...")
				tracks = crawl_timestamps(description, None)
			
		outputFolder = outputFolder if outputFolder != None else "./Tracks"
		
		print()
		splitAudioFile(track, tracks, outputFolder)

		print("\n=> Configuring Tracks...\n")
		configure_tracks(outputFolder, tracks, metadata)
		
		print("\n=> Done! Your tracks are at " + outputFolder)
		

if __name__ == "__main__":
	track = "test resources/test.m4a"
	description = "test resources/test.description"
	thumbnail = "test resources/test.jpg"
	
	desc_format = "artist - title"
	outputFolder = "./Tracks"
		
	metadata = {
		"thumbnail": thumbnail,
		"artist": None,
		"album": None
	}
		
	splitUpTrack(track, description, desc_format, outputFolder, metadata)