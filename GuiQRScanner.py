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
Title = Label(root, text="Barcode Scanner", fg="blue")
Title.grid(row=0)
#####################################
def get_ips():
    IPs = []
    IPfile_Opener = open('UsedIPs.json')
    IPData = json.load(IPfile_Opener)
    for IP in IPData:
        IPs.append(IP)
    return IPs

######################################
Colors = ['RED', "BLUE", "GREEN", "BLACK", "YELLOW"]
live_camera_label = Label(root, text="Camera Nummer/IP")
live_usedIps_label = Label(root, text="Early Used Ips")
live_objectname_label = Label(root, text="Object Naam")
live_framewidth_label= Label(root, text="Frame Width")
live_frameheight_label= Label(root, text="Frame Height")
live_color_label = Label(root, text="Frame Color")

IPs = get_ips()
live_camera_entry = Entry(root)
live_usedIps_entry = Combobox(root, values = IPs)
live_objectname_entry = Entry(root)
live_framewidth_entry = Entry(root)
live_frameheight_entry = Entry(root)
live_colorMenu = Combobox(root, values = Colors)


live_camera_label.grid(row=1)
live_usedIps_label.grid(row=1, column=3)
live_objectname_label.grid(row=2)
live_framewidth_label.grid(row=3)
live_frameheight_label.grid(row=4)
live_color_label.grid(row=5)

live_camera_entry.grid(row=1, column=1)
live_usedIps_entry.grid(row=1, column=4)
live_objectname_entry.grid(row=2, column=1)
live_framewidth_entry.grid(row=3, column=1)
live_frameheight_entry.grid(row=4, column=1)
live_colorMenu.grid(row=5, column=1)
######################################

######################################


def RecognizingStartFile():
    frameWidth, frameHeight, path, camnum, objectName, color = fl.defaultSettings()
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

    fl.cascadeRunning(frameWidth, frameHeight, path, camnum, objectName, color)
    # exec(open('QrRecognizingCombi.py').read())


start_button = Button(root, text="Start Scanning", command=RecognizingStartFile)
start_button.grid(row=5, column=5)
start_command_button = Button(root, text="Start Command Scanning", command=RecognizingStartFile)
start_command_button.grid(row=6, column=5)





##########################################
root.mainloop()