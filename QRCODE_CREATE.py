import qrcode
import cv2
data = "wenzhiyuan"
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