from labels import Label, LabelConfig, LabelCanvas

class ResistorLabel(Label):
    def __init__(self, config: LabelConfig, value=None):
        super().__init__(config, value)

    def draw_custom_value(self, label_canvas: LabelCanvas):
        # Implement specific logic for drawing resistor bands or other specific details
        pass

    def resistor_color_table(num: int) -> HexColor:
        return [
            HexColor("#000000"),
            HexColor("#964B00"),
            HexColor("#FF3030"),
            HexColor("#FFA500"),
            HexColor("#FFFF00"),
            HexColor("#00FF00"),
            HexColor("#0000FF"),
            HexColor("#C520F6"),
            HexColor("#808080"),
            HexColor("#FFFFFF"),
        ][num]


    def draw_fancy_resistor_stripe(
        c: Canvas,
        x: float,
        y: float,
        width: float,
        height: float,
        color_table: List[HexColor]
    ) -> None:
        c.setFillColor(color_table[2])
        c.rect(x, y+height*5/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[1])
        c.rect(x, y+height*4/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[0])
        c.rect(x, y+height*3/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[1])
        c.rect(x, y+height*2/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[2])
        c.rect(x, y+height*1/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[3])
        c.rect(x, y+height*0/6, width, height/6, fill=1, stroke=0)


    def draw_resistor_stripe_border(c: Canvas, x: float, y: float, width: float, height: float) -> None:
        c.setLineWidth(0.3)
        c.setFillColor(black, 0.0)
        c.setStrokeColorRGB(0.2, 0.2, 0.2, 0.5)
        c.rect(x, y, width, height, fill=0, stroke=1)


    def draw_resistor_stripe(c: Canvas, x: float, y: float, width: float, height: float, stripe_value: int) -> None:
        if 0 <= stripe_value <= 9:
            c.setFillColor(resistor_color_table(stripe_value))
            c.rect(x, y, width, height, fill=1, stroke=0)
            draw_resistor_stripe_border(c, x, y, width, height)
            return

        elif stripe_value == -1:
            gold_table = [
                HexColor("#FFF0A0"),
                HexColor("#FFE55C"),
                HexColor("#FFD700"),
                HexColor("#D1B000"),
            ]

            draw_fancy_resistor_stripe(c, x, y, width, height, gold_table)
            draw_resistor_stripe_border(c, x, y, width, height)
            return

        elif stripe_value == -2:
            silver_table = [
                HexColor("#D0D0D0"),
                HexColor("#A9A9A9"),
                HexColor("#929292"),
                HexColor("#7B7B7B"),
            ]

            draw_fancy_resistor_stripe(c, x, y, width, height, silver_table)
            draw_resistor_stripe_border(c, x, y, width, height)
            return

        else:

            c.setLineWidth(0.5)
            c.setFillColor(gray, 0.3)
            c.setStrokeColorRGB(0.5, 0.5, 0.5, 1.0)
            c.rect(x, y, width, height, fill=1, stroke=1)
            c.line(x, y, x + width, y + height)
            c.line(x + width, y, x, y + height)
            return


    def draw_resistor_colorcode(
            c: Canvas,
            value: ResistorValue,
            color1: object,
            color2: object,
            x: float,
            y: float,
            width: float,
            height: float,
            num_codes: int
    ) -> None:

        if value.ohms_exp < num_codes - 4:
            return

        border = height/6
        corner = (height-2*border)/4

        c.saveState()
        p = c.beginPath()
        p.roundRect(x+border, y+border, width-2*border, height-2*border, corner)
        c.clipPath(p, stroke=0)
        c.linearGradient(x+width/2, y+border+height, x+width/2, y+border, (color1, color2))
        c.restoreState()

        width_without_corner = width - 2*border - 2*corner
        stripe_width = width_without_corner/10

        if value.ohms_val == 0:
            draw_resistor_stripe(c,
                                x + border + corner + stripe_width / 2 + 2 * stripe_width * 2,
                                y + border,
                                stripe_width,
                                height - 2 * border,
                                0)
        else:
            for i in range(num_codes):

                if i == num_codes - 1:
                    stripe_value = value.ohms_exp + 2 - num_codes
                else:
                    stripe_value = value.ohms_val
                    for _ in range(2-i):
                        stripe_value //= 10
                    stripe_value %= 10

                draw_resistor_stripe(c,
                                    x + border + corner + stripe_width / 2 + 2 * stripe_width * i,
                                    y + border,
                                    stripe_width,
                                    height - 2 * border,
                                    stripe_value)

            draw_resistor_stripe(c,
                                x + width - border - corner - stripe_width * 1.5,
                                y + border,
                                stripe_width,
                                height - 2 * border,
                                -3)

        c.setFillColor(black)
        c.setStrokeColor(black, 1)
        c.setLineWidth(0.5)
        c.roundRect(x+border, y+border, width-2*border, height-2*border, corner)


    def draw_resistor_sticker(
        c: Canvas,
        layout: PaperConfig,
        row: int,
        column: int,
        ohms: float,
        draw_center_line: bool,
        mirror: bool
    ) -> None:
    with StickerRect(c, layout, row, column, mirror) as rect:

        # Squish horizontally by a bit, to prevent clipping
        rect.width -= 0.1*inch
        rect.left += 0.05*inch



        # Draw resistor value
        resistor_value = ResistorValue(ohms)
        print("Generating sticker '{}'".format(resistor_value.format_value()))

        value_font_size = 0.25 * inch
        ohm_font_size = 0.15 * inch
        smd_font_size = 0.08 * inch
        space_between = 5

        value_string = resistor_value.format_value()
        ohm_string = "\u2126"
        value_width = c.stringWidth(value_string, 'Arial Bold', value_font_size * 1.35)
        ohm_width = c.stringWidth(ohm_string, 'Arial Bold', ohm_font_size * 1.35)
        total_text_width = ohm_width + value_width + space_between
        text_left = rect.left + rect.width/4 - total_text_width/2
        text_bottom = rect.bottom + rect.height/4 - value_font_size/2

        c.setFont('Arial Bold', value_font_size * 1.35)
        c.drawString(text_left, text_bottom, value_string)
        c.setFont('Arial Bold', ohm_font_size * 1.35)
        c.drawString(text_left + value_width + space_between, text_bottom, ohm_string)

        # Draw resistor color code
        draw_resistor_colorcode(c, resistor_value,
                                toColor("hsl(55, 54%, 100%)"), toColor("hsl(55, 54%, 70%)"),
                                rect.left + rect.width/2,
                                rect.bottom + rect.height/4 - rect.height/45,
                                rect.width/4, rect.height/4,
                                3)

        draw_resistor_colorcode(c, resistor_value,
                                toColor("hsl(197, 59%, 100%)"), toColor("hsl(197, 59%, 73%)"),
                                rect.left + rect.width * 0.75,
                                rect.bottom + rect.height/4 - rect.height/45,
                                rect.width/4, rect.height/4,
                                4)

        c.setFont('Arial Bold', smd_font_size * 1.35)
        c.drawString(rect.left + rect.width/2 + rect.width/32, rect.bottom +
                     rect.height/13, get_3digit_code(resistor_value))
        c.drawCentredString(rect.left + rect.width*3/4, rect.bottom +
                            rect.height/13, get_4digit_code(resistor_value))
        c.drawRightString(rect.left + rect.width - rect.width/32, rect.bottom +
                          rect.height/13, get_eia98_code(resistor_value))