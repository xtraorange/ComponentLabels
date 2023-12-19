# components/Component.pyUNIT
from Logger import Logger
from utilities import TypedAttributes
import math
import re

class Component(TypedAttributes):
    _attributes = {
        'value': (float, None),
        'coefficient': (float, None),
        'exponent': (int, None),
        'unit_prefix': (str, ""),
        'decimal_precision': (int, 3),
        'schematic_symbol': (str, None),
        'maintain_user_input': (bool, False),
        '_title': (str, None),
        '_formatted_value': (str, None),
    }

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
        super().__init__()

        if isinstance(value, str):
            self.value = self._parse_value(value)
        else:
            self.value = value
        if(self.coefficient is None or self.exponent is None or self.unit_prefix is None):
            self.set_value_attributes()
        
        Logger.debug(f"Component: {self.NAME} - {self.value} - {self.coefficient} - {self.exponent} - {self.unit_prefix}")



    @property
    def title(self):
        if self._title is None:
            return self.formated_value
        else:
            return self._title
    
    @title.setter
    def title(self, value):
        self._title = value


    @property
    def formated_value(self):
        if self._formatted_value is None:
            coefficient_formatted_value = "{:g}".format(self.coefficient)
            return coefficient_formatted_value + " " + self.unit_prefix + self.UNIT
        else:
            return self._formatted_value

    @formated_value.setter
    def formated_value(self, value):
        self._formatted_value = value


    @property
    def formatted_coefficient(self):
        formatted_value = "{:g}".format(self.coefficient)
        return formatted_value.lstrip('0') if formatted_value != '0' else formatted_value


        

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
            if self.maintain_user_input:
                self.coefficient = numeric_value
                self.exponent = Component.UNIT_PREFIXES[unit]
                self.unit_prefix = unit
                return numeric_value * (10 ** self.exponent)
            else:
                return numeric_value * (10 ** Component.UNIT_PREFIXES[unit])
        else:
            raise ValueError(f"Invalid unit prefix: {unit}")
            Logger.error(f"Invalid unit prefix: {unit}")
        

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


    @staticmethod
    def get_scientific_notation(value, significant_digits, digits_left_of_decimal = 1):
        if value == 0:
            return 0, 0

        exponent = 0

        # Adjust the value to have the desired number of digits to the left of the decimal
        while value >= 10**digits_left_of_decimal:
            value /= 10
            exponent += 1
        while value < 10**(digits_left_of_decimal - 1):
            value *= 10
            exponent -= 1

        # Round to the desired number of significant digits
        # Calculate the number of digits after the decimal for rounding
        digits_after_decimal = significant_digits - digits_left_of_decimal
        coefficient = round(value, digits_after_decimal)

        return coefficient, exponent
