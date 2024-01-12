import threading
import time

# Shared boolean variable
shared_bool = False

def thread_function():
    global shared_bool
    while True:
        time.sleep(1)
        print(f"Thread 1: {shared_bool}")

# Create and start the thread
thread = threading.Thread(target=thread_function)
thread.start()

# Main script logic
while True:
    user_input = input("Enter 'True' or 'False' to update the shared variable: ")
    shared_bool = (user_input.lower() == 'true')
