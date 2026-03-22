# examples/keras_example.py
# KaggleNotify — Keras / TensorFlow usage example
# Copy this into your Kaggle notebook cell

from kaggle_notify import setup, KerasNotifyCallback

# 1. Setup — sends a test ping to Telegram
notifier = setup("My Keras Experiment")

# 2. Build your model as usual
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation="relu", input_shape=(784,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# 3. Pass the callback — that's it!
model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=10,
    callbacks=[KerasNotifyCallback(notifier)],
)
