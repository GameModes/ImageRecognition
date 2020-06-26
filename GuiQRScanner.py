from tkinter import * #tkinter Library
from tkinter.ttk import Combobox #combobox from tkinter Library
from webcolors import * #Html colors to decimal colors Library
import json #use of json files Library
import QrRecognizingCombi as fl #Able to make use of other file

root = Tk() #start of tkinter
###########################################

######################################
root.title('Barcode Scanner') #title
root.iconbitmap('TkinterIcon.ico') #title Picture
FirstSection = Label(root, text="Camera Options", fg="blue") #first title
FirstSection.grid(row=0)
SecondSection = Label(root, text="Recognize Square Options", fg="blue") #second title
SecondSection.grid(row=4)
ThirdSection = Label(root, text="ErrorBox", fg="blue") #third title
ThirdSection.grid(row=4, column=3)
FourthSection = Label(root, text="DataBase Printing (optional)", fg="blue")#fourth title
FourthSection.grid(row=8)
#####################################
def get_ips():
    IPs = [] #create empty list
    IPfile_Opener = open('UsedIPs.json') #opens json file
    IPData = json.load(IPfile_Opener) #loads all data
    for IP in IPData: #seperate data with for loop
        IPs.append(IP) #adds it to empty list
    return IPs

def get_databases():
    Databases = []
    Databasefile_Opener = open('UsedDatabases.json')
    DataBaseData = json.load(Databasefile_Opener)
    for Database in DataBaseData:
        Databases.append(Database)
    return Databases

###################################### First Section
Colors = ['RED', "BLUE", "GREEN", "BLACK", "YELLOW"] #frame colors list
live_camera_label = Label(root, text="Camera Nummer/IP") #Makes Text Box
live_usedIps_label = Label(root, text="Early Used Ips")
live_framewidth_label= Label(root, text="Frame Width")
live_frameheight_label= Label(root, text="Frame Height")
IPs = get_ips() #get Ips from IP function

live_camera_entry = Entry(root) #makes Entry box
live_usedIps_entry = Combobox(root, values = IPs) #Makes Combo Box
live_framewidth_entry = Entry(root)
live_frameheight_entry = Entry(root)

live_camera_label.grid(row=1) #.grid == inserts to tkinter GUI and where
live_usedIps_label.grid(row=1, column=3)
live_framewidth_label.grid(row=2)
live_frameheight_label.grid(row=3)
live_camera_entry.grid(row=1, column=1)
live_usedIps_entry.grid(row=1, column=4)
live_framewidth_entry.grid(row=2, column=1)
live_frameheight_entry.grid(row=3, column=1)

###################################### Second Section
live_objectname_label = Label(root, text="Object Name")
live_color_label = Label(root, text="Frame Color")

live_objectname_entry = Entry(root)
live_colorMenu = Combobox(root, values = Colors)

live_objectname_label.grid(row=5)
live_color_label.grid(row=6)
live_objectname_entry.grid(row=5, column=1)
live_colorMenu.grid(row=6, column=1)

####################################### Third Section
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


live_usedDatabases_label = Label(root, text="Early Used Databases")
Databases = get_databases()
live_usedDatabases_entry = Combobox(root, values = Databases)
live_usedDatabases_label.grid(row=9, column=3)
live_usedDatabases_entry.grid(row=9, column=4)

######################################

def RecognizingStartFile():
    connectie = ''
    execute = ''
    insert = ''
    databaseUse = False #default is not used
    CameraError = False #default if not changed
    frameWidth, frameHeight, path, camnum, objectName, color = fl.defaultSettings() #if not inserted, this data will be used
    try:
        if live_objectname_entry.get() != '': #if entrybox is filled
            objectName = live_objectname_entry.get() #use the filled text
        if live_framewidth_entry.get() != '':
            frameWidth = int(live_framewidth_entry.get())
        if live_frameheight_entry.get()!= '':
            frameHeight = int(live_frameheight_entry.get())
        if live_colorMenu.get() != '':
            color = name_to_rgb(live_colorMenu.get())
        if live_usedIps_entry.get() != '':  #if using formerly used IPS
            if len(live_usedIps_entry.get()) > 4: #if long enough to be IP
                camnum = 'rtsp://root:TO-41212@' + live_usedIps_entry.get() + '/live.sdp' #make useable IP command
            else: #if Camera Number
                camnum = int(live_usedIps_entry.get()) #use only the number
        elif live_camera_entry.get() != '': #else use Manual IP filled text
            if len(live_camera_entry.get()) > 4:
                camnum = 'rtsp://root:TO-41212@' + live_camera_entry.get() + '/live.sdp'
                if live_camera_entry.get() not in IPs: #check if IP already in history
                    IPs.append(live_camera_entry.get()) #append it to list
                with open('UsedIPs.json', 'w') as IP_file: #open the json file
                    json.dump(IPs, IP_file, indent=4) #dump the IP list in Json file
            else:
                camnum = int(live_camera_entry.get())
        if live_usedDatabases_entry.get() != '':
            databaseUse = True
            connectie = live_usedDatabases_entry.get()[0]
            execute = live_usedDatabases_entry.get()[1]
            insert = live_usedDatabases_entry.get()[2]
            database_name = live_usedDatabases_entry.get()[3]
            section_name = live_usedDatabases_entry.get()[4]
        elif live_DBdriver_entry.get() != '' and live_DBserver_entry.get() != '' and live_DBuid_entry.get() != '' and live_DBpwd_entry.get() != '' and live_DBselect_entry.get() != '' and live_DBfrom_entry.get() != '' and live_DBsection_entry.get() != '' and live_DBdatabase_entry.get() != '' :
            #check if all the database insert slots are filled
            databaseUse = True
            connectie = 'Driver=' + live_DBdriver_entry.get() + ';'+'Server=' + live_DBserver_entry.get() + ';'+'Database=' + live_DBdatabase_entry.get() +';' +'UID=' + live_DBuid_entry.get() + ';' + 'PWD=' + live_DBpwd_entry.get() + ';'
            execute = 'SELECT' + live_DBselect_entry.get() + 'FROM' + live_DBfrom_entry.get()
            insert = '''INSERT INTO ''' + live_DBfrom_entry.get() + ''' (''' + live_DBsection_entry.get() + ''')'''
            database_name = live_DBfrom_entry.get()
            section_name = live_DBsection_entry.get()
            connectielist = (connectie, execute, insert, database_name, section_name)
            with open('UsedDatabases.json', 'a+') as IP_file:
                json.dump(connectielist, IP_file, indent=4)
        else:
            print("database not used or filled entirely")
    except ValueError: #if not filled in correctly
        ErrorEntrys(CameraError)

    fl.cascadeRunning(frameWidth, frameHeight, path, camnum, objectName, color, databaseUse, connectie, execute, insert, database_name, section_name)
    #run with the current made settings

def ErrorEntrys(CameraError): #ErrorBox gives correct errorcode
    if CameraError:
        live_answerbox_label = Label(root, text="Camera is not Connectable")
        live_answerbox_label.grid(row=5, column=3)
    else:
        live_answerbox_label = Label(root, text="Value must be Number")
        live_answerbox_label.grid(row=5, column=3)

ShortInstructions = Label(root, text="ESC to close Camera window", fg="green")#fourth title
ShortInstructions.grid(row=5, column=5)
start_button = Button(root, text="Start Scanning", command=RecognizingStartFile)
start_button.grid(row=6, column=5) #at last the Start button when pressed

root.mainloop()