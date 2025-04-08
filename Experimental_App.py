import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import generate as gen
import sounddevice as sd
import make_dir as md
from scipy.io.wavfile import write
from scipy.io.wavfile import read
from PIL import ImageTk, Image
import datetime
from decimal import Decimal, ROUND_HALF_UP
from scipy.signal.windows import hann

global sr #サンプリングレート
sr=44100
global recording_data
recording_data=[]
global cnt
cnt = 0  # レコーディング実行回数
global message_cnt
message_cnt=0
global parameters 

parameters = [
    [0, 0, 0],
    [0, 0, 5],
    [0, 0, 10],
    [0, 5, 5],
    [0, 5, 10],
    [0, 10, 5],
    [0, 10, 10],
    [5, 0, 5],
    [5, 0, 10],
    [5, 5, 5],
    [5, 5, 10],
    [5, 10, 5],
    [5, 10, 10],
    [10, 0, 5],
    [10, 0, 10],
    [10, 5, 5],
    [10, 5, 10],
    [10, 10, 5],
    [10, 10, 10]
]

def setting_submit():
    try:#UIコンポーネントからデータを取得
        playback_device = playback_combobox.get()
        record_device = record_combobox.get()
        sound_type = sound_type_var.get()
        use_fade = fade_check_var.get()
        amplitude=float(amplitude_entry.get())
        frequency = int(freq_entry.get())
        overtone = int(overtone_entry.get())
        sd.default.latency="low"
        if playback_device[2:4].find(" ") != -1:
            playback_device=int(playback_device[3])
        else:
            playback_device=int(playback_device[2:4])
        if record_device[2:4].find(" ") != -1:
            record_device=int(record_device[3])
        else:
            record_device=int(record_device[2:4])
        sd.default.device =record_device,playback_device
    except ValueError:
        messagebox.showerror("エラー", "デバイスを選択してください")
        return
    except Exception as e:
        messagebox.showerror("エラー", f"予期しないエラーが発生しました: \n{e}")
        return
    global signal
    match sound_type:#選択された信号の生成
        case 1: signal=gen.pure_tone(amplitude,frequency);test_signal=gen.pure_tone(amplitude,frequency,duration=1)
        case 2: signal=gen.preodic_complex_tone(amplitude,frequency,overtone=overtone);test_signal=gen.preodic_complex_tone(amplitude,frequency,overtone=overtone,duration=1)
        case 3: sr,signal=read("white_noise.wav");sr,test_signal=read("white_noise.wav");test_signal=test_signal[0:sr*1]
        case 4: signal=gen.periodic_complex_tone_chord(amplitude,overtone=overtone);test_signal=gen.periodic_complex_tone_chord(amplitude,overtone=overtone,duration=1)
    if use_fade==1:#フェードインの使用可否
        signal=gen.fade_in(signal)
    signal=gen.add_silent(signal)
    test_signal=gen.add_silent(test_signal)
    root.withdraw()
    input_level_adjustment_window(test_signal,duration=1)

