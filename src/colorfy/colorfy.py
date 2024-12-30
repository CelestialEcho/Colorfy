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