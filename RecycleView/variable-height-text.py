"""Example showing how to display a large amount of text split into varying block sizes in a recycleview.  This example can be slow on first draw and on resizes with too much text."""
from kivy.app import App
from kivy.properties import *
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView

kv = """
<ScrollLabel>:
    text_size: self.width, None

RVLongText:
    data: app.data
    scroll_type: ['bars', 'content']
    bar_width: 20
    viewclass: 'ScrollLabel'
    RecycleBoxLayout:
        orientation: 'vertical'
        key_size: 'ks'
        default_size_hint: 1, None
        size_hint: 1, None
        height: self.minimum_height
"""


class ScrollLabel(Label):
    pass


class RVLongText(RecycleView):
    font_size = ListProperty()

    def __init__(self, **kwargs):
        self.size_label = ScrollLabel()
        super().__init__(**kwargs)

    def on_width(self, *_):
        self.update_sizes()

    def update_sizes(self):
        for entry in self.data:
            self.size_label.text = entry['text']
            self.size_label.text_size = self.width, None
            entry['ks'] = self.size_label._label.render()
        self.refresh_from_data()


class LongScrollApp(App):
    data = ListProperty()

    def build(self):
        def make_paragraph():
            import random
            words = ['exercitation', 'sint', 'dolore', 'ea', 'eu', 'proident', 'mollit', 'cupidatat', 'id', 'ullamco', 'labore', 'velit', 'in', 'qui', 'officia', 'occaecat', 'ex', 'nisi', 'commodo', 'non', 'ipsum', 'sed', 'ut', 'magna', 'irure', 'consectetur', 'quis', 'enim', 'cillum', 'voluptate', 'et', 'sunt', 'duis', 'eiusmod', 'veniam', 'anim', 'laboris', 'do', 'aute', 'deserunt', 'reprehenderit', 'amet', 'aliquip', 'elit', 'ad', 'dolor', 'sit', 'minim', 'fugiat', 'excepteur', 'pariatur', 'lorem', 'adipiscing', 'tempor', 'consequat', 'est', 'laborum', 'nulla', 'incididunt', 'esse', 'culpa', 'aliqua', 'nostrud']

            def make_sentence():
                length = random.randint(4, 40)
                sentence = [random.choice(words) for i in range(length)]
                for index in random.sample(list(range(length - 1)), int(length / 6)):
                    sentence[index] = sentence[index] + ','
                sentence[0] = sentence[0].title()
                sentence[-1] = sentence[-1] + '.'
                return ' '.join(sentence)

            return ' '.join(make_sentence() for i in range(random.randint(2, 10)))

        for x in range(100):
            self.data.append({'text': make_paragraph()})
            self.data.append({'text': ' '})
        return Builder.load_string(kv)

LongScrollApp().run()