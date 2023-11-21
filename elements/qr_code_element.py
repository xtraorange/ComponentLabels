from elements import Element
from reportlab.lib.utils import ImageReader
from PIL import Image
import io

class QRCodeElement(Element):
    def __init__(self, data, size="auto", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.qr = None
        self.size = size

        try:
            import qrcode
            self.qr = qrcode
        except ImportError:
            pass

    def render(self, canvas, width, height, horizontal_align, vertical_align):
        if self.qr is None:
            raise RuntimeError("QR code library not installed. Please install it to use QR code features using the command 'pip install qrcode[pil]'")
        
        # Determine the size based on the smaller of width and height
        if self.size == 'auto':
            size = min(width, height)
        else:
            size = self.size

        if horizontal_align is None:
            horizontal_align = "center"
        
        if vertical_align is None:
            vertical_align = "middle"

        qr = self.qr.QRCode(
            version=1,
            error_correction=self.qr.constants.ERROR_CORRECT_L,
            box_size=size,
            border=0
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        # Convert to PIL Image for consistency with other elements
        qr_image = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        

        # Convert the PIL Image to BytesIO for consistency with other elements
        img_byte_arr = io.BytesIO()
        qr_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        if horizontal_align == "right":
            x = int(width - size)
        elif horizontal_align == "center":
            x = int((width - size) / 2)
        else:
            x = 0


        if vertical_align == "top":
            y = int(height - size)
        elif vertical_align == "middle":
            y = int((height - size) / 2)
        else:
            y = 0

        canvas.drawImage(ImageReader(io.BytesIO(img_byte_arr)), x, y, size, size)

        return
