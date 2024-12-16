import time
import random


def quicksort(arr):
    if len(arr) <= 1:
        return arr

    mid_index = len(arr) // 2
    middle = arr[mid_index]

    less = []
    equal = []
    greater = []

    for x in arr:
        if x < middle:
            less.append(x)
        elif x == middle:
            equal.append(x)
        else:
            greater.append(x)

    return quicksort(less) + equal + quicksort(greater)


if __name__ == "__main__":

    arr_random = [random.randint(0, 1000) for i in range(1000)]
    start_time = time.time()
    sorted_arr = quicksort(arr_random)
    end_time = time.time()
    print("Рандомно отсортированный массив:", sorted_arr)
    print("Время выполнения сортировки на рандомном массиве: {:.6f} секунд".format(end_time - start_time))