from kivy.event import EventDispatcher
from kivy.properties import ColorProperty, StringProperty
from kivy.utils import get_color_from_hex


class Theme(EventDispatcher):
    mode = StringProperty("dark")
    background = ColorProperty(get_color_from_hex("#1a1a2e"))
    primary = ColorProperty(get_color_from_hex("#667eea"))
    accent = ColorProperty(get_color_from_hex("#764ba2"))
    light = ColorProperty(get_color_from_hex("#e94560"))
    text = ColorProperty((1, 1, 1, 1))

    action_primary = ColorProperty(get_color_from_hex("#2563EB"))
    action_finish = ColorProperty(get_color_from_hex("#2E7D32"))
    action_danger = ColorProperty(get_color_from_hex("#C62828"))

    glass_primary = ColorProperty(get_color_from_hex("#4F8FF045"))
    glass_border = ColorProperty(get_color_from_hex("#FFFFFF40"))
    glass_finish = ColorProperty(get_color_from_hex("#00C85355"))

    def set_dark(self):
        self.mode = "dark"
        self.background = get_color_from_hex("#1a1a2e")
        self.primary = get_color_from_hex("#667eea")
        self.accent = get_color_from_hex("#764ba2")
        self.light = get_color_from_hex("#e94560")
        self.text = (1, 1, 1, 1)

    def set_light(self):
        self.mode = "light"
        self.background = get_color_from_hex("#f5f7ff")
        self.primary = get_color_from_hex("#4f46e5")
        self.accent = get_color_from_hex("#7c3aed")
        self.light = get_color_from_hex("#e11d48")
        self.text = (0.1, 0.1, 0.1, 1)
