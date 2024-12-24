#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import os
import subprocess
import glob
import shutil
import matplotlib.pyplot as plt

import zipfile

import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
import tkinter.font as tkFont


# In[3]:


import numpy as np
import pandas as pd
import os
import subprocess
import glob
import shutil
import matplotlib.pyplot as plt

import zipfile

import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
import tkinter.font as tkFont


# # Robustness

# In[4]:


def Robustness(data_list, save_file, cp_fa, cp_ra, mms):
    data = {}
    output = []
    
    for F in data_list:
        df = pd.read_table(F, sep=',')
        data[F] = df

    if data != []:
        df_con, output = CONCAT_DATA(data, mms)

        if mms == True:
            df_selected = df_con[(df_con['B_VDCActive'] > 0) & (df_con['B_Active_Ext5ms'] == 0)]
        else:
            df_selected = df_con[(df_con['B_VDCActive'] > 0) & (df_con['l_AHA_Act'] == 0)]
        
        df_selected['MbWheelTar_Fx'] = np.maximum(df_selected['MbWheelTar_FL'], df_selected['MbWheelTar_FR'])
        df_selected['MbWheelTar_Rx'] = np.maximum(df_selected['MbWheelTar_RL'], df_selected['MbWheelTar_RR'])
        # df_selected['p_Model_Fx'] = np.maximum(df_selected['p_Model_FL'], df_selected['p_Model_FR'])
        # df_selected['p_Model_Rx'] = np.maximum(df_selected['p_Model_RL'], df_selected['p_Model_RR'])
        
        df_us_fa = df_selected[(df_selected['MbWheelTar_Fx'] > 0) & (df_selected['dMz_TurnDir'] > 0)]
        df_us_ra = df_selected[(df_selected['MbWheelTar_Rx'] > 0) & (df_selected['dMz_TurnDir'] > 0)]
        df_os_fa = df_selected[(df_selected['MbWheelTar_Fx'] > 0) & (df_selected['dMz_TurnDir'] < 0)]
        df_os_ra = df_selected[(df_selected['MbWheelTar_Rx'] > 0) & (df_selected['dMz_TurnDir'] < 0)]

        df_us_fa = df_us_fa.sort_values(by='MbWheelTar_Fx')
        df_os_fa = df_os_fa.sort_values(by='MbWheelTar_Fx')
        df_us_ra = df_us_ra.sort_values(by='MbWheelTar_Rx')
        df_os_ra = df_os_ra.sort_values(by='MbWheelTar_Rx')
        
        x_us_fa = df_us_fa['ayToF']
        y_us_fa = df_us_fa['vRef']
        # values_us_fa = df_us_fa['p_Model_Fx']
        values_us_fa = df_us_fa['MbWheelTar_Fx'] / cp_fa
        
        x_us_ra = df_us_ra['ayToF']
        y_us_ra = df_us_ra['vRef']
        # values_us_ra = df_us_ra['p_Model_Rx']
        values_us_ra = df_us_ra['MbWheelTar_Rx'] / cp_ra
        
        x_os_fa = df_os_fa['ayToF']
        y_os_fa = df_os_fa['vRef']
        # values_os_fa = df_os_fa['p_Model_Fx']
        values_os_fa = df_os_fa['MbWheelTar_Fx'] / cp_fa
        
        x_os_ra = df_os_ra['ayToF']
        y_os_ra = df_os_ra['vRef']
        # values_os_ra = df_os_ra['p_Model_Rx']
        values_os_ra = df_os_ra['MbWheelTar_Rx'] / cp_ra
        
        vmax_fa = 20
        vmax_ra = 20
        
        fig, axs = plt.subplots(2, 2, figsize=(16, 8))
        sc1 = axs[0, 0].scatter(x_us_fa, y_us_fa, c=values_us_fa, vmin=0, vmax=vmax_fa, s=10) 
        axs[0, 0].set_title('US: Front brake[bar]')
        axs[0, 0].set_xlabel('Ay[m/s^2]')
        axs[0, 0].set_ylabel('V[m/s]')
        axs[0, 0].set_xlim(-10, 10)
        axs[0, 0].set_ylim(0, 35)
        fig.colorbar(sc1, ax=axs[0, 0]) 
        
        sc1 = axs[0, 1].scatter(x_us_ra, y_us_ra, c=values_us_ra, vmin=0, vmax=vmax_ra, s=10) 
        axs[0, 1].set_title('US: Rear brake[bar]')
        axs[0, 1].set_xlabel('Ay[m/s^2]')
        axs[0, 1].set_ylabel('V[m/s]')
        axs[0, 1].set_xlim(-10, 10)
        axs[0, 1].set_ylim(0, 35)
        fig.colorbar(sc1, ax=axs[0, 1]) 
        
        sc1 = axs[1, 0].scatter(x_os_fa, y_os_fa, c=values_os_fa, vmin=0, vmax=vmax_fa, s=10) 
        axs[1, 0].set_title('OS: Front brake[bar]')
        axs[1, 0].set_xlabel('Ay[m/s^2]')
        axs[1, 0].set_ylabel('V[m/s]')
        axs[1, 0].set_xlim(-10, 10)
        axs[1, 0].set_ylim(0, 35)
        fig.colorbar(sc1, ax=axs[1, 0]) 
        
        sc1 = axs[1, 1].scatter(x_os_ra, y_os_ra, c=values_os_ra, vmin=0, vmax=vmax_ra, s=10) 
        axs[1, 1].set_title('OS: Rear brake[bar]')
        axs[1, 1].set_xlabel('Ay[m/s^2]')
        axs[1, 1].set_ylabel('V[m/s]')
        axs[1, 1].set_xlim(-10, 10)
        axs[1, 1].set_ylim(0, 35)
        fig.colorbar(sc1, ax=axs[1, 1]) 
        
        plt.subplots_adjust(left=0.05, right=1.0, top=0.95, bottom=0.08, wspace=0.05, hspace=0.25)
        plt.show()
        
        fig.savefig(save_file)

        cols = list(df_selected.columns)
        cols.remove('File')
        cols_new = ['File'] + cols
        df_new = df_selected[cols_new]

        root, ext = os.path.splitext(save_file)
        df_new.to_csv(f'{root}.csv', index=False)

    return output


