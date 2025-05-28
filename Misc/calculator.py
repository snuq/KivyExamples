"""Basic calculator made with as little code as possible.  Uses recycleview to generate buttons."""
from kivy.app import App
from kivy.lang.builder import Builder
KV = """
<FormattedButton@Button>:
    font_size: self.height / 2

<CalcButton@FormattedButton>:
    on_release: app.root.ids['calculator_input'].insert_text(self.text)

BoxLayout:
    orientation: 'vertical'
    TextInput:
        id: calculator_input
        font_size: self.height / 2
        size_hint_y: .2
        hint_text: '0.0'
    RecycleView:
        data: [{'text': '7'}, {'text': '8'}, {'text': '9'}, {'text': '/'}, {'text': '4'}, {'text': '5'}, {'text': '6'}, {'text': '*'}, {'text': '1'}, {'text': '2'}, {'text': '3'}, {'text': '-'}, {'text': '0'}, {'text': '.'}, {'widget': 'Widget'}, {'text': '+'}, {'text': 'Clr', 'widget': 'FormattedButton', 'on_release': lambda: setattr(calculator_input, 'text', '')}, {'text': '<-', 'widget': 'FormattedButton', 'on_release': lambda: calculator_input.do_backspace()}, {'widget': 'Widget'}, {'text': '=', 'widget': 'FormattedButton', 'on_release': lambda: app.calculate(calculator_input)}]
        viewclass: 'CalcButton'
        key_viewclass: 'widget'
        RecycleGridLayout:
            cols: 4
            default_size_hint: 1, 1
"""

class Calculator(App):
    def calculate(self, calculator_input):
        try:
            calculator_input.text = str(eval(calculator_input.text))
        except:
            calculator_input.text = ''

    def build(self):
        return Builder.load_string(KV)

Calculator().run()
