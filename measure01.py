import cv2
import numpy as np
img = cv2.imread("img01.jpg")
print(img.shape)
kernel = np.ones((5,5),np.uint8)
#create roi0
x,y,w,h = 350,430,140,80
roi1 = img[x:x+h,y:y+w]

#create roi1
x1,y1,w1,h1 =10,730,140,150
roi2 = img[x1:x1+h1,y1:y1+w1]



########################roi1########################
gray = cv2.cvtColor(roi1,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
ret,binary = cv2.threshold(gray,60,255,cv2.THRESH_BINARY)
size = roi1.shape
print(size)
#cv2.circle(roi1,(70,40),10,(0,255,0),-1)
#cv2.circle(img,(70+430,1011-300),5,(0,255,0),-1)
for j in range(0, 140, 1):
    if binary[50, j] == 0:
        cv2.circle(roi1,(j,50),4,(0,255,0),-1)
        cv2.line(roi1,(j,50),(j+45,50), (0,255,0), 4)
        cv2.line
        cv2.line(roi1, (j, 50), (j, 50-45),  (0, 255, 0), 4)
        cv2.rectangle(roi1,(0,0),(140,80), (122, 122, 0), 4)
        break

####################################roi2####################
gray2 = cv2.cvtColor(roi2,cv2.COLOR_BGR2GRAY)
gray2 = cv2.GaussianBlur(gray2,(5,5),0)
ret,binary2 = cv2.threshold(gray2,55,255,cv2.THRESH_BINARY)

size2 = roi2.shape
print(size2)
#cv2.circle(roi1,(70,40),10,(0,255,0),-1)
#cv2.circle(img,(70+430,1011-300),5,(0,255,0),-1)
for j in range(0, 140, 1):
    if binary2[50, j] == 0:  #0是黑色
        cv2.circle(roi2,(j,50),4,(0,255,0),-1)
        cv2.line(roi2,(j,50),(j+45,50), (0,255,0), 4)

        cv2.line(roi2, (j, 50), (j, 50-45),  (0, 255, 0), 4)
        cv2.rectangle(roi2,(0,0),(140,80), (122, 122, 0), 4)
        break
####################################################

############################show#####################
cv2.imshow("roi1_edge",binary)
cv2.imshow("roi2_edge",binary2)
cv2.imshow("roi1",roi1)
cv2.imshow("roi2",roi2)
cv2.imshow("origin",img)
cv2.waitKey(0)
###############################################