# In[5]:


def CONCAT_DATA(DATA, mms):
    n = 0
    output = []
    cols_w_mms = ['B_VDCActive', 'B_Active_Ext5ms', 'MbWheelTar_FL', 'MbWheelTar_FR', 'MbWheelTar_RL', 'MbWheelTar_RR', 'dMz_TurnDir', 'ayToF', 'vRef']
    cols_wo_mms = ['B_VDCActive', 'l_AHA_Act', 'MbWheelTar_FL', 'MbWheelTar_FR', 'MbWheelTar_RL', 'MbWheelTar_RR', 'dMz_TurnDir', 'ayToF', 'vRef']

    if mms == True:
        check_cols = cols_w_mms
    else:
        check_cols = cols_wo_mms
    
    for i, file in enumerate(DATA):
        df = DATA[file].copy()
        df['File'] = file
        n1 = n + len(df)
        l_Index = list(np.arange(n, n1))
        # df_['Index'] = l_Index
        df.loc[:, 'Index'] = l_Index
        df = df.set_index('Index')

        not_exsit = []
        for col in check_cols:
            if col not in df.columns:
                not_exsit.append(col)

        if not_exsit != []:
            print(f'no signals: {file}, {not_exsit}')
            output.append(f'no signals: {file}, {not_exsit}')
        
        if i == 0:
            df_out = df
        else:
            df_out = pd.concat([df_out, df])

        n = n1 + 1

    return df_out, output


# # Convert_ZIP_to_CSV

# In[6]:


def Convert_ZIP_to_CSV(data_list, plt_list, Sampling=0.005):    
    outputs = []
    
    for i, Zip in enumerate(data_list):            
        # Size = os.path.getsize(Zip)
        print(i + 1, '/', len(data_list), ';', Zip)
        
        # dirname, basename = os.path.split(Zip)
        # base_name_without_extension = os.path.splitext(os.path.basename(Zip))[0]
        # Csv = f'{dirname}\\{base_name_without_extension}.csv'
        # # Csv = Csv.replace('.ZIP', '.csv')
    
        out, _ = DataTreatment(Zip, plt_list, Sampling)
        
        if out != None:
            outputs.append(out)

    return outputs


# In[7]:


