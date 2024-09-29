'''Example showing how to make a label that will not be longer than it needs to be, and will be 'shortened' by kivy'''
from kivy.app import App
from kivy.lang.builder import Builder
KV = """
<ShortenLabel@Label>:
    canvas.before:
        Color:
            rgba: 1, 0, 0, 1
        Rectangle:
            size: self.size
            pos: self.pos
    parent_width: 100
    size_hint: None, None
    size: min(self.parent_width, ref_label.texture_size[0]), self.texture_size[1]
    text_size: self.size
    shorten: True
    shorten_from: 'right'
    Label:  #This is needed to determine what the maximum size of the label would be if its not shortened
        opacity: 0
        id: ref_label
        text: root.text + ' '

BoxLayout:
    ShortenLabel:
        parent_width: root.width  #needs to be set to allow the label to shorten
        text: 'test long text needs to be shortened if window is too small'
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)

Test().run()
