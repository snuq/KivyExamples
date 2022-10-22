from kivy.app import App
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    FillImage:
        filled: True
        allow_stretch: True
        source: 'test.jpg'
"""

class FillImage(Image):
    filled = BooleanProperty(False)

    def get_norm_image_size(self):
        if not self.texture:
            return self.size
        ratio = self.image_ratio
        w, h = self.size
        tw, th = self.texture.size

        # ensure that the width is always maximized to the containter width
        if self.allow_stretch:
            if not self.keep_ratio:
                return w, h
            if self.filled:
                widget_ratio = w / h
                image_taller = ratio > widget_ratio
                iw = (h * ratio) if image_taller else w
                ih = h if image_taller else (w / ratio)
                return iw, ih
            iw = w
        else:
            iw = min(w, tw)
        # calculate the appropriate height
        ih = iw / ratio
        # if the height is too higher, take the height of the container
        # and calculate appropriate width. no need to test further. :)
        if ih > h:
            if self.allow_stretch:
                ih = h
            else:
                ih = min(h, th)
            iw = ih * ratio

        return iw, ih

    norm_image_size = AliasProperty(get_norm_image_size, bind=('texture', 'size', 'allow_stretch', 'image_ratio', 'keep_ratio'), cache=True)

class Test(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
