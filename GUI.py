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
WindowWidth = 1000
WindowHeight = 850

# Screen Dimensions
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()

# Calculate x and y coordinates for Window
MainWindow_x = (ScreenWidth/2) - (WindowWidth/2) + (2 * ScreenWidth)
MainWindow_y = (ScreenHeight/2) - (WindowHeight/2)

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
Time_frame.place(x=500, y=0)
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

    # Time_frame.Clock_label.configure(text=CurrentTime_text)

    

    # Time_frame.CurrentDate.Date_label.configure(text=DayOfWeek + " " + Month + " " + Day + ", " + Year)


#------------------------------------------------------------------------------
# Generate Ingest Data Frame
Ingest_frame = ctk.CTkFrame(root)
Ingest_frame.place(x=0, y=100)
Ingest_frame.configure(width = 600, height = 300)

# Ingest Title
IngestTitle_label = ctk.CTkLabel(master=Ingest_frame, text="Ingest", font=("Calibri", 35))
IngestTitle_label.place(x=10, y=5)

# https://www.geeksforgeeks.org/python/create-a-date-picker-calendar-tkinter/
# Add Calendar
YearNow = int(time.strftime("%Y"))
MonthNow = int(time.strftime("%m"))
DayNow = int(time.strftime("%d"))

calendar = Calendar(master=Ingest_frame, selectmode = 'day', year = YearNow, month = MonthNow, day = DayNow)
calendar.place(x=25, y=95)




def ParseCalendarDate(CalendarDate):
    ParsedCalendarDate = CalendarDate.split("/")
    return ParsedCalendarDate

def IngestBegin():
    global IngestBeginDate
    IngestBeginDate = np.empty(shape=(1, 3), dtype='object')

    IngestBeginDate_calendar = calendar.get_date()
    IngestBeginDate_parsed = ParseCalendarDate(IngestBeginDate_calendar)

    IngestBeginDate_month = IngestBeginDate_parsed[0]
    IngestBeginDate_day = IngestBeginDate_parsed[1]
    IngestBeginDate_year = "20" + IngestBeginDate_parsed[2]

    IngestBeginDate[0][0] = IngestBeginDate_year
    IngestBeginDate[0][1] = IngestBeginDate_month
    IngestBeginDate[0][2] = IngestBeginDate_day
    
    IngestBeginDate_text = "Begin Date: " + IngestBeginDate[0][0] + "/" + IngestBeginDate[0][1] + "/" + IngestBeginDate[0][2]
    IngestBeginDate_label.configure(text = str(IngestBeginDate_text))

def IngestEnd():
    global IngestEndDate
    IngestEndDate = np.empty(shape=(1, 3), dtype='object')

    IngestEndDate_calendar = calendar.get_date()
    IngestEndDate_parsed = ParseCalendarDate(IngestEndDate_calendar)

    IngestEndDate_month = IngestEndDate_parsed[0]
    IngestEndDate_day = IngestEndDate_parsed[1]
    IngestEndDate_year = "20" + IngestEndDate_parsed[2]

    IngestEndDate[0][0] = IngestEndDate_year
    IngestEndDate[0][1] = IngestEndDate_month
    IngestEndDate[0][2] = IngestEndDate_day
    
    IngestEndDate_text = "End Date: " + IngestEndDate[0][0] + "/" + IngestEndDate[0][1] + "/" + IngestEndDate[0][2]
    IngestEndDate_label.configure(text = str(IngestEndDate_text))

def IngestDataAck():
    root.popup = ctk.CTkToplevel()
    root.popup.wm_title("Ingest Data")

    # Popup Dimensions
    IngestPopupWidth = 400
    IngestPopupHeight = 100

    # Screen Dimensions
    ScreenWidth = root.winfo_screenwidth()
    ScreenHeight = root.winfo_screenheight()

    # Calculate x and y coordinates for Popup
    IngestPopup_x = (ScreenWidth/2) - (IngestPopupWidth/2) + (2 * ScreenWidth)
    IngestPopup_y = (ScreenHeight/2) - (IngestPopupHeight/2)

    # Set Window Dimensions and location
    root.popup.geometry('%dx%d+%d+%d' % (IngestPopupWidth, IngestPopupHeight, IngestPopup_x, IngestPopup_y))

    root.popup.grid_columnconfigure((0, 1, 2, 3), weight=1)
    root.popup.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

    Ack_label = ctk.CTkLabel(master=root.popup, text="Are you sure you want to Ingest Data from:")
    Ack_label.grid(row=0, column=0, columnspan=4)

    AckBegin_label = ctk.CTkLabel(master=root.popup, text="Begin: " + IngestBeginDate[0][0] + "/" + IngestBeginDate[0][1] + "/" + IngestBeginDate[0][2])
    AckBegin_label.grid(row=1, column=1)

    AckEnd_label = ctk.CTkLabel(master=root.popup, text="End: " + IngestEndDate[0][0] + "/" + IngestEndDate[0][1] + "/" + IngestEndDate[0][2])
    AckEnd_label.grid(row=1, column=3)

    Yes_button = ctk.CTkButton(master=root.popup, text="Yes", command=IngestData)
    Yes_button.grid(row=4, column=1)

    No_button = ctk.CTkButton(master=root.popup, text="No", command=root.popup.destroy)
    No_button.grid(row=4, column=3)

    # Make Popup stay ontop
    root.popup.transient(root.popup.master)

    # Hijack all commands from master, clicks on main window are ignored
    root.popup.grab_set()

def IngestData():
    # Close Popup
    root.popup.destroy()

    print("Ingest Data function")

    return

# Ingest Begin Date Button
IngestBeginDate_button = ctk.CTkButton(master=Ingest_frame, text="Begin Date", command=IngestBegin)
IngestBeginDate_button.place(x=200, y=75)

# Ingest End Date Button
IngestEndDate_button = ctk.CTkButton(master=Ingest_frame, text="End Date", command=IngestEnd)
IngestEndDate_button.place(x=200, y=105)

# Ingest Begin Date Text
IngestBeginDate_label = ctk.CTkLabel(master=Ingest_frame, text="")
IngestBeginDate_label.place(x=400, y=75)

# Ingest End Date Text
IngestEndDate_label = ctk.CTkLabel(master=Ingest_frame, text="")
IngestEndDate_label.place(x=400, y=105)

# Ingest Data Button
IngestData_button = ctk.CTkButton(master=Ingest_frame, text="Ingest Data", command=IngestDataAck)
IngestData_button.place(x=200, y=135)

# Call to initiate dates on startup
IngestBegin()
IngestEnd()



#------------------------------------------------------------------------------
# Veritcal Scroll Bar and mouse wheel control
# canvas = ctk.Canvas(root, borderwidth=0, background='#7393B3')
# frame = ctk.Frame(canvas, background="#ffffff")
# vsb = ctk.Scrollbar(root, orient="vertical", command=canvas.yview)
# canvas.configure(yscrollcommand=vsb.set)

# Bind mouse wheel to the canvas
# canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Ensure that the mouse wheel event is updated whenever the window size changes
# frame.update_idletasks()

# canvas.config(scrollregion=canvas.bbox("all"))


#------------------------------------------------------------------------------
# Initiate Clock
# Clock()

#------------------------------------------------------------------------------
# Run Window
# root.after(3000, lambda: root.destroy())
root.mainloop()  

