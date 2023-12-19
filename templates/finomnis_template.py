from components import Resistor
from .template import Template
from elements import TextElement, ResistorElement, LineElement
from .finomnis_stub import FinomnisStub

class FinomnisTemplate(Template):
    _attributes = {
        'component': (Resistor, None),
        'draw_both_sides': (bool, False),
        'draw_center_line': (bool, True),
    }
    def __init__(self, component):
        super().__init__()
        self.component = component



    def _configure_elements(self, canvas):
        cell_x = self.cell_size_x
        cell_y = self.cell_size_y

        if self.draw_center_line:
            self.add_child(
                LineElement()
                .set_position(.5 * cell_x, 3.5 * cell_y)
                .set_size(20 * cell_x, 1 * cell_y)
                .configure(orientation = "horizontal", line_width = .7, stroke_color='#d8d8d8')
            )


        self.add_child(
            FinomnisStub(self.component)
            .set_position(0, 0)
            .set_size(21 * cell_x, 4 * cell_y)
        )

        if self.draw_both_sides:
            self.add_child(
                FinomnisStub(self.component)
                .set_position(21 * cell_x, 8 * cell_y)
                .set_size(21 * cell_x, 4 * cell_y)
                .rotate(180)
            )