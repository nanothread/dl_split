#!./env/bin/python3

from __future__ import unicode_literals

import argparse
import sys
import os
import youtube_dl
import pyperclip

from trim import splitUpTrack

class String:
	def __init__(self, value=""):
		self.value = value

def getVideoID(url):
	return url.split("v=")[1].split("&")[0]

def getDescription(id):
	service = build('youtube', 'v3', developerKey='AIzaSyAd6ROXi1xgo-29XwR394Ozri1x9B5XeRQ')
	result = service.videos().list(part="snippet", id=id).execute()
	return result["items"][0]["snippet"]["description"]

def downloadVideo(url):	
	def completionHandler(info, filename):
		if info["status"] == "finished":
			filename.value = info["filename"]
			
	filename = String() # Need to pass by reference to completion handler

	options = {
		"writedescription": True,
		"nocheckcertificate": True,
		"progress_hooks": [lambda info: completionHandler(info, filename)],
		"format": "bestaudio[ext=m4a]",
		"writethumbnail": True
	}
	
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([url])
		
	return filename.value

def getVideoName(filename, vidID): # VidName.f140.m4a -> VidName.m4a
	return filename.split(".")[0][:-len(vidID)-1]	

def cleanFilename(filename):
	components = filename.split(".")
	return components[0] + ".m4a"

def getArgs():
	script = os.path.basename(__file__)
	desktop = os.path.join(os.environ["HOME"], "Desktop", "Tracks")
	parser = argparse.ArgumentParser(description=f"Download a music compilation video and split it into tracks.\nExample: python3 {script} -o ~/Desktop/Tracks \"<Video URL>\"")
	
	parser.add_argument("-k", "--keep", help="Keep the full audio file", action='store_true')
	parser.add_argument("--dl-only", action="store_true", dest="dl_only", help="Skip splitting the downloaded audio.")
	parser.add_argument("-l", "--local", action="store_true", help="Uses local files instead of downloading new ones. If true, URL should point to the local video file.")
	parser.add_argument("-t", "--timestamps", help="The path of an existing file of timestamps")
	parser.add_argument("-c", "--clipboard", action="store_true", help="Get the description text from the clipboard")
	parser.add_argument("-f", "--format", help="The description layout. Usually 'artist - track' or 'track - artist'")
	parser.add_argument("-o", "--output-to", dest="output_folder", help="The target output folder", default=desktop)
	parser.add_argument("--album", help="Applies to all songs")
	parser.add_argument("--artist", help="Applies to all songs")
	parser.add_argument("url", help="The full YouTube URL of the video")
	
	return parser.parse_args()

if __name__ == "__main__":
	args = getArgs()		
	
	url = args.url
	if args.local:
		videoFile = args.url
		rawName = videoFile.split(".")[0]
		thumbnail = rawName + ".jpg"
		descriptionFile = rawName + ".description"
	else:
		vidID = getVideoID(url)
		rawFilename = downloadVideo(url)
		
		if args.dl_only:
			sys.exit(0)
			
		videoFile = cleanFilename(rawFilename)
		thumbnail = rawFilename.split('.')[0] + ".jpg"
		
		videoName = getVideoName(videoFile, vidID)
		descriptionFile = f"{videoName}-{vidID}.description" if args.timestamps == None else args.timestamps
	
	if args.clipboard:
		with open("description.txt", "w") as f:
			text = pyperclip.paste()
			lines = len(text.split('\n'))
			print(f"=> Saved clipboard: {lines} lines")
			f.write(text)
			
		descriptionFile = "description.txt"
		
	outputFolder = args.output_folder
		
	metadata = {
		"thumbnail": thumbnail,
		"artist": args.artist,
		"album": args.album
	}
	
	desc_format = None if args.artist != None else args.format
	
	splitUpTrack(videoFile, descriptionFile, desc_format, outputFolder, metadata)
	
	os.remove(descriptionFile)
	os.remove(thumbnail)
	
	if not args.keep:
		os.remove(videoFile)