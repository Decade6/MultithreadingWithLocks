"""

Name: Declan Murphy
Date: 09/15/24
Assignment: 3
Due Date: 09/15/24
About this project: Apply parallel and distributed computing to computational problems and analyze the scalability and efficiency of the solutions.
Assumptions: Dataset is valid and able to be run in parallel
All work below was performed by Declan Murphy

"""

import threading
from collections import Counter

def count_starting_digit(data, start, end, counter, event):
    for num in data[start:end]:
        first_digit = int(str(num)[0])
        counter[first_digit] += 1
    event.set()  # Signal that this thread has finished

def thread_solution(income_data):
    num_threads = 4
    chunk_size = len(income_data) // num_threads
    counters = [Counter() for _ in range(num_threads)]
    events = [threading.Event() for _ in range(num_threads)]
    threads = []

    # Create and start threads
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(income_data)
        thread = threading.Thread(target=count_starting_digit, args=(income_data, start, end, counters[i], events[i]))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for event in events:
        event.wait()

    # Combine results from all threads
    total_counter = sum(counters, Counter())
    return total_counter

# Main execution
if __name__ == "__main__":
    # Read and process the input file
    with open("IncomeDF.txt", "r") as file:
        content = file.read().strip()
        # Remove the "IncomeDf = [" prefix and the trailing "]"
        content = content.replace("IncomeDf = [", "").rstrip("]")
        income_data = [int(x.strip()) for x in content.split(',')]

    result = thread_solution(income_data)
    total_count = sum(result.values())

    # Calculate and print percentages
    print("digit %")
    for digit in range(1, 10):
        percentage = result[digit] / total_count
        print(f"{digit}    {percentage:.4f}")

    # Find and print most and least frequent digits
    most_frequent = max(result, key=result.get)
    least_frequent = min(result, key=result.get)

    print(f"Most Freq starting digit: {most_frequent}")
    print(f"Least Freq starting digit: {least_frequent}")
