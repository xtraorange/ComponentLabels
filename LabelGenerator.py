#!/usr/bin/env python3

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.lib.colors import black, toColor, HexColor, gray


from ResistorValue import ResistorValue
from PaperConfig import PaperConfig, AVERY_5260, AVERY_L7157, EJ_RANGE_24
from StickerRect import StickerRect

import sys

from typing import Union, Optional, List

ResistorList = List[Union[Optional[float], List[Optional[float]]]]


def load_font(font_name: str) -> None:
    pdfmetrics.registerFont(TTFont('Arial Bold', font_name))
    print("Using font '{}' ...".format(font_name))


if "--roboto" in sys.argv:
    try:
        load_font('Roboto-Bold.ttf')
    except TTFError as e:
        print("Error: {}".format(e))
        exit(1)

else:
    for font_name in ['ArialBd.ttf', 'Arial_Bold.ttf']:
        try:
            load_font(font_name)
            break
        except TTFError:
            pass
    else:
        print("Error: Unable to load font 'Arial Bold'.")
        print("If you are on Ubuntu, you can install it with:")
        print("    sudo apt install ttf-mscorefonts-installer")
        print("Alternatively, use the 'Roboto' font by invoking this script with")
        print("the '--roboto' flag.")
        print("On Mac OS the '--roboto' flag is mandatory because this script currently")
        print("does not support Arial on Mac OS.")
        exit(1)













def begin_page(c: Canvas, layout: PaperConfig, draw_outlines: bool) -> None:
    # Draw the outlines of the stickers. Not recommended for the actual print.
    if draw_outlines:
        render_outlines(c, layout)


def end_page(c: Canvas) -> None:
    c.showPage()


def render_stickers(
    c: Canvas,
    layout: PaperConfig,
    values: ResistorList,
    draw_outlines: bool,
    draw_center_line: bool,
    draw_both_sides: bool
) -> None:
    def flatten(elem: Union[Optional[float], List[Optional[float]]]) -> List[Optional[float]]:
        if isinstance(elem, list):
            return elem
        else:
            return [elem]

    # Flatten
    values_flat: List[Optional[float]] = [elem for nested in values for elem in flatten(nested)]

    # Set the title
    c.setTitle(f"Resistor Labels - {layout.paper_name}")

    # Begin the first page
    begin_page(c, layout, draw_outlines)

    for (position, value) in enumerate(values_flat):
        rowId = (position // layout.num_stickers_horizontal) % layout.num_stickers_vertical
        columnId = position % layout.num_stickers_horizontal

        # If we are at the first sticker of a new page, change the page
        if rowId == 0 and columnId == 0 and position != 0:
            end_page(c)
            begin_page(c, layout, draw_outlines)

        if value is not None:
            draw_resistor_sticker(c, layout, rowId, columnId, value, draw_center_line, False)
            if draw_both_sides:
                draw_resistor_sticker(c, layout, rowId, columnId, value, False, True)

    # End the page one final time
    end_page(c)


def render_outlines(c: Canvas, layout: PaperConfig) -> None:
    for row in range(layout.num_stickers_vertical):
        for column in range(layout.num_stickers_horizontal):
            with StickerRect(c, layout, row, column, False) as rect:
                c.setStrokeColor(black, 0.1)
                c.setLineWidth(0)
                c.roundRect(rect.left, rect.bottom, rect.width, rect.height, rect.corner)


def main() -> None:

    # ############################################################################
    # Select the correct type of paper you want to print on.
    # ############################################################################
    layout = AVERY_5260
    # layout = AVERY_L7157
    # layout = EJ_RANGE_24

    # ############################################################################
    # Put your own resistor values in here!
    #
    # This has to be either a 2D grid or a 1D array.
    #
    # Add "None" if no label should get generated at a specific position.
    # ############################################################################
    resistor_values: ResistorList = [
        [0,            0.02,         .1],
        [1,            12,           13],
        [210,          220,          330],
        [3100,         3200,         3300],
        [41000,        42000,        43000],
        [510000,       None,         530000],
        [6100000,      6200000,      6300000],
        [71000000,     72000000,     73000000],
        [810000000,    820000000,    830000000],
        [9100000000,   9200000000,   3300000000],
    ]

    # ############################################################################
    # Further configuration options
    #
    # Change the following options as you desire.
    # ############################################################################

    # Enables drawing the resistor values on the other side of the sticker fold line
    # as well, so that the finished resistor plastic bags are labeled on both sides.
    draw_both_sides = False

    # Draws the line where the stickers should be folded.
    # Disable this if you don't like the line.
    draw_center_line = True

    # Draw the outlines of the stickers.
    # This is primarily a debugging option and should most likely not be enabled
    # for the actual printing.
    draw_outlines = False

    # ############################################################################
    # PDF generation
    #
    # The following is the actual functionality of this script - to generate
    # the ResistorLabels PDF file.
    # ############################################################################

    # Create the render canvas
    c = Canvas("ResistorLabels.pdf", pagesize=layout.pagesize)

    # Render the stickers
    render_stickers(c, layout, resistor_values, draw_outlines, draw_center_line, draw_both_sides)

    # Store canvas to PDF file
    c.save()


if __name__ == "__main__":
    main()
