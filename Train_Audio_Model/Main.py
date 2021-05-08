from Load_Audio_Data import get_audio_data, audio_to_fft
from Neural_Models import get_model
from tensorflow import keras
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import sys

SCALE = 0.5

BATCH_SIZE = 5
EPOCHS = 100

def main():
    train_ds, valid_ds, class_names = get_audio_data()
    model, earlystopping_cb, mdlcheckpoint_cb = get_model(class_names)

    history = model.fit(
        train_ds,
        epochs=EPOCHS,
        validation_data=valid_ds,
        callbacks=[earlystopping_cb, mdlcheckpoint_cb]
    )

    #Model Save
    model.save("Saved_Model/Audio_Network.h5")
    model = keras.models.load_model("Saved_Model/Audio_Network.h5")

    #Testing
    for audios, labels in valid_ds.take(1):
        # Get the signal FFT
        #ffts = audio_to_fft(audios)
        # Predict
        y_pred = model.predict(audios)
        y_pred = np.argmax(y_pred, axis=-1)

    print(confusion_matrix(labels, y_pred))

    for index in range(10):
        # For every sample, print the true and predicted label
        # as well as run the voice with the noise
        print(
            "True: {} - Predicted: {}".format(
                class_names[labels[index]],
                class_names[y_pred[index]],
            )
        )

    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

if __name__ == "__main__":
    main()