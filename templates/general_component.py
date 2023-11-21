from Logger import Logger
from components import Component
from .template import Template
from elements import TextElement, QRCodeElement

class GeneralComponent(Template):
    def __init__(self, component:Component):
        super().__init__()
        self.component = component

    def config(self):
        self.grid_x_count = 21
        self.grid_y_count = 8

    def elements(self):
        self.add_grid_element(TextElement("A", wrap=True, auto_truncate=True, font_size=15), 1, 1, 19, 6)
        #self.add_grid_element(QRCodeElement("https://www.reportlab.com", 10), 1, 1, 5, 6)