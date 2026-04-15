from kivy.uix.widget import Widget
from kivy.graphics import RenderContext, Color, Rectangle
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
import os

shader_header = '''
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 frag_color;
varying vec2 tex_coord0;

uniform float time;
uniform vec2 resolution;
uniform float pulse;
uniform float is_recording;
'''

shader_body = '''
void main() {
    vec2 uv = tex_coord0;
    vec2 center = vec2(0.5, 0.5);
    float dist = distance(uv, center);

    // Dynamic liquid glass effect
    float base_radius = 0.35;
    float pulse_factor = pulse * 0.05;
    if (is_recording > 0.5) {
        pulse_factor = pulse * 0.15 * (sin(time * 10.0) * 0.5 + 0.5);
    }

    float circle = smoothstep(base_radius + pulse_factor, base_radius - 0.02 + pulse_factor, dist);

    vec3 color = vec3(0.7, 0.85, 1.0) * circle;
    if (is_recording > 0.5) {
        color = vec3(0.9, 0.4, 0.4) * circle; // Reddish when recording
    }

    // Highlight
    float highlight = smoothstep(0.12, 0.0, distance(uv, center + vec2(-0.08, 0.08)));
    color += highlight * 0.5 * circle;

    // Refraction-like distortion simulation
    float border = smoothstep(base_radius + pulse_factor, base_radius + pulse_factor - 0.05, dist) -
                   smoothstep(base_radius + pulse_factor - 0.02, base_radius + pulse_factor - 0.07, dist);
    color += border * 0.3;

    gl_FragColor = vec4(color, circle * 0.9);
}
'''

class LiquidGlassOrb(Widget):
    pulse = NumericProperty(0)
    is_recording = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True,
                                    use_parent_modelview=True)
        self.canvas.shader.source = shader_header + shader_body
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (300, 300)
        Clock.schedule_interval(self.update_shader, 1 / 60.)

    def update_shader(self, dt):
        self.canvas['projection_mat'] = Window.render_context['projection_mat']
        self.canvas['time'] = Clock.get_boottime()
        self.canvas['resolution'] = list(map(float, self.size))
        self.canvas['pulse'] = float(self.pulse)
        self.canvas['is_recording'] = 1.0 if self.is_recording else 0.0

    def on_size(self, instance, value):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

    def on_pos(self, instance, value):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.is_recording = not self.is_recording
            return True
        return super().on_touch_down(touch)
