import threading
import time
from Mtest2 import thread_function_2

# Shared boolean variable
shared_bool = False
lock = threading.Lock()

def thread_function_1():
    global shared_bool
    while True:
        with lock:
            time.sleep(1)
            print(f"Thread 1: {shared_bool}")

# Create and start both threads, passing shared_bool as an argument
thread_1 = threading.Thread(target=thread_function_1)
thread_2 = threading.Thread(target=thread_function_2, args=(shared_bool, lock))

thread_1.start()
thread_2.start()

# Main script logic
while True:
    user_input = input("Enter 'True' or 'False' to update the shared variable: ")
    with lock:
        shared_bool = (user_input.lower() == 'true')
