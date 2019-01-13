import unittest


def binary_search(indexable, key, comparator, start = 0, end = None):
	if end is None:
		end = len(indexable)
	boundary = end - start
	if boundary == 0:
		return -1, None
	middle_index = start + (boundary // 2)
	comparison = comparator(indexable[middle_index], key)
	if comparison == 0:
		return middle_index, indexable[middle_index]
	if comparison > 0:
		return binary_search(indexable, key, comparator, middle_index, end)
	else:
		return binary_search(indexable, key, comparator, 0, middle_index)


def first_occur_binary_search(indexable, key, comparator, start = 0, end = None):
	if end is None:
		end = len(indexable)
	boundary = end - start
	if boundary == 0:
		return -1, None
	middle_index = start + (boundary // 2)
	comparison = comparator(indexable[middle_index], key)
	if comparison == 0:
		any_before = first_occur_binary_search(indexable, key, comparator, 0, middle_index)
		if any_before[0] == -1:
			return middle_index, indexable[middle_index]
	if comparison > 0:
		return binary_search(indexable, key, comparator, middle_index, end)
	else:
		return binary_search(indexable, key, comparator, 0, middle_index)


class TestBinarySearch(unittest.TestCase):

	@staticmethod
	def numeric_comparator(a, b):
		if a > b:
			return -1
		if a < b:
			return 1
		return 0

	def test_basic_binary_search(self):
		search_list = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21)
		result = binary_search(search_list, 17, TestBinarySearch.numeric_comparator)
		self.assertEqual((8, 17), result, "Binary search not working as expected")

	def test_first_occur_binary_search(self):
		search_list = (1, 3, 5, 6, 7, 8, 9, 9, 9, 9, 9, 9, 9, 10, 44, 100)
		result = first_occur_binary_search(search_list, 9, TestBinarySearch.numeric_comparator)
		self.assertEqual((6, 9), result)
