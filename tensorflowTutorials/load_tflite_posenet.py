#NOTE: cv2 needs to be imported before tensorflow
import cv2

import numpy as np
import tensorflow as tf 

#Load the TFLIte model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="/home/aicamsys/pi_pro/saved_model/my_model/posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(f"input_details: {input_details}")
print(f"output_details: {output_details}")
input_shape = input_details[0]['shape']
print(f"input_shape: {input_shape}")

#using it on random data
input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
# for key in output_data:
#     print(key)
# print(f"output data {output_data}")
print(f"output shape {output_data.shape}")
#get the camera image
#process image into particular shape and format for model
