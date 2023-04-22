"""Example showing how to crease RecycleView items with different heights.
This more complex version shows how to accomplish this with composite widgets."""
from kivy.app import App
from kivy.properties import ListProperty
from kivy.lang.builder import Builder
KV = """
<RecycleItem@BoxLayout>:
    text: ''                #Exposes the label's text to make this work in a recycleview
    height: max(button.width, label.height)
    Button:                 #Just here to show a bit of variation in the composite widget
        id: button
        size_hint: 0.1, 1
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: label
            size_hint_y: None
            text: root.text
            height: self.texture_size[1]
            text_size: self.width, None
        Widget:             #Ensures that label widget is at top of area

RecycleView:
    data: app.data
    viewclass: 'RecycleItem'
    RecycleBoxLayout:
        default_size_hint: 1, None      #Allows recycleview elements to have a variable height
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""
class Test(App):
    data = ListProperty()
    def build(self):
        self.data = [{"text": "First blahblah"}, {"text": "Second blahblahblahblah blahblahblahblahblahblah"}, {"text": "Third blahblahblahblah blahblahblahblahblahblahblahblahblahblah blahblahblahblahblahblahblahblahblahblah blahblahblahblahblahblahblahblah"}, {"text": "Fourth"}]
        return Builder.load_string(KV)

Test().run()
