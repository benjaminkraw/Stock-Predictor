#------------------------------------------------------------------------------
# Import Library
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from tkcalendar import Calendar
from tkinter.messagebox import showinfo

import datetime
import time

import numpy as np

import subprocess

from screeninfo import get_monitors

from os import listdir
from os.path import isfile, join

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


#------------------------------------------------------------------------------
# Define Functions
# Given Mouse Wheel event, Scroll Y on canvas
def on_mouse_wheel(event):
    # canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    return


#------------------------------------------------------------------------------
# Create Window
root = ctk.CTk()

# Set Custom TKinter Appearance
root._set_appearance_mode("dark")
# root.set_default_color_theme("dark-blue")

# Window Title
root.title("Stock Predictor 1000")                    

# Window Dimensions
WindowWidth = 1920
WindowHeight = 1080

# Get connected monitors information
num_monitors = 0
m = ""
monitors =  np.empty(shape=(0, 8), dtype='object')
for m in get_monitors():
    # Collect current monitor's data
    monitor_data = str(m)

    # Parse text between ", "
    x, y, width, height, width_mm, height_mm, name, is_primary = monitor_data.split(", ")
    
    # Parse out data after each "=" and replace itself
    x = x.split("=", 1)[1]
    y = y.split("=", 1)[1]
    width = width.split("=", 1)[1]
    height = height.split("=", 1)[1]
    width_mm = width_mm.split("=", 1)[1]
    height_mm = height_mm.split("=", 1)[1]
    name = name.split("=", 1)[1]
    is_primary = is_primary.split("=", 1)[1]
  
    # Append current loops monitor data
    monitors = np.append(monitors, [[x, y, width, height, width_mm, height_mm, name, is_primary]], axis = 0)

    num_monitors += 1


# Monitor Dimensions
Monitor1Width = int(monitors[0,2])
Monitor1Height = int(monitors[0,3])

Monitor2Width = int(monitors[1,2])
Monitor2Height = int(monitors[0,3])

# Screen Dimensions (Determines Microsoft Windows Scaling)
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()

Monitor1_to_screen_scaling = Monitor1Width / ScreenWidth
Monitor2_to_screen_scaling = Monitor2Width / ScreenWidth

WindowsTaskbarHeight = 48

# Calculate x and y coordinates for Window
MainWindow_x = (Monitor2Width/2) - ((WindowWidth * Monitor2_to_screen_scaling) / 2) + Monitor1Width
MainWindow_y = (Monitor2Height/2) - ((WindowHeight * Monitor2_to_screen_scaling) / 2) - WindowsTaskbarHeight

# Set Window Dimensions and location
root.geometry('%dx%d+%d+%d' % (WindowWidth, WindowHeight, MainWindow_x, MainWindow_y))
root.minsize(600,600)

#------------------------------------------------------------------------------
# Create Window Menu
menu = tk.Menu(root)
root.config(menu=menu)

# Create File in Menu
filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Exit", command=root.quit)

#------------------------------------------------------------------------------
# Generate Title Block Frame
Title_frame = ctk.CTkFrame(root)
Title_frame.place(x=0, y=0)
Title_frame.configure(width = 380, height = 70)

# Title
Title_label = ctk.CTkLabel(master=Title_frame, text="Stock Predictor 1000", font=("Calibri", 34))
Title_label.place(x=20, y=5)

# Credits
Credits_label = ctk.CTkLabel(master=Title_frame, text="Created by: Kiel Penrod & Benjamin Kraw", font=("Calibri", 14))
Credits_label.place(x=45, y=40)



#------------------------------------------------------------------------------
# Generate Time Frame
Time_frame = ctk.CTkFrame(root)
Time_frame.place(x=600, y=0)
Time_frame.configure(width = 380, height = 70)

# Current Date
Date_label = ctk.CTkLabel(master=Time_frame, text="Date", font=("Calibri", 20))
Date_label.place(x=15, y=10)