def DataTreatment(File, d_Plt, Sampling, dir=None):
    Csv_out = None
    NotConvert = False

    root, ext = os.path.splitext(File)
    if (ext == ".ZIP" or ext == ".zip") and "ApplContainer" not in File:
        if dir != None:
            dirname, basename = os.path.split(File)
            copyed_File = f'{dir}\\{basename}'
            shutil.copyfile(File, copyed_File)
            File = copyed_File
        
        d97 = UnPackD97(File)

        if d97 != None:
            Plt_new, d_Plt_new, NotAll = MakePLTFromD97(d97, d_Plt)
            
            if Plt_new != None:
                Csv = RunBat(d97, Plt_new, d_Plt_new, Sampling)
                
                dirname, basename = os.path.split(Csv)
                if dir == None:
                    Folder = os.path.dirname(File) + '\\'
                    Csv_out = Folder + basename
                else:
                    base_name_without_extension = os.path.splitext(os.path.basename(File))[0]
                    # 現在の日時を取得し、指定したフォーマットで文字列に変換
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    Csv_out = f'{dirname}\\{base_name_without_extension}_{timestamp}.csv'
                
                os.replace(Csv, Csv_out)                
            
            if Csv_out == None or NotAll == True:
                NotConvert = True
                
        try:
            Remove_w_ExistFile(d97)
            if dir != None:
                Remove_w_ExistFile(File)
        except TypeError:
            if d97 != None:
                print('TypeError:', File, d97)

    return Csv_out, NotConvert


def UnPackD97(file):
    file_d97 = None
    file_in_zip = ''
    
    dirname, basename = os.path.split(file)
    dirname_ = dirname + '/'
    
    try:
        try:
            with zipfile.ZipFile(file) as zf:
                lst = zf.namelist()

                for file_in_zip in lst:
                    root, ext = os.path.splitext(file_in_zip)
                    
                    if ext == ".D97" or ext == ".d97":  
                        # shutil.unpack_archive(file, dirname_, format='zip')
                        
                        with zipfile.ZipFile(file) as existing_zip:
                            existing_zip.extract(file_in_zip, dirname_)
                            
                        file_d97 = file_in_zip
                        break
                        
        except BadZipFile:
            print('BadZipFile')
            file_d97 = None
    except NameError:
        print('NameError')
        if file_in_zip != '':
            Remove_w_ExistFile(Folder + file_in_zip)
            
        file_d97 = None
    
    if file_d97 != None:
        file_out = UnPackD97__Change_FileName(dirname_, file, file_d97)
    else:
        file_out = None
    
    return file_out


def UnPackD97__Change_FileName(Folder, ZIP, D97):    
    # path = Folder + D97
    root, ext = os.path.splitext(ZIP)
    path_new = root + '.D97'
    
    dirname, basename = os.path.split(ZIP)
    path_base = dirname + '/' + D97
    # path_new = Folder + file_name
    
    # print(path_base, path_new)
    # if path_new != path_base:
    #     if os.path.exists(path_new) == True:
    #         os.remove(path_new)
            
    os.rename(path_base, path_new)
    
    return path_new   


def RunBat(file_, Plt, d_Plt, Sampling):
    dirname, basename = os.path.split(file_)
    file = basename
    
    if ".D97" in file:
        CSV = file.replace(".D97", ".CSV")
    elif ".d97" in file:
        CSV = file.replace(".d97", ".CSV")

    # Bat = dirname + "ChangeFormat.bat"
    File0 = dirname + '/' + file
    File1 = dirname + '/' + "1__" + file
    File2 = dirname + '/' + "2__" + file
    File3 = dirname + '/' + "3__" + CSV

    # Text = "MDFDSET3c ifn=" + File0 + ";pltfn=" + Plt + " ofn=" + File1 + "\n"
    Command = "MDFDSET6c ifn=" + File0 + ";pltfn=" + Plt + " ofn=" + File1 + "\n"
    subprocess.call(Command, shell=True)
    
    # Text = "MDFMDL6c ifn=" + File0 + " ofn=" + File1 + " INCLUDE_SG=" + Plt + "\n" 
    
    Command = "MDFMDL6c ifn=" + File1 + " ofn=" + File2 + " tc=" + str(Sampling) + "\n"
    subprocess.call(Command, shell=True)
    
    Command = "SDTM3c ifn=" + File2 + " ofn=" + File3
    subprocess.call(Command, shell=True)
    
#     f = open(Bat, "w")
#     f.write(Text)
#     f.close()

