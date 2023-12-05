from Logger import Logger
from elements import Element


class LineElement(Element):
    def __init__(self, orientation="horizontal", line_width = .5, stroke_color = "black", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = orientation
        self.line_width = line_width
        self.stroke_color = stroke_color


    def render(self, canvas, width, height, horizontal_align, vertical_align):
        super().render(canvas, width, height, horizontal_align, vertical_align)
        
        if self.orientation == "horizontal":
            x_start = 0
            x_stop = width
            y_start = height / 2
            y_stop = y_start
            
        elif self.orientation == "vertical":
            x_start = width / 2
            x_stop = x_start
            y_start = 0
            y_stop = height
            

        canvas.setLineWidth(self.line_width)
        canvas.setStrokeColor(self.stroke_color)

        canvas.line(x_start, y_start, x_stop, y_stop)
