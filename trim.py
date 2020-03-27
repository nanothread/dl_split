from __future__ import unicode_literals

import argparse
import ffmpeg
from track import crawl_timestamps
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
		
		
def splitUpTrack(track, desc_path, desc_format, outputFolder):
	with open(desc_path, "r") as f:
		description = f.read()
		
		tracks = crawl_timestamps(description, desc_format)
		
		print()
		for t in tracks:
			print(t.pretty())
		
		use_format = input("\nAre these track names & artists correct? [y/n]") == 'y'
			
		if not use_format:
			print("Ok, ignoring artists...")
			tracks = crawl_timestamps(description, None)
			
		print()
		splitAudioFile(track, tracks, outputFolder if outputFolder != None else "./Tracks")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Split an existing compilation file into tracks")
	
	parser.add_argument("track", help="The track to split up")
	parser.add_argument("-o", "--output-to", dest="output_folder", help="The target output folder")
	parser.add_argument("-d", help="Delete compilation track & description when finished.", action="store_true")
	parser.add_argument("-f", "--format", help="The description layout. Usually 'artist - track' or 'track - artist'", default="artist - track")
	parser.add_argument("description", help="The video description file (timestamps)")
	
	args = parser.parse_args()
	splitUpTrack(args.track, args.description, args.format, args.output_folder)
	
	if args.d:
		os.remove(args.track)
		os.remove(args.description)