import os
os.environ['KIVY_AUDIO'] = 'ffpyplayer'
import ffpyplayer.player.core
from songplayer import SongPlayer
from kivy.app import App

class Test(App):
    def build(self):
        song = SongPlayer(source="music.mp3")
        return song

if __name__ == '__main__':
    Test().run()
