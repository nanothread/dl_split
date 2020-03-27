import sys
import mutagen
import subprocess
import os

def configure_tracks(output_folder, tracks, metadata):
	for i in range(len(tracks)):
		track = tracks[i]
		path = output_folder + "/" + track.filename()
		set_metadata(path, metadata, track, i + 1)
		set_file_icon(path, metadata['thumbnail'])

def set_cover_image(track_path, image_path):
	audio = mutagen.File(track_path)
			
	with open(image_path, 'rb') as f:
		cover = mutagen.mp4.MP4Cover(f.read(), imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG)
		
	audio["covr"] = [cover]
	audio.save()

def set_metadata(track_path, metadata, trackInfo, pos):
	image_path = metadata["thumbnail"]
	
	audio = mutagen.File(track_path)
		
	with open(image_path, 'rb') as f:
		cover = mutagen.mp4.MP4Cover(f.read(), imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG)
		
	audio["covr"] = [cover]
	audio["\xa9nam"] = trackInfo.title
	if metadata["artist"] != None:
		audio['\xa9ART'] = metadata["artist"]
	elif trackInfo.artist != None:
		audio['\xa9ART'] = trackInfo.artist
		
	if metadata["album"] != None:
		audio['\xa9alb'] = metadata["album"]
		audio['soal'] = str(pos)
	
	audio.save()
			
def set_file_icon(track_path, image_path):
	subprocess.run(["fileicon", "set", "-q", track_path, image_path])

if __name__ == "__main__":
	filename = "./Tracks/In Motion.m4a"
	image = "/Users/aglen/Desktop/Screenshot.png"
	
#	set_file_icon(filename, image)
	set_metadata(filename, image, "My Custom Artist Dank")