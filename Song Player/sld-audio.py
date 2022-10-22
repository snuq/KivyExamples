from kivy.core.audio.audio_sdl2 import MusicSDL2  #streams audio off disk, better for longer stuff
from kivy.core.audio.audio_sdl2 import SoundSDL2  #loads into memory, better for repeating short sounds
from kivy.uix.button import Button
from kivy.app import App

class Test(App):
    def build(self):
        sound = MusicSDL2(source='music.mp3')
        sound.load()
        sound.play()
        return Button()

Test().run()