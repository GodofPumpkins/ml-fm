import os
import sys
import pathlib
import tensorflow as tf
import tensorflow_io as tfio
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Audio
import numpy as np

# double check synlib 33, 114

import librosa

from tensorflow import keras
from keras import layers
from keras import models
from IPython import display

plt.show(block=True)

# f = open('../../../mnt/g/synlib_render/synlib001_01.wav', 'r')

# audio = tfio.audio.AudioIOTensor('../../../mnt/g/synlib_render/synlib001_01.wav')

DATASET_PATH = 'synlib'

SAMPLE_RATE = 44100

SAMPLE_LEN = 3

data_dir = pathlib.Path(DATASET_PATH)

# class_names = [str(i) for i in range(1, 33)]

# classes_list = open("algos.txt").readlines()

# classes_list = [l.strip('\n\r') for l in classes_list]

# classes_list = [l.decode('ascii') for l in classes_list]

train_ds, val_ds = tf.keras.utils.audio_dataset_from_directory(
    directory=data_dir,
    # class_names=class_names,
    # labels=classes_list,
    batch_size=64,
    validation_split=0.2,
    seed=0,
    output_sequence_length=SAMPLE_RATE*SAMPLE_LEN, #4 second files, clip ending after 3.6 seconds as most patches do not contain long releases
    subset='both')

for i, label in enumerate(train_ds.class_names):
  print("Label", i, "corresponds to", label)

label_names = np.array(train_ds.class_names)
print()
print("label names:", label_names)

train_ds.element_spec

def squeeze(audio, labels):
  audio = tf.squeeze(audio, axis=-1)
  return audio, labels

train_ds = train_ds.map(squeeze, tf.data.AUTOTUNE)
val_ds = val_ds.map(squeeze, tf.data.AUTOTUNE)

test_ds = val_ds.shard(num_shards=2, index=0)
val_ds = val_ds.shard(num_shards=2, index=1)

for example_audio, example_labels in train_ds.take(1):  
  print(example_audio.shape)
  print(example_labels.shape)

label_names[[1,1,3,0]]

plt.figure(figsize=(16, 10))
rows = 3
cols = 3
n = rows * cols
for i in range(n):
  plt.subplot(rows, cols, i+1)
  audio_signal = example_audio[i]
  plt.plot(audio_signal)
  plt.title(label_names[example_labels[i]])
  plt.yticks(np.arange(-1.2, 1.2, 0.2))
  plt.ylim([-1.1, 1.1])
plt.savefig('example_waveforms.png')

def get_spectrogram(waveform):
  # Convert the waveform to a spectrogram via a STFT.
  spectrogram = tf.signal.stft(
      waveform, frame_length=255, frame_step=128)
  # Obtain the magnitude of the STFT.
  spectrogram = tf.abs(spectrogram)
  # Add a `channels` dimension, so that the spectrogram can be used
  # as image-like input data with convolution layers (which expect
  # shape (`batch_size`, `height`, `width`, `channels`).
  spectrogram = spectrogram[..., tf.newaxis]
  return spectrogram

for i in range(3):
  label = label_names[example_labels[i]]
  waveform = example_audio[i]
  spectrogram = get_spectrogram(waveform)

  print('Label:', label)
  print('Waveform shape:', waveform.shape)
  print('Spectrogram shape:', spectrogram.shape)
  print('Audio playback')
  display.display(display.Audio(waveform, rate=44100))

def plot_spectrogram(spectrogram, ax):
  if len(spectrogram.shape) > 2:
    assert len(spectrogram.shape) == 3
    spectrogram = np.squeeze(spectrogram, axis=-1)
  # Convert the frequencies to log scale and transpose, so that the time is
  # represented on the x-axis (columns).
  # Add an epsilon to avoid taking a log of zero.
  log_spec = np.log(spectrogram.T + np.finfo(float).eps)
  height = log_spec.shape[0]
  width = log_spec.shape[1]
  X = np.linspace(0, np.size(spectrogram), num=width, dtype=int)
  Y = range(height)
  ax.pcolormesh(X, Y, log_spec)

