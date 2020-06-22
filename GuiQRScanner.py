from tkinter import *
from tkinter.ttk import Combobox
from webcolors import *

import QrRecognizingCombi as fl

root = Tk()

######################################
Title = Label(root, text="Barcode Scanner", fg="blue")
Title.grid(row=0)

######################################
Colors = ['RED', "BLUE", "GREEN", "BLACK", "YELLOW"]
live_camera_label = Label(root, text="Camera Nummer/IP")
live_objectname_label = Label(root, text="Object Naam")
live_framewidth_label= Label(root, text="Frame Width")
live_frameheight_label= Label(root, text="Frame Height")
live_color_label = Label(root, text="Frame Color")

live_camera_entry = Entry(root)
live_objectname_entry = Entry(root)
live_framewidth_entry = Entry(root)
live_frameheight_entry = Entry(root)
live_colorMenu = Combobox(root, values = Colors)

live_camera_label.grid(row=1)
live_objectname_label.grid(row=2)
live_framewidth_label.grid(row=3)
live_frameheight_label.grid(row=4)
live_color_label.grid(row=5)

live_camera_entry.grid(row=1, column=1)
live_objectname_entry.grid(row=2, column=1)
live_framewidth_entry.grid(row=3, column=1)
live_frameheight_entry.grid(row=4, column=1)
live_colorMenu.grid(row=5, column=1)
######################################

######################################

def RecognizingStartFile():
    frameWidth, frameHeight, path, cap, objectName, color = fl.defaultSettings()
    if live_objectname_entry.get() != '':
        objectName = live_objectname_entry.get()
    if live_framewidth_entry.get() != '':
        frameWidth = int(live_framewidth_entry.get())
    if live_frameheight_entry.get()!= '':
        frameHeight = int(live_frameheight_entry.get())
    if live_colorMenu.get() != '':
        color = name_to_rgb(live_colorMenu.get())


    fl.cascadeRunning(frameWidth, frameHeight, path, cap, objectName, color)
    # exec(open('QrRecognizingCombi.py').read())


start_button = Button(root, text="Start Scanning", command=RecognizingStartFile)
start_button.grid(row=5, column=5)
start_command_button = Button(root, text="Start Command Scanning", command=RecognizingStartFile)
start_command_button.grid(row=6, column=5)





##########################################
root.mainloop()