
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
    


    def get_smd_3_digit_code(self):
        return self.get_smd_marking_code(3)

    def get_smd_4_digit_code(self):
        return self.get_smd_marking_code(4)
    
    def get_smd_marking_code(self, digit_count):
        formatted_value = ""
        
        if self.value == int(self.value) and self.value < 10 ^ (digit_count-1):
            formatted_value = f"{int(self.value)}0"
        else:

            significant_value_short, exponent_short = self.get_scientific_notation(self.value, digit_count-1, digit_count-1)
            significant_value_perfect, exponent_perfect = self.get_scientific_notation(self.value, digit_count, digit_count)
            
            # print(f"Value: {self.value} - {significant_value_short} - {significant_value_perfect} - {exponent_short} - {exponent_perfect}")

                # If the exponent is negative, the integer portion of the value is less than the digit count
            if exponent_perfect < 0:
                # Before trying to format, check to see if the short exponent is 0.  If so, show short value plus a 0 on the end
                
                
                if exponent_short == 0:
                    formatted_value = f"{int(significant_value_short)}0"
                else:
                    formatted_value  = f"{int(significant_value_short)}"
                    # Insert the R in the position it belongs, relative to the exponent
                    # This would be calculated by determing the last position of the full string (digit_count) + the exponent (which will be negative)
                    if exponent_perfect < 0:
                        position = digit_count + exponent_perfect
                        formatted_value = formatted_value[:position] + "R" + formatted_value[position:] 
            else:

                formatted_value = f"{int(significant_value_short)}"
                formatted_value += str(exponent_short)

        return formatted_value.zfill(digit_count)
        


    def get_eia96_code(self):
        if self.value == 0:
            return "000"
        # write value in scientific notation
        significant_value, multiplier_band = self.get_scientific_notation(self.value, 3, 3)

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



    
    @staticmethod
    def calculate_significant_digits_and_multiplier(resistor_value, significant_digit_count):
        normalized_value, exponent = Resistor._normalize_resistance(resistor_value, significant_digit_count)

        # Shift the decimal point to get the right number of significant digits
        shift = significant_digit_count - 1
        normalized_value *= 10 ** shift
        exponent -= shift

        # Get significant digits
        significant_digits = [int(normalized_value // 10**(significant_digit_count - i - 1)) % 10 for i in range(significant_digit_count)]

        # The exponent is now the multiplier band value
        multiplier_band = exponent

        return significant_digits, multiplier_band


    @staticmethod
    def _normalize_resistance(value, significant_digits):
        exponent = 0
        normalized_value = value
        while normalized_value >= 10:
            normalized_value /= 10
            exponent += 1
        while normalized_value < 1:
            normalized_value *= 10
            exponent -= 1
        normalized_value = round(normalized_value, significant_digits - 1)
        return normalized_value, exponent