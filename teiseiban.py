import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.io.wavfile import read
from scipy.signal.windows import hann

def linear_regression(y,f0):
    #FFT
    N=len(y)
    fft=np.fft.fft(y)
    fft_abs=2*(np.abs(fft)/N)
    correction_factor = np.sum(window) / len(window)
    corrected_signal = fft_abs / correction_factor
    fft_log=20*np.log10(corrected_signal)
    dt=1/sr
    freq = np.fft.fftfreq(N, d=dt)
    #基本音、倍音の振幅を取り出す。例：F0=440Hzの場合、440Hz,880Hz,...の振幅が入っているインデックスを計算して取り出す。
    df=sr/N
    idx_array=np.array([])
    for i in range(f0,22050,f0):
    # for i in range(f0,22050,f0*2):#TS9の場合
        idx=int(i/df)#FFTのデータは、周波数分解能dfの整数倍の周波数の時の振幅データが入っており、取り出したい周波数に最も近い周波数を計算するため、(取り出したい周波数/df)をして小数点を切り捨てる計算をしている。
        idx_array=np.append(idx_array,idx,)
    idx_array=(idx_array).astype(int)
    amplitude=fft_log[idx_array]
    deletelist=[]
    for i in range(len(amplitude)):
        if amplitude[i] < -96:#int16bitの分解能は-96dBあたりまでのため-96dB以下のデータを計算に含まないように削除しています。
            deletelist.append(i)
    idx_array=np.delete(idx_array,deletelist)
    amplitude=np.delete(amplitude,deletelist)

    # print(f"idx:{idx_array}")
    # print(f"amplitude:{amplitude}")
    x=idx_array*df
    log2x=np.log2(x)
    slope, intercept, _,_,_= linregress(log2x, amplitude)
    print(f"傾き (slope): {slope}")
    print(f"切片 (intercept): {intercept}")
    y_pred = slope * np.log2(x) + intercept
    plt.figure(figsize=(8, 6))
    plt.plot(freq[0:int(N/2)],fft_log[0:int(N/2)],label="data", color="blue")
    plt.scatter(x, amplitude,color="green")
    plt.plot(x, y_pred, label=f" y = {slope}x + {intercept}", color="red")
    plt.title("linear regression")
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("Amplitude(dB)")
    plt.xscale("log")
    plt.ylim(-100,10)
    plt.legend()
    plt.grid()
    plt.show()
    return slope
second=6
n_fft=2048
dir_path=input("分析するファイルのパスを入力してください。\n")
f0=int(input("基本周波数を入力してください"))
sr,y=read(f"{dir_path}")
y=y/32768
signal=y[int(second*sr):int((second*sr)+n_fft)]
window=hann(n_fft)
w_signal=window*signal
slope=linear_regression(w_signal,f0)
print(f"slope:{slope}")