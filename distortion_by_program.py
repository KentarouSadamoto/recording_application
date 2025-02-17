import generate as gen
from scipy.io.wavfile import read
from scipy.io.wavfile import write
from scipy.signal.windows import hann
import numpy as np
import matplotlib.pyplot as plt

def FFT(point,time):
    N=len(point)
    fft=np.fft.fft(point)
    fft_abs=2*(np.abs(fft)/N)
    correction_factor = np.sum(window) / len(window)  # 窓関数の振幅値の補正
    corrected_signal = fft_abs / correction_factor
    fft_log=20*np.log10(corrected_signal)
    dt=1/sr
    freq = np.fft.fftfreq(N, d=dt)
    plt.figure()
    plt.plot(freq[0:int(N/2)],fft_log[0:int(N/2)])
    plt.xlabel("log-Frequency(Hz)")
    plt.ylabel("Amplitude")
    plt.xscale('log')
    plt.ylim(-100,10)
    plt.grid()
    plt.savefig(fr"distortion_by_program_sound\distortion_puretone\frequency_spectrum_gain[{gain}]_{time}sec.png")
    # plt.savefig(fr"distortion_by_program_sound\distortion_preodic_complex_tone\frequency_spectrum_gain[{gain}]_{time}sec.png")
    # plt.savefig(fr"distortion_by_program_sound\distortion_periodic_complex_tone_chord\frequency_spectrum_gain[{gain}]_{time}sec.png")
    plt.close()

def plot_time_wav(text,point=-1):
    t=np.arange(0,len(distorted_sound)/sr,1/sr)
    plt.figure()
    if point != -1:
        plt.plot(t,distorted_sound)
        range=5/int(frequency) #任意の周波数で5周期分をプロットする。
        match point:
            case 1: plt.xlim(time1,time1+range)
            case 2: plt.xlim(time2,time2+range)
    plt.xlabel("time(s)")
    plt.ylabel("Sound Pressure")
    plt.grid()
    if point == -1:
        plt.plot(t,distorted_sound,label="Output Signal")
        plt.plot(t,fade_default,label="Input Signal", alpha=0.1,color="red")
        plt.legend()
        plt.savefig(fr'distortion_by_program_sound\distortion_puretone\time_wavform_gain[{gain}]_{text}.png')
        # plt.savefig(fr"distortion_by_program_sound\distortion_preodic_complex_tone\time_wavform_gain[{gain}]_{text}.png")
        # plt.savefig(fr"distortion_by_program_sound\distortion_periodic_complex_tone_chord\time_wavform_gain[{gain}]_{text}.png")
    else:
        plt.savefig(fr'distortion_by_program_sound\distortion_puretone\time_wavform_gain[{gain}]_{text}.png')
        # plt.savefig(fr"distortion_by_program_sound\distortion_preodic_complex_tone\time_wavform_gain[{gain}]_{text}.png")
        # plt.savefig(fr"distortion_by_program_sound\distortion_periodic_complex_tone_chord\time_wavform_gain[{gain}]_{text}.png")
    plt.close()

def distortion(signal,gain,level):
    dist_sound=gain*signal
    for i in range(len(dist_sound)):
        if dist_sound[i] > 1:
            dist_sound[i]=1
        elif dist_sound[i] < -1:
            dist_sound[i]=-1
    dist_sound*=level
    return dist_sound

sr=44100
duration=10
frequency=440
time1=6
time2=9
# signal=gen.pure_tone(0.5,frequency,duration=duration)
signal=gen.pure_tone(0.5,440)
# signal=read(".wav")
max= np.iinfo(np.int16).max
signal=(signal/max)
signal=gen.fade_in(signal)
gain=4
level=1
distorted_sound=distortion(signal,gain,level)

#時間波形の描画
default=gen.pure_tone(0.5,440)
default=default/32768
fade_default=gen.fade_in(default)
plot_time_wav(text=f"full")
plot_time_wav(text=f"{time1}sec",point=1)
plot_time_wav(text=f"{time2}sec",point=2)
#周波数スペクトルの描画
full=distorted_sound
n_fft=2048
point1=distorted_sound[int(time1*sr):int(time1*sr+n_fft)]
point2=distorted_sound[int(time2*sr):int(time2*sr+n_fft)]
window=hann(n_fft)
w_signal1=window*point1
w_signal2=window*point2
FFT(w_signal1,time1)
FFT(w_signal2,time2)
#WAVファイル書き出し
distorted_sound=(distorted_sound*max).astype(np.int16)
write(fr"distortion_by_program_sound\distortion_puretone\gain[{gain}].wav",sr,distorted_sound)
# write(fr"distortion_by_program_sound\distortion_preodic_complex_tone\gain[{gain}].wav",sr,distorted_sound)
# write(fr"distortion_by_program_sound\distortion_periodic_complex_tone_chord\gain[{gain}].wav",sr,distorted_sound)
    
