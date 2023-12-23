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

        if self.component is None:
            return


        self.add_child(
            TextElement(self.component.label +  "<font size=70%> " +self.component.UNIT + "</font>")
            .set_position(0, 0)
            .set_size(canvas.width, canvas.height)
            .set_alignment("center", "middle")
            .configure(wrap = False, font_size = 30)
        )
        