def fft_setting_window():#FFTの設定
    fft_setting_window = tk.Toplevel(root)
    fft_setting_window.title("Experimental-App")
    fft_setting_window.geometry("800x600")
    fft_setting_window.resizable(0, 0)
    
    title_label = tk.Label(fft_setting_window, 
                           text="---------------------------------------------------------FFT SET UP----------------------------------------------------------",
                           font=("Times", 14, "bold"))
    title_label.pack(pady=10)
    message_label = tk.Label(fft_setting_window, text="FFTを行うポイント(秒)を設定してください。\n入力する値は0~9の整数値を使用してください。", font=("Times", 14))
    message_label.pack(pady=20)

    canvas = tk.Canvas(fft_setting_window, width=503, height=202)
    canvas.pack()
    image = Image.open(r'c:\Research\recording_application\image\figure.png')
    global photo
    photo = ImageTk.PhotoImage(image, master=fft_setting_window)
    canvas.create_image(251.5, 101, image=photo)
    point_entry_frame = tk.Frame(fft_setting_window, padx=20, pady=10)
    point_entry_frame.pack()

    point1_label = tk.Label(point_entry_frame, text="Point1", font=("Times", 14))
    point1_label.grid(row=0, column=0, padx=40)
    point1_entry = tk.Entry(point_entry_frame, width=10, font=("Times", 14), justify=tk.CENTER)
    point1_entry.insert(0, 3)
    point1_entry.grid(row=1, column=0, padx=40)
    point2_label = tk.Label(point_entry_frame, text="Point2", font=("Times", 14))
    point2_label.grid(row=0, column=1, padx=40)
    point2_entry = tk.Entry(point_entry_frame, width=10, font=("Times", 14), justify=tk.CENTER)
    point2_entry.insert(0, 6)
    point2_entry.grid(row=1, column=1, padx=40)
    point3_label = tk.Label(point_entry_frame, text="Point3", font=("Times", 14))
    point3_label.grid(row=0, column=2, padx=40)
    point3_entry = tk.Entry(point_entry_frame, width=10, font=("Times", 14), justify=tk.CENTER)
    point3_entry.insert(0, 9)
    point3_entry.grid(row=1, column=2, padx=40)
    
    scale_frame=tk.Frame(fft_setting_window, padx=20, pady=10)
    scale_frame.pack()
    xscale_label=tk.Label(scale_frame,text="横軸(周波数)",font=("Times",12))
    xscale_label.grid(row=2,column=0,padx=40)
    linear_scale=tk.Radiobutton(scale_frame,text="線形軸",variable=xscale_var,value=1,font=("Times", 12))
    linear_scale.grid(row=3,column=0,padx=40)
    log_scale=tk.Radiobutton(scale_frame,text="対数軸",variable=xscale_var,value=2,font=("Times", 12))
    log_scale.grid(row=4,column=0,padx=40)
    yscale_label=tk.Label(scale_frame,text="縦軸(振幅)",font=("Times",12))
    yscale_label.grid(row=2,column=1,sticky="w",padx=40)
    default_scale=tk.Radiobutton(scale_frame,text="デフォルト値(0~1)",variable=yscale_var,value=1,font=("Times", 12))
    default_scale.grid(row=3,column=1,sticky="w",padx=40)
    dB_scale=tk.Radiobutton(scale_frame,text="dB値",variable=yscale_var,value=2,font=("Times", 12))
    dB_scale.grid(row=4,column=1,sticky="w",padx=40)
    submit_button = tk.Button(fft_setting_window, text="OK", width=17, bg="black", fg="white", font=("Times", 14), 
                              command=lambda:fft_setting_submit(point1_entry,point2_entry,point3_entry,fft_setting_window))
    submit_button.pack(pady=20)

def fft_setting_submit(entry1,entry2,entry3,window):#FFTの設定値の取得
    fft_point1_var.set(float(entry1.get()))
    fft_point2_var.set(float(entry2.get()))
    fft_point3_var.set(float(entry3.get()))
    window.destroy()

def time_wav_setting_window():#時間波形の設定
    time_wav_setting_window = tk.Toplevel(root)
    time_wav_setting_window.title("Experimental-App")
    time_wav_setting_window.geometry("800x550")
    time_wav_setting_window.resizable(0, 0)
    
    title_label = tk.Label(time_wav_setting_window, 
                           text="---------------------------------------------------------TIME WAVFORM SET UP----------------------------------------------------------",
                           font=("Times", 14, "bold"))
    title_label.pack(pady=10)
    message_label = tk.Label(time_wav_setting_window, text="プロットしたい時間波形ポイント(秒)を設定してください。\n入力する値は0~9の整数値を使用してください。", font=("Times", 14))
    message_label.pack(pady=20)

    canvas = tk.Canvas(time_wav_setting_window, width=503, height=202)
    canvas.pack()
    image = Image.open(r'c:\Research\recording_application\image\figure.png')
    global photo
    photo = ImageTk.PhotoImage(image, master=time_wav_setting_window)
    canvas.create_image(251.5, 101, image=photo)
    point_entry_frame = tk.Frame(time_wav_setting_window, padx=20, pady=10)
    point_entry_frame.pack()

    point1_label = tk.Label(point_entry_frame, text="Point1", font=("Times", 14))
    point1_label.grid(row=0, column=0, padx=40)
    point1_entry = tk.Entry(point_entry_frame, width=10, font=("Times", 14), justify=tk.CENTER)
    point1_entry.insert(0, 3)
    point1_entry.grid(row=1, column=0, padx=40)
    point2_label = tk.Label(point_entry_frame, text="Point2", font=("Times", 14))
    point2_label.grid(row=0, column=1, padx=40)
    point2_entry = tk.Entry(point_entry_frame, width=10, font=("Times", 14), justify=tk.CENTER)
    point2_entry.insert(0, 6)
    point2_entry.grid(row=1, column=1, padx=40)
    point3_label = tk.Label(point_entry_frame, text="Point3", font=("Times", 14))
    point3_label.grid(row=0, column=2, padx=40)
    point3_entry = tk.Entry(point_entry_frame, width=10, font=("Times", 14), justify=tk.CENTER)
    point3_entry.insert(0, 9)
    point3_entry.grid(row=1, column=2, padx=40)
    
    full_check = tk.Checkbutton(time_wav_setting_window, text="時間波形の全体をプロットする。", variable=full_var, font=("Times", 14))
    full_check.pack(anchor=tk.W,padx=140,pady=5)
    submit_button = tk.Button(time_wav_setting_window, text="OK", width=17, bg="black", fg="white", font=("Times", 14), 
                              command=lambda:time_wav_setting_submit(point1_entry,point2_entry,point3_entry,time_wav_setting_window))
    submit_button.pack(pady=20)

