from __future__ import unicode_literals

import argparse
import ffmpeg
from track import crawl_timestamps
from configure import configure_tracks
import os 

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
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Split an existing compilation file into tracks")
	
	parser.add_argument("-o", "--output-to", dest="output_folder", default="/Users/aglen/Desktop/Tracks", help="The target output folder")
	parser.add_argument("-d", help="Delete compilation track & description when finished.", action="store_true")
	parser.add_argument("-f", "--format", help="The description layout. Usually 'artist - track' or 'track - artist'", default="artist - track")
	parser.add_argument("--album", help="Applies to all songs")
	parser.add_argument("--artist", help="Applies to all songs. Overrides -f format")
	parser.add_argument("filename", help="The filename (minus extension) of the video, description, and thumbnail files.")
	
	args = parser.parse_args()

	track = args.filename + ".m4a"
	description = args.filename + ".description"
	thumbnail = args.filename + ".jpg"
	
	desc_format = args.format
	if not 'title' in desc_format or not 'artist' in desc_format:
		desc_format = None
		
	outputFolder = args.output_folder
		
	metadata = {
		"thumbnail": thumbnail,
		"artist": args.artist,
		"album": args.album
	}
	
	desc_format = None if args.artist != None else args.format
	
	splitUpTrack(track, description, desc_format, outputFolder, metadata)
	
	if args.d:
		os.remove(track)
		os.remove(description)
		os.remove(thumbnail)