#     res = subprocess.run([Bat], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    Remove_w_ExistFile(File0)
    Remove_w_ExistFile(File1)
    # Remove_w_ExistFile(Bat)

    try:        
        FileOut = ModifyCSV(File3, d_Plt)
        Remove_w_ExistFile(File2)
        Remove_w_ExistFile(File3)
        Remove_w_ExistFile(Plt)
        
    except FileNotFoundError:
        # dirname, basename = os.path.split(file)
        root, ext = os.path.splitext(file_)
        Plt_ = root + '.PLT'
        # Bat_ = root + '.bat'
        
        os.rename(Plt, Plt_)
        
        root, ext = os.path.splitext(File0)
        File0_ = root + '_.D97'
        File3_ = root + '.csv'
        
        # DFMDL6c ifn=c:/TSDE_Workarea/ktt2yk/Work/CarSim/SIM_ABS_Ice/ABS_Ice_N_Spike_base_.D97 t0=1 t1=23 ofn=c:/TSDE_Workarea/ktt2yk/Work/CarSim/SIM_ABS_Ice/1__ABS_Ice_N_Spike_base.D97
        Command = "MDFMDL6c ifn=" + File0 + " t0=0 t1=30" + " ofn=" + File0_ + "\n"
        subprocess.call(Command, shell=True)
        
        Command = "MDFDSET3c ifn=" + File0_ + ";pltfn=" + Plt_ + " ofn=" + File1 + "\n"
        subprocess.call(Command, shell=True)
        
        Command = "MDFMDL6c ifn=" + File1 + " ofn=" + File2 + " tc=" + str(Sampling) + "\n"
        subprocess.call(Command, shell=True)
        
        Command = "SDTM3c ifn=" + File2 + " ofn=" + File3_
        subprocess.call(Command, shell=True)
        
        # f = open(Bat_, "w")
        # f.write(Text_)
        # f.close()
        
        print("FileNotFoundError", Plt_)
        FileOut = None

    return FileOut


def ChangePath(Folder0, File0):
    FILE1 = File0.split("/")
    File = Folder0 + FILE1[-1]
    Folder = Folder0 + FILE1[-2]
    
    return File, Folder, FILE1[-1]


def ModifyCSV(File, d_Plt):
    for i, S in enumerate(d_Plt):
        if i == 0:
            Text_PLT = "TIME" + "," + d_Plt[S]
        else:
            Text_PLT += "," + d_Plt[S]

    with open(File) as f:
        Text_CSV = f.read()

    Text = Text_PLT + "\n" + Text_CSV
    Text = Text.replace(",", "\t")

    f = open(File, "w")
    f.write(Text)
    f.close()
    
    df = pd.read_table(File, sep="\t", index_col=0, skiprows=[1])
    
    dirname, basename = os.path.split(File)
    File2 = dirname + '/' + basename.replace("3__", "")
    # File2 = File2.replace(".CSV", ".csv")
    
    basename_without_ext = os.path.splitext(os.path.basename(File2))[0]
    dirname, basename = os.path.split(File2)
    # now = datetime.datetime.now()
    # FileOut = dirname + '\\' + basename_without_ext + '_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
    FileOut = dirname + '/' + basename_without_ext + '.csv'
    df.to_csv(FileOut)

    # ExistFile(FileOut)

    return FileOut


def Remove_w_ExistFile(PathFile):
    if os.path.exists(PathFile) == True:
        os.remove(PathFile)


# In[8]:


def MakePLTFromD97(File_D97, d_Plt):
    l_Signals_new = []
    d_Plt_new = {}
    
    dirname, basename = os.path.split(File_D97)
    dirname_ = dirname + '/'
    
    D97 = File_D97

    if os.path.exists(D97) == True:
        l_Signals_D97 = ReadD97(D97)
        l_Signals_PLT = list(d_Plt.keys())
        
        for T in l_Signals_PLT:
            if T in l_Signals_D97:
                l_Signals_new.append(T)
            else:
                Error = "Error: " + T + " is nothing."
                # print(Error)

        d_Plt2 = {}
        for S in d_Plt:
            if d_Plt[S] in d_Plt2:
                d_Plt2[d_Plt[S]] = d_Plt2[d_Plt[S]] + [S]
            else:
                d_Plt2[d_Plt[S]] = [S]

        # print(1, d_Plt2)
        NotAll = False
        for S in d_Plt2:
            Found = False
            
            for S1 in d_Plt2[S]:
                if S1 in l_Signals_new:
                    d_Plt_new[S1] = S
                    Found = True
                    break
            
            if Found == False:
                NotAll = True
                    
        # print(2, d_Plt_new)

        Text = ""
        for T in d_Plt_new:
            Text += T + "\n"
        
        # print(3, Text)
                
        Plt_new = dirname_ + 'Temp.PLT'
        
        if Text != "":
            f = open(Plt_new, 'w')
            f.write(Text)
            f.close()
        else:
            Plt_new = None
            d_Plt_new = None
            NotAll = False
    else:
        Plt_new = None    
        d_Plt_new = None
        NotAll = False

    return Plt_new, d_Plt_new, NotAll


