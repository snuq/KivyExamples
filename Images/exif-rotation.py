from PIL import Image as PILImage
from kivy.app import App
from kivy.properties import *
from kivy.uix.image import Image
from kivy.lang.builder import Builder
Builder.load_string("""
<RotateImage>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            axis: 0,0,1
            origin: self.center
    canvas.after:
        PopMatrix
""")

class RotateImage(Image):
    angle = NumericProperty(0)
    mirror = BooleanProperty(False)

    def on_source(self, *_):
        image = PILImage.open(self.source)
        exif = image._getexif()
        if exif and 274 in exif:
            orientation = exif[274]
            if orientation == 3 or orientation == 4:
                self.angle = 180
            elif orientation == 5 or orientation == 6:
                self.angle = 270
            elif orientation == 7 or orientation == 8:
                self.angle = 90
            else:
                self.angle = 0
            if orientation in [2, 4, 5, 7]:
                self.mirror = True
            else:
                self.mirror = False

    def on_texture(self, instance, value):
        if value is not None:
            self.texture_size = list(value.size)
        if self.mirror:
            self.texture.flip_horizontal()

class Test(App):
    def build(self):
        return RotateImage(source='image.jpg')

Test().run()
