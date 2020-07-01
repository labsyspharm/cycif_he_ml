import numpy as np
import tensorflow as tf
from tensorflow import keras

X = np.load('../data/he_tile_X.npy')
X = X[..., np.newaxis]
y = np.load('../data/he_tile_y.npy')

model = keras.models.Sequential()
model.add(keras.layers.Conv2D(32, (8, 8), activation='relu',
    input_shape=X.shape[1:]))
model.add(keras.layers.Conv2D(32, (8, 8), activation='relu'))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(32, activation='relu'))
model.add(keras.layers.Dense(1, activation='sigmoid'))

model.compile(
        optimizer='adam',
        loss=keras.losses.MeanSquaredError(),
        metrics=keras.metrics.MeanSquaredError(),
        )

ds = tf.data.Dataset.from_tensor_slices((X, y)).batch(32)
model.fit(ds, epochs=3)
