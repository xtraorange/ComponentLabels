
from components import Component

class Resistor(Component):
    LABEL_CLASS = "ResistorLabel"  # Default label class
    UNIT = "\u2126"           # Unit of the component (e.g., Ohm, Farad)
    schematic_symbol = None  # Schematic symbol of the component

    def __init__(self, value=None):
        super().__init__(value)  # Call the parent constructor

        self.resistance = value  # Resistance value in ohms

        #calculate coefficient and exponent


