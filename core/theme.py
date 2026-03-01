from kivy.event import EventDispatcher
from kivy.properties import ColorProperty
from kivy.utils import get_color_from_hex


class Theme(EventDispatcher):
    background = ColorProperty(get_color_from_hex("#1a1a2e"))
    primary = ColorProperty(get_color_from_hex("#667eea"))
    accent = ColorProperty(get_color_from_hex("#764ba2"))
    light = ColorProperty(get_color_from_hex("#e94560"))
    text = ColorProperty((1, 1, 1, 1))
