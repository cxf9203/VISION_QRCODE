import win32print
import win32ui
from PIL import Image, ImageWin
import qrcode
import cv2
data = "sanxing dianji data info, date:2022/04/24"
img_file='code.jpg'
qr = qrcode.QRCode(version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_H,
                   box_size=10,border=4)
qr.add_data(data)
qr.make(fit=True)
img=qr.make_image()
img.save(img_file)
img = cv2.imread(img_file)
img = cv2.resize(img,(203,203))
img=cv2.imwrite("savedcode.jpg",img)
# 物理宽度、高度
PHYSICALWIDTH = 50
PHYSICALHEIGHT = 50
# 物理偏移位置

PHYSICALOFFSETX = 50
PHYSICALOFFSETY =50
printer_name = win32print.GetDefaultPrinter()
# 选择图片路径
file_name = "savedcode.jpg"

hDC = win32ui.CreateDC()
hDC.CreatePrinterDC(printer_name)
printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
# printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)
# 打开图片
bmp = Image.open(file_name)

print(bmp.size)
ratios = [1.0 * 1754 / bmp.size[0], 1.0 * 1240 / bmp.size[1]]
scale = min(ratios)
print(ratios)
print(scale)
hDC.StartDoc(file_name)
hDC.StartPage()

dib = ImageWin.Dib(bmp)

scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
print(scaled_width, scaled_height)
x1 = int((printer_size[0] - scaled_width) / 2)
y1 = int((printer_size[1] - scaled_height) / 2)
# 横向位置坐标
x1 = 1580
# 竖向位置坐标
y1 = 30
# 4倍为自适应图片实际尺寸打印
x2 = x1 + bmp.size[0] * 4
y2 = y1 + bmp.size[1] * 4
dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

hDC.EndPage()
hDC.EndDoc()
hDC.DeleteDC()
