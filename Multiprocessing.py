"""

Name: Declan Murphy
Date: 09/15/24
Assignment: 3
Due Date: 09/15/24
About this project: Apply parallel and distributed computing to computational problems and analyze the scalability and efficiency of the solutions.
Assumptions: Dataset is valid and able to be run in parallel
All work below was performed by Declan Murphy

"""

import multiprocessing as mp
from collections import Counter


def count_starting_digit(data, start, end, shared_array, event):
    local_counter = Counter()
    for num in data[start:end]:
        first_digit = int(str(num)[0])
        local_counter[first_digit] += 1

    for digit, count in local_counter.items():
        shared_array[digit] += count

    event.set()   # Signal that process has finished


def multiprocessing_solution(income_data):
    num_processes = mp.cpu_count()  # Use number of CPU cores
    chunk_size = len(income_data) // num_processes

    shared_array = mp.Array('i', [0] * 10)  # Shared array to store counts for digits 0-9
    events = [mp.Event() for _ in range(num_processes)]
    processes = []

    # Create and start processes
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(income_data)
        process = mp.Process(target=count_starting_digit, args=(income_data, start, end, shared_array, events[i]))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for event in events:
        event.wait()

    for process in processes:
        process.join()

    # Combine results from all processes
    return Counter({i: shared_array[i] for i in range(1, 10)})  # Convert shared array to Counter, excluding 0


# Main execution
if __name__ == "__main__":
    # Read and process the input file
    with open("IncomeDF.txt", "r") as file:
        content = file.read().strip()
        # Remove the "IncomeDf = [" prefix and the trailing "]"
        content = content.replace("IncomeDf = [", "").rstrip("]")
        income_data = [int(x.strip()) for x in content.split(',')]

    result = multiprocessing_solution(income_data)
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

