from Logger import Logger
from elements import Element
from reportlab.lib.utils import ImageReader
from utilities import Image
import io

class QRCodeElement(Element):
    _attributes = {
        'data': (str, ""),
        'size': (str, "auto"),
    }

    def __init__(self, data):
        super().__init__()
        self.data = data
        return

    def _render_self(self, canvas):
        try:
            import qrcode
            qr_lib = qrcode
        except ImportError:
            pass
        if qr_lib is None:
            raise RuntimeError("QR code library not installed. Please install it to use QR code features using the command 'pip install qrcode[pil]'")
        

        # Determine the size based on the smaller of width and height
        if self.size == 'auto':
            Logger.debug(f"Setting size to the minumum of {canvas.width} and {canvas.height}")
            size = min(canvas.width, canvas.height)
        else:
            Logger.debug(f"Setting size to {self.size}")
            size = self.size

        qr = Image()
        qr.create_qr_code(self.data, size)

        x, y = self.calculate_alignment(size, size, canvas.width, canvas.height, self.horizontal_align, self.vertical_align)

        canvas.drawImage(ImageReader(qr.get_BytesIO()), x, y, size, size)

        return
