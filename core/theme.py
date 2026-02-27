from kivy.utils import get_color_from_hex

class Theme:
    PRIMARY = "#667eea"
    ACCENT = "#764ba2"
    BACKGROUND = "#1a1a2e"
    LIGHT = "#e94560"

    @staticmethod
    def hex_to_rgb(hex_color: str):
        return get_color_from_hex(hex_color)

    @classmethod
    def primary_rgba(cls):
        return cls.hex_to_rgb(cls.PRIMARY)

    @classmethod
    def accent_rgba(cls):
        return cls.hex_to_rgb(cls.ACCENT)

    @classmethod
    def bg_rgba(cls):
        return cls.hex_to_rgb(cls.BACKGROUND)

    @classmethod
    def light_rgba(cls):
        return cls.hex_to_rgb(cls.LIGHT)
