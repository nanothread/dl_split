from __future__ import unicode_literals

import sys
import os
import youtube_dl
from googleapiclient.discovery import build

'''
	Call this script in the virtualenv like:
	python3 script.py "<video-link>"
'''

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
		print("===> Completion called: " + info["status"])
		if info["status"] == "finished":
			print("===> Download Finished: " + info["filename"])
			filename.value = info["filename"]
			
	filename = String() # Need to pass by reference to completion handler

	options = {
#		"verbose": True,
		"writedescription": True,
		"nocheckcertificate": True,
		"progress_hooks": [lambda info: completionHandler(info, filename)]
	}
	
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([url])
		
	return filename.value

def getVideoName(filename, vidID): # Shortest Video on Youtube-tPEE9ZwTmy0.f140.m4a
	return filename.split(".")[0][:-len(vidID)-1]	

def cleanFilename(filename):
	components = filename.split(".")
	return components[0] + ".mp4"

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Need the video URL as the argument")
		sys.exit()
		
	url = sys.argv[1]
	vidID = getVideoID(url)
	
	rawFilename = downloadVideo(url)
	videoFile = cleanFilename(rawFilename)
	
	videoName = getVideoName(videoFile, vidID)
	descriptionFile = f"{videoName}-{vidID}.description"
	
	with open(descriptionFile, "r") as f:
		description = f.read()
		
	print("Description:\n" + description)
	
	os.remove(videoFile)
	os.remove(descriptionFile)