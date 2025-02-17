import librosa
import numpy as np
import generate as gen

file_path=input("分析するファイルのパスを入力してください。\n")
y, sr = librosa.load(fr"{file_path}",sr=44100)
# sr=44100
# y=gen.preodic_complex_tone(0.3,440)
# max= np.iinfo(np.int16).max
# y=y/max
duration=sr
second=6
y=y[second*sr:second*sr+duration]
cent_9sec = librosa.feature.spectral_centroid(y=y, sr=sr)
print(cent_9sec[0,][3:-2])
print(np.round(np.average(cent_9sec[0,][3:-2])))