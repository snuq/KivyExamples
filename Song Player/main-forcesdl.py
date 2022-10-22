from kivy.core.audio.audio_sdl2 import MusicSDL2
from kivy.core.audio.audio_sdl2 import SoundSDL2
from songplayer import SongPlayer
from kivy.app import App

class Test(App):
    def build(self):
        song = SongPlayer(sound_class=SoundSDL2, source="music.mp3")
        return song

if __name__ == '__main__':
    Test().run()
