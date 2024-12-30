from typing import Union, Tuple
import random
import sys
import os
import ctypes

class Colorfy:
    """
    A utility class for working with colors in HEX and RGBA formats.
    Includes methods for color manipulation and analysis.
    """
    def __init__(self, color: Union[str, Tuple[int, int, int, int]]):
        """
        Initialize a Colorfy object with a HEX string or an RGBA tuple.
        
        Args:
            color (Union[str, Tuple[int, int, int, int]]): The color to initialize.
                Can be a HEX string (#RRGGBB) or an RGBA tuple (r, g, b, a).
        """
        self.hex = "#000000"
        self.rgba = (0, 0, 0, 255)
        self.r, self.g, self.b, self.a = 0, 0, 0, 255

        if isinstance(color, str) and color.startswith("#"):
            self.r, self.g, self.b = self._hex2rgb(color)
            self.a = 255  # Default alpha value
            self.hex = color
            self.rgba = (self.r, self.g, self.b, self.a)
        elif isinstance(color, tuple) and len(color) == 4:
            if not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
                raise ValueError("RGBA values must be integers between 0 and 255.")
            self.r, self.g, self.b, self.a = color
            self.rgba = color
            self.hex = self._rgb2hex((self.r, self.g, self.b))
        else:
            raise ValueError("Color must be a hex string (#RRGGBB) or an RGBA tuple (r, g, b, a).")
    
    @staticmethod
    def init():
        """
        ANSI codes initialization (especially for Windows).
        This function turns on text-formatting in Windows.
        """
        if sys.platform == "win32":
            try:
                std_output_handle = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
                mode = ctypes.c_uint32()
                ctypes.windll.kernel32.GetConsoleMode(std_output_handle, ctypes.byref(mode))
                ctypes.windll.kernel32.SetConsoleMode(std_output_handle, mode.value | 0x4)  # 0x4 - ENABLE_VIRTUAL_TERMINAL_PROCESSING
            except Exception as e:
                print(f"An error was occures while enabling ANSI codes support: {e}")

        else:
            pass

    def _hex2rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert a HEX color to an RGB tuple.
        
        Args:
            hex_color (str): HEX color string (#RRGGBB).
            
        Returns:
            Tuple[int, int, int]: The RGB representation.
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            raise ValueError("HEX color must be in the format #RRGGBB.")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def _rgb2hex(self, rgb: Tuple[int, int, int]) -> str:
        """
        Convert an RGB tuple to a HEX color.
        
        Args:
            rgb (Tuple[int, int, int]): RGB values.
            
        Returns:
            str: HEX color string (#RRGGBB).
        """
        return "#{:02X}{:02X}{:02X}".format(*rgb)

    def gc(self) -> str:
        """
        Get the ANSI escape code for the color.
        
        Returns:
            str: ANSI escape code string.
        """
        return f"\033[38;2;{self.r};{self.g};{self.b}m"

    def apply(self, text: str) -> str:
        """
        Apply the color to a given text using ANSI escape codes.
        
        Args:
            text (str): The text to colorize.
            
        Returns:
            str: The colorized text.
        """
        return f"{self.gc()}{text}\033[0m"

    # New Methods with Definitions

    def comp(self) -> 'Colorfy':
        """
        Get the complementary color (inverted RGB).
        
        Returns:
            Colorfy: The complementary color.
        """
        return Colorfy((255 - self.r, 255 - self.g, 255 - self.b, self.a))

    def brighten(self, factor: float) -> 'Colorfy':
        """
        Adjust the brightness of the color by a factor.
        
        Args:
            factor (float): Brightness factor (>1 to increase, <1 to decrease).
            
        Returns:
            Colorfy: The brightened color.
        """
        new_r = min(255, max(0, int(self.r * factor)))
        new_g = min(255, max(0, int(self.g * factor)))
        new_b = min(255, max(0, int(self.b * factor)))
        return Colorfy((new_r, new_g, new_b, self.a))

    def set_alpha(self, a: int) -> 'Colorfy':
        """
        Set a new alpha (transparency) value.
        
        Args:
            a (int): Alpha value (0-255).
            
        Returns:
            Colorfy: The color with updated alpha.
        """
        if not (0 <= a <= 255):
            raise ValueError("Alpha must be between 0 and 255.")
        return Colorfy((self.r, self.g, self.b, a))

    def blend(self, other: 'Colorfy', ratio: float) -> 'Colorfy':
        """
        Blend the color with another color.
        
        Args:
            other (Colorfy): The other color to blend with.
            ratio (float): Blending ratio (0-1).
            
        Returns:
            Colorfy: The blended color.
        """
        if not 0 <= ratio <= 1:
            raise ValueError("Ratio must be between 0 and 1.")
        new_r = int(self.r * (1 - ratio) + other.r * ratio)
        new_g = int(self.g * (1 - ratio) + other.g * ratio)
        new_b = int(self.b * (1 - ratio) + other.b * ratio)
        new_a = int(self.a * (1 - ratio) + other.a * ratio)
        return Colorfy((new_r, new_g, new_b, new_a))

    def gray(self) -> 'Colorfy':
        """
        Convert the color to grayscale.
        
        Returns:
            Colorfy: The grayscale color.
        """
        #convert using a grayscale formula
        gray = int(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
        return Colorfy((gray, gray, gray, self.a))

    def is_bright(self) -> bool:
        """
        Check if the color is considered "bright."
        
        Returns:
            bool: True if bright, False otherwise.
        """
        luminance = 0.299 * self.r + 0.587 * self.g + 0.114 * self.b
        return luminance > 128

    def hsl(self) -> Tuple[float, float, float]:
        """
        Convert the color to HSL format.
        
        Returns:
            Tuple[float, float, float]: The HSL representation.
        """
        r, g, b = self.r / 255, self.g / 255, self.b / 255
        max_c, min_c = max(r, g, b), min(r, g, b)
        l = (max_c + min_c) / 2
        if max_c == min_c:
            h = s = 0
        else:
            delta = max_c - min_c
            s = delta / (2 - max_c - min_c) if l > 0.5 else delta / (max_c + min_c)
            if max_c == r:
                h = (g - b) / delta + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / delta + 2
            elif max_c == b:
                h = (r - g) / delta + 4
            h /= 6
        return (h * 360, s * 100, l * 100)

    @staticmethod
    def rand() -> 'Colorfy':
        """
        Generate a random color.
        
        Returns:
            Colorfy: A random color.
        """
        return Colorfy((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255))
        
    

    def dist(self, other: 'Colorfy') -> float:
        """
        Calculate the Euclidean distance to another color in RGB space.
        
        Args:
            other (Colorfy): The other color.
            
        Returns:
            float: The color distance.
        """
        return ((self.r - other.r) ** 2 + (self.g - other.g) ** 2 + (self.b - other.b) ** 2) ** 0.5

    def css(self) -> str:
        """
        Get the CSS RGBA string representation of the color.
        
        Returns:
            str: CSS string in the format 'rgba(r, g, b, a)'.
        """
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a / 255:.2f})"

