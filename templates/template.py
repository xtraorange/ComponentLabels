from reportlab.lib.units import inch, mm
from reportlab.lib.colors import black

from Logger import Logger

class Template:
    def __init__(self):
        self.grid_x_count = 21
        self.grid_y_count = 8
        self.grid_elements = []
        self.direct_elements = []
        self.config()

    def config(self):
        pass


    def elements(self):
        pass


    def add_grid_element(self, element, x, y, width, height, horizontal_align=None, vertical_align=None):
        Logger.info("Adding grid element %s at (%s, %s, %s, %s, %s, %s)" % (element, x, y, width, height, horizontal_align, vertical_align))
        self.grid_elements.append((element, x, y, width, height, horizontal_align, vertical_align))

    def add_direct_element(self, element, x, y, width, height, horizontal_align=None, vertical_align=None):
        Logger.info("Adding direct element %s at (%s, %s, %s, %s, %s, %s)" % (element, x, y, width, height, horizontal_align, vertical_align))
        self.direct_elements.append((element, x, y, width, height, horizontal_align, vertical_align))

    def render(self, canvas, width, height):
        
        self.elements()

        # Render grid elements
        Logger.info("Rendering on to canvas of size %s, %s" % (width, height))
        grid_width = width / self.grid_x_count
        grid_height = height / self.grid_y_count
        Logger.info("Rendering grid elements with grid sizes of width: %s and height: %s...)" % (grid_width, grid_height))

        for element, x, y, width, height, horizontal_align, vertical_align in self.grid_elements:
            x_pt = x * grid_width
            y_pt = y * grid_height
            width_pt = width * grid_width
            height_pt = height * grid_height

            Logger.info("Rendering grid element %s at (%s, %s) with width: %s and height: %s" % (element, x_pt, y_pt, width_pt, height_pt))
            self._render_element(canvas, element, x_pt, y_pt, width_pt, height_pt, horizontal_align, vertical_align)

        Logger.info("Rendering direct elements...")
        # Render direct elements
        for element, x_pt, y_pt, width_pt, height_pt in self.direct_elements:
            Logger.info("Rendering direct element %s at (%s, %s) with width: %s and height: %s" % (element, x_pt, y_pt, width_pt, height_pt))
            self._render_element(canvas, element, x_pt, y_pt, width_pt, height_pt)

    def _render_element(self, canvas, element, x, y, width, height, horizontal_align=None, vertical_align=None):
        canvas.create_sub_canvas(x, y, width, height)
        element.render(canvas, width, height, horizontal_align, vertical_align)
        canvas.restore_canvas()

