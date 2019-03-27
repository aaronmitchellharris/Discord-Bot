from song import Song

class Playlist:

    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    def nextSong(self):
        return self.queue.pop(0)

    def add(self, url):
        newSong = Song(url)

        if newSong not in self.queue:
            self.queue.append(newSong)
            return 'added'
        else:
            return 'not added'

    def delete(self, song):
        if type(song) is string:
            self.queue.remove(queue[index(song)])
        elif type(song) is int:
            sel.fqueue.remove(queue[song])

    def shuffle(self):
        pass
    def skip(self):
        pass
