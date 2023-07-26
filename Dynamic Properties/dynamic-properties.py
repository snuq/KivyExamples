from kivy import app
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout

class TestWidget(BoxLayout):
    def add(self):
        self.create_property('test_prop', value=0)
        self.bind(test_prop=lambda instance, value: print("Callback called, test_prop="+str(value)))

app.runTouchApp(Builder.load_string("""
TestWidget:
    Button:
        text: 'Add Property'
        on_release: root.add()
    Button:
        text: 'Test Property'
        on_release: root.test_prop += 1"""))