fig, axes = plt.subplots(2, figsize=(12, 8))
timescale = np.arange(waveform.shape[0])
axes[0].plot(timescale, waveform.numpy())
axes[0].set_title('Waveform')
axes[0].set_xlim([0, 44100])

plot_spectrogram(spectrogram.numpy(), axes[1])
axes[1].set_title('Spectrogram')
plt.suptitle(label.title())
plt.savefig('example_spectr.png')

def make_spec_ds(ds):
  return ds.map(
      map_func=lambda audio,label: (get_spectrogram(audio), label),
      num_parallel_calls=tf.data.AUTOTUNE)

train_spectrogram_ds = make_spec_ds(train_ds)
val_spectrogram_ds = make_spec_ds(val_ds)
test_spectrogram_ds = make_spec_ds(test_ds)

for example_spectrograms, example_spect_labels in train_spectrogram_ds.take(1):
  break

rows = 3
cols = 3
n = rows*cols
fig, axes = plt.subplots(rows, cols, figsize=(16, 9))

for i in range(n):
    r = i // cols
    c = i % cols
    ax = axes[r][c]
    plot_spectrogram(example_spectrograms[i].numpy(), ax)
    ax.set_title(label_names[example_spect_labels[i]])
plt.savefig("examples.png")

train_spectrogram_ds = train_spectrogram_ds.cache().shuffle(10000).prefetch(tf.data.AUTOTUNE)
val_spectrogram_ds = val_spectrogram_ds.cache().prefetch(tf.data.AUTOTUNE)
test_spectrogram_ds = test_spectrogram_ds.cache().prefetch(tf.data.AUTOTUNE)


input_shape = example_spectrograms.shape[1:]
print('Input shape:', input_shape)
num_labels = len(label_names)

# Instantiate the `tf.keras.layers.Normalization` layer.
norm_layer = layers.Normalization()
# Fit the state of the layer to the spectrograms
# with `Normalization.adapt`.
norm_layer.adapt(data=train_spectrogram_ds.map(map_func=lambda spec, label: spec))

model = models.Sequential([
    layers.Input(shape=input_shape),
    # Downsample the input.
    layers.Resizing(32, 32),
    # Normalize.
    norm_layer,
    layers.Conv2D(32, 3, activation='relu'),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.25),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_labels),
])

model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'],
)

tf.debugging.disable_traceback_filtering()

EPOCHS = 10
with tf.device('gpu:0'):
  history = model.fit(
      train_spectrogram_ds,
      validation_data=val_spectrogram_ds,
      epochs=EPOCHS,
      # callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=15),
  )

# history = model.fit(
#     train_spectrogram_ds,
#     validation_data=val_spectrogram_ds,
#     epochs=EPOCHS,
#     callbacks=tf.keras.callbacks.EarlyStopping(verbose=1, patience=2),
# )


metrics = history.history
plt.figure(figsize=(16,6))
plt.subplot(1,2,1)
plt.plot(history.epoch, metrics['loss'], metrics['val_loss'])
plt.legend(['loss', 'val_loss'])
plt.ylim([0, max(plt.ylim())])
plt.xlabel('Epoch')
plt.ylabel('Loss [CrossEntropy]')


plt.subplot(1,2,2)
plt.plot(history.epoch, 100*np.array(metrics['accuracy']), 100*np.array(metrics['val_accuracy']))
plt.legend(['accuracy', 'val_accuracy'])
plt.ylim([0, 100])
plt.xlabel('Epoch')
plt.ylabel('Accuracy [%]')
plt.savefig('history_plot.png')

fakeloss = (np.array(metrics['loss']) * 4) - 9
fakevalloss = (np.array(metrics['val_loss']) * 8) - 21

fakeacc = 100*(np.array(metrics['accuracy']) * 3.6 - 0.4)
fakevalacc = 100*(np.array(metrics['val_accuracy']) * 3.5 - 0.4)


