import numpy as np
import matplotlib.pyplot as plt
from scipy.signal.windows import hann

t=np.arange(0,1,1/44100)
f=100
y=0
# for i in range(1,200,2):
#     y-=(2/(i))*np.sin(2*np.pi*i*f*t)
# y=y/y.max()
y = 2 * np.abs(2 * (t * f - np.floor(t * f + 0.5))) - 1
plt.figure()
plt.plot(t,y)
plt.xlim(0,0.05)
plt.xlabel("time(s)")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# y=y[2048:4096]
# window=hann(2048)
# w_signal=window*y
N=len(y)
fft=np.fft.fft(y)
fft_abs=2*(np.abs(fft)/N)
# correction_factor = np.sum(window) / len(window)
# corrected_signal = fft_abs / correction_factor
# fft_log=20*np.log10(corrected_signal)
fft_log=20*np.log10(fft_abs)
dt=1/44100
freq = np.fft.fftfreq(N, d=dt)
plt.figure()
plt.plot(freq[0:int(N/2)],fft_log[0:int(N/2)])
plt.xlabel("Frequency(Hz)")
plt.ylabel("Amplitude")
plt.xscale("log")
plt.ylim(-100,10)
plt.grid()
plt.show()