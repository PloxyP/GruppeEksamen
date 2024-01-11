from tkinter import *
import datetime

def showCalender():
    gui = Tk()
    gui.config(background='grey')
    gui.title("5-Day Calendar")

    # Set fullscreen
    gui.attributes("-fullscreen", True)

    # Calculate the current date and next four days
    today = datetime.date.today()
    dates = [today + datetime.timedelta(days=i) for i in range(5)]

    # Create a frame for the dates
    frame = Frame(gui, bg='grey')
    frame.pack(expand=True)

    # Create a label for each date and display it in the frame with a larger font size
    for i, date in enumerate(dates):
        Label(frame, text=date.strftime("%A, %B %d, %Y"), font="Consolas 15 bold", bg='grey').grid(row=i, column=0, padx=20, pady=10, sticky="ew")

    # Log-off button
    def logOff():
        gui.destroy()

    logOffButton = Button(gui, text="Log Off", command=logOff, font="Consolas 12 bold", padx=10, pady=5)
    logOffButton.pack(side='right', padx=20, pady=20)

    gui.mainloop()

if __name__=='__main__':
    showCalender()
