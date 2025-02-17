import librosa
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment

sr=44100
sr,y=read(r"C:\Research\recording_application\output_data\TS9_純音\wav_files\TS9Bypass.wav")
y=y[sr*9:sr*10]
print(type(y))
cent_def = librosa.feature.spectral_centroid(y=y, sr=sr)
print("default",np.round(np.average(cent_def)))

N=len(y)
fft=np.fft.fft(y)
fft_abs=2*np.abs(fft)/N
freq=np.fft.fftfreq(N,d=1/sr)

threshold=10**(-80/20)
fft[(fft_abs < threshold)] = 0
# print(np.min(fft))
# print(np.min(fft_abs))
filtered=np.fft.ifft(fft)
filtered=filtered.real
# print(np.min(fft_abs))

# N=len(y)
# fft=np.fft.fft(y)
# fft_abs=2*np.abs(fft)/N
# freq=np.fft.fftfreq(N,d=1/sr)

cent_filtered=librosa.feature.spectral_centroid(y=filtered, sr=sr)
print("filtered",np.round(np.average(cent_filtered)))

plt.figure()
plt.plot(freq[0:int(N/2)],fft_abs[0:int(N/2)])
plt.xlim(0,2000)
plt.show()