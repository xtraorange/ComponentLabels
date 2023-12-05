from PIL import Image as PILImage
import qrcode
import os
import io

class Image():
    def __init__(self, image_name=None, image_path="", image_folder="images"):
        self.image_folder = image_folder
        self.image_path = image_path
        self.image_name = image_name
        self._image = None

        if self.image_name is not None:
            self._load_image()

    def _load_image(self):
        if self.image_name is None:
            raise ValueError("Image name not provided")

        image_path = os.path.join(self.image_folder, self.image_path, self.image_name)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        self._image = PILImage.open(image_path)

    def get_image(self):
        if self._image is None:
            raise RuntimeError("No image loaded or generated")
        return self._image
    

        
    
    def get_BytesIO(self, image_format='PNG'):
        if self._image is None:
            raise RuntimeError("No image loaded or generated")
        img_byte_arr = io.BytesIO()

        self._image.save(img_byte_arr, format=image_format)
        binary = img_byte_arr.getvalue()
        return io.BytesIO(binary)
    
    def get_image_size(self):
        if self._image is None:
            raise RuntimeError("No image loaded or generated")
        return self._image.size
    
    def resize(self, resize_mode="auto", width=None, height=None):
        if self._image is None:
            raise RuntimeError("No image loaded or generated")

        if resize_mode is None:
            return

        if resize_mode not in ["auto", "stretch"]:
            raise ValueError("Invalid resize mode")

        original_width, original_height = self._image.size
        target_width = int(width) if width is not None else int(original_width)
        target_height = int(height) if height is not None else int(original_height)

        if resize_mode == "auto":
            # Maintain aspect ratio
            aspect_ratio = min(target_width / original_width, target_height / original_height)
            new_width = int(original_width * aspect_ratio)
            new_height = int(original_height * aspect_ratio)
            self._image = self._image.resize((new_width, new_height), PILImage.LANCZOS)
        elif resize_mode == "stretch":
            self._image = self._image.resize((target_width, target_height), PILImage.LANCZOS)


    def create_qr_code(self, data, size):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=0,
        )
        qr.add_data(data)
        qr.make(fit=True)
        self._image = qr.make_image(fill_color="black", back_color="white").convert('RGB')



    def remove_transparency(self, replacement_color="#FFFFFF"):
        if self._image.mode in ('RGBA', 'LA') or (self._image.mode == 'P' and 'transparency' in self._image.info):
            background = PILImage.new(self._image.mode[:-1], self._image.size, replacement_color)
            background.paste(self._image, self._image.split()[-1])  # Split off the alpha channel
            self._image = background
