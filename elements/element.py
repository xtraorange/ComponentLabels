from Logger import Logger


class Element:
    def __init__(self):
        self.default_horizontal_align = "left"
        self.default_vertical_align = "bottom"

    def render(self, canvas, width, height, horizontal_align, vertical_align):
        Logger.debug("Rendering element using horizontal align: {}, vertical align: {}".format(horizontal_align, vertical_align))

        if horizontal_align is None:
            self.horizontal_align = self.default_horizontal_align
        else:
            self.horizontal_align = horizontal_align

        if vertical_align is None:
            self.vertical_align = self.default_vertical_align
        else:
            self.vertical_align = vertical_align

        Logger.debug("self.horizontal_align: {}, self.vertical_align: {}".format(self.horizontal_align, self.vertical_align))

    def calculate_alignment(self, object_width, object_height, canvas_width, canvas_height, horizontal_align="left", vertical_align="bottom"):
        x = self.calculate_horizontal_alignment(object_width, canvas_width, horizontal_align)

        y = self.calculate_vertical_alignment(object_height, canvas_height, vertical_align)

        return x, y
    

    def calculate_horizontal_alignment(self, object_width, canvas_width, horizontal_align="left"):
        if horizontal_align == "right":
            x = canvas_width - object_width
        elif horizontal_align == "center":
            x = (canvas_width - object_width) / 2
        elif horizontal_align == "left":
            x = 0
        else:
            raise ValueError(f"Invalid horizontal alignment: {horizontal_align}")

        return x

    def calculate_vertical_alignment(self, object_height, canvas_height, vertical_align="bottom"):
        if vertical_align == "top":
            y = canvas_height - object_height
        elif vertical_align == "middle":
            y = (canvas_height - object_height) / 2
        elif vertical_align == "bottom":
            y = 0
        else:
            raise ValueError(f"Invalid vertical alignment: {vertical_align}")

        return y