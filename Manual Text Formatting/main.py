from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.factory import Factory
from kivy.lang.builder import Builder
Builder.load_string("""
<SingleLabel@Label>:
    size: self.texture_size
    size_hint: None, None
    font_size: '18dp'
    markup: True
""")

class Test(App):
    def build(self):
        layout = StackLayout()
        split = ['a','b','w','i','a']
        for w in split:
            label = Factory.SingleLabel(text=w)
            layout.add_widget(label)
        return layout

Test().run()