def ReadD97(Path):
    Out = []

    #f=open(Path, 'r', encoding="utf_8")
    f = open(Path, 'rb')

    i = 2
    while True:
        line_b = f.readline()
        line = str(line_b)

        # if "[SIGNAL0]" not in line and "[SIGNAL" in line:
        if "[SIGNAL" in line:
            i = 0

        if i == 1 and "NAME=" in line:
            T = line.replace("NAME=", "")
            T = T.replace("\n", "")
            T = T.replace("b'", "")
            T = T.replace("'", "")
            T = T.replace("\\", "*")
            T = T.replace("*r*n", "")

            Out.append(T)

        if "[DATA]" in line:
            break

        i += 1

    f.close()

    return Out


# # Select_Signal
# - D97ファイルをCSV変換するためのPLT作成で使用する信号
# - PLTから計測信号を設定する。

# In[9]:


def Select_Signal(File):
    d_Signal = {}
    
    f = open(File, 'r', encoding="ascii")
    l_line_plt = f.readlines()

    for line in l_line_plt:
        line = line.replace("\n", "")
        l_line = line.split(" ")

        if l_line[0] != "" and "~" not in l_line[0] and "//" not in l_line[0] and "+" not in l_line[0] and "*" not in l_line[0]:
            d_Signal[l_line[0]] = GetKey(l_line)

    f.close()

    return d_Signal


def GetKey(l_in):
    Out = l_in[0]
    
    for Text in l_in:
        l_Text = Text.split("=")
        
        if l_Text[0] == "key":
            Out = l_Text[1]
            
    return Out


# # Read_DCM

# In[10]:


PARAMETER_TYPE = ["FESTWERT", "KENNLINIE", "KENNFELD"]


# In[11]:


def ParameterName(TEXT):
    for TYPE in PARAMETER_TYPE:
        TEXT = TEXT.replace(TYPE, "")

    TEXT = TEXT.replace("\n", "")

    P = TEXT.split(" ")

    return P[1]


def Read_DCM_w_Text(FILE):
    l_line = []

    i = 0

    try:
        f = open(FILE, 'r')

        while True:
            line = f.readline()
            l_line.append(line)

            if line == "":
                i += 1

            if i > 100:
                break

    except UnicodeDecodeError:
        try:
            f = open(FILE, 'r', encoding='shift-jis')

            while True:
                line = f.readline()
                l_line.append(line)

                if line == "":
                    i += 1

                if i > 100:
                    break

        except UnicodeEncodeError:
            f = open(FILE, 'r', encoding="utf_8")

            while True:
                line = f.readline()
                l_line.append(line)

                if line == "":
                    i += 1

                if i > 100:
                    break

    Parameter = {}
    Read = False
    P = None
    l_TEXT = []
    i = 0

    for line in l_line:
        line = str(line)
        line = line.replace("\t", "   ")

        if Read == False:
            for T in PARAMETER_TYPE:
                if T in line:
                    Read = True
                    l_TEXT.append(line)
                    P = ParameterName(line)
                    i = 0
        else:
            l_TEXT.append(line)

            A = line.replace(" ", "")
            A = A.replace("\n", "")

            if A == "END":
                if l_TEXT != []:
                    Parameter[P] = l_TEXT
                Read = False
                P = None

                l_TEXT = []
    f.close()

    return Parameter


# In[12]:


def CheckFloat(X):
    if X != None:
        try:
            Y = float(X)
            J = True
        except ValueError:
            J = False
    else:
        J = False

    return J


def ValueList(Mode, L_Data1, L_Data2):
    X1 = []
    X2 = []
    Y1 = []
    Y2 = []
    Z1 = []
    Z2 = []

    if Mode == 1:
        if L_Data1 == None:
            Z1 = None
        else:
            Z1 = L_Data1[2][0]

        if L_Data2 == None:
            Z2 = None
        else:
            Z2 = L_Data2[2][0]

    elif Mode == 2:
        if L_Data1 != None:
            X1 = L_Data1[0]

        if L_Data2 != None:
            X2 = L_Data2[0]

        if L_Data1 != None:
            Z1 = L_Data1[2]

        if L_Data2 != None:
            Z2 = L_Data2[2]

    elif Mode == 3:
        if L_Data1 != None:
            X1 = L_Data1[0]

        if L_Data2 != None:
            X2 = L_Data2[0]

        if L_Data1 != None:
            Y1 = L_Data1[1]

        if L_Data2 != None:
            Y2 = L_Data2[1]

        if L_Data1 != None:
            Z1 = L_Data1[2]

        if L_Data2 != None:
            Z2 = L_Data2[2]

    return X1, X2, Y1, Y2, Z1, Z2