# Current Time
Clock_label = ctk.CTkLabel(master=Time_frame, text="Time", font=("Calibri", 20))
Clock_label.place(x=15, y=35)
# Time_frame.Clock()
# Clock_label.after(1000, Clock)
   


#------------------------------------------------------------------------------
# Current Time
# https://www.geeksforgeeks.org/python/time-strftime-function-in-python/
def Clock():
    DayOfWeek = time.strftime("%A")

    Year = time.strftime("%Y")
    Month = time.strftime("%B")
    Day = time.strftime("%d")

    Hour = time.strftime("%H")
    Minute = time.strftime("%M")
    Second = time.strftime("%S")
    TimeZone = time.strftime("%Z")
    TimeZoneOffset = time.strftime("%z")

    CurrentTime_text = Hour + ":" + Minute + ":" + Second + " " + TimeZone + " " + TimeZoneOffset

    Clock_label.configure(text=CurrentTime_text)
    Clock_label.after(1000, Clock)
    
    Date_label.configure(text=DayOfWeek + " " + Month + " " + Day + ", " + Year)

#------------------------------------------------------------------------------
# Generate Project Setup Frame
Project_frame = ctk.CTkFrame(root)
Project_frame.place(x=0, y=100)
Project_frame.configure(width = 1000, height = 200)

ProjectDirectory = "C:/Users/Benjamin/Documents/DarwinAI/v3.2"
TrainingDirectory = ProjectDirectory + str("/20-data/100-ingest/40-training/ibkr/MES/1m")
BacktestDirectory = ProjectDirectory + str("/20-data/100-ingest/50-backtest/ibkr/MES/1m")


def SetProjectDirectory():
    # File Directory for Project
    global ProjectDirectory
    global ProjectDirectory_label

    # Request from user Project Directory
    ProjectDirectory = ctk.filedialog.askdirectory(initialdir=ProjectDirectory)

    # Update label
    ProjectDirectory_label.configure(text=ProjectDirectory)

def SetTrainingDirectory():
    # File Directory for Training
    global TrainingDirectory
    global TrainingDirectory_label

    # Request from user Training Directory
    TrainingDirectory = ctk.filedialog.askdirectory(initialdir=TrainingDirectory)

    # Update label
    TrainingDirectory_label.configure(text=TrainingDirectory)

    UpdateFileListbox(Training_listbox, TrainingDirectory)

def SetBacktestDirectory():
    # File Directory for Backtest
    global BacktestDirectory
    global BacktestDirectory_label

    # Request from user Backtest Directory
    BacktestDirectory = ctk.filedialog.askdirectory(initialdir=BacktestDirectory)

    # Update label
    BacktestDirectory_label.configure(text=BacktestDirectory)

    UpdateFileListbox(Backtest_listbox, BacktestDirectory)

# Project Title
ProjectTitle_label = ctk.CTkLabel(master=Project_frame, text="Project", font=("Calibri", 35))
ProjectTitle_label.place(x=10, y=5)

# Project Directory Button
ProjectDirectory_button = ctk.CTkButton(master=Project_frame, text="Set Project Directory", command=SetProjectDirectory)
ProjectDirectory_button.place(x=10, y=75)
ProjectDirectory_button.configure(width=150, height=25)

# Project Directory Text
ProjectDirectoryText_label = ctk.CTkLabel(master=Project_frame, text="Project Directory:")
ProjectDirectoryText_label.place(x=180, y=75)

# Project Directory
ProjectDirectory_label = ctk.CTkLabel(master=Project_frame, text=ProjectDirectory)
ProjectDirectory_label.place(x=300, y=75)


# Training Directory Button
TrainingDirectory_button = ctk.CTkButton(master=Project_frame, text="Set Training Directory", command=SetTrainingDirectory)
TrainingDirectory_button.place(x=10, y=105)
TrainingDirectory_button.configure(width=150, height=25)

# Training Directory Text
TrainingDirectoryText_label = ctk.CTkLabel(master=Project_frame, text="Training Directory:")
TrainingDirectoryText_label.place(x=180, y=105)

