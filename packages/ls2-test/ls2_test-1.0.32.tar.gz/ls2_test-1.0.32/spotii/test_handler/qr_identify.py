import cv2
import numpy as np
from pyzbar import pyzbar
##        block_width  = 100
##        block = image[ weak_row_start: weak_row_start+weak_height,
##                              x + block_offset : x + block_offset + block_width]

def qrCut(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]

    reverse = cv2.bitwise_not(thresh)

    kernel = np.ones((15,15), np.uint8)
#    dilation = cv2.erode(morph, kernel, iterations=1)
    dilation = cv2.dilate(reverse, kernel, iterations=1)
##    cv2.imshow("morph", morph)
##    cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:

        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)

        target = reverse[y:y+h,x:x+w]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
        target = cv2.morphologyEx(target, cv2.MORPH_OPEN, kernel)

        target = cv2.bitwise_not(target)
#         cv2.imshow("target", target)
# #        cv2.imshow("image", image)
#         cv2.waitKey(0)
        return target

    return thresh



def qrIdentify(image):
    try:
        image = qrCut(image)
##        cv2.imshow("image", image)
##        cv2.waitKey(0)


        qr = pyzbar.decode(image)
        if qr!=[]:
            return(qr[0].data.decode("utf-8"))

        return None


##        decoder = cv2.QRCodeDetector()
##        value, points, _ = decoder.detectAndDecode(image)
##        print('qrIdentify, value:',value)
##        print('qrIdentify, points:',points)
##        if points.any() == None:
##            print('qr')
    except Exception as e:
        print(e)
        return None




if __name__ == "__main__":
    from PyQt5 import QtWidgets
    from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
    from PyQt5 import QtCore
    import sys
     
     
    def dialog():
        options = QtWidgets.QFileDialog.Options()
        file , check = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Png, Jpg Files (*.jpg; *.png)", options=options)
        if check:
            image=cv2.imread(file)
  
            print(qrIdentify(image))
     
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(400,400,300,300)
    win.setWindowTitle("CodersLegacy")
      
    button = QPushButton(win)
    button.setText("Press")
    button.clicked.connect(dialog)
    button.move(50,50)
     
    win.show()
    sys.exit(app.exec_())        

