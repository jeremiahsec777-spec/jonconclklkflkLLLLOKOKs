from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import RenderContext, Color, Rectangle
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

shader_header = '''
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 frag_color;
varying vec2 tex_coord0;

uniform float time;
uniform vec2 resolution;
'''

shader_body = '''
void main() {
    vec2 uv = tex_coord0;

    // Glassmorphism background effect
    vec3 color = vec3(1.0, 1.0, 1.0) * 0.1; // Base white tint
    float alpha = 0.2;

    // Add subtle frost/noise
    float noise = fract(sin(dot(uv.xy ,vec2(12.9898,78.233))) * 43758.5453);
    color += noise * 0.05;

    gl_FragColor = vec4(color, alpha);
}
'''

class GlassCard(MDCard):
    text = StringProperty("")
    title = StringProperty("Note")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = "16dp"
        self.spacing = "8dp"
        self.elevation = 0
        self.md_bg_color = [1, 1, 1, 0.1]
        self.radius = [24, 24, 24, 24]

        self.title_label = MDLabel(
            text=self.title,
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height="32dp"
        )
        self.content_label = MDLabel(
            text=self.text,
            theme_text_color="Secondary",
            valign="top"
        )
        self.content_label.bind(size=self.content_label.setter('text_size'))

        self.add_widget(self.title_label)
        self.add_widget(self.content_label)

    def on_title(self, instance, value):
        self.title_label.text = value

    def on_text(self, instance, value):
        self.content_label.text = value