# Training Directory
TrainingDirectory_label = ctk.CTkLabel(master=Project_frame, text=TrainingDirectory)
TrainingDirectory_label.place(x=300, y=105)


# Backtest Directory Button
BacktestDirectory_button = ctk.CTkButton(master=Project_frame, text="Set Backtest Directory", command=SetBacktestDirectory)
BacktestDirectory_button.place(x=10, y=135)
BacktestDirectory_button.configure(width=150, height=25)

# Backtest Directory Text
BacktestDirectoryText_label = ctk.CTkLabel(master=Project_frame, text="Backtest Directory:")
BacktestDirectoryText_label.place(x=180, y=135)

# Backtest Directory
BacktestDirectory_label = ctk.CTkLabel(master=Project_frame, text=BacktestDirectory)
BacktestDirectory_label.place(x=300, y=135)


#------------------------------------------------------------------------------
# Generate Ingest Data Frame
Ingest_frame = ctk.CTkFrame(root)
Ingest_frame.place(x=0, y=310)
Ingest_frame.configure(width = 1000, height = 300)

# Ingest Title
IngestTitle_label = ctk.CTkLabel(master=Ingest_frame, text="Ingest", font=("Calibri", 35))
IngestTitle_label.place(x=10, y=5)

# https://www.geeksforgeeks.org/python/create-a-date-picker-calendar-tkinter/
# Add Calendar
YearNow = int(time.strftime("%Y"))
MonthNow = int(time.strftime("%m"))
DayNow = int(time.strftime("%d"))

calendar = Calendar(master=Ingest_frame, selectmode = 'day', year = YearNow, month = MonthNow, day = DayNow)
calendar.configure(font=("Calibri", 20))
calendar.place(x=25, y=95)

# Given a Number return Month String
def ConvertNumtoMonth(MonthNumber):
    if MonthNumber == 1:
        return "January"
    elif MonthNumber == 2:
        return "February"
    elif MonthNumber == 3:
        return "March"
    elif MonthNumber == 4:
        return "April"
    elif MonthNumber == 5:
        return "May"
    elif MonthNumber == 6:
        return "June"
    elif MonthNumber == 7:
        return "July"
    elif MonthNumber == 8:
        return "August"
    elif MonthNumber == 9:
        return "September"
    elif MonthNumber == 10:
        return "October"
    elif MonthNumber == 11:
        return "November"
    elif MonthNumber == 12:
        return "December"
      





def ParseCalendarDate(CalendarDate):
    ParsedCalendarDate = CalendarDate.split("/")
    return ParsedCalendarDate

#-------------------
# Training Ingest
def TrainingBegin():
    global TrainingBeginDate
    TrainingBeginDate = np.empty(shape=(1, 3), dtype='object')

    TrainingBeginDate_calendar = calendar.get_date()
    TrainingBeginDate_parsed = ParseCalendarDate(TrainingBeginDate_calendar)

    TrainingBeginDate_month = TrainingBeginDate_parsed[0]
    TrainingBeginDate_day = TrainingBeginDate_parsed[1]
    TrainingBeginDate_year = "20" + TrainingBeginDate_parsed[2]

    TrainingBeginDate[0][0] = TrainingBeginDate_year
    TrainingBeginDate[0][1] = TrainingBeginDate_month
    TrainingBeginDate[0][2] = TrainingBeginDate_day

    TrainingBeginDate_text = "Training Begin Date: " + ConvertNumtoMonth(int(TrainingBeginDate[0][1])) + " " + TrainingBeginDate[0][2] + ", " + TrainingBeginDate[0][0]
    TrainingBeginDate_label.configure(text = str(TrainingBeginDate_text))

