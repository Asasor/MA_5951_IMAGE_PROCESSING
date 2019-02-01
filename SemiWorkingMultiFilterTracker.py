import numpy as np
import cv2

capture = cv2.VideoCapture(r'''C:\Users\Asaf Soreq\Downloads\afds2.mp4''')

minHSV = (0,0,0)
maxHSV = (0,0,0)

# HSV threshold range
threshR = 7.
SampleHSVmean = False
mc = (0,0,0)
ix,iy = -1,-1

# window names
wName1 = 'RGB/BGR'
wName2 = 'GRAY_THRESH'
#wName3 = 'HSV'

# how segmented the RGB colours are
lOfQuant = 5

indices = np.arange(0,256)

divider = np.linspace(0,255,lOfQuant+1)[1]

quantiz = np.int0(np.linspace(0,255,lOfQuant))

color_levels = np.clip(np.int0(indices/divider),0,lOfQuant-1)

palette = quantiz[color_levels]

def sampleMean(event,x,y,flags,param):
    global ix,iy,minHSV,maxHSV,mc,AvgCursorHSV,SampleHSVmean
    # mc == meanColour

    if event == cv2.EVENT_LBUTTONDOWN:

        ix,iy  = x,y
        mc = cv2.mean(HSVimg[y-1:y+1,x-1:x+1])

        HSVcolour = (mc[0],mc[1],mc[2])

        minHSV = np.uint8([mc[0] - threshR ,mc[1] - threshR ,mc[2]- threshR])
        maxHSV = np.uint8((mc[0] + threshR ,mc[1] + threshR ,mc[2] + threshR))

        np.clip(minHSV , [0,0,0] , [180,255,255] , out=minHSV)
        np.clip(maxHSV , [0,0,0] , [180,255,255] , out=maxHSV)

        for i in range(0,3):
            
            if minHSV[i] > maxHSV[i]:
                minHSV[i] = 0
                #print("working - ", i)

    
    SampleHSVmean = True

#changeCondition to true if cam
while(capture.isOpened()):

    ret, frame = capture.read()

    blurredImg = cv2.GaussianBlur(frame,(5,5),0)

    quantizedImg = palette[blurredImg]

    quantizedImg = cv2.convertScaleAbs(quantizedImg)

    HSVimg = cv2.cvtColor(quantizedImg, cv2.COLOR_BGR2HSV)

    cv2.setMouseCallback(wName1,sampleMean)

    HSVthresh = cv2.inRange(HSVimg,minHSV,maxHSV)

    if SampleHSVmean == True:
        cv2.rectangle(quantizedImg, (ix - 5,iy - 5), (ix + 5,iy + 5), mc, 5)

    cv2.imshow(wName1,quantizedImg)
    cv2.imshow(wName2,HSVthresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
