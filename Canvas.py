from reportlab.pdfgen.canvas import Canvas as ReportLabCanvas
from reportlab.lib.colors import black
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

    def create_sub_canvas(self, x, y, width, height, shape="rectangle", radius=0, allow_overflow=False, draw_outline=True):
        Logger.info(f"Creating sub-canvas at position ({x}, {y}) with dimensions ({width}, {height})")
        # Core functionality for creating a sub-canvas
        self.save_style_state()
        self.sub_canvas_stack.append((self.current_width, self.current_height))

        # Set up the sub-canvas
        self.saveState()
        self.translate(x, y)
        path = self.beginPath()  # Shared path initialization

        # Apply clipping based on shape
        if shape == "rectangle":
            path.rect(0, 0, width, height)
        elif shape == "rounded_rectangle":
            path.roundRect(0, 0, width, height, radius)
        elif shape == "ellipse":
            path.ellipse(0, 0, width, height)

        if not allow_overflow:
            self.clipPath(path, stroke=0, fill=0)  # Common clipPath call

        # Draw an outline for debugging if requested
        if draw_outline:
            self.setStrokeColorRGB(1, 0, 0)  # Red color for visibility
            self.setLineWidth(1)  # Set a visible stroke width
            self.drawPath(path, stroke=1, fill=0)  # Draw the outline

        # Update current width and height
        self.current_width, self.current_height = width, height
        



    def restore_canvas(self):
        if self.sub_canvas_stack:
            self.restoreState()  # Restore the state of the sub-canvas
            self.current_width, self.current_height = self.sub_canvas_stack.pop()
            self.restore_style_state()  # Restore saved font and color state