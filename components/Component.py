# components/Component.pyUNIT
from Logger import Logger
import math
import re

class Component():
    LABEL_CLASS = "Label"  # Default label class
    UNIT = ""             # Unit of the component
    BASE_UNIT_PREFIX = ""  # Base unit prefix of the component (what values are typically based on)
    value = None         # Value of the component
    coefficient = None   # Coefficient of the component
    exponent = None      # Exponent of the component
    unit_prefix = ""     # Unit prefix of the component
    decimal_precision = 2  # Decimal precision of the component
    schematic_symbol = None  # Schematic symbol of the component

    UNIT_PREFIXES = {
        "a": -18,  # atto
        "f": -15,  # femto
        "p": -12,  # pico
        "n": -9,   # nano
        "u": -6,   # micro
        "m": -3,   # milli
        "": 0,     # None
        "k": 3,    # kilo
        "M": 6,    # Mega
        "G": 9,     # Giga
        "T": 12,    # Tera
        "P": 15,    # Peta
    }

    def __init__(self, value=None):
        self.coefficient = None
        self.exponent = None
        self.unit_prefix = None
        self.schematic_symbol = None
        if isinstance(value, str):
            self.value = self._parse_value(value)
        else:
            self.value = value
        if(self.coefficient is None or self.exponent is None or self.unit_prefix is None):
            self.set_value_attributes()


    def _parse_value(self, value_str):
        # Remove leading and trailing spaces
        value_str = value_str.strip()

        # Remove spaces within the string
        value_str = value_str.replace(" ", "")

        match = re.match(r"(\d*\.?\d+)([pnumkMG]?)", value_str)
        if not match:
            Logger.error(f"Invalid value format: {value_str}")
            raise ValueError(f"Invalid value format: {value_str}")
            

        numeric_value, unit = match.groups()
        numeric_value = float(numeric_value)
        
        if unit in Component.UNIT_PREFIXES:
            self.coefficient = numeric_value
            self.exponent = Component.UNIT_PREFIXES[unit]
            self.unit_prefix = unit
            return numeric_value * (10 ** self.exponent)
        else:
            return numeric_value
        

    def set_value_attributes(self):
        base_unit_exponent = Component.UNIT_PREFIXES.get(self.UNIT, 0)
        
        if self.value == 0 or self.value is None:
            self.coefficient = 0
            self.unit_prefix = ""
            self.exponent = 0
            return

        # Calculate the initial exponent and temporary coefficient
        initial_exponent = math.floor(math.log10(self.value))
        significant_figures = round( self.value  / math.pow(10, initial_exponent - ( self.decimal_precision - 1)))
        coefficient = significant_figures / math.pow(10, ( self.decimal_precision - 1 ))
        print(f"initial_exponent: {initial_exponent}")
        if (initial_exponent < base_unit_exponent):
            self.exponent = math.ceil((initial_exponent + 1) / 3) * 3	
        else:
            self.exponent = math.floor(initial_exponent / 3) * 3

        # Round the coefficient to the desired precision
        rounding_value = 3 if self.decimal_precision <= 3 else self.decimal_precision
        self.coefficient = round(coefficient * math.pow(10, initial_exponent - self.exponent), rounding_value)


        # Determine the unit prefix
        self.unit_prefix = self._get_unit_prefix(self.exponent)

    def _get_unit_prefix(self, exponent):
        for unit, unit_exponent in self.UNIT_PREFIXES.items():
            if exponent == unit_exponent:
                return unit
        Logger.warning("No valid unit prefix found.")
        return ""



    def print_attributes(self):
        coefficient_formatted_value = "{:g}".format(self.coefficient)
        print(f"Value: {self.value}, Coefficient: {coefficient_formatted_value}, "
              f"Exponent: {self.exponent}, Unit Prefix: {self.unit_prefix}")