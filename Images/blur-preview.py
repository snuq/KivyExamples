"""
Example that shows how to create a special image widget that can toggle a blured version of itself
"""
from kivy.app import App
from kivy.properties import *
from kivy.core.image import Image as CoreImage
from io import BytesIO
from PIL import Image as EditImage, ImageFilter
from kivy.uix.image import Image
from kivy.lang import Builder


class ImagePreview(Image):
    use_blur = BooleanProperty(True)  #Set this to toggle blur mode
    fit_mode = StringProperty('contain')  #Necessary to make a smaller blur preview scale up to image
    _blur_image = None  #Stores the blur image to allow quick toggling without extra processing

    def on_use_blur(self, *_):  #updates image when use blur variable is changed
        self.texture_update()

    def display_blur(self):  #switches to blurred image
        self._coreimage = self.generate_blur()
        self._on_tex_change()

    def display_original(self):  #switches to original image
        self.set_texture_from_resource(self.source)  #Original kivy image load routine

    def generate_blur(self):  #returns a blurred coreimage, generates if needed
        if self._blur_image is None:  #No blur image yet, generate one
            original_image = EditImage.open(self.source)
            original_image.thumbnail(size=(500, 500))  #Resize image to make blur uniform and quicker
            blur_image = original_image.filter(filter=ImageFilter.GaussianBlur(10))
            image_bytes = BytesIO()
            blur_image.save(image_bytes, 'jpeg')  #Save blurred image to a jpg so it can be loaded
            image_bytes.seek(0)  #Necessary to reset cursor position so image can be loaded
            self._blur_image = CoreImage(image_bytes, ext='jpg')  #Save blurred image for easy toggle between original
        return self._blur_image

    def texture_update(self, *largs):  #Overrides internal kivy function to which image is enabled
        if self.use_blur:
            self.display_blur()
        else:
            self.display_original()


class Test(App):
    def build(self):
        return Builder.load_string("""
BoxLayout:
    orientation: 'vertical'
    ImagePreview:
        id: image_preview
        source: 'test.jpg'
    Button:
        size_hint_y: 0.1
        text: 'Toggle Blur'
        on_release: image_preview.use_blur = not image_preview.use_blur
""")
Test().run()
