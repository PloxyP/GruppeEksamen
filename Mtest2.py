import time
import threading

def thread_function_2(shared_bool, lock):
    while True:
        with lock:
            time.sleep(1)
            print(f"Thread 2: {shared_bool}")

# Shared boolean variable and lock
shared_bool = False
lock = threading.Lock()

# Create and start thread for script2
thread_2 = threading.Thread(target=thread_function_2, args=(shared_bool, lock))
thread_2.start()

# Main script logic for script2
while True:
    # Additional script2 logic if needed
    pass
