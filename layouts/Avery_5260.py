from .layout import Layout
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch

class Avery_5260(Layout):
    def __init__(self):
        super().__init__(
                paper_name="Avery 5260",
                pagesize=LETTER,
                sticker_width=(2 + 5/8) * inch,
                sticker_height=1 * inch,
                sticker_corner_radius=0.1 * inch,
                left_margin=3/16 * inch,
                top_margin=0.5 * inch,
                horizontal_stride=(2 + 6/8) * inch,
                vertical_stride=1 * inch,
                num_stickers_horizontal=3,
                num_stickers_vertical=10
        )