import time
import threading

def thread_function_2(shared_bool, lock):
    while True:
        with lock:
            time.sleep(1)
            print(f"Thread 2: {shared_bool}")
