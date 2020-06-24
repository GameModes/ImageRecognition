from tkinter import *
from tkinter.ttk import Combobox
from webcolors import *
import json

import QrRecognizingCombi as fl

root = Tk()
###########################################
#https://datatofish.com/entry-box-tkinter/
#https://stackoverflow.com/questions/28905984/tkinter-how-to-create-choice-box
#https://pypi.org/project/webcolors/1.3/
#https://www.delftstack.com/nl/howto/python-tkinter/how-to-set-window-icon-in-tkinter/
#https://www.youtube.com/watch?v=lt78_05hHSk
#https://stackoverflow.com/questions/2395431/using-tkinter-in-python-to-edit-the-title-bar
#https://thispointer.com/python-how-to-check-if-an-item-exists-in-list-search-by-value-or-condition/
#
#
######################################
root.title('Barcode Scanner')
root.iconbitmap('TkinterIcon.ico')
FirstSection = Label(root, text="Camera Options", fg="blue")
FirstSection.grid(row=0)
SecondSection = Label(root, text="Recognize Square Options", fg="blue")
SecondSection.grid(row=4)
ThirdSection = Label(root, text="ErrorBox", fg="blue")
ThirdSection.grid(row=4, column=3)
FourthSection = Label(root, text="DataBase Printing (optional)", fg="blue")
FourthSection.grid(row=8)
#####################################
def get_ips():
    IPs = []
    IPfile_Opener = open('UsedIPs.json')
    IPData = json.load(IPfile_Opener)
    for IP in IPData:
        IPs.append(IP)
    return IPs

def get_databases():
    Databases = []
    Databasefile_Opener = open('UsedDatabases.json')
    DataBaseData = json.load(Databasefile_Opener)
    for Database in DataBaseData:
        Databases.append(Database)
    return Databases

######################################
Colors = ['RED', "BLUE", "GREEN", "BLACK", "YELLOW"]
live_camera_label = Label(root, text="Camera Nummer/IP")
live_usedIps_label = Label(root, text="Early Used Ips")
live_framewidth_label= Label(root, text="Frame Width")
live_frameheight_label= Label(root, text="Frame Height")
IPs = get_ips()
live_camera_entry = Entry(root)
live_usedIps_entry = Combobox(root, values = IPs)
live_framewidth_entry = Entry(root)
live_frameheight_entry = Entry(root)
live_camera_label.grid(row=1)
live_usedIps_label.grid(row=1, column=3)
live_framewidth_label.grid(row=2)
live_frameheight_label.grid(row=3)
live_camera_entry.grid(row=1, column=1)
live_usedIps_entry.grid(row=1, column=4)
live_framewidth_entry.grid(row=2, column=1)
live_frameheight_entry.grid(row=3, column=1)

######################################
live_objectname_label = Label(root, text="Object Name")
live_color_label = Label(root, text="Frame Color")
live_objectname_entry = Entry(root)
live_colorMenu = Combobox(root, values = Colors)
live_objectname_label.grid(row=5)
live_color_label.grid(row=6)
live_objectname_entry.grid(row=5, column=1)
live_colorMenu.grid(row=6, column=1)
#######################################
live_DBdriver_label = Label(root, text="Driver:")
live_DBdriver_label.grid(row=9)
live_DBdriver_entry = Entry(root)
live_DBdriver_entry.grid(row=9, column=1)
live_DBserver_label = Label(root, text="Server:")
live_DBserver_label.grid(row=10)
live_DBserver_entry = Entry(root)
live_DBserver_entry.grid(row=10, column=1)
live_DBdatabase_label = Label(root, text="Database:")
live_DBdatabase_label.grid(row=11)
live_DBdatabase_entry = Entry(root)
live_DBdatabase_entry.grid(row=11, column=1)
live_DBuid_label = Label(root, text="UID:")
live_DBuid_label.grid(row=12)
live_DBuid_entry = Entry(root)
live_DBuid_entry.grid(row=12, column=1)
live_DBpwd_label = Label(root, text="PWD:")
live_DBpwd_label.grid(row=13)
live_DBpwd_entry = Entry(root)
live_DBpwd_entry.grid(row=13, column=1)
live_DBselect_label = Label(root, text="SELECT:")
live_DBselect_label.grid(row=14)
live_DBselect_entry = Entry(root)
live_DBselect_entry.grid(row=14, column=1)
live_DBfrom_label = Label(root, text="FROM:")
live_DBfrom_label.grid(row=15)
live_DBfrom_entry = Entry(root)
live_DBfrom_entry.grid(row=15, column=1)
live_DBsection_label = Label(root, text="SECTION:")
live_DBsection_label.grid(row=16)
live_DBsection_entry = Entry(root)
live_DBsection_entry.grid(row=16, column=1)

