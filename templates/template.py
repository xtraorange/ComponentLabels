from reportlab.lib.units import inch, mm
from reportlab.lib.colors import black
from utilities import DesignObject
from Logger import Logger

class Template (DesignObject):
    _attributes = {
        "grid_count_x": (float, 21),
        "grid_count_y": (float, 8),
        "cell_size_x": (float, 0),
        "cell_size_y": (float, 0),
    }


    def _configure_elements(self, canvas):
        pass


    def _pre_render(self, canvas):
        self.cell_size_x = canvas.width / self.grid_count_x
        self.cell_size_y = canvas.height / self.grid_count_y
        self._configure_elements(canvas)