from components import Resistor
from .template import Template
from elements import TextElement, ResistorElement, LineElement

class MartinStumpfTemplate(Template):
    def __init__(self, component:Resistor):
        super().__init__()
        self.grid_x_count = 21
        self.grid_y_count = 8
        self.component = component


    def elements(self):
        self.add_grid_element(LineElement("horizontal", line_width=.7, stroke_color="#d8d8d8"), 0.5, 3.5, 20, 1)


        self.add_grid_element(TextElement(str(self.component.formatted_coefficient) + self.component.unit_prefix, wrap=False, auto_truncate=False, font_size=22), .5, .5, 7, 3.5, horizontal_align="right", vertical_align="bottom")
        self.add_grid_element(TextElement(self.component.UNIT, wrap=False, auto_truncate=True, font_size=15), 7.75, .6, 2, 2, horizontal_align="left", vertical_align="bottom")

        self.add_grid_element(ResistorElement(self.component.value, "tan", 4, unrepresentable_behavior="draw_x"), 10, 2, 4.75, 1.5, horizontal_align="left")
        self.add_grid_element(ResistorElement(self.component.value), 15.25, 2, 4.75, 1.5, horizontal_align="right")

        self.add_grid_element(TextElement(self.component.get_smd_3_digit_code(), font_size=8), 10, .5, 3, 1, horizontal_align="left")
        self.add_grid_element(TextElement(self.component.get_smd_4_digit_code(), font_size=8), 13.5, .5, 3, 1, horizontal_align="center")

        # self.add_grid_element(TextElement(self.component.get_smd_4_digit_code(), font_size=8), 17, .5, 3, 1, horizontal_align="right")
        self.add_grid_element(TextElement(self.component.get_eia96_code(), font_size=8), 17, .5, 3, 1, horizontal_align="right")


        self.add_grid_element(TextElement(str(self.component.formatted_coefficient) + self.component.unit_prefix, wrap=False, auto_truncate=False, font_size=22), .5, 5, 7, 3.5, horizontal_align="right", vertical_align="bottom")
        