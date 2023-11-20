from Logger import Logger
from components import Component
from .template import Template
from elements import TextElement

class GeneralComponent(Template):
    def __init__(self, component:Component):
        super().__init__()
        self.component = component

    def config(self):
        self.grid_x_count = 21
        self.grid_y_count = 8

    def elements(self):
        self.add_grid_element(TextElement("Ajasdfadasdasdf fsasfd `asdfasdf 1a1sdfasdf 2asdfasdfadsf", wrap=True, auto_truncate=True, font_size='auto'), 1, 1, 19, 6)
    