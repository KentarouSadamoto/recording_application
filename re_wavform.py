import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import generate as gen

def plot_wavform(data,point):
        time=np.arange(0,10,1/sr)
        range=5/int(freq)
        plt.figure()
        if point != -1:
            plt.plot(time,data)
        else:
            plt.plot(time,data,label="Output Signal")
            plt.plot(time,fade_default,label="Input Signal", alpha=0.1,color="red")
        plt.xlabel("Time(s)")
        plt.ylabel("Sound Pressure")
        plt.grid()
        plt.ylim(-1,1)
        if point != -1:
            plt.xlim(point-(dt/10),point+range+(dt/10))
            plt.savefig(f"{savepath}\[{g}, {t}, {l}]{point}sec.png")
        else :
            plt.legend()
            plt.savefig(f"{savepath}\[{g}, {t}, {l}]_full.png")
        plt.close()

sr=44100
filepath=input("分析するフォルダのパスを入力してください")
savepath=input("保存先のフォルダのパスを入力してください")
freq=int(input("基本周波数を入力してください"))
gain=[0,5,10]
tone=[0,5,10]
level=[0,5,10]
cnt=0
default=gen.preodic_complex_tone(0.3,440)
default=default/32768
fade_default=gen.fade_in(default)
dt=1/freq
for g in gain:
        for t in tone:
                for l in level:
                    if l != 0 or g == t == l == 0:
                        sr,signal=read(fr"{filepath}\[{g}, {t}, {l}].wav")
                        signal=signal/32768
                        plot_wavform(signal,3)
                        plot_wavform(signal,6)
                        plot_wavform(signal,9)
                        plot_wavform(signal,-1)