def TrainingEnd():
    global TrainingEndDate
    TrainingEndDate = np.empty(shape=(1, 3), dtype='object')

    TrainingEndDate_calendar = calendar.get_date()
    TrainingEndDate_parsed = ParseCalendarDate(TrainingEndDate_calendar)

    TrainingEndDate_month = TrainingEndDate_parsed[0]
    TrainingEndDate_day = TrainingEndDate_parsed[1]
    TrainingEndDate_year = "20" + TrainingEndDate_parsed[2]

    TrainingEndDate[0][0] = TrainingEndDate_year
    TrainingEndDate[0][1] = TrainingEndDate_month
    TrainingEndDate[0][2] = TrainingEndDate_day
    
    TrainingEndDate_text = "Training End Date:    " + ConvertNumtoMonth(int(TrainingEndDate[0][1])) + " " + TrainingEndDate[0][2] + ", " + TrainingEndDate[0][0]
    TrainingEndDate_label.configure(text = str(TrainingEndDate_text))

def TrainingDataAck():
    root.popup = ctk.CTkToplevel()
    root.popup.wm_title("Training Data")

    # Popup Dimensions
    TrainingPopupWidth = 400
    TrainingPopupHeight = 100

    # Screen Dimensions
    ScreenWidth = root.winfo_screenwidth()
    ScreenHeight = root.winfo_screenheight()

    # Calculate x and y coordinates for Popup
    TrainingPopup_x = (ScreenWidth/2) - (TrainingPopupWidth/2) + (2 * ScreenWidth)
    TrainingPopup_y = (ScreenHeight/2) - (TrainingPopupHeight/2)

    # Set Window Dimensions and location
    root.popup.geometry('%dx%d+%d+%d' % (TrainingPopupWidth, TrainingPopupHeight, TrainingPopup_x, TrainingPopup_y))

    root.popup.grid_columnconfigure((0, 1, 2, 3), weight=1)
    root.popup.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

    Ack_label = ctk.CTkLabel(master=root.popup, text="Are you sure you want to Ingest Training Data from:")
    Ack_label.grid(row=0, column=0, columnspan=4)

    AckBegin_label = ctk.CTkLabel(master=root.popup, text="Begin: " + TrainingBeginDate[0][0] + "/" + TrainingBeginDate[0][1] + "/" + TrainingBeginDate[0][2])
    AckBegin_label.grid(row=1, column=1)

    AckEnd_label = ctk.CTkLabel(master=root.popup, text="End: " + TrainingEndDate[0][0] + "/" + TrainingEndDate[0][1] + "/" + TrainingEndDate[0][2])
    AckEnd_label.grid(row=1, column=3)

    Yes_button = ctk.CTkButton(master=root.popup, text="Yes", command=TrainingData)
    Yes_button.grid(row=4, column=1)

    No_button = ctk.CTkButton(master=root.popup, text="No", command=root.popup.destroy)
    No_button.grid(row=4, column=3)

    # Make Popup stay ontop
    root.popup.transient(root.popup.master)

    # Hijack all commands from master, clicks on main window are ignored
    root.popup.grab_set()

def TrainingData():
    # Close Popup
    root.popup.destroy()

    TrainingEndDate_year = TrainingEndDate[0][0]
    TrainingEndDate_month = TrainingEndDate[0][1]
    TrainingEndDate_day = TrainingEndDate[0][2]
    TrainingEndDate_date = TrainingEndDate_year + TrainingEndDate_month + TrainingEndDate_day

    print("Ingesting Training Data")
    subprocess.run(["powershell", "-c", "python 10-code/10-runners/100-ingest.py -m training -d" + TrainingEndDate_date])

    UpdateFileListbox(Training_listbox, TrainingDirectory)

    return

def UpdateFileListbox(Listbox, Directory):
    # Clear Listbox
    Listbox.delete(0, tk.END)

    # Query all files stored in Directory with specific file type
    Files = [f for f in listdir(Directory) if f.endswith('.parquet')]
    
    # Insert each File into Listbox
    for File in Files:
        Listbox.insert(tk.END, File)

# Training Files Listbox
Training_listbox = tk.Listbox(Ingest_frame, width = 40, height = 5)
Training_listbox.place(x=520, y=320)
Training_listbox.configure(font=("Calibri", 18))

# Update Listbox with files from Directory
UpdateFileListbox(Training_listbox, TrainingDirectory)


