import cv2

#core starting point
dispW = 640
dispH = 480
flip=2
#camSet = f'nvarguscamerasrc ! video/x-raw(memory:MVMM),width=3262,height=2464,format=NV12,framerate=28/1 ! nvvidconv flip-method={flip} ! video/x-raw,width={display_width},height={display_height},format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink'

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)
face_cascade = cv2.CascadeClassifier("/home/aicamsys/pi_pro/data/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("/home/aicamsys/pi_pro/data/haarcascade_eye_tree_eyeglasses.xml")
while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)
    
    print(faces)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),3)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h,x:x+h]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (xEye,yEye, widthEye, heightEye) in eyes:
           # cv2.rectangle(roi_color, (xEye,yEye),(xEye+widthEye,yEye+heightEye),(0,255,0),2)
            cv2.circle(roi_color, (int(xEye+widthEye/2),int(yEye+heightEye/2)),40,(0,0,0),-1)
            print(f"eyes {xEye} {yEye}")
    cv2.imshow("picam",frame)
    cv2.moveWindow("piCam",0,0)

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
