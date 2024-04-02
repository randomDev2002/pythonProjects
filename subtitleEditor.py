import customtkinter
from tkinter import filedialog
from tkinter import messagebox
import os
import datetime as dt

defaultPath = "C:\\Users\\lovro\\Downloads"


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("300x300")
app.title("Subtitle Editor")

filePath = ""
def browseFiles():
    global filePath

    filename=filedialog.askopenfilename(initialdir=defaultPath, title="Izberi datoteko", filetypes=(("SRT files", "*.srt*"), ("All files", "*.*")))
    
    label_1 = customtkinter.CTkLabel(app, text="Datoteka izbrana \u2713")
    label_1.place(x=100, y= 70)

    entry.place(x=80, y= 130)
    potrdiButton.place(x=90,y=170)

    filePath = filename
    return filename

def extractTime(time_str):
    startTime = dt.datetime(100,1,1, int(time_str[:2]), int(time_str[3:5]), int(time_str[6:8]), int(time_str[9:12])*1000)
    endTime = dt.datetime(100, 1, 1, int(time_str[17:19]), int(time_str[20:22]), int(time_str[23:25]), int(time_str[26:29])*1000)

    return [startTime, endTime]

def addTime(time_list,add):
    newTimeList = []
    for i in time_list:
        newTime = i + dt.timedelta(seconds=add)
        if newTime.hour == 23:
            newTime = i + dt.timedelta(seconds=(i.second*(-1)))
        newTimeList.append(newTime)
    return newTimeList

def extractFolderName(file_path):
    i = len(file_path)-1
    while i > 0:
        if file_path[i] == "/":
            folderName = file_path[:i]
            break
        i-=1
    
    return folderName


def potrdiFunct(file_path):
    alreadyClicked = False
    try:
        add_secs = float(entry.get())
        originalSubFile = open(file_path, 'r')
        newSubFile = open("{}\\corrected_subs.srt".format(extractFolderName(file_path)), 'w')
        for line in originalSubFile.readlines():
            if '-->' in line:
                timeObj = addTime(extractTime(line),add_secs)
                startT = timeObj[0]
                endT = timeObj[1]
                newSubFile.writelines([startT.strftime('%H:%M:%S,%f')[:-3], ' --> ', endT.strftime('%H:%M:%S,%f')[:-3], '\n'])
            else:
                newSubFile.writelines(line)
            
        originalSubFile.close()
        newSubFile.close()
                    
        koncanoLabel = customtkinter.CTkLabel(app, text="KONČANO \u2713")
        koncanoLabel.place(x=120,y=220)
        alreadyClicked=True


    except:
        if alreadyClicked == False:
            messagebox.showwarning(title="ERR", message="VNESI ŽELJEN ZAMIK !")
  
    return 0

fileDial_button = customtkinter.CTkButton(app, text="Prebrskaj", command=browseFiles)

fileDial_button.place(x=85,y=40)

entry = customtkinter.CTkEntry(app, placeholder_text = "Vnesi željen zamik v sek.", width=160)

potrdiButton = customtkinter.CTkButton(app, text="Potrdi", command=lambda:potrdiFunct(filePath))

app.mainloop()
