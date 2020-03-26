from __future__ import unicode_literals

import sys
import youtube_dl
from googleapiclient.discovery import build

'''
	Call this script in the virtualenv like:
	python3 script.py "<video-link>"
'''

def getVideoID(url):
	return url.split("v=")[1].split("&")[0]

def getDescription(id):
	service = build('youtube', 'v3', developerKey='AIzaSyAd6ROXi1xgo-29XwR394Ozri1x9B5XeRQ')
	result = service.videos().list(part="snippet", id=id).execute()
	return result["items"][0]["snippet"]["description"]
	
def crawlTimestamps(text):
	print()
	
def downloadVideo(url):
	options = {
		"verbose": True,
		"forcedescription": True,
		"simulate": True
	}
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([url])

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Need the video URL as the argument")
		sys.exit()
		
	url = sys.argv[1]
	downloadVideo(url)
#	id = getVideoID(url)
#	print(id)