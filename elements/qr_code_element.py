from elements import Element
from reportlab.lib.utils import ImageReader
from utilities import Image
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
        super().render(canvas, width, height, horizontal_align, vertical_align)
        if self.qr is None:
            raise RuntimeError("QR code library not installed. Please install it to use QR code features using the command 'pip install qrcode[pil]'")
        
        # Determine the size based on the smaller of width and height
        if self.size == 'auto':
            size = min(width, height)
        else:
            size = self.size

        qr = Image()
        qr.create_qr_code(self.data, self.size)

        x, y = self.calculate_alignment(size, size, width, height, self.horizontal_align, self.vertical_align)

        canvas.drawImage(ImageReader(qr.get_BytesIO()), x, y, size, size)

        return
