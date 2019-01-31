import numpy as np
import cv2

capture = cv2.VideoCapture(0)
img = np.zeros((480,640,3), np.uint8)

minHsv = (0,0,0)
maxHsv = (0,0,0)
# threshR = (HSV) thresh(old) R(ange)
threshR = 7.5;
ix,iy = -1,-1
mode = False
mu = (0,0,0)


def sampleMean(event,x,y,flags,param):
    global ix,iy,mode,mu,minHsv,maxHsv,h,s,v

    if event == cv2.EVENT_LBUTTONDOWN:

        # mouse location
        print("ix is - ", ix," & iy is - ", iy)
        ix,iy = x,y
        mu = cv2.mean(hsvImg[y-1:y+1,x-1:x+1])
        
        # get H(ue)S(aturation)V(alue)
        #h,s,v = cv2.split(mu)
        h,s,v,_ = (mu[0],mu[1],mu[2],mu[3])
        HsvColour = (h,s,v)
        minHsv = np.uint8([h - threshR,s - threshR,v - threshR])
        maxHsv = np.uint8((minHsv[0] + threshR * 2,minHsv[1] + threshR * 2,minHsv[2] + threshR * 2))
        np.clip(minHsv , [0,0,0] , [180,255,255] , out=minHsv)
        np.clip(maxHsv , [0,0,0] , [180,255,255] , out=maxHsv)

        for i in range(0,3):
            
            if minHsv[i] > maxHsv[i]:
                minHsv[i] = 0
                print("working - ", i)
                
        print(h,s,v)

        #for i in HsvColour:

        # threshold update
        print("MinHsv - ", minHsv, " && MaxHsv", maxHsv)
        #print("estimated x is - ", x,"& estimated y is - ", y)
        #print("colour - ", colour)
        #print("working")
        mode = True
        
            # not working
            #cv2.rectangle(img,(ix-50,iy-50),(ix+50,iy+50),mu,10)  

#changeCondition?
while(True):

     # captureCurrentFrame

     # ret = return, ret == True while frame = present & False while ret != True
     # read() = reads (VideoCapture Type) capture output
     ret, frame = capture.read()
     
     # applies Gaussian Blur to soften and Blur the frame (Always Apply)
     blurredImg = cv2.GaussianBlur(frame,(5,5),0)
     
     # convert color from RGB to HSV
     hsvImg = cv2.cvtColor(blurredImg, cv2.COLOR_BGR2HSV)
     
     # process HSV image
     win_name = 'frame'
     win_name2 = 'frame2'
     img = hsvImg;
     cv2.setMouseCallback(win_name,sampleMean)
     
     # simple threshold settings
     thresh = cv2.inRange(hsvImg, minHsv, maxHsv)
     img = blurredImg;
     
     
     # display processed / thresholded frame
     print("MinHsv - ", minHsv, " && MaxHsv", maxHsv)
     
     if mode == True:
         cv2.rectangle(img,(ix-5,iy-5),(ix+5,iy+5),mu,5)

     cv2.imshow(win_name,img)
     cv2.imshow(win_name2,thresh)
     
     # end while loop when q key is pressed
     # ord(ReturnsUnicodeForChar)
     if cv2.waitKey(1) & 0xFF == ord('q'):
         break

# end program and close display panel
capture.release()
cv2.destroyAllWindows()
