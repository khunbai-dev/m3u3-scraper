## Prerequisite
* `ffmpeg` installed on machine, for Fedora using `dnf install ffmpeg-free`.


## What is it doing?
* Extract mp4 download links from m3u8 url.
* Download all mp4 files and concatnate into single file.
* Files download using `grequests` which is async downloading base on original 
`requests` package.
* Specific use for `joodkangtad` website.