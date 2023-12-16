from Logger import Logger
from elements import Element


class LineElement(Element):

    _attributes = {
        'orientation': (str, "horizontal"),
        'line_width': (float, 0.5),
        'stroke_color': (str, "black"),
    }


    def _render_self(self, canvas):

        if self.orientation == "horizontal":
            x_start = 0
            x_stop = canvas.width
            y_start = canvas.height / 2
            y_stop = y_start
            
        elif self.orientation == "vertical":
            x_start = canvas.width / 2
            x_stop = x_start
            y_start = 0
            y_stop = canvas.height
            

        canvas.setLineWidth(self.line_width)
        canvas.setStrokeColor(self.stroke_color)

        canvas.line(x_start, y_start, x_stop, y_stop)
