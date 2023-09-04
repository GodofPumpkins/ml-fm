import librosa as lb

import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.io
import scipy.signal as signal

audiofile1 = "epiano1_5.wav"
audiofile2 = "output.wav"


duration = 5.0
fs = 44100.0
samples = int(fs*duration)
t = np.arange(samples) / fs

samplerate, audio1     = scipy.io.wavfile.read(audiofile1)
samplerate, audio2     = scipy.io.wavfile.read(audiofile2)
audio2 = np.delete(audio2, 1, 0)
print(np.shape(audio1))
print(np.shape(audio2))

# signal = chirp(t, 20.0, t[-1], 100.0)
# signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*3.0*t))
# https://stackoverflow.com/questions/49953379/tensorflow-multiple-loss-functions-vs-multiple-training-ops
# multiple loss functions - one to compare total spectra, one to compare audio change over time.

b, a = signal.butter(3, 0.001)

zi = signal.lfilter_zi(b, a)
z, _ = signal.lfilter(b, a, audio1, zi=zi*audio1[0])

z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])

y = signal.filtfilt(b, a, audio1)

analytic_signal = signal.hilbert(y)
amplitude_envelope1 = np.abs(analytic_signal)

b, a = signal.butter(3, 0.001)

zi = signal.lfilter_zi(b, a)
z, _ = signal.lfilter(b, a, audio2, zi=zi*audio2[0])

z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])

y = signal.filtfilt(b, a, audio2)

analytic_signal = signal.hilbert(y)
amplitude_envelope2 = np.abs(analytic_signal)

plt.plot(t, audio2, label='signal')
plt.plot(t, amplitude_envelope2, label='envelope')
plt.show()



# def compare_envelope(): 
