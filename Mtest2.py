import time

def program2_shared_variable(shared_variable):
    while True:
        print("Program 2 is running")
        time.sleep(1)
        # Access the shared variable
        print(f"Shared variable in Program 2: {shared_variable.value}")

if __name__ == "__main__":
    # Create a shared variable between processes
    shared_variable = multiprocessing.Value('b', False)

    # Start the function in program2.py
    program2_shared_process = multiprocessing.Process(target=program2_shared_variable, args=(shared_variable,))
    program2_shared_process.start()

    # Wait for the process to finish
    program2_shared_process.join()
