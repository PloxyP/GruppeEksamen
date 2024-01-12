import time
import threading

def thread_function_2(shared_bool, lock):
    while True:
        with lock:
            time.sleep(1)
            print(f"Thread 2: {shared_bool}")

# Main script logic for script2
if __name__ == "__main__":
    # Shared boolean variable (moved inside __main__ guard)
    shared_bool = False
    lock = threading.Lock()

    # Create and start thread for script2
    thread_2 = threading.Thread(target=thread_function_2, args=(shared_bool, lock))
    thread_2.start()

    # Additional script2 logic if needed
    while True:
        pass
