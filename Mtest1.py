import multiprocessing
import time
from Mtest2 import program2_function

def program1_function(shared_variable):
    while True:
        time.sleep(1)  # Simulate some work
        shared_variable.value = not shared_variable.value
        print(f"Program 1 - Shared Variable: {shared_variable.value}")

if __name__ == "__main__":
    shared_variable = multiprocessing.Value('b', False)
    program2_process = multiprocessing.Process(target=program2_function, args=(shared_variable,))
    program2_process.start()

    program1_function(shared_variable)