class Palette:
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    YELLOW = "#FFFF00"
    CYAN = "#00FFFF"
    MAGENTA = "#FF00FF"

    class Catppuccin:
        class Latte:
            ROSEWATER = "#dc8a78"
            FLAMINGO = "#dd7878"
            PINK = "#ea76cb"
            MAUVE = "#8839ef"
            RED = "#d20f39"
            MAROON = "#e64553"
            PEACH = "#fe640b"
            YELLOW = "#df8e1d"
            GREEN = "#40a02b"
            TEAL = "#179299"
            SKY = "#04a5e5"
            SAPPHIRE = "#209fb5"
            BLUE = "#1e66f5"
            LAVENDER = "#7287fd"
            TEXT = "#4c4f69"
            SUBTEXT1 = "#5c5f77"
            SUBTEXT0 = "#6c6f85"
            OVERLAY2 = "#7c7f93"
            OVERLAY1 = "#8c8fa1"
            OVERLAY0 = "#9ca0b0"
            SURFACE2 = "#acb0be"
            SURFACE1 = "#bcc0cc"
            SURFACE0 = "#ccd0da"
            BASE = "#eff1f5"
            MANTLE = "#e6e9ef"
            CRUST = "#dce0e8"

        class Frappe:
            ROSEWATER = "#f2d5cf"
            FLAMINGO = "#eebebe"
            PINK = "#f4b8e4"
            MAUVE = "#ca9ee6"
            RED = "#e78284"
            MAROON = "#ea999c"
            PEACH = "#ef9f76"
            YELLOW = "#e5c890"
            GREEN = "#a6d189"
            TEAL = "#81c8be"
            SKY = "#99d1db"
            SAPPHIRE = "#85c1dc"
            BLUE = "#8caaee"
            LAVENDER = "#babbf1"
            TEXT = "#c6d0f5"
            SUBTEXT1 = "#b5bfe2"
            SUBTEXT0 = "#a5adce"
            OVERLAY2 = "#949cbb"
            OVERLAY1 = "#838ba7"
            OVERLAY0 = "#737994"
            SURFACE2 = "#626880"
            SURFACE1 = "#51576d"
            SURFACE0 = "#414559"
            BASE = "#303446"
            MANTLE = "#292c3c"
            CRUST = "#232634"

        class Macchiato:
            ROSEWATER = "#f4dbd6"
            FLAMINGO = "#f0c6c6"
            PINK = "#f5bde6"
            MAUVE = "#c6a0f6"
            RED = "#ed8796"
            MAROON = "#ee99a0"
            PEACH = "#f5a97f"
            YELLOW = "#eed49f"
            GREEN = "#a6da95"
            TEAL = "#8bd5ca"
            SKY = "#91d7e3"
            SAPPHIRE = "#7dc4e4"
            BLUE = "#8aadf4"
            LAVENDER = "#b7bdf8"
            TEXT = "#cad3f5"
            SUBTEXT1 = "#b8c0e0"
            SUBTEXT0 = "#a5adcb"
            OVERLAY2 = "#939ab7"
            OVERLAY1 = "#8087a2"
            OVERLAY0 = "#6e738d"
            SURFACE2 = "#5b6078"
            SURFACE1 = "#494d64"
            SURFACE0 = "#363a4f"
            BASE = "#24273a"
            MANTLE = "#1e2030"
            CRUST = "#181926"

        class Mocha:
            ROSEWATER = "#f5e0dc"
            FLAMINGO = "#f2cdcd"
            PINK = "#f5c2e7"
            MAUVE = "#cba6f7"
            RED = "#f38ba8"
            MAROON = "#eba0ac"
            PEACH = "#fab387"
            YELLOW = "#f9e2af"
            GREEN = "#a6e3a1"
            TEAL = "#94e2d5"
            SKY = "#89dceb"
            SAPPHIRE = "#74c7ec"
            BLUE = "#89b4fa"
            LAVENDER = "#b4befe"
            TEXT = "#cdd6f4"
            SUBTEXT1 = "#bac2de"
            SUBTEXT0 = "#a6adc8"
            OVERLAY2 = "#9399b2"
            OVERLAY1 = "#7f849c"
            OVERLAY0 = "#6c7086"
            SURFACE2 = "#585b70"
            SURFACE1 = "#45475a"
            SURFACE0 = "#313244"
            BASE = "#1e1e2e"
            MANTLE = "#181825"
            CRUST = "#11111b"
            
    class Solarized:
        BASE03 = "#002b36"
        BASE02 = "#073642"
        BASE01 = "#586e75"
        BASE00 = "#657b83"
        BASE0 = "#839496"
        BASE1 = "#93a1a1"
        BASE2 = "#eee8d5"
        BASE3 = "#fdf6e3"
        YELLOW = "#b58900"
        ORANGE = "#cb4b16"
        RED = "#dc322f"
        MAGENTA = "#d33682"
        VIOLET = "#6c71c4"
        BLUE = "#268bd2"
        CYAN = "#2aa198"
        GREEN = "#859900"

    class Dracula:
        BACKGROUND = "#282a36"
        CURRENT_LINE = "#44475a"
        SELECTION = "#44475a"
        FOREGROUND = "#f8f8f2"
        COMMENT = "#6272a4"
        CYAN = "#8be9fd"
        GREEN = "#50fa7b"
        ORANGE = "#ffb86c"
        PINK = "#ff79c6"
        PURPLE = "#bd93f9"
        RED = "#ff5555"
        YELLOW = "#f1fa8c"

        class Pro:
            BACKGROUND = "#1e1f29"
            FOREGROUND = "#f8f8f2"
            COMMENT = "#6272a4"
            CYAN = "#8be9fd"
            GREEN = "#50fa7b"
            ORANGE = "#ffb86c"
            PINK = "#ff79c6"
            PURPLE = "#bd93f9"
            RED = "#ff5555"
            YELLOW = "#f1fa8c"

    class Monokai:
        BACKGROUND = "#272822"
        FOREGROUND = "#f8f8f2"
        COMMENT = "#75715e"
        RED = "#f92672"
        ORANGE = "#fd971f"
        YELLOW = "#e6db74"
        GREEN = "#a6e22e"
        CYAN = "#66d9ef"
        BLUE = "#268bd2"
        PURPLE = "#ae81ff"

        class Pro:
            BACKGROUND = "#2e2e2e"
            FOREGROUND = "#d6d6d6"
            COMMENT = "#797979"
            RED = "#f92672"
            ORANGE = "#fd971f"
            YELLOW = "#e6db74"
            GREEN = "#a6e22e"
            CYAN = "#66d9ef"
            BLUE = "#268bd2"
            PURPLE = "#ae81ff"
            
class Stylist:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    WNORMAL = "\033[22m" # normal weight text
    UNDLINE = "\033[4m"
    SWAP = "\033[7m"
    ITALIC = "\033[3m"
    STRIKETHROUGHT = "\033[9m"
