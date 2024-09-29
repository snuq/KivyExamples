'''Updated and simplified version of Kivy's plasma shader example.  Shows a more complex and auto-updating shader'''
from kivy import app
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.graphics import RenderContext

class ShaderWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas = RenderContext(use_parent_frag_modelview=True, use_parent_projection=True)  #Replace the canvas entirely with a custom render context that lets us set the shader
        Clock.schedule_interval(self.update_glsl, 1 / 60.)  #Set up the update function to animate the shader
        self.canvas.shader.fs = '''
$HEADER$
uniform vec2 resolution;
uniform float time;

void main(void)
{
   vec4 frag_coord = frag_modelview_mat * gl_FragCoord;
   float x = frag_coord.x;
   float y = frag_coord.y;
   float mov0 = x+y+cos(sin(time)*2.)*100.+sin(x/100.)*1000.;
   float mov1 = y / resolution.y / 0.2 + time;
   float mov2 = x / resolution.x / 0.2;
   float c1 = abs(sin(mov1+time)/2.+mov2/2.-mov1-mov2+time);
   float c2 = abs(sin(c1+sin(mov0/1000.+time)
              +sin(y/40.+time)+sin((x+y)/100.)*3.));
   float c3 = abs(sin(c2+cos(mov1+mov2+c2)+cos(mov2)+sin(x/1000.)));
   gl_FragColor = vec4( c1,c2,c3,1.0);
}'''
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size)  #Standin that holds the actual shader graphics
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *_):  #Ensure that variables are up-to-date when widget is changed
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.canvas['resolution'] = list(map(float, self.size))  #Update a variable for the shader

    def update_glsl(self, *_):
        self.canvas['time'] = Clock.get_boottime()
        win_rc = Window.render_context  #This is needed for the default vertex shader.
        self.canvas['projection_mat'] = win_rc['projection_mat']
        self.canvas['modelview_mat'] = win_rc['modelview_mat']
        self.canvas['frag_modelview_mat'] = win_rc['frag_modelview_mat']

app.runTouchApp(ShaderWidget())