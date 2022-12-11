"""Example of a widget that will display an image at proper aspect ratio and always completely fill the widget area."""
from kivy.app import App
from kivy.uix.image import Image
from kivy.properties import AliasProperty
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    FillImage:
        source: 'test.jpg'
"""

class FillImage(Image):
    def get_filled_image_size(self):
        ratio = self.image_ratio
        w, h = self.size

        widget_ratio = w / h
        iw = (h * ratio) if ratio > widget_ratio else w
        ih = (w / ratio) if ratio <= widget_ratio else h
        return iw, ih

    norm_image_size = AliasProperty(get_filled_image_size, bind=('texture', 'size', 'allow_stretch', 'image_ratio', 'keep_ratio'), cache=True)

class Test(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
