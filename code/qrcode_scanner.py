import pyqrcode
import qrtools
from PIL import Image
# qr = pyqrcode.create("HORN O.K. PLEASE.")
# qr.png("/Users/grashin/video_detection/barcode_4.png", scale=6)

qr = qrtools.QR()
qr.decode(Image.open("/Users/grashin/video_detection/barcode_4.png"))
print (qr.data)