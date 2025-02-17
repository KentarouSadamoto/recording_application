import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal.windows import hann

def plotWaveForm(data,dt):
    t=np.arange(0,len(data)/sr,1/sr)
    period_num=5
    n_period=dt*period_num
    plt.figure()
    plt.plot(t,data)
    plt.xlabel("time(s)")
    plt.ylabel("Amplitude")
    plt.xlim(0,0.01)
    plt.grid()
    plt.show()
    
def plotFFT(data):
    N=len(data)
    fft=np.fft.fft(data)
    fft_abs=2*(np.abs(fft)/N)
    fft_log=20*np.log10(fft_abs)
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
f=20
sr=44100
dt=1/f
plotWaveForm(data,dt)
n_fft=4096
# window=hann(n_fft)
# w_signal=window*data
plotFFT(data)


