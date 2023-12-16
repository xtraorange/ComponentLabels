from Logger import Logger
from elements import Element
from reportlab.lib.utils import ImageReader
from utilities import Image
import io
import os

class ImageElement(Element):

    _attributes = {
        'image_name': (str, None),
        'image_folder': (str, "images"),
        'image_path': (str, ""),
        'resize_mode': (str, "auto"),
        'target_width': (int, None),
        'target_height': (int, None),
        'transparency_replacement_color': (str, "#FFFFFF")
    }

    def __init__(self, image_name=None):
        super().__init__()
        self.image_name = image_name

    def _render_self(self, canvas):
        image = Image(self.image_name, self.image_path, self.image_folder)

        if self.target_width is None:
            self.target_width = canvas.width   
        if self.target_height is None:
            self.target_height = canvas.height

        image.resize(self.resize_mode, self.target_width, self.target_height)

        # Calculate x, y positions based on alignment
        img_width, img_height = image.get_image_size()
        x, y = self.calculate_alignment(img_width, img_height, canvas.width, canvas.height, self.horizontal_align, self.vertical_align)

        image.remove_transparency(self.transparency_replacement_color)

        canvas.drawImage(ImageReader(image.get_BytesIO()), x, y, img_width, img_height)

