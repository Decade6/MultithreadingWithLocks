"""

Name: Declan Murphy
Date: 09/22/2024
Assignment: 4
Due Date: 09/22/2024
About this project: Apply parallel and distributed computing to computational problems and
analyze the scalability and efficiency of the solutions.
Assumptions: Threads are being used over multiprocesses, loan account initialized to -25000,
payments.txt file already exists in directory
All work below was performed by Declan Murphy

"""

import threading
import random

# Lock for thread safety
lock = threading.Lock()

# Initialize player's loan account
loan_account = -25000

# Initialize a file path
file_path = 'payments.txt'


# Clear the file
def clear_file(file_path):
    with open(file_path, 'w') as file:
        file.truncate()


# Append a number to a file
def append_to_file(file_path, number):
    with open(file_path, 'a') as file:
        file.write(str(number) + '\n')


# 'Pay' function
def pay():
    global loan_account
    for _ in range(5):
        amount = random.randint(1, 1500)
        with lock:
            loan_account += amount
            append_to_file(file_path, amount)


# Accountant function
def accountant():
    global loan_account
    while True:
        with lock:
            with open(file_path, 'r') as file:
                payments = file.readlines()
                for payment in payments:
                    loan_account += int(payment.strip())
            print('Current loan account:', loan_account)
            clear_file(file_path)
            if loan_account >= 0:
                break


# Main function to manage threads
def main():
    # Create Accountant thread
    accountant_thread = threading.Thread(target=accountant)
    accountant_thread.start()

    # Create 25 Pay threads
    pay_threads = []
    for _ in range(25):
        thread = threading.Thread(target=pay)
        pay_threads.append(thread)
        thread.start()

    # Waiting for all Pay threads to finish
    for thread in pay_threads:
        thread.join()

    # Waiting for Accountant thread to finish
    accountant_thread.join()


if __name__ == "__main__":
    main()
