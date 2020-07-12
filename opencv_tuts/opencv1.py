import cv2

#core starting point
dispW = 1280
dispH = 720
flip=2
#camSet = f'nvarguscamerasrc ! video/x-raw(memory:MVMM),width=3262,height=2464,format=NV12,framerate=28/1 ! nvvidconv flip-method={flip} ! video/x-raw,width={display_width},height={display_height},format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink'

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)
while True:
    ret, frame = cam.read()
    cv2.imshow("picam",frame)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
