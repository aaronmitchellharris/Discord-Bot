import youtube_dl

class Song:

    def __init__(self, url):
        self.url = url

        # extracts info from youtube url
        opts = {}
        with youtube_dl.YoutubeDL(opts) as ydl:
            song_info = ydl.extract_info(self.url, download=False)

        self.title = song_info['title']
        self.duration = song_info['duration']

        # finds audio url with highest average bit rate
        seq = [x.get('abr') for x in song_info['formats'] if x.get('abr') is not None]
        self.maxAbrIndex = seq.index(max(seq))

        self.source = song_info['formats'][self.maxAbrIndex]['url']