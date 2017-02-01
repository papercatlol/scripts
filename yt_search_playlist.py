#!/bin/env python3
from lxml import html
import requests
import sys
import subprocess


def main():
    if len(sys.argv) == 1:
        query = input("Search playlists: ")
    else:
        query = sys.argv[1:]
    
    request = "https://www.youtube.com/results?q={}&sp=EgIQAw%253D%253D"
    response = requests.get(request.format(query))
    tree = html.fromstring(response.content.decode("utf-8"))
    playlist_elems = tree.cssselect('div.yt-lockup-playlist')

    title = ".//a[@title]/@title"
    link = ".//div/div/div/ul/li/a"

    playlists = [(e.xpath(title)[0], e.xpath(link)[0]) for e in playlist_elems]

    for i, p in enumerate(playlists):
        count = p[1].text.split("(")[1].split()[0]
        print("{}. {} ({})".format(i + 1, p[0], count))

    mpv_args = ["mpv", "--no-video", "--ytdl-raw-options=yes-playlist=",
            "--term-playing-msg=[${playlist-pos:1} / ${playlist-count}] ${media-title}"]
    while 1:
        try:
            n = int(input("Enter playlist number: "))
            mpv_args.append("https://www.youtube.com{}".format(playlists[n - 1][1].get("href")))
            subprocess.call(mpv_args)
            return
        except (IndexError, ValueError): pass
        except KeyboardInterrupt: return



    



if __name__ == "__main__":
    main()

