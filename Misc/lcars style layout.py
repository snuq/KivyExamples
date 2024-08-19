from math import copysign
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.graphics import Color, Mesh
from kivy.graphics.tesselator import Tesselator
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    padding: 40, 40
    LCARSBox:
        border_color: 1, 0, 0, 1
        border_cutoff_top: 200, 0
        border_cutoff_right: 100, -80
        border_cutoff_left: -80, 100
        borders: [100, 20, 20, 0]
        inner_arc_divisor: 2
        rounding: True
        rounding_limit: 10
        Button:
            opacity: 0.5
            text: 'Test'
"""


class LCARS(Widget):
    def generate_arc(self, arc_start_x, arc_start_y, arc_width, arc_height, concave=False):
        #Generate points for a 32 segment arc at the given position and size.
        arc = 0.0, 0.049068, 0.098017, 0.146730, 0.195090, 0.242980, 0.290285, 0.336890, 0.382683, 0.427555, 0.471397, 0.514103, 0.555570, 0.595699, 0.634393, 0.671559, 0.707107, 0.740951, 0.773010, 0.803208, 0.831470, 0.857729, 0.881921, 0.903989, 0.923880, 0.941544, 0.956940, 0.970031, 0.980785, 0.989177, 0.995185, 0.998795, 1.0
        arc_points = []
        total_points = len(arc)
        for index, arc_point in enumerate(arc):
            arc_point_reverse = arc[total_points - 1 - index]
            if concave:
                x = arc_start_x + (arc_point * arc_width)
                y = arc_start_y + ((1 - arc_point_reverse) * arc_height)
            else:
                x = arc_start_x + ((1 - arc_point_reverse) * arc_width)
                y = arc_start_y + (arc_point * arc_height)
            arc_points.extend([x, y])
        return arc_points

    def generate_arc_corner(self, v_edge_x, v_edge_y, h_edge_x, h_edge_y, v_edge_width, h_edge_width, inner_arc_divisor):
        #Generates the rounded corner mesh points
        arc_edge_shorter = min(abs(v_edge_width), abs(h_edge_width))
        arc_size_x = copysign(arc_edge_shorter, v_edge_width)
        arc_size_y = copysign(arc_edge_shorter, h_edge_width)
        inner_arc_size_x = arc_size_x / inner_arc_divisor
        inner_arc_size_y = arc_size_y / inner_arc_divisor
        outer_arc = self.generate_arc(v_edge_x, h_edge_y - arc_size_y, arc_size_x, arc_size_y)
        inner_arc = self.generate_arc(v_edge_x + v_edge_width + inner_arc_size_x, h_edge_y - h_edge_width, 0-inner_arc_size_x, 0-inner_arc_size_y, True)
        #                     vertical edge inner           vertical edge outer                horizontal edge outer        horizonntal edge inner
        mesh_points = [v_edge_x + v_edge_width, v_edge_y] + [v_edge_x, v_edge_y] + outer_arc + [h_edge_x, h_edge_y] + [h_edge_x, h_edge_y - h_edge_width] + inner_arc
        return arc_edge_shorter / inner_arc_divisor, mesh_points

    def generate_box(self, left, top, right, bottom):
        #Generates the mesh points for a basic box
        return [left, bottom, left, top, right, top, right, bottom]

    def generate_rounded_box(self, left, top, right, bottom, round_tl=False, round_tr=False, round_bl=False, round_br=False, round_limit=None):
        #Generates the mesh points for a box that maay have rounded edges
        #round_ variables: round off one corner of the box, tl=top-left, tr=top-right, bl=bottom-left, br=bottom-right
        #round_limit: set to an integer to limit the size of the cornr rounding

        width = right - left
        height = top - bottom
        round_size = int(min(width, height) / 2)
        if round_limit is not None and round_size > round_limit:
            round_size = round_limit
        mesh_points = []
        if round_tl:
            mesh_points.extend(self.generate_arc(left, top - round_size, round_size, round_size))
        else:
            mesh_points.extend([left, top])
        if round_tr:
            mesh_points.extend(self.generate_arc(right - round_size, top, round_size, 0-round_size, concave=True))
        else:
            mesh_points.extend([right, top])
        if round_br:
            mesh_points.extend(self.generate_arc(right, bottom + round_size, 0-round_size, 0-round_size))
        else:
            mesh_points.extend([right, bottom])
        if round_bl:
            mesh_points.extend(self.generate_arc(left + round_size, bottom, 0-round_size, round_size, concave=True))
        else:
            mesh_points.extend([left, bottom])
        return mesh_points


class LCARSLayout(LCARS):
    border_color = ColorProperty()
    borders = ListProperty([0, 0, 0, 0])  #Set the size of each border edge in pixels: left, top, right, bottom
    border_cutoff_top = ListProperty([0, 0])  #top-left, top-right
    border_cutoff_bottom = ListProperty([0, 0])  #bottom-left, bottom-right
    border_cutoff_left = ListProperty([0, 0])  #left-top, left-bottom
    border_cutoff_right = ListProperty([0, 0])  #right-top, right-bottom
    inner_arc_divisor = NumericProperty(4)
    extra_padding = BooleanProperty(True)
    rounding = BooleanProperty(False)
    rounding_limit = NumericProperty(None, allownone=True)
    _redraw_cache = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.redraw_arcs)
        self.bind(pos=self.redraw_arcs)
        self.bind(border_color=self.redraw_arcs)
        self.bind(borders=self.redraw_arcs)
        self.bind(border_cutoff_top=self.redraw_arcs)
        self.bind(border_cutoff_bottom=self.redraw_arcs)
        self.bind(border_cutoff_left=self.redraw_arcs)
        self.bind(border_cutoff_right=self.redraw_arcs)
        self.bind(inner_arc_divisor=self.redraw_arcs)
        self.bind(extra_padding=self.redraw_arcs)
        self.bind(rounding=self.redraw_arcs)
        self.bind(rounding_limit=self.redraw_arcs)

    def redraw_arcs(self, *_):
        #prevent redraw being called multiple times in one frame by all the bound variables
        if self._redraw_cache is None:
            self._redraw_cache = Clock.schedule_once(self._redraw_arcs, -1)

    def _redraw_arcs(self, *_):
        border_left, border_top, border_right, border_bottom = self.borders
        cut_left_top, cut_left_bottom = self.border_cutoff_left
        cut_right_top, cut_right_bottom = self.border_cutoff_right
        cut_top_left, cut_top_right = self.border_cutoff_top
        cut_bottom_left, cut_bottom_right = self.border_cutoff_bottom
        o_top = self.top
        o_bottom = self.y
        o_left = self.x
        o_right = self.right
        i_top = self.top - border_top
        i_bottom = self.y + border_bottom
        i_left = self.x + border_left
        i_right = self.right - border_right
        mid_y = self.y + int(self.height / 2)
        mid_x = self.x + int(self.width / 2)

        mesh_contours = []
        top_extra_padding = [0]
        bottom_extra_padding = [0]
        left_extra_padding = [0]
        right_extra_padding = [0]

        #top-left area
        if border_left and border_top:
            arc_edge_shorter, mesh_points = self.generate_arc_corner(o_left, mid_y + cut_left_top, mid_x - cut_top_left, o_top, border_left, border_top, self.inner_arc_divisor)
            mesh_contours.append(mesh_points)
            top_extra_padding.append(arc_edge_shorter)
            left_extra_padding.append(arc_edge_shorter)
        elif border_left:
            mesh_contours.append(self.generate_rounded_box(o_left, o_top, i_left, mid_y + cut_left_top, round_tl=self.rounding, round_tr=self.rounding, round_limit=self.rounding_limit))
        elif border_top:
            mesh_contours.append(self.generate_rounded_box(o_left, o_top, mid_x - cut_top_left, i_top, round_tl=self.rounding, round_bl=self.rounding, round_limit=self.rounding_limit))

        #top-right area
        if border_right and border_top:
            arc_edge_shorter, mesh_points = self.generate_arc_corner(o_right, mid_y + cut_right_top, mid_x + cut_top_right, o_top, 0-border_right, border_top, self.inner_arc_divisor)
            mesh_contours.append(mesh_points)
            top_extra_padding.append(arc_edge_shorter)
            right_extra_padding.append(arc_edge_shorter)
        elif border_right:
            mesh_contours.append(self.generate_rounded_box(i_right, o_top, o_right, mid_y + cut_right_top, round_tl=self.rounding, round_tr=self.rounding, round_limit=self.rounding_limit))
        elif border_top:
            mesh_contours.append(self.generate_rounded_box(mid_x + cut_top_right, o_top, o_right, i_top, round_tr=self.rounding, round_br=self.rounding, round_limit=self.rounding_limit))

        #bottom-left area
        if border_left and border_bottom:
            arc_edge_shorter, mesh_points = self.generate_arc_corner(o_left, mid_y - cut_left_bottom, mid_x - cut_bottom_left, o_bottom, border_left, 0-border_bottom, self.inner_arc_divisor)
            mesh_contours.append(mesh_points)
            bottom_extra_padding.append(arc_edge_shorter)
            left_extra_padding.append(arc_edge_shorter)
        elif border_left:
            mesh_contours.append(self.generate_rounded_box(o_left, mid_y - cut_left_bottom, i_left, o_bottom, round_bl=self.rounding, round_br=self.rounding, round_limit=self.rounding_limit))
        elif border_bottom:
            mesh_contours.append(self.generate_rounded_box(o_left, i_bottom, mid_x - cut_bottom_left, o_bottom, round_tl=self.rounding, round_bl=self.rounding, round_limit=self.rounding_limit))

        #bottom-right area
        if border_right and border_bottom:
            arc_edge_shorter, mesh_points = self.generate_arc_corner(o_right, mid_y - cut_right_bottom, mid_x + cut_bottom_right, o_bottom, 0-border_right, 0-border_bottom, self.inner_arc_divisor)
            mesh_contours.append(mesh_points)
            bottom_extra_padding.append(arc_edge_shorter)
            right_extra_padding.append(arc_edge_shorter)
        elif border_right:
            mesh_contours.append(self.generate_rounded_box(i_right, mid_y - cut_right_bottom, o_right, o_bottom, round_bl=self.rounding, round_br=self.rounding, round_limit=self.rounding_limit))
        elif border_bottom:
            mesh_contours.append(self.generate_rounded_box(mid_x - cut_bottom_right, i_bottom, o_right, o_bottom, round_tr=self.rounding, round_br=self.rounding, round_limit=self.rounding_limit))

        tess = Tesselator()
        for contour in mesh_contours:
            if contour:
                tess.add_contour(contour)
        success = tess.tesselate()
        self.canvas.before.clear()
        self.canvas.before.add(Color(rgba=self.border_color))
        if success:
            for vertices, indices in tess.meshes:
                self.canvas.before.add(Mesh(vertices=vertices, indices=indices, mode="triangle_fan"))

        if self.extra_padding:
            self.padding = border_left + max(left_extra_padding), border_top + max(top_extra_padding), border_right + max(right_extra_padding), border_bottom + max(bottom_extra_padding)
        else:
            self.padding = border_left, border_top, border_right, border_bottom
        self._redraw_cache = None


class LCARSBox(BoxLayout, LCARSLayout):
    pass


class Test(App):
    def build(self):
        return Builder.load_string(KV)
Test().run()