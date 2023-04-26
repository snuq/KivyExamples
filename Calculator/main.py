"""Basic calculator made with as little code as possible.  Uses recycleview to generate buttons."""
from kivy.app import App
from kivy.lang.builder import Builder
Builder.load_string("""
<FormattedButton@Button>:
    font_size: self.height / 2
    opacity: 0 if not self.text else 1      #Hide the button if it has no text for easier layouts

<CalcButton@FormattedButton>:
    on_release: self.parent.calculator_input.insert_text(self.text)

<Calculator@BoxLayout>:
    orientation: 'vertical'
    TextInput:
        id: calculator_input
        font_size: self.height / 2
        size_hint_y: .25
        hint_text: '0.0'
    RecycleView:
        data: [{'text': '7'}, {'text': '8'}, {'text': '9'}, {'text': '/'}, {'text': '4'}, {'text': '5'}, {'text': '6'}, {'text': '*'}, {'text': '1'}, {'text': '2'}, {'text': '3'}, {'text': '-'}, {'text': '0'}, {'text': '.'}, {'text': ''}, {'text': '+'}]
        viewclass: 'CalcButton'
        RecycleGridLayout:
            calculator_input: calculator_input
            cols: 4
            default_size_hint: 1, 1
    BoxLayout:
        size_hint_y: .25
        FormattedButton:
        FormattedButton:
            text: 'Clr'
            on_release: calculator_input.text = ''
        FormattedButton:
            text: '<-'
            on_release: calculator_input.do_backspace()
        FormattedButton:
            text: '='
            on_release: calculator_input.text = app.calculate(calculator_input.text)
""")

class Calculator(App):
    def calculate(self, text):
        try:
            return str(eval(text))      #this is actually kinda dangerous, since it will run code too!
        except:
            return ''

    def build(self):
        return Builder.load_string("Calculator:")

Calculator().run()
