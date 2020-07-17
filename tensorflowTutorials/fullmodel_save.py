import os
import tensorflow as tf
from tensorflow import keras

print(tf.version.VERSION)

(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
train_labels = train_labels[:1000]
test_labels = test_labels[:1000]
train_images = train_images[:1000].reshape(-1, 28*28)/255.0
test_images = test_images[:1000].reshape(-1, 28*28)/255.0

#Define a simple sequential model
def create_model():
    model = tf.keras.Sequential([
        keras.layers.Dense(512, activation="relu", input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10)
    ])
    model.compile(optimizer="adam",
        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])
    return model

model = create_model()
model.fit(train_images, train_labels, epochs=10)
model.save("saved_model/my_model")

loaded_model = tf.keras.models.load_model("saved_model/my_model")

loaded_model.summary()