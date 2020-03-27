from __future__ import unicode_literals

import argparse
import sys
import os
import youtube_dl
from googleapiclient.discovery import build

from track import crawl_timestamps
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
#		"verbose": True,
		"writedescription": True,
		"nocheckcertificate": True,
		"progress_hooks": [lambda info: completionHandler(info, filename)],
		"format": "bestaudio[ext=m4a]"
	}
	
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([url])
		
	return filename.value

def getVideoName(filename, vidID): # Shortest Video on Youtube-tPEE9ZwTmy0.f140.m4a
	return filename.split(".")[0][:-len(vidID)-1]	

def cleanFilename(filename):
	components = filename.split(".")
	return components[0] + ".m4a"

def getArgs():
	script = os.path.basename(__file__)
	parser = argparse.ArgumentParser(description=f"Download a music compilation video and split it into tracks.\nExample: python3 {script} -o ~/Desktop/Tracks \"<Video URL>\"")
	
	parser.add_argument("-k", "--keep", help="Keep the full audio file", action='store_true')
	parser.add_argument("-f", "--format", help="The description layout. Usually 'artist - track' or 'track - artist'", default="artist - track")
	parser.add_argument("-o", "--output-to", dest="output_folder", help="The target output folder")
	parser.add_argument("url", help="The full YouTube URL of the video")
	
	return parser.parse_args()

if __name__ == "__main__":
	args = getArgs()
		
	url = args.url
	vidID = getVideoID(url)
	
	rawFilename = downloadVideo(url)
	videoFile = cleanFilename(rawFilename)
	
	videoName = getVideoName(videoFile, vidID)
	descriptionFile = f"{videoName}-{vidID}.description"
	
	splitUpTrack(videoFile, descriptionFile, args.format, args.output_folder)
	
	os.remove(descriptionFile)
	
	if not args.keep:
		os.remove(videoFile)