from Logger import Logger
from .template import Template
from elements import TextElement

class HelloWorld(Template):
    def config(self):
        pass

    def elements(self):
        Logger.info("Hello World")
        self.add_grid_element(TextElement("Hello World!"), 10, 5, 5, 3)
