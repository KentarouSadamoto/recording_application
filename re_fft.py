import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal.windows import hann

sr=44100

def FFT(data,point):
        N=len(data)
        fft=np.fft.fft(data)
        fft_abs=2*(np.abs(fft)/N)
        correction_factor = np.sum(window) / len(window)  # 窓関数の平均値を計算
        corrected_signal = fft_abs / correction_factor    # 窓関数の振幅値の補正      
        fft_log=20*np.log10(corrected_signal)
        dt=1/sr
        freq = np.fft.fftfreq(N, d=dt)
        plt.figure()
        plt.plot(freq[0:int(N/2)],fft_log[0:int(N/2)])
        plt.xlabel("log-Frequency(Hz)")
        plt.ylabel("Amplitude(dB)")
        plt.xscale('log')
        plt.ylim(-100,0)
        plt.grid()
        plt.savefig(f"{savepath}\[{g}, {t}, {l}]{point}sec.png")
        plt.close()

filepath=input("分析するフォルダのパスを入力してください")
savepath=input("保存先のフォルダのパスを入力してください")
gain=[0,5,10]
tone=[0,5,10]
level=[0,5,10]
cnt=0
for g in gain:
        for t in tone:
                for l in level:
                    if l != 0 or g == t == l == 0:
                        sr,signal=read(fr"{filepath}\[{g}, {t}, {l}].wav")
                        signal=signal/32768
                        n_fft=2048
                        three_sec=signal[int(3*sr):int(3*sr)+n_fft]
                        six_sec=signal[int(6*sr):int(6*sr)+n_fft]
                        nine_sec=signal[int(9*sr):int(9*sr)+n_fft]
                        window=hann(n_fft)
                        w_three=three_sec*window
                        w_six=six_sec*window
                        w_nine=nine_sec*window
                        FFT(w_three,3)
                        FFT(w_six,6)
                        FFT(w_nine,9)

