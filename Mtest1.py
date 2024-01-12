import multiprocessing
import time

def program1_shared_variable(shared_variable):
    while True:
        print("Program 1 is running")
        time.sleep(1)
        # Update the shared variable
        shared_variable.value = not shared_variable.value

if __name__ == "__main__":
    # Create a shared variable between processes
    shared_variable = multiprocessing.Value('b', False)

    # Start program2.py as a separate process
    process2 = multiprocessing.Process(target=multiprocessing.run_path, args=("program2.py",))

    # Start the function in program1.py
    program1_shared_process = multiprocessing.Process(target=program1_shared_variable, args=(shared_variable,))
    program1_shared_process.start()

    # Start program2.py
    process2.start()

    # Wait for both processes to finish
    program1_shared_process.join()
    process2.join()
