from Logger import Logger
from components import Component
from .template import Template
from elements import LineElement, ImageElement, QRCodeElement, TextElement, ResistorElement

class GeneralComponent(Template):
    _attributes = {
        'component': (Component, None),
    }

    def __init__(self, component):
        super().__init__()
        self.component = component
        


    def _configure_elements(self, canvas):
        #self.add_grid_element(TextElement("A", wrap=True, auto_truncate=True, font_size=15), 1, 1, 19, 6)
        # self.add_grid_element(QRCodeElement("https://www.reportlab.com", 10), 1, 1, 5, 6)
        #self.add_grid_element(ImageElement("image.png", "stretch"), 1, 1, 5, 6, horizontal_align="center", vertical_align="middle")
        #self.add_grid_element(ResistorElement(self.component.value), 1, 1, 5, 3)

       

        # test = LineElement().set_position(10,10).set_size(100,100)
        # test = ImageElement("image.png").set_position(10,10).set_size(50,50)
        # test = QRCodeElement("XXXXXXXXXXXXXXXXXXXXXXXXX").set_position(10,10).set_size(50,50)
        # test = TextElement("Test of this element").set_position(10,10).set_size(50,50)
        # test = ResistorElement(self.component.value).set_position(10,10).set_size(50,50)
        # self.add_child(test)
        pass
        