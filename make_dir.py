import datetime
import os

def make_empty_dir():
    dt_now = datetime.datetime.now()
    now=dt_now.strftime('%Y%m%d')
    cnt=1
    make_dir_path=rf"output_data\analysis_{now}"
    while True:
        if os.path.isdir(make_dir_path):
            make_dir_path=rf"output_data\analysis_{now}({cnt})"
            cnt+=1
        else:
            os.makedirs(make_dir_path)
            break
    return make_dir_path

def make_dir(path,name):
    path=rf"{path}\{name}"
    os.makedirs(path)
    return path
    
        