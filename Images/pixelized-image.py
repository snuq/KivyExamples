from kivy.app import App
from kivy.uix.image import Image

class PixelImage(Image):
    def on_texture(self, *_):
        self.texture.mag_filter = "nearest"
        self.texture.min_filter = "nearest"

class Test(App):
    def build(self):
        return PixelImage(source='W_Pawn.png', allow_stretch=True)

Test().run()