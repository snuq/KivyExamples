from kivy.app import App
from smoothsetting import SmoothSetting
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
    orientation: 'vertical'
    SmoothSetting:
        size_hint_y: None
        height: 40

        content: ['First', 'Second', 'Third', 'Fourth', 'Fifth']
        item_width: 80
    SmoothSetting:
        size_hint_x: .5
        size_hint_y: None
        height: 40

        content: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
        item_width: 40
        start_on: 5
        repeat_length: 2
        repeat_minimum: 0.5
        left_image: 'data/left.png'
        right_image: 'data/right.png'
        on_active: print('active: '+str(self.active))
        control_width: 80
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
