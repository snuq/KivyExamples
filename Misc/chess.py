"""Simple chess game with basic logic and movement implemented but no rules"""
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import *
from kivy.graphics import Rectangle, Color
from kivy.lang.builder import Builder
Builder.load_string("""
<ChessPiece>:
    canvas.before:
        Color:
            rgb: self.piece_color
        Ellipse:
            size: self.size
            pos: self.pos
        Color:
            rgb: self.outline_color
        Line:
            width: 3
            ellipse: self.pos[0], self.pos[1], self.size[0], self.size[1]
    canvas.after:
        Color:
            rgba: 0, 1, 0, (.3 if self.selected else 0)
        Rectangle:
            size: self.size
            pos: self.pos
    outline_color: (0,0,0) if self.side == 'w' else (1,1,1)
    piece_color: (0,0,0) if self.side == 'b' else (1,1,1)
    color: self.outline_color
    font_size: self.height - 6
    size_hint: 0.125, 0.125
    pos_hint: {'x': self.grid_x/8, 'y': self.grid_y/8}
""")
animation_speed = 0.5
columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
starting = [
    'wr1a', 'wn1b', 'wb1c', 'wq1d', 'wk1e', 'wb1f', 'wn1g', 'wr1h',
    'wp2a', 'wp2b', 'wp2c', 'wp2d', 'wp2e', 'wp2f', 'wp2g', 'wp2h',
    'bp7a', 'bp7b', 'bp7c', 'bp7d', 'bp7e', 'bp7f', 'bp7g', 'bp7h',
    'br8a', 'bn8b', 'bb8c', 'bq8d', 'bk8e', 'bb8f', 'bn8g', 'br8h'
]

class ChessBoard(RelativeLayout):
    selected_piece = ObjectProperty(allownone=True)

    def setup_board(self, pieces):
        self.clear_widgets()
        for piece in pieces:
            self.setup_piece(piece)

    def setup_piece(self, notation):
        side = notation[0]
        piece_type = notation[1]
        row = int(notation[2]) - 1
        column = columns.index(notation[3].lower())
        piece = ChessPiece(grid_x=column, grid_y=row, text=piece_type, side=side)
        self.add_widget(piece)

    def find_piece(self, grid_x, grid_y):
        for piece in self.children:
            if piece.grid_x == grid_x and piece.grid_y == grid_y:
                return piece
        return None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.selected_piece:
                grid_x = int(touch.pos[0] / self.width * 8)
                grid_y = int(touch.pos[1] / self.height * 8)
                found = self.find_piece(grid_x, grid_y)
                if found and found.side == self.selected_piece.side:
                    self.selected_piece.moved()
                    super().on_touch_down(touch)
                    return
                if found:
                    found.capture()
                self.selected_piece.move(grid_x, grid_y)
            else:
                super().on_touch_down(touch)

    def on_size(self, *_):
        self.draw_board()

    def on_pos(self, *_):
        self.draw_board()

    def draw_board(self):
        black = 0.1, 0.1, 0.1
        white = 0.9, 0.9, 0.9
        is_white = True
        grid_size_x = self.width / 8
        grid_size_y = self.height / 8
        with self.canvas.before:
            for y in range(8):
                for x in range(8):
                    if is_white:
                        Color(rgb=white)
                    else:
                        Color(rgb=black)
                    Rectangle(pos=(grid_size_x * x, grid_size_y * y), size=(grid_size_x, grid_size_y))
                    is_white = not is_white
                is_white = not is_white

class ChessPiece(Label):
    selected = BooleanProperty(False)
    side = StringProperty('w')
    outline_color = ColorProperty()
    piece_color = ColorProperty()
    anim = ObjectProperty(allownone=True)
    grid_x = NumericProperty()
    grid_y = NumericProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selected = True
            self.parent.selected_piece = self
            return True

    def capture(self):
        self.move(-1 if self.side != 'w' else 9, 3.5, delay=animation_speed)
        Clock.schedule_once(self.remove_self, animation_speed * 2)

    def remove_self(self, *_):
        self.parent.remove_widget(self)

    def move(self, grid_x, grid_y, delay=0.0):
        anim = Animation(duration=delay) + Animation(grid_x=grid_x, grid_y=grid_y, t='in_quad', duration=animation_speed)
        anim.start(self)
        self.moved()

    def moved(self):
        self.selected = False
        if self.parent.selected_piece == self:
            self.parent.selected_piece = None

class ChessApp(App):
    def build(self):
        return ChessBoard()

    def on_start(self):
        self.root.setup_board(starting)

ChessApp().run()
