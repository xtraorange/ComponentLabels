
from Logger import Logger
from components import Component

class Resistor(Component):
    _attributes = {
        
    }

    LABEL_CLASS = "ResistorLabel"  # Default label class
    UNIT = "\u2126"           # Unit of the component (e.g., Ohm, Farad)
    schematic_symbol = None  # Schematic symbol of the component
    NAME = "Resistor"

    MULTIPLIER_TABLE = {
        -3: "Z",
        -2: "Y",
        -1: "X",
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F"
    }
    EIA96_CODING_TABLE = {
        100: "01", 178: "25", 316: "49", 562: "73",
        102: "02", 182: "26", 324: "50", 576: "74",
        105: "03", 187: "27", 332: "51", 590: "75",
        107: "04", 191: "28", 340: "52", 604: "76",
        110: "05", 196: "29", 348: "53", 619: "77",
        113: "06", 200: "30", 357: "54", 634: "78",
        115: "07", 205: "31", 365: "55", 649: "79",
        118: "08", 210: "32", 374: "56", 665: "80",
        121: "09", 215: "33", 383: "57", 681: "81",
        124: "10", 221: "34", 392: "58", 698: "82",
        127: "11", 226: "35", 402: "59", 715: "83",
        130: "12", 232: "36", 412: "60", 732: "84",
        133: "13", 237: "37", 422: "61", 750: "85",
        137: "14", 243: "38", 432: "62", 768: "86",
        140: "15", 249: "39", 442: "63", 787: "87",
        143: "16", 255: "40", 453: "64", 806: "88",
        147: "17", 261: "41", 464: "65", 825: "89",
        150: "18", 267: "42", 475: "66", 845: "90",
        154: "19", 274: "43", 487: "67", 866: "91",
        158: "20", 280: "44", 499: "68", 887: "92",
        162: "21", 287: "45", 511: "69", 909: "93",
        165: "22", 294: "46", 523: "70", 931: "94",
        169: "23", 301: "47", 536: "71", 953: "95",
        174: "24", 309: "48", 549: "72", 976: "96",
        }
    

    @property
    def smd_3_digit_code(self):
        return self._get_smd_marking_code(3)

    @property
    def smd_4_digit_code(self):
        return self._get_smd_marking_code(4)
    
    @property
    def eia96_code(self):
        if self.value == 0:
            return "000"
        # write value in scientific notation
        significant_value, multiplier_band = self.get_modified_notation(3, 3)

        significant_value = int(significant_value)
        
        # Check if the significant value exists in the EIA-96 table
        if significant_value not in self.EIA96_CODING_TABLE:
            Logger.warning(f"EIA-96 code not found for significant value: {significant_value}")
            return ""

        # Retrieve the digits from the EIA-96 table
        digits = self.EIA96_CODING_TABLE[significant_value]


        # Find the minimum and maximum keys in the MULTIPLIER_TABLE
        min_key = min(self.MULTIPLIER_TABLE.keys())
        max_key = max(self.MULTIPLIER_TABLE.keys())

        # Check if multiplier_band is within the valid range
        if not (min_key <= multiplier_band <= max_key):
            Logger.warning(f"Invalid multiplier index for EIA-96 code: {multiplier_band}")
            return ""

        # Append the multiplier to the digits
        multiplier = self.MULTIPLIER_TABLE[multiplier_band]
        return digits + multiplier
    
    def _get_smd_marking_code(self, digit_count):
        if self.value is None:
            return ""
        
        value = self.value

        if value == 0:
            # return a number of zeroes equal to digit count
            return "0" * digit_count
        
        formatted_value = ""
       
        # If it uses the same number of digits, or more, of the digit count, we need to use a multiplier
        if value >= 10 ** (digit_count-1):
            formatted_value, exponent = self.get_modified_notation(digit_count-1, digit_count-1)
            formatted_value = formatted_value + str(exponent)

        # We know it's under 1 less the number of digits, so if it's an integer, simply add a zero (we left pad the zeros at the end)
        elif  value == float(int(self.value)):
            formatted_value = str(int(value)) + "0"
        
        # The lowest amount we can represent (other than zero) is RXXXXX1, where X is a number of zeroes equal to digit_count-2
        elif value >= 10 ** (-(digit_count-1)):
            # First we'll start with a normalized value
            formatted_value = str(self.coefficient)
            exponent = self.exponent

            formatted_value, exponent = self.get_modified_notation(digit_count-1)
            new_value = float(formatted_value) * 10 ** exponent


            # These first two statements check for rounding pushing us up to one of the previous conditions
            if(new_value >= 10 ** (digit_count-1)):
                formatted_value, exponent = self.get_modified_notation(digit_count-1, digit_count-1)
                formatted_value = formatted_value + str(exponent)
            elif new_value == float(int(new_value)):
                formatted_value = str(int(new_value)) + "0"
            else:
                # We know the decimal point is in the second position (1) because of scientific notation
                decimal_point_index = 1

                
                formatted_value = formatted_value.replace('.', '')

                new_decimal_point_index = decimal_point_index + exponent

                while(len(formatted_value) < new_decimal_point_index + 1):
                    formatted_value = formatted_value + "0"
                while(new_decimal_point_index) < 0:
                    formatted_value = "0" + formatted_value
                    new_decimal_point_index = new_decimal_point_index + 1

                # Add R into the string as the decimal point
                formatted_value = formatted_value[:new_decimal_point_index] + "R" + formatted_value[new_decimal_point_index:]

                # Strip zeroes from the end
                formatted_value = formatted_value.rstrip('0')

                if(len(formatted_value) < digit_count):
                    formatted_value = "0" + formatted_value
                
                while(len(formatted_value) < digit_count):
                    formatted_value = formatted_value + "0"

        else:
            Logger.warning(f"Value {self.value} is too small to be represented in {digit_count} digits.")

        # Add zeroes to the left to make the length equal to digit_count
        while(len(formatted_value) < digit_count):
            formatted_value = "0" + formatted_value

        return formatted_value   




