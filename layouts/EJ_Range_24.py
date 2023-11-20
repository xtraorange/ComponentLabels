from .layout import Layout
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

class EJ_Range_24(Layout):
    def __init__(self):
        super().__init__(
            paper_name="EJRange 24",
            pagesize=A4,
            sticker_width=63.5 * mm,
            sticker_height=33.9 * mm,
            sticker_corner_radius=2 * mm,
            left_margin=6.5 * mm,
            top_margin=13.2 * mm,
            horizontal_stride=66.45 * mm,
            vertical_stride=33.9 * mm,
            num_stickers_horizontal=3,
            num_stickers_vertical=8,
        )