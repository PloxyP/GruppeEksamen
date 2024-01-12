import time

def program2_function(shared_variable):
    while True:
        time.sleep(1)  # Simulate some work
        print(f"Program 2 - Shared Variable: {shared_variable.value}")
