from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Convolution2D, Flatten, Dense
from tensorflow.python.keras.optimizer_v2.adam import Adam


adam = Adam()


def create_model():
    model = Sequential()

    model.add(Convolution2D(24, (5, 5), (2, 2), input_shape=(66, 200, 3), activation="elu"))  # type: ignore
    model.add(Convolution2D(36, (5, 5), (2, 2), activation="elu"))  # type: ignore
    model.add(Convolution2D(48, (5, 5), (2, 2), activation="elu"))  # type: ignore
    model.add(Convolution2D(64, (3, 3), activation="elu"))  # type: ignore
    model.add(Convolution2D(64, (3, 3), activation="elu"))  # type: ignore

    model.add(Flatten())  # type: ignore
    model.add(Dense(100, activation="elu"))  # type: ignore
    model.add(Dense(50, activation="elu"))  # type: ignore
    model.add(Dense(10, activation="elu"))  # type: ignore
    model.add(Dense(1))  # type: ignore

    model.compile(optimizer=adam, loss="mse")  # type: ignore
    return model
