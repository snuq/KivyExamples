from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout
KV = """
<AdaptiveLayout>:
    cols: 2 if self.width > self.height else 1

AdaptiveLayout:
    Button:
        text: 'Button 1'
    Button:
        text: 'Button 2'
"""

class AdaptiveLayout(GridLayout):
    pass

class Test(App):
    def build(self):
        return Builder.load_string(KV)

Test().run()