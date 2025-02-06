import tkinter as tk
from tkinter import ttk, messagebox
import math
import pandas as pd
import random
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def generate_list(length, name):
    return {name:random.sample(range(1, length+1), length)}

def generate_test_data():
    size = 100

    test_cases = { 'Sorted': list(range(1, size + 1)),
                'RevSorted': list(range(size, 0, -1))}
    for i in range(100):
        test_cases.update(generate_list(i+1,'Test' + str(i+1)))

    max_len = max(len(l) if isinstance(l, list) else 1 for l in test_cases.values())

    for key in test_cases.keys():
        while len(test_cases[key]) != max_len:
            test_cases[key].append(0)

    file_name = 'Test_cases.xlsx'
    df2 = pd.DataFrame(test_cases)
    df2.to_excel(file_name)
    print(f"Test data saved to {file_name}")


class StepCounter:
    comparisons = 0
    swaps = 0
    def _init_(self):
        self.comparisons = 0
        self.swaps = 0

    def add_comparison(self):
        self.comparisons += 1

    def add_swap(self):
        self.swaps += 1

    def total_steps(self):
        return self.comparisons + self.swaps


def insertion_sort_steps(arr):
    counter = StepCounter()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        counter.add_comparison()  # Initial comparison in while condition
        while j >= 0 and key < arr[j]:
            counter.add_swap()  # Count moving element
            arr[j + 1] = arr[j]
            j -= 1
            if j >= 0:  # Only count if we'll do another comparison
                counter.add_comparison()
        counter.add_swap()  # Count placing key
        arr[j + 1] = key
    return counter.total_steps()

def merge_sort_steps(arr):
    counter = StepCounter()

    def merge(A, p, q, r):
        n1 = q - p + 1
        n2 = r - q

        # Create temporary arrays L and R
        L = [0] * (n1 + 1)
        R = [0] * (n2 + 1)

        # Copy data to L and R
        for i in range(n1):
            L[i] = A[p + i]
            counter.add_swap()
        for j in range(n2):
            R[j] = A[q + 1 + j]
            counter.add_swap()

        # Set sentinel values
        L[n1] = float('inf')
        R[n2] = float('inf')

        i = 0
        j = 0

        # Merge the arrays back into A
        for k in range(p, r + 1):
            counter.add_comparison()
            if L[i] <= R[j]:
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1
            counter.add_swap()

    def merge_sort(A, p, r):
        counter.add_comparison()
        if p < r:
            # Find the middle point
            q = (p + r) // 2

            # Sort the first and second halves
            merge_sort(A, p, q)
            merge_sort(A, q + 1, r)

            # Merge the sorted halves
            merge(A, p, q, r)

    merge_sort(arr, 0, len(arr) - 1)
    return counter.total_steps()


def bubble_sort_steps(arr):
    counter = StepCounter()
    for n in range(len(arr) - 1, 0, -1):
        for i in range(n):
            counter.add_comparison()  # Compare adjacent elements
            if arr[i] > arr[i + 1]:
                counter.add_swap()  # Count swap if needed
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return counter.total_steps()


def quick_sort_steps(arr):
    counter = StepCounter()

    def partition(A, p, r):
        x = A[r]  # Pivot element
        i = p - 1  # Index of smaller element

        for j in range(p, r):
            counter.add_comparison()
            if A[j] <= x:
                i += 1
                # Swap A[i] and A[j]
                A[i], A[j] = A[j], A[i]
                counter.add_swap()

        # Swap A[i + 1] and A[r] (the pivot element)
        A[i + 1], A[r] = A[r], A[i + 1]
        counter.add_swap()
        return i + 1

    def quick_sort(A, p, r):
        counter.add_comparison()
        if p < r:

            # Partition the array and get the pivot index
            q = partition(A, p, r)

            # Recursively sort elements before and after partition
            quick_sort(A, p, q - 1)
            quick_sort(A, q + 1, r)


    quick_sort(arr.copy(), 0 ,len(arr)-1)
    return counter.total_steps()


