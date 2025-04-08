import numpy as np
from scipy.signal import chirp

def pure_tone(A,f,sr=44100,duration=10):
        #generate pure tone:
        t=np.arange(0,duration,1/sr)
        max= np.iinfo(np.int16).max
        y=(max*A*np.sin(2*np.pi*f*t)).astype(np.int16)  #int16bitに変換
        return y

def preodic_complex_tone(A,f0,sr=44100,overtone=5,duration=10):
        #generate preodic complex tone:
        t=np.arange(0,duration,1/sr)
        y=0
        for i in range(1,overtone+1):
                y+=(1/i)*np.sin(2*np.pi*i*f0*t)
        y=A*(y/y.max()) #振幅を正規化
        max= np.iinfo(np.int16).max
        y=(max*y).astype(np.int16) #int16bitに変換
        return y

def periodic_complex_tone_chord(A,overtone=5,f1=329,f2=246,f3=207,f4=164,f5=123,f6=82,duration=10):
        #generate chord tone of periodic complex tone:
        max= np.iinfo(np.int16).max
        first=preodic_complex_tone(1,f1,overtone=overtone,duration=duration)/max
        second=preodic_complex_tone(1,f2,overtone=overtone,duration=duration)/max
        third=preodic_complex_tone(1,f3,overtone=overtone,duration=duration)/max
        fourth=preodic_complex_tone(1,f4,overtone=overtone,duration=duration)/max
        fifth=preodic_complex_tone(1,f5,overtone=overtone,duration=duration)/max
        sixth=preodic_complex_tone(1,f6,overtone=overtone,duration=duration)/max
        y=first+second+third+fourth+fifth+sixth
        y=A*(y/y.max())
        y=(y*max).astype(np.int16)
        return y
        

# def sweep_signal(f_start=20,f_finish=20000,sr=44100,duration=10):
#         #generate chirp signal: 
#         t=np.arange(0,duration,1/sr,dtype=np.float32)
#         t1=duration*sr
#         y=chirp(t,f0=f_start,f1=f_finish,t1=t1,method="linear")
#         return y
#f0:開始周波数
# f1:最高周波数
#t1:f1の周波数に達する時間

def add_silent(y,sr=44100):
        silent=np.zeros(int(sr*1),dtype=np.int16)
        y=np.append(y,silent)
        return y

def fade_in(y):
        for i in range(len(y)):
            y[i]=y[i]*((1+i)/len(y))
        return y

