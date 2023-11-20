from .layout import Layout
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

class Avery_L7157(Layout):
    def __init__(self):
        super().__init__(
            paper_name="Avery L7157",
            pagesize=A4,
            sticker_width=64 * mm,
            sticker_height=24.3 * mm,
            sticker_corner_radius=3 * mm,
            left_margin=6.4 * mm,
            top_margin=14.1 * mm,
            horizontal_stride=66.552 * mm,
            vertical_stride=24.3 * mm,
            num_stickers_horizontal=3,
            num_stickers_vertical=11,
        )