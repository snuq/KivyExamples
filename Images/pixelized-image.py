from kivy.uix.image import Image

class PixelImage(Image):
    def on_texture(self, *_):
        self.texture.mag_filter = "nearest"  #filter when image is larger than original
        self.texture.min_filter = "nearest"  #filter when image is smaller than original

from kivy import app; app.runTouchApp(PixelImage(source='small.bmp', fit_mode='contain'))