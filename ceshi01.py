# version:1.0.2022.0518
import gxipy as gx
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
import sanxing02
import procCallback
import procCallback as cb
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import cv2
import time
import qrcode
import win32print
import win32ui
import win32api
from PIL import Image, ImageWin
import numpy as np
import threading
import os
import openpyxl
from openpyxl.drawing.image import  Image as IMG
def print_label(Qinfo="need more information", number="444422"):#need string
    data=Qinfo
    img_file = 'code.jpg'
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(img_file)
    img = cv2.imread(img_file)
    img = cv2.resize(img, (200, 200))

    #############构建图片与文字#######################
    newImg = np.zeros((200, 360, 3), dtype=np.uint8)
    newImg[:] = [255, 255, 255]
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(newImg, 'SX(B4R8)', (200, 30), font, 0.8, (0, 0, 0), 1)
    cv2.putText(newImg, 'DC9721134A', (200, 55), font, 0.8, (0, 0, 0),1)
    cv2.putText(newImg, str(time.strftime('%Y%m%d', time.localtime(time.time()))), (200, 85), font,0.8, (0, 0, 0), 1)
    cv2.putText(newImg, str(number), (200, 100), font, 0.8, (0, 0, 0), 1)
    newImg[0:200, 0:200] = img
    newImg = cv2.imwrite("savedcode.jpg", newImg)

    #################打印机##############################

    # 物理宽度、高度
    PHYSICALWIDTH = 30
    PHYSICALHEIGHT = 30
    # 物理偏移位置

    PHYSICALOFFSETX = 30
    PHYSICALOFFSETY = 30
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
    x1 = 0
    # 竖向位置坐标
    y1 = 0
    # 4倍为自适应图片实际尺寸打印
    x2 = x1 + bmp.size[0] * 1
    y2 = y1 + bmp.size[1] * 1
    dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()
    print("finish print")
