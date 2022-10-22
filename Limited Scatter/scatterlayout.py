import kivy
from kivy.uix.scatterlayout import ScatterLayout

class LimitedScatter(ScatterLayout):
    def on_transform_with_touch(self, touch):
        limit_pos = self.parent.pos
        limit_size = self.parent.size
        bbox = self.bbox
        pos = bbox[0]
        size = bbox[1]

        #Setup variables for horizontal check
        width = size[0]
        pos_x = pos[0]
        scale_x = width / self.width
        xmin = limit_pos[0]
        xmax = xmin + limit_size[0]
        local_left = pos_x
        local_right = local_left+width
        right_offset = xmax - local_right
        left_offset = local_left - xmin
        
        if right_offset >= 0 and left_offset >= 0:
            #scatter is smaller and inside the parent horizontally, do nothing
            pass
        elif right_offset > 0:
            #right side is out of bounds
            if self.scale > 1:
                #widget is scaled up, keep right side from going too far left
                pos_x = xmax - width
            else:
                #widget is scaled down, prevent right side from going too far right
                pos_x = xmin
        elif left_offset > 0:
            #left side is out of bounds
            if self.scale > 1:
                #widget is scaled up, prevent left side from going too far right
                pos_x = xmin
            else:
                #widget is scaled down, prevent left side from going too far left
                pos_x = xmax - width

        #Setup variables for vertical check
        height = size[1]
        pos_y = pos[1]
        scale_y = height / self.height
        ymin = limit_pos[1]
        ymax = ymin + limit_size[1]
        
        local_bottom = pos_y
        local_top = local_bottom+height
        top_offset = ymax - local_top
        bottom_offset = local_bottom - ymin

        if top_offset >= 0 and bottom_offset >= 0:
            #scatter is smaller and inside the parent vertically, do nothing
            pass
        elif top_offset > 0:
            #top side is out of bounds
            if height > self.height:
                #widget is scaled up, keep top side from going too far down
                pos_y = ymax - height
            else:
                #widget is scaled down, keep top side from going too far up
                pos_y = ymin
        elif bottom_offset > 0:
            #bottom side is out of bounds
            if height > self.height:
                #widget is scaled up, keep bottom side from going too far up
                pos_y = ymin
            else:
                #widget is scaled down, keep bottom side from going too far down
                pos_y = ymax - height
        newpos = (pos_x, pos_y)
        self.pos = newpos