# Training Begin Date Button
TrainingBeginDate_button = ctk.CTkButton(master=Ingest_frame, text="Set Train Begin Date", command=TrainingBegin)
TrainingBeginDate_button.place(x=285, y=55)
TrainingBeginDate_button.configure(width=150, height=25)

# Training End Date Button
TrainingEndDate_button = ctk.CTkButton(master=Ingest_frame, text="Set Train End Date", command=TrainingEnd)
TrainingEndDate_button.place(x=445, y=55)
TrainingEndDate_button.configure(width=150, height=25)

# Training Data Button
TrainingData_button = ctk.CTkButton(master=Ingest_frame, text="Ingest Train Data", command=TrainingDataAck)
TrainingData_button.place(x=360, y=145)
TrainingData_button.configure(width=150, height=25)


# Training Begin Date Text
TrainingBeginDate_label = ctk.CTkLabel(master=Ingest_frame, text="")
TrainingBeginDate_label.place(x=350, y=90)
TrainingBeginDate_label.configure(width=150, height=25)

# Training End Date Text
TrainingEndDate_label = ctk.CTkLabel(master=Ingest_frame, text="")
TrainingEndDate_label.place(x=350, y=110)

#-------------------
# Backtest Ingest
def BacktestBegin():
    global BacktestBeginDate
    BacktestBeginDate = np.empty(shape=(1, 3), dtype='object')

    BacktestBeginDate_calendar = calendar.get_date()
    BacktestBeginDate_parsed = ParseCalendarDate(BacktestBeginDate_calendar)

    BacktestBeginDate_month = BacktestBeginDate_parsed[0]
    BacktestBeginDate_day = BacktestBeginDate_parsed[1]
    BacktestBeginDate_year = "20" + BacktestBeginDate_parsed[2]

    BacktestBeginDate[0][0] = BacktestBeginDate_year
    BacktestBeginDate[0][1] = BacktestBeginDate_month
    BacktestBeginDate[0][2] = BacktestBeginDate_day
   
    BacktestBeginDate_text = "Backtest Begin Date: " + ConvertNumtoMonth(int(BacktestBeginDate[0][1])) + " " + BacktestBeginDate[0][2] + ", " + BacktestBeginDate[0][0]
    BacktestBeginDate_label.configure(text = str(BacktestBeginDate_text))

def BacktestEnd():
    global BacktestEndDate
    BacktestEndDate = np.empty(shape=(1, 3), dtype='object')

    BacktestEndDate_calendar = calendar.get_date()
    BacktestEndDate_parsed = ParseCalendarDate(BacktestEndDate_calendar)

    BacktestEndDate_month = BacktestEndDate_parsed[0]
    BacktestEndDate_day = BacktestEndDate_parsed[1]
    BacktestEndDate_year = "20" + BacktestEndDate_parsed[2]

    BacktestEndDate[0][0] = BacktestEndDate_year
    BacktestEndDate[0][1] = BacktestEndDate_month
    BacktestEndDate[0][2] = BacktestEndDate_day
   
    BacktestEndDate_text = "Backtest End Date:    " + ConvertNumtoMonth(int(BacktestEndDate[0][1])) + " " + BacktestEndDate[0][2] + ", " + BacktestEndDate[0][0]
    BacktestEndDate_label.configure(text = str(BacktestEndDate_text))

