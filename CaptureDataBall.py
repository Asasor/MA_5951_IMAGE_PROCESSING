import numpy as np
import cv2
from time import sleep


capture = cv2.VideoCapture(0)

# intensity of blur
sigma = 2
swap = False

# deprecated
#low_H = 0
#low_S = 30
#low_V = 0
#high_H = 100
#high_S = 255
#high_V = 255

lowBall = [0,130,50]
highBall = [20,255,255]

window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
window_ui = 'UI'

def round_up_to_odd(f):
    return np.ceil(f / 2.) * 2 + 1



while capture.isOpened():

    ret, frame = capture.read()

    small = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
    resizedImg = small.shape

    kernel_size = int(round_up_to_odd(resizedImg[1]*0.01))
    blurredImg = cv2.GaussianBlur(small, (kernel_size, kernel_size), sigma)
    frame_HSV = cv2.cvtColor(blurredImg, cv2.COLOR_BGR2HSV)
    frame_threshold = cv2.inRange(frame_HSV, (lowBall[0], lowBall[1], lowBall[2]),
                                  (highBall[0], highBall[1], highBall[2]))
    
    contours,hierarchy = cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(blurredImg, contours, -1, (0, 255, 0), 3)

    print(len(contours))

    for i in contours:
        global path, d, w, h
        cnt = i
        M = cv2.moments(cnt)
        #x, y, width, height = cv2.boundingRect(M)
        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        x, y, w, h = cv2.boundingRect(cnt)
        d = 0

        #print(w*h)

        if M['m00'] is not None:
            if w > 500:
                crop_img = blurredImg[y-5:y+h+5, x-5:x+w+5]
                #blargh = cv2.rectangle(blurredImg, (x, y), (x+w, y+h), (0, 255, 0), 2)
                try:
                    cv2.imshow("cropped", crop_img)
                except Exception as e:
                    print("Got an error" + str(crop_img.size))
                    continue
                d = d + 1

                # input own path
                path = r'''C:\Users\Asaf Soreq\Desktop\BallData\hj''' + str(i[0]) + ".jpg"
                print(path)
                cv2.imwrite(path, crop_img)

    cv2.imshow(window_capture_name, blurredImg)
    cv2.imshow(window_detection_name, frame_threshold)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break
    if k == ord('s'):
        print(cv2.contourArea(cnt))
        k = 0
        if swap is True:
            swap = False
        else:
            swap = True
    if swap is False:
        img = blurredImg
    else:
        img = frame_threshold
        #cv2.imwrite('TestImg',blurredImg)

    sleep(0.1)

capture.release()
cv2.destroyAllWindows()
