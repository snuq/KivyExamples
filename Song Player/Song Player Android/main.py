from audio_android import SoundAndroid
from kivy.core.audio import SoundLoader
SoundLoader.register(SoundAndroid)
from kivy.app import App
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    orientation: 'horizontal'
    Button:
        text: 'Play'
        on_release: app.song.play()
    Button:
        text: 'Stop'
        on_release: app.song.stop()
"""

class Test(App):
    def build(self):
        self.song = SoundLoader.load("music.mp3")
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
