import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal.windows import hann

def compute_spectral_slope(signal, fs, f_min=100, f_max=None, plot=True):
    # FFTを計算
    N=len(signal)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    fft_abs = np.abs(np.fft.rfft(signal))/N
    correction_factor = np.sum(window) / len(window)
    corrected_signal = fft_abs / correction_factor
    # dBスケールへ変換
    spectrum_db = 20 * np.log10(corrected_signal) 
    # 指定範囲の周波数を抽出
    valid_idx = (freqs >= f_min) & (freqs <= f_max)
    freqs = freqs[valid_idx]
    spectrum_db = spectrum_db[valid_idx]
    
    print("freqs",freqs)
    log_freqs = np.log2(freqs)
    # #-96dB以下のデータを削除
    # spectrum_db_96=spectrum_db[spectrum_db > -96]
    # log_freqs_96=log_freqs[spectrum_db > -96]
    # 最小二乗法で直線回帰
    slope, intercept = np.polyfit(log_freqs, spectrum_db, 1)

    if plot:
        plt.figure(figsize=(8, 5))
        plt.plot(freqs, spectrum_db, label="spectrum", color="blue", alpha=0.7)
        plt.plot(freqs, slope * np.log2(freqs) + intercept, label=f"spectral slope ({slope:.2f} dB/oct)", color="red", linestyle="--")
        plt.xscale("log")  
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude (dB)")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", alpha=0.5)
        plt.show()

    return slope  # dB/oct の値

n_fft=2048
dir_path=input("分析するファイルのパスを入力してください。\n")
second=int(input("何秒時点のデータを分析しますか"))
f_min,f_max=int(input("分析に使う最低周波数は何Hzですか。")),int(input("分析に使う最高周波数は何Hzですか。"))
sr,y=read(f"{dir_path}")
y=y/32768
signal=y[int(second*sr):int((second*sr)+n_fft)]
window=hann(n_fft)
w_signal=window*signal
slope = compute_spectral_slope(w_signal, sr,f_min=f_min,f_max=f_max)
print(f"スペクトル傾斜: {slope} dB/oct")
