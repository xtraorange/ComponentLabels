from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.units import inch, mm
from typing import Tuple

class Layout:
    def __init__(
        self,
        paper_name: str,
        pagesize: Tuple[float, float],
        sticker_width: float,
        sticker_height: float,
        sticker_corner_radius: float,
        left_margin: float,
        top_margin: float,
        horizontal_stride: float,
        vertical_stride: float,
        num_stickers_horizontal: int,
        num_stickers_vertical: int,
    ) -> None:
        self.paper_name = paper_name
        self.pagesize = pagesize
        self.sticker_width = sticker_width
        self.sticker_height = sticker_height
        self.sticker_corner_radius = sticker_corner_radius
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.horizontal_stride = horizontal_stride
        self.vertical_stride = vertical_stride
        self.num_stickers_horizontal = num_stickers_horizontal
        self.num_stickers_vertical = num_stickers_vertical