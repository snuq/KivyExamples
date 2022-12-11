"""
Example that demonstrates loading an image directly from a string in memory.
"""
from io import BytesIO
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

class Test(App):
    def build(self):
        #Read the image data into a string so we have something to test with
        with open('test.jpg', 'rb') as image_file:
            image_data = image_file.read()
        #Convert data string into a BytesIO object
        image_bytes = BytesIO(image_data)
        #Create a kivy image out of the bytes data
        core_image = CoreImage(image_bytes, ext='jpg')
        #Create an image widget and replace its texture
        image = Image()
        image.texture = core_image.texture
        return image

Test().run()
