import math
from reportlab.lib.colors import HexColor, black, toColor, PCMYKColor, Color

from Logger import Logger
from components import Resistor
from .element import Element

class ResistorElement(Element):
    _attributes = {
        'resistor_value': (float, 0),
        'body_color': (str, "#92cce3"),
        'band_count': (int, 5),
        'tolerance_percentage': (str, "any"),
        'temperature_coefficient': (str, "any"),
        'unrepresentable_behavior': (str, None),
        # 'significant_digit_count': (int, None),

    }

    # Common resistor body colors
    BODY_COLORS = {
        "blue": "#92cce3",
        "tan": "#dfd995",
        "green": "#8ABD5E",
        "brown": "#9B6D4D",
        "grey": "#909090"
    }

    BAND_TABLE = {
        -2: {"hex": "#C0C0C0", "name": "silver", "metallic": True, "tolerance_percent": 10.0},
        -1: {"hex": "#FFD700", "name": "gold",   "metallic": True, "tolerance_percent": 5.0},
        0:  {"hex": "#000000", "name": "black",  "metallic": False, "tolerance_percent": 20.0, "temperature_coefficient": 250},
        1:  {"hex": "#964B00", "name": "brown",  "metallic": False, "tolerance_percent": 1.0, "temperature_coefficient": 100},
        2:  {"hex": "#FF3030", "name": "red",    "metallic": False, "tolerance_percent": 2.0, "temperature_coefficient": 50},
        3:  {"hex": "#FFA500", "name": "orange", "metallic": False, "tolerance_percent": 3.0, "temperature_coefficient": 15},
        4:  {"hex": "#FFFF00", "name": "yellow", "metallic": False, "tolerance_percent": 4.0, "temperature_coefficient": 25},
        5:  {"hex": "#00FF00", "name": "green",  "metallic": False, "tolerance_percent": .5, "temperature_coefficient": 20},
        6:  {"hex": "#0000FF", "name": "blue",   "metallic": False, "tolerance_percent": .25, "temperature_coefficient": 10},
        7:  {"hex": "#C520F6", "name": "violet", "metallic": False, "tolerance_percent": .1, "temperature_coefficient": 5},
        8:  {"hex": "#808080", "name": "grey",   "metallic": False, "tolerance_percent": .05, "temperature_coefficient": 1},
        9:  {"hex": "#FFFFFF", "name": "white",  "metallic": False}
    }


    def __init__(self, resistor_value):
        super().__init__()
        self.resistor_value = resistor_value




    def _render_self(self, canvas):

        if not self._is_representable(self.resistor_value, self._significant_digit_count()):
            Logger.info(f"Resistor value {self.resistor_value} cannot be accurately represented with {self.band_count} bands.")
            self._draw_resistor(canvas, [])
            return

        bands = self._generate_bands_table()
        
        #Empty bands if any are not set to none, wild, or a number in the range of the resistor color table
        for band in bands:
            if band is not None and band != "wildcard" and band not in ResistorElement.BAND_TABLE:
                bands = []
        


        

        self._draw_resistor(canvas, bands)



    def _draw_resistor(self, canvas, bands):
        if not bands and self.unrepresentable_behavior is None:
            return

        aspect_ratio = 3.2

        # Calculate the maximum size of the resistor that fits in the available space
        width = min(canvas.width, canvas.height * aspect_ratio)
        height = width / aspect_ratio

        # Calculate the position to center the resistor
        x = (canvas.width - width) / 2
        y = (canvas.height - height) / 2


        corner_radius = height / 4

        canvas.create_sub_canvas(x, y, width, height, 'rounded_rectangle', corner_radius, draw_outline = True, outline_color = "#000000")
        canvas.linearGradient(canvas.width/2, canvas.height, canvas.width/2, 0, (toColor("#ffffff"), toColor(self.body_color)))

        # if bands is empty, call draw unpresentable resistor method
        if not bands:
            if self.unrepresentable_behavior == "draw_x":
                canvas.setStrokeColor(toColor("black"))
                canvas.setLineWidth(.75)

                height_offset = canvas.height/15 # to adjust for the oval not allowing the x to hit the right spot

                canvas.line(0, height_offset, canvas.width, canvas.height - height_offset)
                canvas.line(0, canvas.height - height_offset, canvas.width, height_offset)
        else:   
            # Render the background, color codes, and additional details
            self._draw_resistor_color_codes(canvas, canvas.width, canvas.height, bands)


        canvas.restore_canvas()


    def _is_representable(self, resistor_value, significant_digit_count):
        """
        Check if the resistor value can be represented with the given number of significant figures.
        """
        normalized_value = resistor_value
        while normalized_value >= 10:
            normalized_value /= 10
        while normalized_value < 1 and normalized_value != 0:
            normalized_value *= 10

        normalized_value *= 10 ** (significant_digit_count - 1)
        return int(normalized_value) == normalized_value
    
        #check if the resistor exponent exists


    def _significant_digit_count(self):
        """
        Calculate the number of significant figures for the band count.
        """
        return 2 if self.band_count in [3, 4] else 3

    def _generate_bands_table(self):
        if self.resistor_value == 0:
            # A single black band in the middle for 0 ohm
            return [None, None, 0, None, None]


        # Determine the number of significant figures
        significant_digit_count = self._significant_digit_count()

        # Extract significant digits and multiplier
        significant_digits, multiplier_band = Resistor.calculate_significant_digits_and_multiplier(self.resistor_value, significant_digit_count)

        # Determine tolerance and temperature coefficient bands
        tolerance_band = self._find_matching_band(self.tolerance_percentage, "tolerance_percent") if self.tolerance_percentage != "any" else "wildcard"
        temperature_band = self._find_matching_band(self.temperature_coefficient, "temperature_coefficient") if self.temperature_coefficient != "any" else "wildcard"

        # Construct the bands array
        bands = significant_digits + [multiplier_band]

        if self.band_count <= 4:
            bands.append(None)

        bands.append(tolerance_band)

        if self.band_count == 6:
            bands.append(temperature_band)


        Logger.debug(f"Generated bands: {bands}")
        return bands




    def _find_matching_band(self, parameter, parameter_name):
        if parameter is None:
            return None
        for num in range(-2, 10):
            value = ResistorElement.BAND_TABLE[num]
            if parameter_name in value and value[parameter_name] == parameter:
                return num
        return None



    def _draw_resistor_color_codes(self, canvas, width, height, bands):
        # Calculate spacing and positions for the bands
        stripe_unit = width / 12
        working_width = width - (1.5 * stripe_unit) * 2
        band_count = len(bands)

        padding = (working_width - stripe_unit * band_count) / (band_count - 1)
        x_positions = [1.5 * stripe_unit + i * (stripe_unit + padding) for i in range(band_count)]

        # Draw the bands
        for x, color_value in zip(x_positions, bands):
            self._draw_resistor_band(canvas, x, 0, stripe_unit, height, color_value)






    def _draw_resistor_band(self, canvas, x, y, band_width, band_height, color_value=None, draw_outline = True):
        if(color_value == None):
            return
        if(color_value == "wildcard"):
            self._draw_wild_resistor_band(canvas, x, y, band_width, band_height)
        else:
            try:
                band_data = ResistorElement.BAND_TABLE[color_value]
            except:
                ValueError("Invalid resistor color value: " + str(color_value))
                return
            
            color = HexColor(band_data["hex"])
            metallic = band_data["metallic"]

            if metallic:
                # Metallic shine effect with gradient
                highlight_position = 0.66  # Highlight at two-thirds up the band
                highlight_width = 0.2  # Highlight spans 20% of the band height

                # Apply the linear gradient
                self._draw_metallic_shine(canvas, x, y, band_width, band_height, color, highlight_position, highlight_width)
            else:
                # Solid color band
                canvas.setFillColor(color)
                canvas.rect(x, y, band_width, band_height, fill=1, stroke=0)
    
        if draw_outline:
            canvas.setLineWidth(.3)  # You can adjust the thickness of the outline
            canvas.setStrokeColorRGB(0.2, 0.2, 0.2, 0.5)
            canvas.line(x, y, x, y + band_height)
            canvas.line(x + band_width, y, x + band_width, y + band_height)



    def _lighten_color(self, color, percentage):
        """
        Lightens the given color by a given percentage.
        """
        assert 0 <= percentage <= 1, "Percentage must be between 0 and 1"
        
        if isinstance(color, Color):
            r, g, b = color.red, color.green, color.blue
        else:
            raise ValueError("Unsupported color type")

        # Calculate the lightened color
        r = min(1, r + r * percentage)
        g = min(1, g + g * percentage)
        b = min(1, b + b * percentage)

        # Return the new color
        return toColor((r, g, b))

    def _darken_color(self, color, percentage):
        """
        Darkens the given color by a given percentage.
        """
        assert 0 <= percentage <= 1, "Percentage must be between 0 and 1"
        
        if isinstance(color, Color):
            r, g, b = color.red, color.green, color.blue
        else:
            raise ValueError("Unsupported color type")

        # Calculate the darkened color
        r = max(0, r - r * percentage)
        g = max(0, g - g * percentage)
        b = max(0, b - b * percentage)

        # Return the new color
        return toColor((r, g, b))
    
    def _draw_metallic_shine(self, canvas, x, y, band_width, band_height, color, highlight_position, highlight_width):

        # Calculate the positions of the gradient transitions
        highlight_start = y + band_height * (highlight_position - highlight_width / 2)
        highlight_end = y + band_height * (highlight_position + highlight_width / 2)

        highlight_color = self._lighten_color(color, 0.2)
        background_color = self._darken_color(color, 0.2)

        # Ensure the highlight is within the bounds of the band
        highlight_start = max(y, min(highlight_start, y + band_height))
        highlight_end = max(y, min(highlight_end, y + band_height))

        Logger.debug(f"Band height: {band_height}, Highlight start: {highlight_start}, Highlight end: {highlight_end}")

        # Apply gradient in each section
        self._apply_gradient(canvas, x, y, band_width, highlight_start - y, background_color, background_color)
        self._apply_gradient(canvas, x, highlight_start, band_width, highlight_end - highlight_start, background_color, highlight_color)
        self._apply_gradient(canvas, x, highlight_end, band_width, y + band_height - highlight_end, highlight_color, background_color)

    def _apply_gradient(self, canvas, x, y, width, height, start_color, end_color):
        if height > 0:
            canvas.saveState()
            path = canvas.beginPath()
            path.rect(x, y, width, height)
            canvas.clipPath(path, stroke=0, fill=0)
            canvas.linearGradient(x, y, x, y + height, (start_color, end_color))
            canvas.restoreState()
            Logger.debug(f"Applying gradient from {start_color} to {end_color} at ({x}, {y}) with height {height} and width {width}")

    def _draw_wild_resistor_band(self, canvas, x, y, band_width, band_height, background="white", draw_x=True):
        canvas.setLineWidth(.3)  # You can adjust the thickness of the outline
        canvas.setStrokeColorRGB(0.2, 0.2, 0.2, 0.5)
        
        if background == "rainbow":
            stripe_colors = [HexColor("#FF3030"), HexColor("#FFA500"), HexColor("#00FF00"), HexColor("#0000FF"), HexColor("#FFFF00")]  # Example colors
            stripe_count = len(stripe_colors)
            stripe_height = band_height / stripe_count

            for i, color in enumerate(stripe_colors):
                stripe_y = y + i * stripe_height
                canvas.setFillColor(color)
                canvas.rect(x, stripe_y, band_width, stripe_height, fill=1, stroke=0)
        elif background is not None:
            canvas.setFillColor(toColor(background))
            canvas.rect(x, y, band_width, band_height, fill=1, stroke=0)
    
        if draw_x:
            # Draw an X from corner to corner
            canvas.line(x, y, x + band_width, y + band_height)
            canvas.line(x + band_width, y, x, y + band_height)
