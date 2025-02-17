import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal.windows import hann

def plotWaveForm(data,dt):
    t=np.arange(0,10,1/sr)
    period_num=5
    n_period=dt*period_num
    plt.figure()
    plt.plot(t,data)
    plt.xlabel("time(s)")
    plt.ylabel("Sound Pressure")
    plt.xlim(9.8-(dt/10),9.8+n_period+(dt/10))
    plt.ylim(-1,1)
    plt.grid()
    plt.show()
    
def plotFFT(data):
    N=len(data)
    fft=np.fft.fft(data)
    fft_abs=2*(np.abs(fft)/N)
    correction_factor = np.sum(window) / len(window)  # 窓関数の振幅値の補正
    corrected_signal = fft_abs / correction_factor
    fft_log=20*np.log10(corrected_signal)
    dt=1/sr
    freq = np.fft.fftfreq(N, d=dt)
    plt.figure()
    plt.plot(freq[0:int(N/2)],fft_log[0:int(N/2)])
    plt.ylim(-100,10)
    plt.xlabel("log-Frequency(Hz)")
    plt.ylabel("Amplitude(dB)")
    plt.xscale('log')
    plt.grid()
    plt.show()
    
file_path=input("分析するファイルのパスを入力してください。\n")
sr, data = read(fr"{file_path}")
import generate as gen
f=100
# data=gen.periodic_complex_tone_chord(0.5)
# sr=44100
# data=data/32768
data=data/2
second=9.8
dt=1/f
plotWaveForm(data,dt)
n_fft=2048
signal=data[int(second*sr):int((second*sr)+n_fft)]
window=hann(n_fft)
w_signal=window*signal
plotFFT(w_signal)