def BacktestDataAck():
    root.popup = ctk.CTkToplevel()
    root.popup.wm_title("Backtest Data")

    # Popup Dimensions
    BacktestPopupWidth = 400
    BacktestPopupHeight = 100

    # Screen Dimensions
    ScreenWidth = root.winfo_screenwidth()
    ScreenHeight = root.winfo_screenheight()

    # Calculate x and y coordinates for Popup
    BacktestPopup_x = (ScreenWidth/2) - (BacktestPopupWidth/2) + (2 * ScreenWidth)
    BacktestPopup_y = (ScreenHeight/2) - (BacktestPopupHeight/2)

    # Set Window Dimensions and location
    root.popup.geometry('%dx%d+%d+%d' % (BacktestPopupWidth, BacktestPopupHeight, BacktestPopup_x, BacktestPopup_y))

    root.popup.grid_columnconfigure((0, 1, 2, 3), weight=1)
    root.popup.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

    Ack_label = ctk.CTkLabel(master=root.popup, text="Are you sure you want to Ingest Backtest Data from:")
    Ack_label.grid(row=0, column=0, columnspan=4)

    AckBegin_label = ctk.CTkLabel(master=root.popup, text="Begin: " + BacktestBeginDate[0][0] + "/" + BacktestBeginDate[0][1] + "/" + BacktestBeginDate[0][2])
    AckBegin_label.grid(row=1, column=1)

    AckEnd_label = ctk.CTkLabel(master=root.popup, text="End: " + BacktestEndDate[0][0] + "/" + BacktestEndDate[0][1] + "/" + BacktestEndDate[0][2])
    AckEnd_label.grid(row=1, column=3)

    Yes_button = ctk.CTkButton(master=root.popup, text="Yes", command=BacktestData)
    Yes_button.grid(row=4, column=1)

    No_button = ctk.CTkButton(master=root.popup, text="No", command=root.popup.destroy)
    No_button.grid(row=4, column=3)

    # Make Popup stay ontop
    root.popup.transient(root.popup.master)

    # Hijack all commands from master, clicks on main window are ignored
    root.popup.grab_set()

def BacktestData():
    # Close Popup
    root.popup.destroy()

    BacktestEndDate_year = BacktestEndDate[0][0]
    BacktestEndDate_month = BacktestEndDate[0][1]
    BacktestEndDate_day = BacktestEndDate[0][2]
    BacktestEndDate_date = BacktestEndDate_year + BacktestEndDate_month + BacktestEndDate_day

    print("Ingesting Backtest Data")
    subprocess.run(["powershell", "-c", "python 10-code/10-runners/100-ingest.py -m backtest -d" + BacktestEndDate_date])

    UpdateFileListbox(Backtest_listbox, BacktestDirectory)

    return


# Backtest Files Listbox
Backtest_listbox = tk.Listbox(Ingest_frame, width = 40, height = 5)
Backtest_listbox.place(x=1220, y=320)
Backtest_listbox.configure(font=("Calibri", 18))

# Update Listbox with files from Directory
UpdateFileListbox(Backtest_listbox, BacktestDirectory)



# Backtest Begin Date Button
BacktestBeginDate_button = ctk.CTkButton(master=Ingest_frame, text="Set Backtest Begin Date", command=BacktestBegin)
BacktestBeginDate_button.place(x=685, y=55)
BacktestBeginDate_button.configure(width=150, height=25)

# Backtest End Date Button
BacktestEndDate_button = ctk.CTkButton(master=Ingest_frame, text="Set Backtest End Date", command=BacktestEnd)
BacktestEndDate_button.place(x=845, y=55)
BacktestEndDate_button.configure(width=150, height=25)

# Backtest Data Button
BacktestData_button = ctk.CTkButton(master=Ingest_frame, text="Ingest Backtest Data", command=BacktestDataAck)
BacktestData_button.place(x=760, y=145)
BacktestData_button.configure(width=150, height=25)


# Backtest Begin Date Text
BacktestBeginDate_label = ctk.CTkLabel(master=Ingest_frame, text="")
BacktestBeginDate_label.place(x=750, y=90)
BacktestBeginDate_label.configure(width=150, height=25)

# Backtest End Date Text
BacktestEndDate_label = ctk.CTkLabel(master=Ingest_frame, text="")
BacktestEndDate_label.place(x=750, y=110)



# Call to initiate dates on startup
TrainingBegin()
TrainingEnd()

BacktestBegin()
BacktestEnd()



#------------------------------------------------------------------------------
# Initiate Clock
Clock()

#------------------------------------------------------------------------------
# Run Window
root.after(3000, lambda: root.destroy())
root.mainloop()  

