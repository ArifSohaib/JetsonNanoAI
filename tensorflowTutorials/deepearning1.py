import jetson.inference
import jetson.utils
import time
width = 1280
height = 720
import cv2 
import numpy as np

dispW = 640
dispH = 480
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

#cam = jetson.utils.gstCamera(width, height, '0')
cam = cv2.VideoCapture(camSet)
#display= jetson.utils.glDisplay()
net = jetson.inference.imageNet("inception-v4")
timeMark = time.time()
fpsFilter = 0
font = jetson.utils.cudaFont()
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    #frame, width, height = cam.CaptureRGBA(zeroCopy=1)
    _,frame = cam.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA).astype(np.float32)
    img = jetson.utils.cudaFromNumpy(img)
    classID, confidence = net.Classify(img, width, height)
    item = net.GetClassDesc(classID)
    dt = time.time() - timeMark 
    fps = 1/dt
    fpsFilter = 0.95*fpsFilter + 0.05 * fps 
    timeMark = time.time()
    #font.OverlayText(frame, width, height, str(round(fpsFilter,1))+" fps "+item,5,5,font.Magenta, font.Blue)
    #display.RenderOnce(frame, width, height)
    #frame = jetson.utils.cudaToNumpy(frame, width, height,4)
    #frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2BGR).astype(np.uint8)
    cv2.putText(frame, f"{str(round(fpsFilter,1))} fps {item}",(0,30),font,1,(0,0,255),2)
    cv2.imshow('recCam',frame)
    cv2.moveWindow('recCam',0,0)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