def ParameterValue(Target, Text):
    OUT_temp = []

    L_Text = Text.split(" ")
    i = 0
    for T in L_Text:
        if T == Target:
            OUT_temp = L_Text[i + 1 :]
            break
        i += 1

    OUT = []
    for O in OUT_temp:
        if O != "":
            try:
                OUT.append(float(O))
            except ValueError:
                OUT.append(O)

    return OUT


def PramameterToXYZ(L_Text):
    X = []
    Y = []
    Z = []
    for T in L_Text:
        T = T.replace("\n", "")
        T = T.replace("\t", "")

        if "ST/X" in T:
            X += ParameterValue("ST/X", T)
        elif "ST/Y" in T:
            Y += ParameterValue("ST/Y", T)
        elif "WERT" in T:
            Z += ParameterValue("WERT", T)
        elif "TEXT" in T:
            Z += ParameterValue("TEXT", T)

    return [X, Y, Z]


def ParameterValueFromDCM(File):
    D_Parameter = {}
    TEXT = []
    READ = False

    TYPE = ["FESTWERT", "KENNLINIE", "KENNFELD"]

    try:
        f = open(File, "r")
        datalist = f.readlines()
    except UnicodeDecodeError:
        try:
            f = open(File, "r", encoding="shift-jis")
            datalist = f.readlines()
        except UnicodeEncodeError:
            f = open(File, "r", encoding="utf_8")
            datalist = f.readlines()

    for data in datalist:
        for T in TYPE:
            if T in data:
                READ = True

                X = data.split(" ")
                Parameter = X[1].replace("\n", "")

        if READ == True:
            TEXT.append(data)

            X = data.replace(" ", "")
            X = X.replace("\n", "")
            if X == "END":
                READ = False
                D_Parameter[Parameter] = TEXT
                TEXT = []

    f.close()

    return D_Parameter


def Read_DCM_wo_Text(File):
    d_Parameter = {}

    d_Parameter_1 = ParameterValueFromDCM(File)

    for Target in d_Parameter_1:
        d_Parameter[Target] = PramameterToXYZ(d_Parameter_1[Target])

    return d_Parameter


# In[13]:


def Read_DCM(File):
    d_Out = {}
    
    d_P = Read_DCM_w_Text(File)
    d_P_wo = Read_DCM_wo_Text(File)
    
    for P in d_P.keys():
        _ = d_P_wo[P]
        X = _[0]
        Y = _[1]
        Z = _[2]
        T = d_P[P][0]

        # if X != [] and Y != []:
        #     Type = "KENNFELD"
        # elif X != []:
        #     Type = "KENNLINIE"
        # else:
        #     Type = "FESTWERT"

        for F in ["FESTWERT TEXT", "FESTWERT", "KENNLINIE", "KENNFELD"]:
            if F in T:
                Type = F
            
        d_Out[P] = (Type, X, Y, Z, d_P[P])
        
    return d_Out


# # RUN

# In[14]:


def RUN():
    outputs = []
    
    save_file = savefilename()
    
    dcms = Read_List(ListIn1)
    datas = Read_List(ListIn2)
    plts = Read_List(ListIn3)
    mms = state_checkbox.get()
    
    print(f'DCM: {dcms[0]}')
    outputs.append(f'DCM: {dcms[0]}')
    print(f'Measurements: {datas}')
    outputs.append(f'Measurements: {datas}')
    print(f'MMS: {mms}')
    outputs.append(f'MMS: {mms}')
    
    cp_fa, cp_ra = Read_Parameter_Cp(dcms[0])
    print(f'Cp_FA: {cp_fa}')
    outputs.append(f'Cp_FA: {cp_fa}')
    print(f'Cp_RA: {cp_ra}')
    outputs.append(f'Cp_RA: {cp_ra}')

    sigs = Select_Signal(plts[0])
    print(f'Signals in PLT: {sigs}')
    outputs.append(f'Signals in PLT: {sigs}')
    
    csvs = Convert_ZIP_to_CSV(datas, sigs, Sampling=0.005)

    output = Robustness(csvs, save_file, cp_fa, cp_ra, mms)
    outputs += output

    for file in csvs:
        Remove_w_ExistFile(file)

    output_txt = ''
    for txt in outputs:
        output_txt += f'{txt}\n'
    
    root, ext = os.path.splitext(save_file)
    f = open(f'{root}.txt', 'w')
    f.write(output_txt)
    f.close()

    # messagebox.showinfo('message', 'done')


