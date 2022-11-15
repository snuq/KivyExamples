import os
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang.builder import Builder
KV = """
<FileItem>:
    orientation: 'vertical'
    Image: 
        source: 'atlas://data/images/defaulttheme/filechooser_%s' % ('folder' if root.folder else 'file')
    Label:
        id: text
        text: root.filename

RecycleView:
    data: app.data
    viewclass: 'FileItem'
    RecycleGridLayout:
        spacing: 10
        rows: int(root.height / dp(80))
        default_size_hint: None, None
        default_size: dp(160), dp(80)
        size_hint: None, None
        height: self.minimum_height
        width: self.minimum_width
"""

class FileItem(ButtonBehavior, BoxLayout):
    folder = BooleanProperty(True)
    filename = StringProperty()

    def on_release(self, *_):
        print("Clicked on: "+self.filename)

class Test(App):
    data = ListProperty()

    def build(self):
        folder = '/'
        folder_files = list(os.scandir(folder))
        self.data = [{"filename": file.name, 'folder': not file.is_file()} for file in folder_files]
        return Builder.load_string(KV)

Test().run()
