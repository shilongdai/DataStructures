import random
import unittest


def exchange(arr, i, j):
	temp = arr[i]
	arr[i] = arr[j]
	arr[j] = temp


def selection_sort(arr):
	length = len(arr)
	for i in range(length):
		current_min = i
		for j in range(i, length):
			if arr[j] < arr[current_min]:
				current_min = j
		exchange(arr, i, current_min)


def insertion_sort(arr):
	_range_insertion_sort(arr, 0, len(arr))


def _range_insertion_sort(array, low, high):
	length = high - low
	for i in range(low + 1, high):
		insertion_point = i
		insertion_val = array[i]
		while insertion_point > low and array[insertion_point - 1] > insertion_val:
			array[insertion_point] = array[insertion_point - 1]
			insertion_point -= 1
		array[insertion_point] = insertion_val


def shell_sort(arr):
	length = len(arr)
	h = 1
	while h < length // 3:
		h = 3 * h + 1
	while h >= 1:
		for i in range(1, length):
			insertion_point = i
			insertion_val = arr[i]
			while insertion_point > 0 and arr[insertion_point - h] > insertion_val:
				arr[insertion_point] = arr[insertion_point - h]
				insertion_point -= h
			arr[insertion_point] = insertion_val
		h = h // 3


def _merge(input_array, aux, low, mid, high):
	a_pos = low
	b_pos = mid
	if mid < high:
		if aux[mid] >= aux[mid - 1]:
			for j in range(high - low):
				input_array[low + j] = aux[low + j]
			return
	for i in range(high - low):
		k = i + low
		if a_pos == mid:
			input_array[k] = aux[b_pos]
			b_pos += 1
			continue
		if b_pos >= high:
			input_array[k] = aux[a_pos]
			a_pos += 1
			continue
		if aux[a_pos] > aux[b_pos]:
			input_array[k] = aux[b_pos]
			b_pos += 1
		else:
			input_array[k] = aux[a_pos]
			a_pos += 1


def merge_sort(input_array):
	original = input_array
	segment_size = 16
	length = len(input_array)

	# use insertion sort for small sub-array
	start = 0
	end = segment_size
	while end < length:
		_range_insertion_sort(input_array, start, end)
		start = end
		end += segment_size
	_range_insertion_sort(input_array, start, length)

	aux = [None for i in range(length)]
	while segment_size < len(input_array):
		start = 0
		end = segment_size * 2
		aux, input_array = input_array, aux
		while end < length:
			mid = start + segment_size
			_merge(input_array, aux, start, mid, end)
			start = end
			end += (segment_size * 2)
		final_mid = start + segment_size
		_merge(input_array, aux, start, final_mid, length)
		segment_size = segment_size * 2
	for i in range(length):
		original[i] = input_array[i]


class SortingTest:

	def test_sort(self):
		n = 10000
		random.seed(n)
		to_sort = []
		for i in range(n):
			to_sort.append(random.randint(0, 1000))
		algorithm = self._get_sorting_algorithm()
		algorithm(to_sort)
		for i in range(1, n):
			self.assertTrue(to_sort[i] >= to_sort[i - 1], "Sorting algorithm failed to put everything in order")


class SelectionSortTest(unittest.TestCase, SortingTest):

	def _get_sorting_algorithm(self):
		return selection_sort


class InsertionSortTest(unittest.TestCase, SortingTest):

	def _get_sorting_algorithm(self):
		return insertion_sort


class ShellSortTest(unittest.TestCase, SortingTest):

	def _get_sorting_algorithm(self):
		return shell_sort


class MergeSortTest(unittest.TestCase, SortingTest):

	def _get_sorting_algorithm(self):
		return merge_sort
