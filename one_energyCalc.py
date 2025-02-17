import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.io.wavfile import read
from scipy.signal.windows import hann

def EnergyCalc(y,sf,ef):
    N=len(y)
    fft=np.fft.fft(y)
    fft_abs=2*((np.abs(fft))**2/N)
    correction_factor = np.sum(window) / len(window)
    corrected_signal = fft_abs / correction_factor
    fft_log=20*np.log10(corrected_signal)
    dt=1/sr
    freq = np.fft.fftfreq(N, d=dt)
    df=sr/N
    start=int(sf/df)
    end=int(ef/df)
    data=fft_abs[start:end]
    data=data[data>-96]
    energy=sum(data)
    # plt.figure(figsize=(8, 6))
    # plt.plot(freq[0:int(N/2)],fft_log[0:int(N/2)])
    # plt.xlabel("Frequency(Hz)")
    # plt.ylabel("Amplitude")
    # plt.xscale("log")
    # plt.ylim(-100,10)
    # plt.grid()
    # plt.show()
    return energy
n_fft=2048
window=hann(n_fft)
path=input("分析するファイルのパスを入力してください。\n")
second=int(input("何秒時点のエネルギーを計算しますか"))
sf=int(input("何Hzからのエネルギーを計算しますか"))
ef=22050
sr,y=read(path)
y=y/32768
signal=y[int(second*sr):int((second*sr)+n_fft)]
w_signal=window*signal
print(f"{sf}HZから{ef}HZまでのエネルギー：{EnergyCalc(w_signal,sf,ef)}")