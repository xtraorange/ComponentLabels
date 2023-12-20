from components import Resistor
from .generator import Generator
from templates import FinomnisTemplate, Blank

class FinomnisExampleGenerator(Generator):
    resistor_values = [
        0,            0.02,         .1,
        1,            12,           13,
        210,          220,          330,
        3100,         3200,         3300,
        41000,        42000,        43000,
        510000,       None,         530000,
        6100000,      6200000,      6300000,
        71000000,     72000000,     73000000,
        810000000,    820000000,    830000000,
        9100000000,   9200000000,   3300000000,
    ]

    def generate(self):
        if self.template is None:
            self.template = FinomnisTemplate
        
        for value in self.resistor_values:
            if value is None:
                self._add_label(Blank())
            else:
                self._add_label(self.template(Resistor(value)))

        return self.labels
        
