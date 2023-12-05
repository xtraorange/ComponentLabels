from Logger import Logger
from elements import Element
from reportlab.lib.utils import ImageReader
from utilities import Image
import io
import os

class ImageElement(Element):
    def __init__(self, image_name, resize_mode="auto", target_width=None, target_height=None, transparency_replacement_color="#FFFFFF", image_path="", image_folder="images", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_name = image_name
        self.image_folder = image_folder
        self.image_path = image_path
        self.resize_mode = resize_mode
        self.target_width = target_width
        self.target_height = target_height
        self.transparency_replacement_color = transparency_replacement_color

    def render(self, canvas, width, height, horizontal_align, vertical_align):
        super().render(canvas, width, height, horizontal_align, vertical_align)
        
        image = Image(self.image_name, self.image_path, self.image_folder)

        if self.target_width is None:
            self.target_width = width   
        if self.target_height is None:
            self.target_height = height

        image.resize(self.resize_mode, self.target_width, self.target_height)

        # Calculate x, y positions based on alignment
        img_width, img_height = image.get_image_size()
        x, y = self.calculate_alignment(img_width, img_height, width, height, self.horizontal_align, self.vertical_align)

        image.remove_transparency(self.transparency_replacement_color)

        canvas.drawImage(ImageReader(image.get_BytesIO()), x, y, img_width, img_height)

