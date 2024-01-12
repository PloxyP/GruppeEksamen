import tkinter as tk
import time

# Function to clear the welcome message
def clear_welcome_message():
    welcome_label.pack_forget()

# Create the main window
root = tk.Tk()
root.title('Welcome Message')
root.geometry('800x480')
root.attributes('-fullscreen', True)

# Background color
background_color = 'black'
root.configure(bg=background_color)

# Font settings
font = ('Helvetica', 36)
font_color = 'white'

# Create a label for the welcome message
welcome_label = tk.Label(root, text='Welcome!', font=font, fg=font_color, bg=background_color)
welcome_label.pack(expand=True)

# Display the first welcome message
root.update()
time.sleep(3)

# Clear the screen for the second message
clear_welcome_message()
root.update()
time.sleep(0.1)

# Display the second welcome message
welcome_label.config(text='Please use your ID Card to log in')
welcome_label.pack(expand=True)
root.update()
time.sleep(2)

# Clear the screen
clear_welcome_message()
root.update()
time.sleep(0.1)

# Close the window after a short delay
time.sleep(1)
root.destroy()
root.mainloop()