##############################create class for UI#############################
class MainCode(QMainWindow, sanxing02.Ui_mainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        sanxing02.Ui_mainWindow.__init__(self)
        self.setupUi(self)
        self.initial()
        self.painter = QPainter(self)
        self.lineEdit.textChanged.connect(self.textChanged0)
        self.lineEdit_2.textChanged.connect(self.textChanged2)
        self.lineEdit_3.textChanged.connect(self.textChanged3)
        self.lineEdit_4.textChanged.connect(self.textChanged4)
        self.lineEdit_5.textChanged.connect(self.textChanged5)
        self.lineEdit_6.textChanged.connect(self.textChanged6)
        self.lineEdit_7.textChanged.connect(self.textChanged7)
        self.lineEdit_8.textChanged.connect(self.textChanged8)
        self.lineEdit_10.textChanged.connect(self.textChanged10)
        self.camera1flag = False
        self.camera2flag = False
        self.print_sensor = threading.Thread(target=self.print_trig)
        self.print_sensor.start()
    def initial(self):
        self.label_10.setPixmap(QPixmap("blank01.jpg", ))
        self.label_11.setPixmap(QPixmap("blank01.jpg", ))
        self.label_12.setPixmap(QPixmap("blank01.jpg", ))
        self.triggerflag = False
        self.num = 0 #总数
        self.cam1good = 0
        self.cam1goodrate=0
        self.cam2good = 0
        self.cam2goodrate=0
        self.label_14.setText(str(self.num))
        self.label_24.setText(str(self.cam1good))
        self.label_22.setText(str(self.cam1goodrate))
        self.label_25.setText(str(self.cam2good))
        self.label_23.setText(str(self.cam2goodrate))
        self.triggerflag = False
        print("Initializing camera......")
        # create a device manager
        self.device_manager = gx.DeviceManager()
        dev_num, dev_info_list = self.device_manager.update_device_list()
        print(dev_info_list)
        if dev_num is 0:
            print("Number of enumerated devices is 0")
            return
        else:
            print("get device")
        # open the first device
        self.cam = self.device_manager.open_device_by_index(2)
        self.cam2 = self.device_manager.open_device_by_index(1)
        self.cam.TriggerMode.set(gx.GxSwitchEntry.ON)  # 设置触发条件 开启
        self.cam2.TriggerMode.set(gx.GxSwitchEntry.ON)  # 设置触发条件 开启
        # 监听line0当前状态
        self.cam.LineSelector.set(0)
        print("status is :", self.cam.LineStatus.get())
        sensortrig =threading.Thread(target=self.trigersensor)
        sensortrig.start()
    def trigersensor(self):
       # self.triggerflag = False
        last_state = False
        self.cam.LineSelector.set(0)
        #print("status is :", self.cam.LineStatus.get())
        while 1:
            # 监听line0当前状态
            #print("current line2 status is :", self.cam.LineStatus.get())
            #self.cam.LineSelector.set(0)
            current_state = self.cam.LineStatus.get()
            if last_state == 0 and current_state == 1:  # 上升沿触发
                self.triggerflag = True
                self.num = self.num+1
                self.label_14.setText(str(self.num))
                self.camera1()
                self.camera2()

            else:
                #print("i am here,no photo took")
                pass
            last_state = current_state

    def camera1(self):
        self.cam.ExposureTime.set(15000)
        # set gain
        self.cam.Gain.set(10.0)
        # 流开启
        self.cam.stream_on()
        # start data acquisition+
        time.sleep(0.2)
        self.cam.TriggerSoftware.send_command()  # 软件触发
        #time.sleep(0.5)
        num = 1
        for i in range(num):
            # get raw image
            raw_image = self.cam.data_stream[0].get_image()
            if raw_image is None:
                print("Getting image failed.")
                continue
            # create numpy array with data from raw image
            numpy_image = raw_image.get_numpy_array()
            # print(type(numpy_image)) cv2的图片了。
            if numpy_image is None:
                continue
            # todo
            # 图像处理
            self.gap, self.img = procCallback.measure_distance(numpy_image)#长度距离检测
            print(self.gap)
            if self.gap<10000:#检测条件构建
                self.cam1good = self.cam1good+1
                self.cam1goodrate = self.cam1good/self.num
                self.label_24.setText(str(self.cam1good))
                self.label_22.setText(str(self.cam1goodrate))
                self.camera1flag=True
                self.label_10.setPixmap(QPixmap("OKSHOW.jpg", ))
            else:
                self.cam1goodrate = self.cam1good / self.num
                # self.label_24.setText(str(self.cam2good))
                self.label_22.setText(str(self.cam1goodrate))
                self.label_10.setPixmap(QPixmap("NGSHOW.jpg", ))
            # show acquired image
            img = Image.fromarray(self.img, 'L')
            print("imgformate is:",type(img))
            self.cv2img = cv2.cvtColor(np.asarray(img), cv2.COLOR_GRAY2RGB)
            self.cv2img = cv2.resize(self.cv2img,(600,600))
            #cv2.imshow("this is cv2 window", cv2img)
            #cv2.waitKey(0)
            self.Qframe_daheng1 = QImage(self.cv2img.data, self.cv2img.shape[1],self.cv2img.shape[0], self.cv2img.shape[1] * 3,
                                 QImage.Format_RGB888)
            # print(Qframe)
            # pix = QPixmap(Qframe).scaled(frame.shape[1], frame.shape[0])
            # self.setPixmap(pix)
            # QRect qq(20,50,self.img.width,self.img.height)
            self.label.setPixmap(QPixmap.fromImage(self.Qframe_daheng1))
            print("show success")
            # print height, width, and frame ID of the acquisition image
            print("Frame ID: %d   Height: %d   Width: %d"
                  % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))
        #self.cam.stream_off()
        #self.cam.close_device()
    def camera2(self):

        self.cam2.ExposureTime.set(10000)
        # set gain
        self.cam2.Gain.set(10.0)
        # 流开启
        self.cam2.stream_on()
        # start data acquisition+
        time.sleep(0.2)
        self.cam2.TriggerSoftware.send_command()  # 软件触发
        #time.sleep(0.5)
        num = 1
        for i in range(num):
            # get raw image
            raw_image = self.cam2.data_stream[0].get_image()
            if raw_image is None:
                print("Getting image failed.")
                continue
            # create numpy array with data from raw image
            numpy_image = raw_image.get_numpy_array()
            # print(type(numpy_image)) cv2的图片了。
            if numpy_image is None:
                continue
            # todo
            # 图像处理
            self.distance,self.img = procCallback.cepianyizhi(numpy_image)#偏心距
            print("pianxiju:",self.distance)
            if self.distance<10000:#检测条件构建
                self.cam2good = self.cam2good+1
                self.cam2goodrate = self.cam2good/self.num
                self.label_25.setText(str(self.cam2good))
                self.label_23.setText(str(self.cam2goodrate))
                self.label_11.setPixmap(QPixmap("OKSHOW.jpg", ))
                self.camera2flag=True
            else:
                #self.cam2good = self.cam2good+1
                self.cam2goodrate = self.cam2good/self.num
                #self.label_25.setText(str(self.cam2good))
                self.label_23.setText(str(self.cam2goodrate))
                self.label_11.setPixmap(QPixmap("NGSHOW.jpg", ))
            # show acquired image
            img = Image.fromarray(self.img, 'L')
            print("imgformate is:",type(img))
            self.cv2img2 = cv2.cvtColor(np.asarray(img), cv2.COLOR_GRAY2RGB)
            self.cv2img2 = cv2.resize(self.cv2img2,(600,600))
            #cv2.imshow("this is cv2 window", cv2img)
            #cv2.waitKey(0)
            self.Qframe_daheng2 = QImage(self.cv2img2.data, self.cv2img2.shape[1],self.cv2img2.shape[0], self.cv2img2.shape[1] * 3,
                                 QImage.Format_RGB888)
            # print(Qframe)
            # pix = QPixmap(Qframe).scaled(frame.shape[1], frame.shape[0])
            # self.setPixmap(pix)
            # QRect qq(20,50,self.img.width,self.img.height)
            self.label_2.setPixmap(QPixmap.fromImage(self.Qframe_daheng2))
            print("show success")
            # print height, width, and frame ID of the acquisition image
            print("Frame ID: %d   Height: %d   Width: %d"
                  % (raw_image.get_frame_id(), raw_image.get_height(), raw_image.get_width()))
        #self.cam.stream_off()
        #self.cam.close_device()
    def textChanged0(self):
        print(self.lineEdit.text())
    def textChanged2(self):
        print(self.lineEdit_2.text())
    def textChanged3(self):
        print(self.lineEdit_3.text())
    def textChanged4(self):
        print(self.lineEdit_4.text())
    def textChanged5(self):
        print(self.lineEdit_5.text())
    def textChanged6(self):
        print(self.lineEdit_6.text())
    def textChanged7(self):
        print(self.lineEdit_7.text())
    def textChanged8(self):
        print(self.lineEdit_8.text())
    def textChanged10(self):
        print(self.lineEdit_10.text())
    def print_trig(self):
        # 获得product的打印信息
        while 1:
            if self.camera1flag == 1 and self.camera2flag == 1:
                self.product_infomation = "B4DC9721134AB4R8T552591QRCNH02SZ0203/" + str(
                    time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + "/" + str(
                    self.lineEdit.text()) + str(self.gap) + "-" + str(self.lineEdit_5.text()) + "-" + str(
                    self.lineEdit_7.text()) + "/" + str(
                    self.lineEdit_2.text()) + str(self.distance) + "-" + str(self.lineEdit_6.text()) + "-" + str(
                    self.lineEdit_8.text())
                print(self.product_infomation)
                print_label(self.product_infomation, self.num)
                self.camera1flag=False
                self.camera2flag=False
            else:
                pass


###########################Main Proc############################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MainCode()
    md.show()
    sys.exit(app.exec_())
#################