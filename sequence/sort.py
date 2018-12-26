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
	length = len(arr)
	for i in range(1, length):
		insertion_point = i
		insertion_val = arr[i]
		for j in range(1, i + 1):
			if insertion_val < arr[i - j]:
				arr[i - j + 1] = arr[i - j]
				insertion_point = i - j
		arr[insertion_point] = insertion_val


class SortingTest:

	def test_sort(self):
		to_sort = []
		for i in range(100):
			to_sort.append(random.randint(0, 100))
		algorithm = self._get_sorting_algorithm()
		algorithm(to_sort)
		for i in range(1, 100):
			self.assertTrue(to_sort[i] >= to_sort[i - 1], "Sorting algorithm failed to put everything in order")


class SelectionSortTest(unittest.TestCase, SortingTest):

	def _get_sorting_algorithm(self):
		return selection_sort


class InsetionSortTest(unittest.TestCase, SortingTest):

	def _get_sorting_algorithm(self):
		return insertion_sort
