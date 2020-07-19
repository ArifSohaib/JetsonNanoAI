import cv2
import numpy as np
import tensorflow as tf 
width = 1280
height = 720


dispW = 640
dispH = 480
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(camSet)


#Load the TFLIte model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="/home/aicamsys/pi_pro/saved_model/my_model/posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
font = cv2.FONT_HERSHEY_SIMPLEX

print(f"input_details: {input_details}")
print(f"output_details: {output_details}")
input_shape = input_details[0]['shape']
print(f"input_shape: {input_shape}")

while True:
    ret, frame = cam.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32)
    #feed image into tensorflow model
    img = cv2.resize(img, (257,257),interpolation = cv2.INTER_CUBIC)
    img = np.expand_dims(img, axis=0).astype(np.float32)
    #get results
    # input_data = np.array(img, dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], img)

    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    #cv2.putText(frame, f"{str(round(fpsFilter,1))} fps {item}",(0,30),font,1,(0,0,255),2)
    cv2.putText(frame, f"output shape {output_data[0,0]}",(0,30),font,1,(0,0,255),2)
    cv2.imshow('recCam',frame)
    cv2.moveWindow('recCam',0,0)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()