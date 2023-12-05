from reportlab.pdfgen.canvas import Canvas as ReportLabCanvas
from reportlab.lib.colors import black, toColor
from Logger import Logger
from fonts import FontManager

class Canvas(ReportLabCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_name = "Helvetica"
        self.font_size = 12
        self.stroke_color = black
        self.fill_color = black
        self.current_width = self._pagesize[0]
        self.current_height = self._pagesize[1]
        self.state_stack = []  # Stack for saving states
        self.sub_canvas_stack = []  # Stack for sub-canvases
        self.development_mode = True


    def set_font_name(self, font_name):
        if font_name == self.font_name:
            return

        if font_name is None:
            return

        FontManager.load_font(font_name)
        self.font_name = font_name
        self.setFont(self.font_name, self.font_size)

    def set_font_size(self, font_size):
        if font_size == self.font_size:
            return
        
        if font_size is None:
            return

        self.font_size = font_size
        Logger.debug(f"Setting font size to {self.font_size}")
        self.setFont(self.font_name, self.font_size)

    def set_stroke_color(self, stroke_color):
        if stroke_color == self.stroke_color:
            return
            
        if stroke_color is None:    
            return

        self.stroke_color = stroke_color
        self.setStrokeColor(self.stroke_color)
    
    def set_fill_color(self, fill_color):
        if fill_color == self.fill_color:
            return
            
        if fill_color is None:    
            return
        self.fill_color = fill_color
        self.setFillColor(self.fill_color)
    

    def save_style_state(self):
        state = {
            "font_name": self.font_name,
            "font_size": self.font_size,
            "stroke_color": self.stroke_color,
            "fill_color": self.fill_color
        }
        self.state_stack.append(state)

    def restore_style_state(self):
        if self.state_stack:
            last_state = self.state_stack.pop()
            self.font_name = last_state["font_name"]
            self.font_size = last_state["font_size"]
            self.stroke_color = last_state["stroke_color"]
            self.fill_color = last_state["fill_color"]

            # Reapply the attributes to the canvas
            self.setFont(self.font_name, self.font_size)
            self.setFillColor(self.fill_color)
            self.setStrokeColor(self.stroke_color)

    def create_sub_canvas(self, x, y, width, height, shape="rectangle", radius=0, allow_overflow=False, rotate=None, draw_outline = False, outline_color = "#FF0000", outline_width = .5, background_color = None):
        Logger.info(f"Creating sub-canvas at position ({x}, {y}) with dimensions ({width}, {height})")
        # Core functionality for creating a sub-canvas

        if self.development_mode:
            # Draw an outline around the sub-canvas for development purposes
            Logger.info("Development mode enabled. Drawing outline around sub-canvas.")
            draw_outline = True
            if outline_color is None:
                outline_color = "#FF0000"
            if outline_width is None or outline_width < .5:
                outline_width = .5
        self.save_style_state()
        self.sub_canvas_stack.append((self.current_width, self.current_height))



        if draw_outline:
            path = self._create_path(shape, x + outline_width / 2, y + outline_width / 2, width - outline_width, height - outline_width, radius)
            self.setStrokeColor(toColor(outline_color))
            self.setLineWidth(outline_width) 
            self.drawPath(path, stroke=1, fill=0)  # Draw the outline
            x += outline_width
            y += outline_width
            width -= outline_width * 2
            height -= outline_width * 2
            radius = max(0, radius - outline_width / 2)  # Adjust the radius to account for the outline width


        # Set up the sub-canvas
        self.saveState()
        self.translate(x, y)
        if rotate is not None:
            self.rotate(rotate)

        if radius > 0:
            self.setLineWidth(radius)  # Set the line width to the radius for rounded corners

        path = self._create_path(shape, 0, 0, width, height, radius)

        if not allow_overflow:
            self.clipPath(path, stroke=0, fill=0)  # Common clipPath call

        
        if background_color is not None:
            self.setFillColor(toColor(background_color))  # White color for background
            self.drawPath(path, stroke=0, fill=1)  # Draw the background

        
        self.current_width, self.current_height = width, height
        
    def _create_path(self, shape, x, y, width, height, radius=0):
        path = self.beginPath()  # Shared path initialization
        if shape == "rectangle":
            path.rect(x, y, width, height)
        elif shape == "rounded_rectangle":
            path.roundRect(x, y, width, height, radius)
        elif shape == "ellipse":
            path.ellipse(x, y, width, height)
        return path


    def restore_canvas(self):
        if self.sub_canvas_stack:
            self.restoreState()  # Restore the state of the sub-canvas
            self.current_width, self.current_height = self.sub_canvas_stack.pop()
            self.restore_style_state()  # Restore saved font and color state