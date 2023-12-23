from components import Resistor
from .template import Template
from elements import TextElement, ResistorElement, LineElement
class FinomnisStub(Template):
    _attributes = {
        'component': (Resistor, None),
    }
    def __init__(self, component):
        super().__init__()
        self.component = component
        self.grid_count_y = 4


    def _configure_elements(self, canvas):
        if self.component is None:
            return

        cell_x = self.cell_size_x
        cell_y = self.cell_size_y


        self.add_child(
            TextElement(self.component.label +  "<font size=70%> " +self.component.UNIT + "</font>")
            .set_position(.5 * cell_x, .5 * cell_y)
            .set_size(9.25 * cell_x, 3.5 * cell_y)
            .set_alignment("center", "middle")
            .configure(wrap = False, font_size = 22)
        )



        self.add_child(
            ResistorElement(self.component.value)
            .set_position(10 * cell_x, 2 * cell_y)
            .set_size(4.75 * cell_x, 1.5 * cell_y)
            .set_alignment("left")
            .configure(body_color = "tan", band_count = 4, unrepresentable_behavior = None)
        )

        self.add_child(
            ResistorElement(self.component.value)
            .set_position(15.25 * cell_x, 2 * cell_y)
            .set_size(4.75 * cell_x, 1.5 * cell_y)
            .set_alignment("right")
            .configure(unrepresentable_behavior = None)
        )

        self.add_child(
            TextElement(self.component.smd_3_digit_code)
            .set_position(10 * cell_x, .5 * cell_y)
            .set_size(3 * cell_x, 1 * cell_y)
            .set_alignment("left")
            .configure(font_size = 8)
        )

        self.add_child(
            TextElement(self.component.smd_4_digit_code)
            .set_position(13.5 * cell_x, .5 * cell_y)
            .set_size(3 * cell_x, 1 * cell_y)
            .set_alignment("center")
            .configure(font_size = 8)
        )

        self.add_child(
            TextElement(self.component.eia96_code)
            .set_position(17 * cell_x, .5 * cell_y)
            .set_size(3 * cell_x, 1 * cell_y)
            .set_alignment("right")
            .configure(font_size = 8)
        )