def heap_sort_steps(arr):
    counter = StepCounter()

    def max_heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
            counter.add_comparison()
        else:
            largest = i

        if right < n and arr[right] > arr[largest] :
                largest = right
                counter.add_comparison()

        if largest != i:
            counter.add_swap()
            arr[i], arr[largest] = arr[largest], arr[i]
            max_heapify(arr, n, largest)


    def build_max_heap(arr):
        n = len(arr)
        for i in range(n //2 -1 , -1,-1 ):
            max_heapify(arr,n,i)

    n = len(arr)
    build_max_heap(arr)


    for i in range(n - 1, 0, -1):
        counter.add_swap()
        arr[i], arr[0] = arr[0], arr[i]
        max_heapify(arr, i, 0)

    return counter.total_steps()



def test_comp(file_name , algorithm , testcase):
    df = pd.read_excel(file_name)
    arr = []
    steps_number = []


    for i in range(100):
        arr3 = []
        if testcase == 'Random':
            arr1 = df['Test' + str(i + 1)].tolist()
        elif testcase == 'Sorted' :
            arr1 = df['Sorted'].tolist()
        else:
            arr1 = df['RevSorted'].tolist()
        for j in range(i+1):
            # print(arr1[j])
            arr3.append(arr1[j])
        arr.append(arr3)
    print(arr)
    for case in arr:
            y = algorithm(case.copy())
            steps_number.append(y)
            # print(y)

    return steps_number



def plot_results(steps1, steps2, alg1_name, alg2_name, plot_title, x_label, y_label):
    fig, ax = plt.subplots()
    ax.plot(steps1, marker='.', label=alg1_name)
    ax.plot(steps2, marker='.', label=alg2_name)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(plot_title)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=results_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def run_comparison():
    try:
        alg1 = algorithm_var1.get()
        alg2 = algorithm_var2.get()
        testcase = test_var1.get()

        if alg1 == "Select an algorithm" or alg2 == "Select an algorithm" or alg1 == alg2:
            raise ValueError("Please select two different algorithms.")

        steps1 = test_comp('Test_cases.xlsx', algorithms[alg1], testcase)
        steps2 = test_comp('Test_cases.xlsx', algorithms[alg2], testcase)

        plot_results(steps1, steps2, alg1, alg2, "Algorithm Comparison", "Test Cases", "Number of Steps")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except FileNotFoundError:
        messagebox.showerror("Error", "Test data file not found. Please generate test data first.")


def run_asymptotic_analysis():
    try:
        alg1 = asymptotic_algorithm_var.get()
        testcase = test_var2.get()
        if alg1 == "Select an algorithm":
            raise ValueError("Please select an algorithm.")
        test_files = 'Test_cases.xlsx'
        alg_eff = asym_eff[alg1][1]
        steps1 = test_comp(test_files, algorithms[alg1] , testcase)
        steps2 = []

        for i in range(100):
            steps2.append(asym_eff[alg1][0](i + 1))
        plot_results(steps1, steps2, alg1, "Asymptotic " + alg_eff, "Asymptotic Efficiency Analysis", "Test Cases(n)", "Number of Steps")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except FileNotFoundError:
        messagebox.showerror("Error", "Test data file not found. Please generate test data first.")

def generate_data_gui():
    generate_test_data()
    messagebox.showinfo("Success", "Test data generated successfully!")

root = tk.Tk()
root.title("Sorting Algorithm Analysis")

window_width = 1000
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT ,fill= tk.BOTH)
# Frames for organization
button_frame = ttk.LabelFrame(left_frame,text="Options", padding=20)
button_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=True)



comparison_frame = ttk.LabelFrame(left_frame, text="Algorithm Comparison", padding=10)
comparison_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

asymptotic_frame = ttk.LabelFrame(left_frame, text="Asymptotic Efficiency", padding=10)
asymptotic_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

results_frame = ttk.LabelFrame(root, text="Graphical Results", padding=10)
results_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)


generate_data_button = ttk.Button(button_frame, text="Generate Test Data", command=generate_data_gui)
generate_data_button.pack(side=tk.TOP, padx=10)


algorithms = {
    'Insertion Sort': insertion_sort_steps,
    'Merge Sort': merge_sort_steps,
    'Bubble Sort': bubble_sort_steps,
    'Quick Sort': quick_sort_steps,
    'Heap Sort': heap_sort_steps
}


test_options = ['Sorted', 'Reverse Sorted' , 'Random']
algorithm_var1 = tk.StringVar(value="Select an algorithm")
algorithm_var2 = tk.StringVar(value="Select an algorithm")
test_var1 = tk.StringVar(value="Select Test Case")

test_dropdown1 = ttk.Combobox(comparison_frame,textvariable=test_var1, values=test_options)
test_dropdown1.pack(pady=5)
algorithm_dropdown1 = ttk.Combobox(comparison_frame, textvariable=algorithm_var1, values=list(algorithms.keys()))
algorithm_dropdown1.pack(pady=5)
algorithm_dropdown2 = ttk.Combobox(comparison_frame, textvariable=algorithm_var2, values=list(algorithms.keys()))
algorithm_dropdown2.pack(pady=5)

compare_button = ttk.Button(comparison_frame, text="Compare Algorithms", command=run_comparison)
compare_button.pack(pady=10)


asym_eff = {
    'Insertion Sort': [lambda n: math.pow(n, 2), 'O(n^2)'],
    'Merge Sort': [lambda n: (n * math.log2(n)), 'O(nlog(n))'],
    'Bubble Sort': [lambda n: math.pow(n, 2), 'O(n^2)'],
    'Quick Sort': [lambda n: math.pow(n, 2), 'O(n^2)'],
    'Heap Sort': [lambda n: (n * math.log2(n)), 'O(nlog(n))']
}

asymptotic_algorithm_var = tk.StringVar(value="Select an algorithm")
test_var2 = tk.StringVar(value="Select Test Case")

test_dropdown2 = ttk.Combobox(asymptotic_frame,textvariable=test_var2, values=test_options)
test_dropdown2.pack(pady=5)
asymptotic_algorithm_dropdown = ttk.Combobox(asymptotic_frame, textvariable=asymptotic_algorithm_var, values=list(algorithms.keys()))
asymptotic_algorithm_dropdown.pack(pady=5)

asymptotic_button = ttk.Button(asymptotic_frame, text="Analyze Asymptotic Efficiency", command=run_asymptotic_analysis)
asymptotic_button.pack(pady=10)


def clear_results():
    # Clear all widgets in the results frame
    for widget in results_frame.winfo_children():
        widget.destroy()


def plot_results(steps1, steps2, alg1_name, alg2_name, plot_title, x_label, y_label):
    # Clear previous results first
    clear_results()

    fig, ax = plt.subplots()
    ax.plot(steps1, marker='.', label=alg1_name)
    ax.plot(steps2, marker='.', label=alg2_name)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(plot_title)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=results_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

clear_results_button = ttk.Button(button_frame, text="Clear Results", command=clear_results)
clear_results_button.pack(pady=10, side=tk.TOP)

button_frame = ttk.Frame(root)
button_frame.pack()






root.mainloop()