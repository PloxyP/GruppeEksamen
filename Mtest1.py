import multiprocessing
import time
from Mtest2 import program2_function

def program1_function(shared_variable):
    while True:
        user_input = input("Enter 'True' or 'False': ").lower()
        if user_input == 'true':
            shared_variable.value = True
        elif user_input == 'false':
            shared_variable.value = False
        else:
            print("Invalid input. Please enter 'True' or 'False'.")

if __name__ == "__main__":
    shared_variable = multiprocessing.Value('b', False)
    program2_process = multiprocessing.Process(target=program2_function, args=(shared_variable,))
    program2_process.start()

    program1_function(shared_variable)