def time_wav_setting_submit(entry1,entry2,entry3,window):#時間波形の設定
    time_wav_point1_var.set(float(entry1.get()))
    time_wav_point2_var.set(float(entry2.get()))
    
    time_wav_point3_var.set(float(entry3.get()))
    window.destroy()

def save_settings_to_file(path):#設定をテキストファイルに保存する処理
    filename = fr"{path}\settings_file.txt"
    with open(filename, "w", encoding="utf-8") as f:
        dt_now = datetime.datetime.now()
        f.write(f"録音日時：{dt_now.strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write(f"サンプリング周波数: {sr} Hz\n")
        f.write(f"再生機器: {playback_devices[playback_combobox.current()]}\n")
        f.write(f"録音機器: {record_devices[record_combobox.current()]}\n")
        sound_type_str = "純音" if sound_type_var.get() == 1 else "周期的複合音"
        f.write(f"音の種類: {sound_type_str}\n")
        f.write(f"振幅値:{amplitude_entry.get()}\n")
        f.write(f"周波数(基本周波数): {freq_entry.get()} Hz\n")
        fade_str = "使用" if fade_check_var.get() == 1 else "不使用"
        f.write(f"フェード: {fade_str}\n")
        if sound_type_var.get() == 2:  # 周期的複合音の場合
            f.write(f"倍音数: {overtone_entry.get()}\n")
        f.write("時間波形の保存:Yes\n") if time_wave_var.get() == 1 else f.write("時間波形の保存:No\n")
        f.write("周波数スペクトルの保存:Yes\n") if frequency_spectrum_var.get() == 1 else f.write("周波数スペクトルの保存:No\n")
        f.write("WAVファイルの保存::Yes\n") if save_wav_var.get() == 1 else f.write("WAVファイルの保存::No\n")
        f.write(f"FFTポイント1: {fft_point1_var.get()}秒\n")
        f.write(f"FFTポイント2: {fft_point2_var.get()}秒\n")
        f.write(f"FFTポイント3: {fft_point3_var.get()}秒\n")
        f.write(f"時間波形をプロットするポイント1: {time_wav_point1_var.get()}秒\n")
        f.write(f"時間波形をプロットするポイント2: {time_wav_point2_var.get()}秒\n")
        f.write(f"時間波形をプロットするポイント3: {time_wav_point3_var.get()}秒\n")
        f.write("横軸:  線形軸\n") if xscale_var.get() == 1 else f.write("横軸:  対数軸\n")
        f.write("縦軸:  デフォルト値(0~1)\n") if xscale_var.get() == 1 else f.write("縦軸:  dB値\n")
    print(f"設定が'{filename}'に保存されました。")

def input_level_adjustment_window(test_signal,duration):#オーディオI/Oの入力レベルを調整する処理
    level_window = tk.Toplevel(root)
    level_window.title("Experimental-App")
    level_window.geometry("800x450")
    level_window.resizable(0, 0)
    def display_input_level():
        try:
            recording=sd.playrec(test_signal,samplerate=sr,channels=1,dtype=np.int16)
            sd.wait()
        except Exception as e:
            messagebox.showerror("エラー", f"予期しないエラーが発生しました: \n{e}")
            return
        for i in range((duration+1)*sr):
            if(recording[i]!=0):
                break
        rec_time=sr*duration
        signal=recording[i:i+rec_time]/np.iinfo(np.int16).max
        max=Decimal(str(signal.max())).quantize(Decimal("0.001"),ROUND_HALF_UP)
        max_input_level.set(f"振幅値: {max}")
        
    title_label = tk.Label(level_window, text="---------------------------------------------------------INPUT LEVEL ADJUSTMENT----------------------------------------------------------", font=("Times", 14, "bold"))
    title_label.pack(pady=10)
    title_label = tk.Label(level_window, text=
                           "オーディオインターフェイスの入力レベルを調整します\n画面に表示される値が設定した振幅値と同じになるように\nオーディオインターフェイスの入力レベル調整してください。\nまた最大出力が1.0より小さい値になることを確認してください。", font=("Times", 14))
    title_label.pack(pady=10)
    max_input_level = tk.StringVar()
    max_input_level.set("振幅値：")
    level_label = tk.Label(level_window, textvariable=max_input_level, font=("Times", 14))
    level_label.pack(pady=20)

    recording_button = tk.Button(level_window, text="現在の録音レベルを確認", bg="black", fg="white", width=25, font=("Times", 12),relief=tk.RAISED ,command=display_input_level)
    recording_button.pack()
    start_button = tk.Button(level_window, text="録音開始", bg="black", fg="white", width=10, font=("Times", 12),relief=tk.RAISED,pady=10, command=lambda:recording_window(level_window))
    if(rec_times.get() == 1):
        start_button.config(command=lambda:n_times_recording_window(level_window))
    start_button.pack(padx=50,pady=65,anchor=tk.E)
    
def analysis():#録音データの分析
    path=md.make_empty_dir()
    def plot_time_wav(text,point=-1):#時間波形の描画用の関数
        t=np.arange(0,len(recording_data[i])/sr,1/sr)
        data=np.array(recording_data[i])/np.iinfo(np.int16).max
        plt.figure()
        plt.plot(t,data)
        if point != -1:
            range=5/int(freq_entry.get()) #任意の周波数で5周期分をプロットする。
            match point:
                case 1: plt.xlim(int(time_wav_point1_var.get()),int(time_wav_point1_var.get())+range)
                case 2: plt.xlim(int(time_wav_point2_var.get()),int(time_wav_point2_var.get())+range)
                case 3: plt.xlim(int(time_wav_point3_var.get()),int(time_wav_point3_var.get())+range)
        plt.xlabel("time(s)")
        plt.ylabel("Sound Pressure") 
        plt.grid()
        plt.ylim(-1,1)
        if rec_times.get() == 0 :
            plt.savefig(fr'{path_time_domain}\{parameters[i]}_{text}.png')
        else:
            plt.savefig(fr'{path_time_domain}\plot{i+1}_{text}.png')
        plt.close()
    if time_wave_var.get()==True:#時間波形の描画処理
        path_time_domain=md.make_dir(path,"time_domain")
        for i in range(len(recording_data)):
            if full_var.get() == True:
                plot_time_wav(text="full")
            plot_time_wav(text=f"{time_wav_point1_var.get()}sec",point=1)
            plot_time_wav(text=f"{time_wav_point2_var.get()}sec",point=2)
            plot_time_wav(text=f"{time_wav_point3_var.get()}sec",point=3)

    if save_wav_var.get()==True:#録音データをWAVファイルとして保存する処理
        path_wav=md.make_dir(path,"wav_files")  
        for i in range(len(recording_data)):
            if rec_times.get() == 0:
                write(fr"{path_wav}\{parameters[i]}.wav",sr,recording_data[i]) 
            else:
                write(fr"{path_wav}\recording{i+1}.wav",sr,recording_data[i]) 
            
    def FFT(data,point):#FFTの実行及び周波数スペクトルの保存を行う関数
        N=len(data)
        window=hann(n_fft)
        w_data=window*data
        fft=np.fft.fft(w_data)
        fft_abs=2*(np.abs(fft)/N)#FFT値の絶対値
        correction_factor = np.sum(window) / len(window)#窓関数の計算誤差を補正
        corrected_signal = fft_abs / correction_factor
        dt=1/sr
        freq = np.fft.fftfreq(N, d=dt)
        plt.figure()
        plt.grid()
        if(yscale_var.get()==1):
        #相対値(0~1)
            plt.plot(freq[0:int(N/2)],fft_abs[0:int(N/2)])
            use_frequency=int(freq_entry.get())
            plt.xlim(use_frequency-(use_frequency/2),use_frequency*10)
            if(xscale_var.get()==1):
            #linear-scale
                plt.xlabel("Frequency(Hz)")
                plt.ylabel("Amplitude")
            else:
            #log-scale
                plt.xlabel("log-Frequency(Hz)")
                plt.ylabel("Amplitude")
                plt.xscale('log')
        else:
        #dB値
            fft_log=20*np.log10(corrected_signal)
            plt.plot(freq[0:int(N/2)],fft_log[0:int(N/2)])
            plt.ylim(-100,10)
            if(xscale_var.get()==1):
            #linear-scale
                plt.xlabel("Frequency(Hz)")
                plt.ylabel("Amplitude(dB)")
            else:
            #log-scale
                plt.xlabel("log-Frequency(Hz)")
                plt.ylabel("Amplitude(dB)")
                plt.xscale('log')
        if(rec_times.get()==0):
            plt.savefig(fr"{path_spectrum}\{parameters[i]}{point}sec.png")
        else:
            plt.savefig(fr"{path_spectrum}\plot[{i}]{point}sec.png")
        plt.close()
            
    if frequency_spectrum_var.get()==True:#FFTの実行および周波数スペクトルの保存
        n_fft=2048
        path_spectrum=md.make_dir(path,"frequency_spectrum")
        for i in range(len(recording_data)):
            if rec_times.get() == 0:
                fs,data=read(fr"{path_wav}\{parameters[i]}.wav")
            else:
                fs,data=read(fr"{path_wav}\recording{i+1}.wav")
            data=data/np.iinfo(np.int16).max
            data1=data[int(fft_point1_var.get()*sr):int((fft_point1_var.get()*sr)+n_fft)]
            data2=data[int(fft_point2_var.get()*sr):int((fft_point2_var.get()*sr)+n_fft)]
            data3=data[int(fft_point3_var.get()*sr):int((fft_point3_var.get()*sr)+n_fft)]
            FFT(data1,fft_point1_var.get())
            FFT(data2,fft_point2_var.get())
            FFT(data3,fft_point3_var.get())
    return path

def end():#アプリケーションの終了
    root.quit()
    root.destroy()
    
def analysis_window():#分析中の画面
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Experimental-App")
    analysis_window.geometry("800x400")
    analysis_window.resizable(0, 0)
    title_label = tk.Label(
        analysis_window, 
        text="-------------------------------------------------------ANALYSIS--------------------------------------------------------",
        font=("Times", 14, "bold"))
    title_label.pack(pady=10)
    
    analysis_message_label = tk.Label(analysis_window, text="録音データを分析しています。", font=("Times", 14))
    analysis_message_label.pack(pady=20)
    path=analysis()
    save_settings_to_file(path)
    analysis_message_label.configure(text=f"録音データの分析が終了しました。\n分析結果は{path}に保存されています。")
    end_button=tk.Button(analysis_window,text="END",bg="black", fg="white", width=17, font=("Times", 12), command=end)
    end_button.pack(pady=10)
    
def recording_window(level_window):#レコーディング中の画面
    level_window.destroy()
    recording_window = tk.Toplevel(root)
    recording_window.title("Experimental-App")
    recording_window.geometry("800x400")
    recording_window.resizable(0, 0)
    
    def recording():#18通りのパラメータ設定でのレコーディング用の関数
        global cnt
        global message_cnt
        
        if cnt < len(parameters):  # レコーディング処理 
            message_label.config(text=messages[message_cnt+1])
            ready_button.config(state=tk.DISABLED)
            recorded_signal=sd.playrec(signal,samplerate=sr,channels=1,dtype=np.int16)#録音開始された時点を調べる
            sd.wait()
            for i in range((10+1)*sr):#録音開始された時点を調べる
                if(recorded_signal[i]!=0):
                    break
            rec_time=sr*10
            sliced_signal=recorded_signal[i:i+rec_time]#録音部分を抽出
            recording_data.append(sliced_signal)#録音データを保存する。
            cnt += 1
            if cnt < len(parameters):  # 次のパラメータがある場合
                message_label.config(text=messages[message_cnt+1])
                drive_val_label.config(text=parameters[cnt][0])
                tone_val_label.config(text=parameters[cnt][1])
                level_val_label.config(text=parameters[cnt][2])
                ready_button.config(state=tk.NORMAL)
            else:  # レコーディング終了時の処理
                message_label.config(text=messages[message_cnt+2])
                ready_button.config(state=tk.DISABLED)
                recording_window.destroy()
                recording_window.after(1000, analysis_window())  
            
    title_label = tk.Label(recording_window, 
                           text="---------------------------------------------------------RECORDING----------------------------------------------------------",
                           font=("Times", 14, "bold"))
    title_label.pack(pady=10)
    messages=[
        "まずはBYPASSの状態で録音を行います。\nエフェクターをOFFにして、準備完了ボタンを押してください。",
        "パラメータを変更してください。",
        "全パラメータで録音が終了しました",
    ]
    message_label = tk.Label(recording_window, text=messages[message_cnt], font=("Times", 14))
    message_label.pack(pady=20)
    param_frame = tk.Frame(recording_window)
    param_frame.pack(pady=20)
    drive_label = tk.Label(param_frame, text="DRIVE", font=("Helvetica", 12, "bold"))
    drive_label.grid(row=0, column=0, padx=20)
    drive_val_label = tk.Label(param_frame, text=parameters[cnt][0], font=("Times", 14), borderwidth=3, relief=tk.RAISED, width=5, height=2)
    drive_val_label.grid(row=1, column=0, padx=20)
    tone_label = tk.Label(param_frame, text="TONE", font=("Helvetica", 12, "bold"))
    tone_label.grid(row=0, column=1, padx=20)
    tone_val_label = tk.Label(param_frame, text=parameters[cnt][1], font=("Times", 14), borderwidth=3, relief=tk.RAISED, width=5, height=2)
    tone_val_label.grid(row=1, column=1, padx=20)
    level_label = tk.Label(param_frame, text="LEVEL", font=("Helvetica", 12, "bold"))
    level_label.grid(row=0, column=2, padx=20)
    level_val_label = tk.Label(param_frame, text=parameters[cnt][2], font=("Times", 14), borderwidth=3, relief=tk.RAISED, width=5, height=2)
    level_val_label.grid(row=1, column=2, padx=20)
    ready_button = tk.Button(recording_window, text="準備完了", bg="black", fg="white", font=("Times", 12), command=lambda:recording())
    ready_button.pack(pady=20)
    
def n_times_recording_window(level_window):#ユーザ指定の回数の録音を行う場合
    level_window.destroy()
    recording_window = tk.Toplevel(root)
    recording_window.title("Experimental-App")
    recording_window.geometry("800x400")
    recording_window.resizable(0, 0)
    
    def recording():#レコーディング処理
        global cnt
        global message_cnt
        if cnt < int(rec_times_entry.get()):  # レコーディング処理 
            ready_button.config(state=tk.DISABLED)
            recorded_signal=sd.playrec(signal,samplerate=sr,channels=1,dtype=np.int16)#再生・録音
            sd.wait()
            for i in range((10+1)*sr):#録音開始された時点を調べる
                if(recorded_signal[i]!=0):
                    break
            signal_length=sr*10
            sliced_signal=recorded_signal[i:i+signal_length]#録音部分を抽出
            recording_data.append(sliced_signal)#録音データを保存する。
            cnt += 1
            done_label.config(text=f"実行回数\n{cnt}")#録音回数を更新
            if cnt < int(rec_times_entry.get()):  # 次のパラメータがある場合
                ready_button.config(state=tk.NORMAL)
            else:  # レコーディング終了時の処理
                message_label.config(text=messages[message_cnt+1])
                ready_button.config(state=tk.DISABLED)
                recording_window.destroy()
                recording_window.after(1000, analysis_window())  
            
    title_label = tk.Label(recording_window, 
                        text="---------------------------------------------------------RECORDING----------------------------------------------------------",
                        font=("Times", 14, "bold"))
    title_label.pack(pady=10)
    messages=[
        "録音の準備が完了したら、準備完了ボタンを押してください。",
        "録音が終了しました",
    ]
    message_label = tk.Label(recording_window, text=messages[message_cnt], font=("Times", 14))
    message_label.pack(pady=40)
    times_frame=tk.Frame(recording_window)
    times_frame.pack(pady=20)
    total_label=tk.Label(times_frame,text=f"録音回数\n{rec_times_entry.get()}",font=("Times", 14))
    total_label.grid(row=0,column=0,padx=20)
    done_label=tk.Label(times_frame,text=f"実行回数\n{cnt}",font=("Times", 14))
    done_label.grid(row=0,column=1,padx=20)
    ready_button = tk.Button(recording_window, text="準備完了", bg="black", fg="white", font=("Times", 12), command=lambda:recording())
    ready_button.pack(pady=20)

#ルートウィンドウの設定
root = tk.Tk()
root.title("Experimental-App")
root.resizable(0, 0)
root.geometry("1000x450")
# セットアップウィンドウ
setup_label = tk.Label(root, 
                       text="---------------------------------------------------------SET UP----------------------------------------------------------",
                       font=("Times", 14, "bold"))
setup_label.pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(expand=True)

# デバイスセッティング
frame_device = tk.Frame(main_frame, padx=20, pady=10)
frame_device.grid(row=0, column=0, sticky="n")

device_label = tk.Label(frame_device, text="デバイスセッティング", font=("Helvetica", 12, "bold"))
device_label.pack(anchor=tk.W)

playback_label = tk.Label(frame_device, text="再生デバイス", font=("Times", 12))
playback_label.pack(anchor=tk.W)
playback_devices=str(sd.query_devices()).splitlines()
playback_combobox = ttk.Combobox(frame_device, values=playback_devices, font=("Times", 12), state="readonly", width=40)
playback_combobox.set("Select Device")
playback_combobox.pack(anchor=tk.W, pady=10)

record_label = tk.Label(frame_device, text="録音デバイス", font=("Times", 12))
record_label.pack(anchor=tk.W)
record_devices =str(sd.query_devices()).splitlines()
record_combobox = ttk.Combobox(frame_device, values=record_devices, font=("Times", 12), state="readonly", width=40)
record_combobox.set("Select Device")
record_combobox.pack(anchor=tk.W, pady=10)

rec_times_label=tk.Label(frame_device,text="録音方式",font=("Helvetica", 12, "bold"))
rec_times_label.pack(anchor=tk.W, pady=10)
rec_times=tk.IntVar()
rec_times.set(0)
default_radio=tk.Radiobutton(frame_device, text="エフェクタの全パラメータで録音を行う", variable=rec_times, value=0, font=("Times", 12))
default_radio.pack(anchor=tk.W)
any_radio=tk.Radiobutton(frame_device, text="任意の回数録音を行う", variable=rec_times, value=1, font=("Times", 12))
any_radio.pack(anchor=tk.W)
rec_times_entry=tk.Entry(frame_device, font=("Times", 12))
rec_times_entry.insert(0,1)
rec_times_entry.pack(anchor=tk.W, pady=10)

# サウンドセッティング
frame_sound = tk.Frame(main_frame, padx=20, pady=10)
frame_sound.grid(row=0, column=1, sticky="n")

sound_label = tk.Label(frame_sound, text="サウンド・セッティング", font=("Helvetica", 12, "bold"))
sound_label.pack(anchor=tk.W)

sound_type_var = tk.IntVar(value=1)
pure_tone_radio = tk.Radiobutton(frame_sound, text="純音", variable=sound_type_var, value=1, font=("Times", 12))
pure_tone_radio.pack(anchor=tk.W)

preodic_complex_tone_radio = tk.Radiobutton(frame_sound, text="調波複合音", variable=sound_type_var, value=2, font=("Times", 12))
preodic_complex_tone_radio.pack(anchor=tk.W)

whitenoise_radio = tk.Radiobutton(frame_sound, text="ホワイトノイズ", variable=sound_type_var, value=3, font=("Times", 12))
whitenoise_radio.pack(anchor=tk.W)

chord_tone_radio=tk.Radiobutton(frame_sound, text="調波複合音の和音", variable=sound_type_var, value=4, font=("Times", 12))
chord_tone_radio.pack(anchor=tk.W)

fade_check_var = tk.IntVar(value=1)
fade_check = tk.Checkbutton(frame_sound, text="フェードの使用", variable=fade_check_var, font=("Times", 12))
fade_check.pack(anchor=tk.W, pady=5)

amplitude_label=tk.Label(frame_sound, text="振幅値", font=("Times", 12))
amplitude_label.pack(anchor=tk.W)
amplitude_entry = tk.Entry(frame_sound,width=20, font=("Times", 12))
amplitude_entry.insert(0,1)
amplitude_entry.pack(anchor=tk.W, pady=5)

freq_label = tk.Label(frame_sound, text="周波数(基本周波数)", font=("Times", 12))
freq_label.pack(anchor=tk.W)
freq_entry = tk.Entry(frame_sound,width=20, font=("Times", 12))
freq_entry.insert(0,1000)
freq_entry.pack(anchor=tk.W, pady=5)

overtone_label = tk.Label(frame_sound, text="倍音数 (※複合音の場合)", font=("Times", 12))
overtone_label.pack(anchor=tk.W)
overtone_entry = tk.Entry(frame_sound, textvariable=5,width=20, font=("Times", 12))
overtone_entry.insert(0,5)
overtone_entry.pack(anchor=tk.W, pady=5)

# 分析項目
frame_analysis = tk.Frame(main_frame, padx=20, pady=10)
frame_analysis.grid(row=0, column=2, sticky="n")

analysis_label = tk.Label(frame_analysis, text="分析項目", font=("Helvetica", 12, "bold"))
analysis_label.pack(anchor=tk.W)

time_wave_var = tk.IntVar(value=1)
time_wave_check = tk.Checkbutton(frame_analysis, text="時間波形の保存", variable=time_wave_var, font=("Times", 12))
time_wave_check.pack(anchor=tk.W)

frequency_spectrum_var = tk.IntVar(value=1)
frequency_spectrum_check = tk.Checkbutton(frame_analysis, text="周波数スペクトルの保存", variable=frequency_spectrum_var, font=("Times", 12))
frequency_spectrum_check.pack(anchor=tk.W)

save_wav_var = tk.IntVar(value=1)
save_wav_check = tk.Checkbutton(frame_analysis, text="WAVファイルの保存", variable=save_wav_var, font=("Times", 12))
save_wav_check.pack(anchor=tk.W)

fft_setting_button = tk.Button(frame_analysis, text="FFTの設定", bg="black", fg="white", width=17, font=("Times", 12),relief=tk.RAISED, command=fft_setting_window)
fft_setting_button.pack(anchor=tk.W, pady=10)
fft_point1_var=tk.DoubleVar()
fft_point1_var.set(3)
fft_point2_var=tk.DoubleVar()
fft_point2_var.set(6)
fft_point3_var=tk.DoubleVar()
fft_point3_var.set(9)
xscale_var=tk.IntVar()
xscale_var.set(2)
yscale_var=tk.IntVar()
yscale_var.set(2)

time_wav_setting_button = tk.Button(frame_analysis, text="時間波形の設定", bg="black", fg="white", width=17, font=("Times", 12),relief=tk.RAISED, command=time_wav_setting_window)
time_wav_setting_button.pack(anchor=tk.W, pady=10)
time_wav_point1_var=tk.DoubleVar()
time_wav_point1_var.set(3)
time_wav_point2_var=tk.DoubleVar()
time_wav_point2_var.set(6)
time_wav_point3_var=tk.DoubleVar()
time_wav_point3_var.set(9)
full_var = tk.BooleanVar(value=True)

start_button = tk.Button(frame_analysis, text="START", bg="red", fg="white", width=17, height=2, font=("Times", 12),relief=tk.RAISED, command=setting_submit)
start_button.pack(anchor=tk.W, pady=40)

# アプリケーションの実行
root.mainloop()

