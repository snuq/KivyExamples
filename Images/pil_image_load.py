"""
Example that demonstrates displaying an image in kivy from a PIL image
"""
from io import BytesIO
from kivy.app import App
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
from PIL import Image

class Test(App):
    def build(self):
        #Use PIL/Pillow to open the image file
        image_pil = Image.open('test.jpg')
        #Use PIL to save the image into a BytesIO object
        image_bytes = BytesIO()
        image_pil.save(image_bytes, 'jpeg')
        image_bytes.seek(0)
        #Create a kivy image out of the bytes data
        core_image = CoreImage(image_bytes, ext='jpg')
        #Create an image widget and replace its texture
        image = KivyImage()
        image.texture = core_image.texture
        return image

Test().run()