#~
# live_usedDatabases_label = Label(root, text="Early Used Databases")
# Databases = get_databases()
# live_usedDatabases_entry = Combobox(root, values = Databases)
# live_usedDatabases_label.grid(row=9, column=3)
# live_usedDatabases_entry.grid(row=9, column=4)
#~
######################################


def RecognizingStartFile():
    connectie = ''
    execute = ''
    insert = ''
    databaseUse = False
    frameWidth, frameHeight, path, camnum, objectName, color = fl.defaultSettings()
    try:
        if live_objectname_entry.get() != '':
            objectName = live_objectname_entry.get()
        if live_framewidth_entry.get() != '':
            frameWidth = int(live_framewidth_entry.get())
        if live_frameheight_entry.get()!= '':
            frameHeight = int(live_frameheight_entry.get())
        if live_colorMenu.get() != '':
            color = name_to_rgb(live_colorMenu.get())
        if live_usedIps_entry.get() != '':
            if len(live_usedIps_entry.get()) > 4:
                camnum = 'rtsp://root:TO-41212@' + live_usedIps_entry.get() + '/live.sdp'
            else:
                camnum = int(live_usedIps_entry.get())
        elif live_camera_entry.get() != '':
            if len(live_camera_entry.get()) > 4:
                camnum = 'rtsp://root:TO-41212@' + live_camera_entry.get() + '/live.sdp'
                if live_camera_entry.get() not in IPs:
                    IPs.append(live_camera_entry.get())
                with open('UsedIPs.json', 'w') as IP_file:
                    json.dump(IPs, IP_file, indent=4)
            else:
                camnum = int(live_camera_entry.get())
        if live_DBdriver_entry.get() != '' and live_DBserver_entry.get() != '' and live_DBuid_entry.get() != '' and live_DBpwd_entry.get() != '' and live_DBselect_entry.get() != '' and live_DBfrom_entry.get() != '' and live_DBsection_entry.get() != '' and live_DBdatabase_entry.get() != '' :
            databaseUse = True
            connectie = 'Driver=' + live_DBdriver_entry.get() + ';'+'Server=' + live_DBserver_entry.get() + ';'+'Database=' + live_DBdatabase_entry.get() +';' +'UID=' + live_DBuid_entry.get() + ';' + 'PWD=' + live_DBpwd_entry.get() + ';'
            execute = 'SELECT' + live_DBselect_entry.get() + 'FROM' + live_DBfrom_entry.get()
            insert = '''INSERT INTO ''' + live_DBfrom_entry.get() + ''' (''' + live_DBsection_entry.get() + ''')'''
            connectielist = [connectie, execute, insert]
            with open('UsedDatabases.json', 'w') as IP_file:
                json.dump(IPs, IP_file, indent=4)
    except ValueError:
        CameraError = False
        ErrorEntrys(CameraError)

    fl.cascadeRunning(frameWidth, frameHeight, path, camnum, objectName, color, databaseUse, connectie, execute, insert)

def ErrorEntrys(CameraError):
    if CameraError:
        live_answerbox_label = Label(root, text="Camera is not Connectable")
        live_answerbox_label.grid(row=5, column=3)
    else:
        live_answerbox_label = Label(root, text="Value must be Number")
        live_answerbox_label.grid(row=5, column=3)

start_button = Button(root, text="Start Scanning", command=RecognizingStartFile)
start_button.grid(row=6, column=5)





##########################################
root.mainloop()