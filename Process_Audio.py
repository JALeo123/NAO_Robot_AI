import numpy as np
import tensorflow as tf
from pathlib import Path
import os
import sys

def process_audio_input(audio_model, path):
    train_ds = get_audio(path)

    #Prediction
    for audio, label in train_ds:
        # Predict
        y_pred = audio_model.predict(audio)
        y_pred = np.argmax(y_pred, axis=-1)

    return y_pred[0]

def get_audio(path):
    # Seed to use when shuffling the dataset and the noise
    SHUFFLE_SEED = 43

    SAMPLING_RATE = 16000
    SCALE = 0.5
    BATCH_SIZE = 128

    def paths_and_labels_to_dataset(audio_paths, labels):
        """Constructs a dataset of audios and labels."""
        path_ds = tf.data.Dataset.from_tensor_slices(audio_paths)
        audio_ds = path_ds.map(lambda x: path_to_audio(x))
        label_ds = tf.data.Dataset.from_tensor_slices(labels)
        return tf.data.Dataset.zip((audio_ds, label_ds))

    def path_to_audio(path):
        """Reads and decodes an audio file."""
        audio = tf.io.read_file(path)
        audio, _ = tf.audio.decode_wav(audio, 1, SAMPLING_RATE)
        return audio

    def audio_to_fft(audio):
        # Since tf.signal.fft applies FFT on the innermost dimension,
        # we need to squeeze the dimensions and then expand them again
        # after FFT
        audio = tf.squeeze(audio, axis=-1)
        fft = tf.signal.fft(
            tf.cast(tf.complex(real=audio, imag=tf.zeros_like(audio)), tf.complex64)
        )
        fft = tf.expand_dims(fft, axis=-1)

        # Return the absolute value of the first half of the FFT
        # which represents the positive frequencies
        return tf.math.abs(fft[:, : (audio.shape[1] // 2), :])

    # Get the list of audio file paths along with their corresponding labels

    audio = []
    audio.append(path)
    labels = []
    labels.append(1)

    # Split into training and validation
    train_labels = labels

    train_ds = paths_and_labels_to_dataset(audio, labels)
    train_ds = train_ds.shuffle(buffer_size=BATCH_SIZE * 8, seed=SHUFFLE_SEED).batch(
        BATCH_SIZE
    )

    train_ds = train_ds.map(
        lambda x, y: (audio_to_fft(x), y)
    )

    return train_ds

def audio_to_fft(audio):
    # Since tf.signal.fft applies FFT on the innermost dimension,
    # we need to squeeze the dimensions and then expand them again
    # after FFT
    audio = tf.squeeze(audio, axis=-1)
    fft = tf.signal.fft(
        tf.cast(tf.complex(real=audio, imag=tf.zeros_like(audio)), tf.complex64)
    )
    fft = tf.expand_dims(fft, axis=-1)

    # Return the absolute value of the first half of the FFT
    # which represents the positive frequencies
    return tf.math.abs(fft[:, : (audio.shape[1] // 2), :])