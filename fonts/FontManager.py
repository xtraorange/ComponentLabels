from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from Logger import Logger
import os

class FontManager:
    loaded_fonts = set()
    standard_fonts = {"Helvetica", "Times-Roman", "Courier", "Symbol", "ZapfDingbats"}
    font_folder = "fonts"

    @staticmethod
    def load_font(font_name):
        if font_name is None:
            return

        # Check if the font is a standard font or already loaded
        if font_name in FontManager.standard_fonts or font_name in FontManager.loaded_fonts:
            return True

        Logger.info(f"Loading font '{font_name}'")
        # Attempt to load the font from the file
        font_path = os.path.join(FontManager.font_folder, font_name + '.ttf')
        if not os.path.exists(font_path):
            Logger.error(f"Font file not found: {font_path}")
            return False

        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            FontManager.loaded_fonts.add(font_name)
            return True
        except Exception as e:
            Logger.error(f"Failed to load font: {e}")
            return False

