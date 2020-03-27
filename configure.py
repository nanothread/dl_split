import sys
import mutagen
import subprocess
import os

def configure_tracks(output_folder, tracks, cover_image_path):
	for track in tracks:
		path = output_folder + "/" + track.filename()
		set_metadata(path, cover_image_path, track)
		set_file_icon(path, cover_image_path)

def set_cover_image(track_path, image_path):
	audio = mutagen.File(track_path)
			
	with open(image_path, 'rb') as f:
		cover = mutagen.mp4.MP4Cover(f.read(), imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG)
		
	audio["covr"] = [cover]
	audio.save()

def set_metadata(track_path, image_path, info):
	audio = mutagen.File(track_path)
		
	with open(image_path, 'rb') as f:
		cover = mutagen.mp4.MP4Cover(f.read(), imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG)
		
	audio["covr"] = [cover]
	audio["\xa9nam"] = info.title
	if info.artist != None:
		audio['\xa9ART'] = info.artist
	
	audio.save()
			
def set_file_icon(track_path, image_path):
	subprocess.run(["fileicon", "set", track_path, image_path])

if __name__ == "__main__":
	filename = "./Tracks/In Motion.m4a"
	image = "/Users/aglen/Desktop/Screenshot.png"
	
#	set_file_icon(filename, image)
	set_metadata(filename, image, "My Custom Artist Dank")