'''  A very basic shader widget example'''
from kivy import app
from kivy.uix.widget import Widget
from kivy.graphics import RenderContext, Rectangle

class ShaderWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas = RenderContext(use_parent_frag_modelview=True, use_parent_projection=True)  #Replace the canvas entirely with a custom render context that lets us set the shader
        self.canvas.shader.fs = '''
$HEADER$
uniform vec2 resolution;  //Use the resolution variable as set in python

void main(void) {
    float alpha_channel_rate = gl_FragCoord.x / resolution.x;  //Calculate a pixel color based on the passed-in data and horizontal pixel position
    vec4 color = vec4(1.0 - alpha_channel_rate, 0.0, alpha_channel_rate, 1.0);
    gl_FragColor = color;  //Assigns a color for each pixel
}'''
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size)  #Standin that holds the actual shader graphics
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *_):  #Ensure that variables are up-to-date when widget is changed
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.canvas['resolution'] = list(map(float, self.size))  #Update a variable for the shader

app.runTouchApp(ShaderWidget())