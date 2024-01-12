import time

def thread_function_2(shared_bool):
    while True:
        time.sleep(1)
        print(f"Thread 2: {shared_bool}")
