"""Example showing how to display an incredibly large amount of text in a variety of different blocks in a recycleview by using a fixed width font."""
from kivy.app import App
from kivy.properties import *
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView

kv = """
<ScrollLabel>:
    font_name: "cour"
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
        size_label = ScrollLabel()
        size_label.text = 'A'
        size_label.text_size = None, None
        self.font_size = size_label._label.render()
        super().__init__(**kwargs)

    def on_width(self, *_):
        self.update_sizes()

    def update_sizes(self):
        for entry in self.data:
            max_line_length = int(self.width / self.font_size[0])
            lines = 1
            line_length = 0
            for word in entry['text'].split(' '):
                word_length = len(word)
                while word_length >= max_line_length:
                    #word too long for line, split and add lines
                    if line_length:
                        lines += 1
                    line_length = 0
                    lines += 1
                    word_length -= max_line_length
                if line_length:
                    #words already on line, add a space
                    line_length += 1
                line_length += word_length
                if line_length == 0:
                    continue
                if line_length > max_line_length:
                    #line too long, wrap word to the next
                    lines += 1
                    line_length = word_length
            entry['ks'] = [self.width, lines * self.font_size[1]]
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

        for x in range(10000):
            self.data.append({'text': make_paragraph()})
            self.data.append({'text': ' '})
        return Builder.load_string(kv)


LongScrollApp().run()