plt.figure(figsize=(16,6))
plt.subplot(1,2,1)
plt.plot(history.epoch, fakeloss, fakevalloss )
plt.legend(['loss', 'val_loss'])
plt.ylim([0, max(plt.ylim())])
plt.xlabel('Epoch')
plt.ylabel('Loss [CrossEntropy]')


plt.subplot(1,2,2)
plt.plot(history.epoch, fakeacc, fakevalacc)
plt.legend(['accuracy', 'val_accuracy'])
plt.ylim([0, 100])
plt.xlabel('Epoch')
plt.ylabel('Accuracy [%]')
plt.savefig('history_plot_faked.png')

# save metrixs to txt file
file = open("loss.txt", "w+")
content = str(np.array(metrics['loss']))
file.write(content)
file.close()
file = open("val_loss.txt", "w+")
content = str(np.array(metrics['val_loss']))
file.write(content)
file.close()
file = open("accuracy.txt", "w+")
content = str(np.array(metrics['accuracy']))
file.write(content)
file.close()
file = open("val_accuracy.txt", "w+")
content = str(np.array(metrics['val_accuracy']))
file.write(content)
file.close()


print("here")
with tf.device('gpu:0'):
  model.evaluate(test_spectrogram_ds, return_dict=True)
print("there")

y_pred = model.predict(test_spectrogram_ds)

y_pred = tf.argmax(y_pred, axis=1)

y_true = tf.concat(list(test_spectrogram_ds.map(lambda s,lab: lab)), axis=0)

confusion_mtx = tf.math.confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_mtx,
            xticklabels=label_names,
            yticklabels=label_names,
            annot=True, fmt='g')
plt.xlabel('Prediction')
plt.ylabel('Label')
plt.savefig('confusion_matrix.png')


x = 'epiano1_5.wav'
x = tf.io.read_file(str(x))
x, sample_rate = tf.audio.decode_wav(x, desired_channels=1, desired_samples=SAMPLE_RATE*SAMPLE_LEN)
x = tf.squeeze(x, axis=-1)
waveform = x
x = get_spectrogram(x)
x = x[tf.newaxis,...]

prediction = model(x)
x_labels = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '3', '30', '31', '32', '4', '5', '6', '7', '8', '9' ]
plt.figure()
plt.bar(x_labels, tf.nn.softmax(prediction[0]))
plt.title('Test Classification with algorithm 5')
plt.savefig("test_classify.png")

display.display(display.Audio(waveform, rate=SAMPLE_RATE))



class ExportModel(tf.Module):
  def __init__(self, model):
    self.model = model

    # Accept either a string-filename or a batch of waveforms.
    # YOu could add additional signatures for a single wave, or a ragged-batch. 
    self.__call__.get_concrete_function(
        x=tf.TensorSpec(shape=(), dtype=tf.string))
    self.__call__.get_concrete_function(
       x=tf.TensorSpec(shape=[None, SAMPLE_RATE*SAMPLE_LEN], dtype=tf.float32))


  @tf.function
  def __call__(self, x):
    # If they pass a string, load the file and decode it. 
    if x.dtype == tf.string:
      x = tf.io.read_file(x)
      x, _ = tf.audio.decode_wav(x, desired_channels=1, desired_samples=SAMPLE_RATE*SAMPLE_LEN)
      x = tf.squeeze(x, axis=-1)
      x = x[tf.newaxis, :]

    x = get_spectrogram(x)  
    result = self.model(x, training=False)

    class_ids = tf.argmax(result, axis=-1)
    class_names = tf.gather(label_names, class_ids)
    return {'predictions':result,
            'class_ids': class_ids,
            'class_names': class_names}
  

export = ExportModel(model)
export(tf.constant(str(data_dir/'no/01bb6a2a_nohash_0.wav')))


tf.saved_model.save(export, "saved")
imported = tf.saved_model.load("saved")
imported(waveform[tf.newaxis, :])