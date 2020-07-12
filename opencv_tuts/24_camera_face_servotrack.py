import cv2
from adafruit_servokit import ServoKit

#core starting point
dispW = 640
dispH = 480
flip=2
#camSet = f'nvarguscamerasrc ! video/x-raw(memory:MVMM),width=3262,height=2464,format=NV12,framerate=28/1 ! nvvidconv flip-method={flip} ! video/x-raw,width={display_width},height={display_height},format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink'


kit = ServoKit(channels=16)
pan = 90
tilt  = 90
kit.servo[0].angle = pan
kit.servo[1].angle = tilt
face_cascade = cv2.CascadeClassifier("/home/aicamsys/pi_pro/data/haarcascade_frontalface_default.xml")
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)
width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),3)
        area = w*h
        if area > 50:
            faceX = x + w / 2
            faceY = y + h / 2
            errorPan = faceX-width/2
            errorTilt = faceY - height / 2
            if abs(errorPan)>15:
                pan=pan-errorPan/50
            if abs(errorTilt)>15:
                tilt=tilt-errorTilt/50
            if pan>180:
                pan=180
                print("Pan Out of  Range")   
            if pan<0:
                pan=0
                print("Pan Out of  Range") 
            if tilt>180:
                tilt=180
                print("Tilt Out of  Range") 
            if tilt<0:
                tilt=0
                print("Tilt Out of  Range")                 

            kit.servo[0].angle=pan
            kit.servo[1].angle=tilt 
    cv2.imshow("picam",frame)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()