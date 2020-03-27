# dl_split: A Song Compilation Downloader

**dl_split** is a python script I made for personal use that takes online song compilations (for example, [this](https://www.youtube.com/watch?v=ByS1Rlk_AL8&t=80s)) and splits them into tracks. It does this in a few steps.

1. It uses `youtube-dl` to download the video, description, and thumbnail.
2. It searches the video description for the timestamp of each song and splits the video into tracks based on what's found.
3. It configures each track with metadata (if found) such as the song title and artist. It also sets the album art to the video thumbnail so it looks great when you drag it into Apple's Music.app.

This script is only intended for use on songs that are in the public domain.



### Usage

**Warning**: I haven't tested this on any machines other than my own (running macOS). There may be a fair amount of configuration work to do if you try to use it.

* Extract the repo and cd into the top level folder.
* Run `./dl_split.py -h` to see all the options.



#### Examples

Download the video, split it into tracks based on the description text. Tracks will be added to a new `Tracks` folder on your Desktop.

```bash
$ ./dl_split.py "<Video URL>"
```



Search the description for timestamps and look for artists too. For example, if the description is:

```
00:00 Beethoven - Moonlight Sonata
5:14 Bach - Prelude in C major
15:43 Chopin - Prelude Op.28 No.4 in E minor
```

then you should use `-f "artist - track"`

```bash
$ ./dl_split.py -f "track - artist" -o "/path/to/folder" "<Video URL>"
```



If you know that all the songs have the same artist, you can set some of these flags too.

```bash
$ ./dl_split.py --album="Panic!" --artist="Caravan Palace" "<Video URL>"
```



Finally, use the `-c` flag to get the description text directly from your clipboard. This is useful if the timestamps are in a place other than the video description. If you already have a file with the timestamps, pass it in with `--timestamps="/path/to/timestamps.txt"`