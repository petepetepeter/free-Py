import time
import random

# https://en.wikipedia.org/wiki/Sorting_algorithm

def rando(size):
    array = []

    for i in range(size):
        array.append(random.randint(0, 10000000))

    return array

def insertion_sort(input_list):

    for i in range(1, len(input_list)):
        count = i - 1
        temp = input_list[i]
        while count >= 0 and temp < input_list[count]:
            input_list[count + 1] = input_list[count]
            count -= 1
        input_list[count + 1] = temp

    # print(input_list)
    return input_list

def selection_sort(input_list):
    switch = 0

    for i in range(len(input_list)):
        minimum = i

        for k in range(i + 1, len(input_list)):
            if input_list[k] < input_list[minimum]:
                minimum = k
                switch = 1
        if switch != 0:
            input_list[i], input_list[minimum] = input_list[minimum], input_list[i]
            switch = 0

    # print(input_list)
    return input_list

"""
Ripped the 'merge_separate()' and 'merge_merge()' builds from:
https://towardsdatascience.com/how-to-implement-merge-sort-algorithm-in-python-4662a89ae48c
vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""

def merge_separate(input_list):
    length = len(input_list)

    if length == 1:
        return input_list
    else:
        midpoint = length // 2

        left = input_list[:midpoint]
        right = input_list[midpoint:]
        return_1 = merge_separate(left)
        return_2 = merge_separate(right)

        return merge_merge(return_1, return_2)

def merge_merge(return_1, return_2):
    merged_list = []
    i = k = 0

    while i < len(return_1) and k < len(return_2):

        if return_1[i] < return_2[k]:
            merged_list.append(return_1[i])
            i += 1
        else:
            merged_list.append(return_2[k])
            k += 1
    
    merged_list.extend(return_1[i:])
    merged_list.extend(return_2[k:])

    return merged_list

"""
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ripped the 'merge_separate()' and 'merge_merge()' builds from:
https://towardsdatascience.com/how-to-implement-merge-sort-algorithm-in-python-4662a89ae48c
"""

def bubble_sort(input_list):

    for i in range(len(input_list)):
        for k in range(len(input_list) - 1):
            if input_list[k] > input_list[k + 1]:
                input_list[k], input_list[k + 1] = input_list[k + 1], input_list[k]

    # print(input_list)
    return input_list

def exchange_sort(input_list):

    for i in range(len(input_list)):
        for k in range(i + 1, len(input_list)):
            if input_list[i] > input_list[k]:
                input_list[k], input_list[i] = input_list[i], input_list[k]

    # print(input_list)
    return input_list

size = 1000
sample = rando(size)
x1 = sample.copy()
x2 = sample.copy()
x3 = sample.copy()
x4 = sample.copy()
x5 = sample.copy()

print(f"Array Size: {size}\n{('=' * 20)}")

time.sleep(2)

# print(f"INPUT 1: {x1}")
start_1 = time.perf_counter()
out_1 = insertion_sort(x1)
end_1 = time.perf_counter()
# print(f"OUTPUT 1: {out_1}")

time.sleep(2)

# print(f"INPUT 2: {x2}")
start_2 = time.perf_counter()
out_2 = selection_sort(x2)
end_2 = time.perf_counter()
# print(f"OUTPUT 2: {out_2}")

time.sleep(2)

# print(f"INPUT 3: {x3}")
start_3 = time.perf_counter()
out_3 = merge_separate(x3)
end_3 = time.perf_counter()
# print(f"OUTPUT 3: {out_3}")

time.sleep(2)

# print(f"INPUT 4: {x4}")
start_4 = time.perf_counter()
out_4 = bubble_sort(x4)
end_4 = time.perf_counter()
# print(f"OUTPUT 4: {out_4}")

time.sleep(2)

# print(f"INPUT 5: {x5}")
start_5 = time.perf_counter()
out_5 = exchange_sort(x5)
end_5 = time.perf_counter()
# print(f"OUTPUT 5: {out_5}")

print(f"{'Insertion sort:':15} {(end_1 - start_1):023.20f} seconds")
print(f"{'Selection sort:':15} {(end_2 - start_2):023.20f} seconds")
print(f"{'Merge sort:':15} {(end_3 - start_3):023.20f} seconds")
print(f"{'Bubble sort:':15} {(end_4 - start_4):023.20f} seconds")
print(f"{'Exchange sort:':15} {(end_5 - start_5):023.20f} seconds")