# In[15]:


def savefilename():
    global DIR
    
    if DIR == None:
        DIR = "c:/"
    
    filename = filedialog.asksaveasfilename(
        title = "Save as",
        filetypes = [("PNG", ".png")], # ファイルフィルタ
        # initialdir = "./", # 自分自身のディレクトリ
        initialdir = DIR, # 自分自身のディレクトリ
        defaultextension = "png")
    print(filename)

    return filename


def Read_Parameter_Cp(dcm):
    d_parameter = Read_DCM(dcm)
    Cp_FA = d_parameter['Cp_FA'][3][0]
    Cp_RA = d_parameter['Cp_RA'][3][0]

    return Cp_FA, Cp_RA


# # tkinter

# ## dialog

# In[16]:


DIR = None


def dialog_clicked_list1():
    dialog_clicked([("", "*.dcm")], ListIn1, add=False)


def dialog_clicked_list2():
    dialog_clicked([("", "*.zip")], ListIn2, add=True)


def dialog_clicked_list3():
    dialog_clicked([("", "*.plt")], ListIn3, add=False)


def dialog_clicked(fTyp, ListIn, add=False):
    global DIR
    # iDir = os.path.abspath(os.path.dirname(__file__))

    if DIR == None:
        DIR = "c:/"
        
    if add == True:
        Out = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=DIR)
    else:
        Out = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=DIR)

    if Out != "":
        if add == False:
            ListIn.delete(0, END)
            ListIn.insert(END, Out)
            DIR = os.path.split(Out)
        else:
            for add in Out:
                ListIn.insert(END, add)
            DIR = os.path.split(Out[0])


# ## listbox

# In[17]:


def listbox_selected_File(event):
    for i in ListIn1.curselection():
        # s=ListIn1.get(i)
        ListIn1.delete(0, END)
        # ListIn2.delete(0, END)

    for i in ListIn2.curselection():
        # select = ListIn2.get(i)
        # print(select)
        Update_List(i, ListIn2)
        # ListIn1.delete(i, END)
        # ListIn2.delete(i, END)

    for i in ListIn3.curselection():
        # select = ListIn2.get(i)
        # print(select)
        ListIn3.delete(0, END)
        # ListIn1.delete(i, END)
        # ListIn2.delete(i, END)


def Update_List(i, ListIn):
    files = Read_List(ListIn)
    remove_file = ListIn.get(i)
    files.remove(remove_file)
    ListIn.delete(0, END)

    for file in files:
        ListIn.insert(END, file)


def Read_List(ListIn):
    List = []
    n = ListIn.size()
    for i in range(0, n):
        List.append(ListIn.get(i))

    return List


# ## main window

# In[19]:


