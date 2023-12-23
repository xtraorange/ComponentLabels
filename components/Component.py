# components/Component.pyUNIT
from decimal import Decimal
from Logger import Logger
from utilities import TypedAttributes
import math
import re

class Component(TypedAttributes):
    _attributes = {
        'value': (float, None),
        'decimal_precision': (int, 3),
        'schematic_symbol': (str, None),
        'maintain_user_input': (bool, False),
        '_title': (str, None),
        '_formatted_value': (str, None),
        'base_unit_exponent': (int, 0),
        '_integer_scientific_notation': (str, None),
        '_integer_scientific_notation_value': (float, None),
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



    @property
    def label(self):
        return f"{self.label_coefficient}{self.label_unit_prefix}"



    @property
    def label_coefficient(self):
        coefficient, exponent = self._calculate_label_coefficient_and_exponent()
        return coefficient
    
    @property
    def label_exponent(self):
        coefficient, exponent = self._calculate_label_coefficient_and_exponent()
        return exponent
    
    @property
    def label_unit_prefix(self):
        coefficient, exponent = self._calculate_label_coefficient_and_exponent()
        return self._get_unit_prefix(exponent)


    @property
    def scientific_notation(self):
        # Format the value in scientific notation directly
        sci_notation_str = "{:e}".format(self.value)

        # Split into mantissa and exponent parts
        mantissa, exponent_str = sci_notation_str.split('e')

        # Remove trailing zeros from the mantissa
        mantissa = mantissa.rstrip('0').rstrip('.')  # Remove trailing zeros and the decimal point if it's all zeros

        # Reconstruct the scientific notation string
        updated_sci_notation_str = f"{mantissa}e{exponent_str}"

        return updated_sci_notation_str
    
    @property
    def coefficient(self):
        return float(self.scientific_notation.split('e')[0])
    
    @property
    def exponent(self):
        return int(self.scientific_notation.split('e')[1])

    @property
    def integer_scientific_notation(self):
        if(self.value == self._integer_scientific_notation_value):
            return self._integer_scientific_notation

        # Get the scientific notation string
        sci_notation_str = self.scientific_notation

        # Split into mantissa and exponent parts
        mantissa, exponent_str = sci_notation_str.split('e')
        exponent = int(exponent_str)

        # Remove the decimal point from the mantissa
        decimal_position = mantissa.find('.')
        mantissa = mantissa.replace('.', '')
        if decimal_position != -1:
            exponent  = exponent + decimal_position - len(mantissa)

        # Construct the integer-based scientific notation string
        integer_sci_notation_str = f"{mantissa}e{exponent}"

        self._integer_scientific_notation = integer_sci_notation_str
        self._integer_scientific_notation_value = self.value

        return integer_sci_notation_str


      
    @property
    def integer_coefficient(self):
        return int(self.integer_scientific_notation.split('e')[0])
    
    @property
    def integer_exponent(self):
        return int(self.integer_scientific_notation.split('e')[1])



    def get_modified_notation(self, significant_digits, digits_left_of_decimal=1):
        mantissa = str(self.integer_coefficient)
        exponent = self.integer_exponent


        negative = False
        if mantissa.find('-') != -1:
            negative = True
            mantissa = mantissa.replace('-', '')

        if len(mantissa) > significant_digits:
            adjustment = len(mantissa) - significant_digits
            mantissa = mantissa[:significant_digits] + '.' + mantissa[significant_digits:]
            mantissa = float(mantissa)
            mantissa = round(mantissa)
            mantissa = str(mantissa)
            exponent = exponent + adjustment

            # Rounding may have added a digit:
            if len(mantissa) > significant_digits:
                mantissa = mantissa[:significant_digits] + '.' + mantissa[significant_digits:]
                mantissa = float(mantissa)
                mantissa = round(mantissa)
                mantissa = str(mantissa)
                exponent = exponent + 1




        while len(mantissa) < digits_left_of_decimal:
            mantissa = mantissa + '0'
            exponent = exponent - 1

        if len(mantissa) > digits_left_of_decimal:
            adjustment = len(mantissa) - digits_left_of_decimal
            mantissa = mantissa[:digits_left_of_decimal] + '.' + mantissa[digits_left_of_decimal:]
            exponent += adjustment

        if(len(mantissa.replace(".", "")) < significant_digits):
            # search mantissa for decimal point
            decimal_index = mantissa.find('.')
            if decimal_index == -1:
                mantissa = mantissa + '.'
            
            while(len(mantissa.replace(".", "")) < significant_digits):
                mantissa = mantissa + '0'

        if negative:
            mantissa = '-' + mantissa

        return mantissa, exponent




    def _parse_value(self, value_str):
        # Remove leading and trailing spaces
        value_str = value_str.strip()

        # Remove spaces within the string
        value_str = value_str.replace(" ", "")

        match = re.match(r"(\d*\.?\d+)([pnumkMG]?)", value_str)
        if not match:
            raise ValueError(f"Invalid value format: {value_str}")
            

        numeric_value_str, unit = match.groups()
        numeric_value = Decimal(numeric_value_str)
        
        if unit in Component.UNIT_PREFIXES:
            exponent = Component.UNIT_PREFIXES[unit]
            if self.maintain_user_input:
                self.coefficient = float(numeric_value)
                self.exponent = exponent
                self.unit_prefix = unit
                return float(numeric_value * (10 ** exponent))
            else:
                return float(numeric_value * (10 ** exponent))
        else:
            raise ValueError(f"Invalid unit prefix: {unit}")
        

    def _get_unit_prefix(self, exponent):
        for unit, unit_exponent in self.UNIT_PREFIXES.items():
            if exponent == unit_exponent:
                return unit
        Logger.warning("No valid unit prefix found.")
        return ""




    def _calculate_label_coefficient_and_exponent(self):
        if self.value == 0 or self.value is None:
            return 0, 0

        # Calculate the initial exponent
        initial_exponent = math.floor(math.log10(abs(self.value)))

        # Adjust exponent to a multiple of 3 for standard unit prefixes
        if initial_exponent >= self.base_unit_exponent:
            exponent = 3 * math.floor((initial_exponent - self.base_unit_exponent) / 3) + self.base_unit_exponent
        else:
            exponent = 3 * math.ceil((initial_exponent - self.base_unit_exponent) / 3) + self.base_unit_exponent

        # Adjust coefficient based on the new exponent
        coefficient = self.value / (10 ** exponent)

        coefficient = "{:g}".format(coefficient)
        coefficient = coefficient.lstrip('0') if coefficient != '0' else coefficient

        return coefficient, exponent