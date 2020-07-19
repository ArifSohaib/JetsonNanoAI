import jetson.inference
import jetson.utils 

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.6)
dispW = 640
dispH = 480
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = jetson.utils.gstCamera(0)
disp = jetson.utils.glDisplay()
font = jetson.utils.cudaFont()
net = jetson.inference.imageNet("googlenet")
while disp.IsOpen():
    frame, width, height = cam.CaptureRGBA()

    classID, confident = net.Classify(frame, width, height)
    item = net.GetClassDesc(classID)
    font.OverlayText(frame, width, height,item,5,5,font.Magenta, font.Blue)
    disp.RenderOnce(frame, width, height)