# =============================================================================
#
# =============================================================================
# In[ ]:
if __name__ == "__main__":
    # ルートウィンドウ
    root = Tk()

    TITLE1 = "Robutsness Tool"
    root.title(TITLE1)

    root.geometry('1000x300')

    root_frm = tk.Frame(root, bg="mint cream")

    root_frm.pack(expand=YES, fill=BOTH)

    Frame1 = tk.LabelFrame(root_frm, text='DCM', relief='groove', borderwidth=4, bg="gold", font=("Meiryo", 10))
    Frame3 = tk.LabelFrame(root_frm, text='PLT', relief='groove', borderwidth=4, bg="gold", font=("Meiryo", 10))
    Frame2 = tk.LabelFrame(root_frm, text='Measurements', relief='groove', borderwidth=4, bg="gold", font=("Meiryo", 10))

    # currententry1 = ['c:\\Users\\ktt2yk\\Desktop\\Work\\VDC_for_Robust\\10_Takasu_Robust\\SharCC_PMSe.dcm']
    currententry1 = []
    entry1 = StringVar(value=currententry1)
    Frame_ListIn1 = tk.Frame(Frame1, bg="gold")
    scroll_ListIn1 = tk.Scrollbar(Frame_ListIn1, orient=HORIZONTAL)
    scroll_ListIn1.pack(side="bottom", fill="x")
    ListIn1 = Listbox(Frame_ListIn1, listvariable=entry1, width=30, height=1, xscrollcommand=scroll_ListIn1.set, font=("Meiryo", 10))
    scroll_ListIn1.config(command=ListIn1.xview)
    ListIn1.bind('<<ListboxSelect>>', listbox_selected_File)
    ListIn1["yscrollcommand"] = scroll_ListIn1
    Button_ListIn1 = tk.Button(Frame1, text="add", command=dialog_clicked_list1, bg="gray78", font=("Meiryo", 10))

    # currententry3 = ['c:\\Users\\ktt2yk\\Desktop\\Work\\VDC_for_Robust\\Robust.PLT']
    currententry3 = []
    entry3 = StringVar(value=currententry3)
    Frame_ListIn3 = tk.Frame(Frame3, bg="gold")
    scroll_ListIn3 = tk.Scrollbar(Frame_ListIn3, orient=HORIZONTAL)
    scroll_ListIn3.pack(side="bottom", fill="x")
    ListIn3 = Listbox(Frame_ListIn3, listvariable=entry3, width=30, height=1, xscrollcommand=scroll_ListIn3.set, font=("Meiryo", 10))
    scroll_ListIn3.config(command=ListIn1.xview)
    ListIn3.bind('<<ListboxSelect>>', listbox_selected_File)
    ListIn3["yscrollcommand"] = scroll_ListIn3
    Button_ListIn3 = tk.Button(Frame3, text="add", command=dialog_clicked_list3, bg="gray78", font=("Meiryo", 10))

    # currententry2 = ['c:\\Users\\ktt2yk\\Desktop\\Work\\VDC_for_Robust\\10_Takasu_Robust\\00_EU1_2\\20221018_0004.ZIP', 
    #                  'c:\\Users\\ktt2yk\\Desktop\\Work\\VDC_for_Robust\\10_Takasu_Robust\\00_EU1_2\\20221018_0005.ZIP']
    currententry2 = []
    entry2 = StringVar(value=currententry2)
    Frame_ListIn2 = tk.Frame(Frame2, bg="gold")
    scroll_ListIn2_Y = tk.Scrollbar(Frame_ListIn2)
    scroll_ListIn2_Y.pack(side="right", fill="y")
    ListIn2 = Listbox(Frame_ListIn2, listvariable=entry2, width=30, height=5, yscrollcommand=scroll_ListIn2_Y.set, font=("Meiryo", 10))
    ListIn2.bind('<<ListboxSelect>>', listbox_selected_File)
    ListIn2["yscrollcommand"] = scroll_ListIn2_Y
    Button_ListIn2 = tk.Button( Frame2, text="add", command=dialog_clicked_list2, bg="gray78", font=("Meiryo", 10))

    state_checkbox = tk.BooleanVar()
    state_checkbox.set(True)
    checkbox = tk.Checkbutton(root_frm, text="w/ MMS Vehicle", variable=state_checkbox)
    
    Button_Export = tk.Button(root_frm, text="Run", command=RUN, bg="gray78", font=("Meiryo", 10))

    Frame1.pack(expand=NO, fill=BOTH, padx=2, pady=2)
    Frame_ListIn1.pack(side=LEFT, expand=YES, fill=BOTH)
    ListIn1.pack(side=LEFT, expand=YES, fill=BOTH)
    scroll_ListIn1.config(command=ListIn1.xview)
    Button_ListIn1.pack(side=LEFT, expand=NO, padx=2)

    Frame3.pack(expand=NO, fill=BOTH, padx=2, pady=2)
    Frame_ListIn3.pack(side=LEFT, expand=YES, fill=BOTH)
    ListIn3.pack(side=LEFT, expand=YES, fill=BOTH)
    scroll_ListIn3.config(command=ListIn3.xview)
    Button_ListIn3.pack(side=LEFT, expand=NO, padx=2)
    
    Frame2.pack(expand=YES, fill=BOTH, padx=2, pady=2)
    Frame_ListIn2.pack(side=LEFT, expand=YES, fill=BOTH)
    ListIn2.pack(side=LEFT, expand=YES, fill=BOTH)
    scroll_ListIn2_Y.config(command=ListIn2.yview)
    Button_ListIn2.pack(side=LEFT, expand=NO, padx=2)

    checkbox.pack()

    Button_Export.pack(side=LEFT, expand=YES, fill=X, padx=2, pady=2)

    root.mainloop()


# In[ ]:




