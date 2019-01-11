import functools
import random
import timeit
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


# TODO: implement k-way and linked list merge sort
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
	while segment_size < length:
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
	if input_array is not original:
		for i in range(length):
			original[i] = input_array[i]


# TODO: apply performance tricks to smaller sized chunks
def natural_merge_sort(array):
	length = len(array)
	aux = [None for i in range(length)]
	while True:
		start = 0
		mid = 1
		merge_count = 0
		while start < length:
			while mid < length:
				if array[mid] < array[mid - 1]:
					break
				mid += 1
			if mid == length:
				break
			end = mid + 1
			while end < length:
				if array[end] < array[end - 1]:
					break
				end += 1
			if end - start < 16:
				_range_insertion_sort(array, start, end)
			else:
				for i in range(start, end):
					aux[i] = array[i]
				_merge(array, aux, start, mid, end)
			merge_count += 1
			start = end
			mid = start + 1
		if merge_count == 0:
			break


def _partition(array, low, high):
	lt = low + 1
	gt = high - 1
	spliter = array[low]
	adv_lt = False
	adv_gt = False
	while True:
		while array[lt] <= spliter:
			if array[lt] == spliter:
				adv_lt = True
				break
			lt += 1
			if lt >= high:
				break
		while array[gt] >= spliter:
			if array[gt] == spliter:
				adv_gt = True
				break
			gt -= 1
			if gt <= low:
				break
		if lt >= gt:
			break
		exchange(array, lt, gt)
		if adv_gt:
			gt -= 1
			adv_gt = False
		if adv_lt:
			lt += 1
			adv_lt = False
	exchange(array, low, gt)
	return gt


def _sampling_partition(array, low, high, sample_size):
	sample = []
	for i in range(sample_size):
		sample.append((i, array[i]))
	for i in range(1, sample_size):
		insertion_point = i
		insertion_val = sample[i]
		while insertion_point > low and sample[insertion_point - 1][1] > insertion_val[1]:
			sample[insertion_point] = sample[insertion_point - 1]
			insertion_point -= 1
		sample[insertion_point] = insertion_val
	median = sample[sample_size // 2 + 1]
	exchange(array, 0, median[0])
	return _partition(array, low, high)


def _three_way_partitioning(array, low, high):
	v = array[low]
	p = low + 1
	q = high - 1
	i = low + 1
	j = high - 1
	while True:
		if i < high and array[i] == v:
			exchange(array, p, i)
			p += 1
			i += 1
		if q >= low and array[j] == v:
			exchange(array, q, j)
			q -= 1
			j -= 1
		while array[i] < v:
			i += 1
			if i == high:
				break
		while array[j] > v:
			j -= 1
		if i == j and array[i] == v:
			exchange(array, i, p)
			p += 1
		if i >= j:
			break
		exchange(array, i, j)
	p -= 1
	while p >= low:
		exchange(array, j, p)
		j -= 1
		p -= 1
	q += 1
	while q < high:
		exchange(array, i, q)
		i += 1
		q += 1
	return j, i


def _quick_sort_recursive(array, low, high):
	if high - low < 16:
		_range_insertion_sort(array, low, high)
		return
	middle = _partition(array, low, high)
	_quick_sort_recursive(array, low, middle)
	_quick_sort_recursive(array, middle + 1, high)


def _quick_sort_sampling_recursive(array, low, high, sample_size):
	if high - low < 16:
		_range_insertion_sort(array, low, high)
		return
	middle = _sampling_partition(array, low, high, sample_size)
	_quick_sort_sampling_recursive(array, low, middle, sample_size)
	_quick_sort_sampling_recursive(array, middle + 1, high, sample_size)


def _quick_sort_threeway_recursive(array, low, high):
	if high - low < 16:
		_range_insertion_sort(array, low, high)
		return
	j, i = _three_way_partitioning(array, low, high)
	_quick_sort_threeway_recursive(array, low, j + 1)
	_quick_sort_threeway_recursive(array, i, high)


def quick_sort(array):
	random.shuffle(array)
	_quick_sort_recursive(array, 0, len(array))


def iterative_quick_sort(array):
	random.shuffle(array)
	to_do_stack = []
	to_do_stack.append((0, len(array)))
	while len(to_do_stack) != 0:
		segment = to_do_stack.pop()
		segment_length = segment[1] - segment[0]
		if segment_length < 15:
			_range_insertion_sort(array, segment[0], segment[1])
			continue
		middle = _partition(array, segment[0], segment[1])
		length_a = middle - segment[0]
		length_b = segment[1] - middle - 1
		if length_a >= length_b:
			to_do_stack.append((segment[0], middle))
			to_do_stack.append((middle + 1, segment[1]))
		else:
			to_do_stack.append((segment[0], middle))
			to_do_stack.append((middle + 1, segment[1]))


def sampling_quick_sort(array, sample_size = 3):
	random.shuffle(array)
	_quick_sort_sampling_recursive(array, 0, len(array), sample_size)


def threeway_quick_sort(array):
	random.shuffle(array)
	_quick_sort_threeway_recursive(array, 0, len(array))


def _demote(array, k, n):
	while k * 2 < n:
		to_exchange = k * 2
		if to_exchange + 1 < n and array[to_exchange] < array[to_exchange + 1]:
			to_exchange += 1
		if array[k] < array[to_exchange]:
			exchange(array, k, to_exchange)
		else:
			break
		k = to_exchange


def heap_sort(array):
	array.insert(0, None)
	n = len(array)
	i = n // 2
	while i > 0:
		_demote(array, i, n)
		i -= 1
	while n > 1:
		exchange(array, 1, n - 1)
		n -= 1
		_demote(array, 1, n)
	del array[0]


def doubling_test(alg1, start_size = 16, sample_size = 5):
	to_sort = []
	for i in range(start_size):
		to_sort.append(random.randint(0, start_size))
	prev_time = 0
	avg = 0
	while True:
		time_sum = 0
		for i in range(sample_size):
			timer = timeit.Timer(functools.partial(alg1, to_sort))
			time_sum += timer.timeit(1)
		avg = time_sum / sample_size
		compare_to_prev = 0
		if prev_time != 0:
			compare_to_prev = avg / prev_time
		print("Current Size: {}, Sample Size: {}, Avg Time: {}, {} divided by previous".format(start_size, sample_size,
		                                                                                       avg, compare_to_prev))
		prev_time = avg
		start_size *= 2
		to_sort.clear()
		for i in range(start_size):
			to_sort.append(random.randint(0, start_size))


class SortingTest:

	def test_sort(self):
		n = 10000
		random.seed(n)
		to_sort = []
		for i in range(n):
			to_sort.append(random.randint(0, 5))
		algorithm = self.get_sorter()
		algorithm(to_sort)
		for i in range(1, n):
			self.assertTrue(to_sort[i] >= to_sort[i - 1], "Sorting algorithm failed to put everything in order")


class SelectionSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return selection_sort


class InsertionSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return insertion_sort


class ShellSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return shell_sort


class MergeSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return merge_sort


class NaturalMergeSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return natural_merge_sort


class QuickSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return quick_sort


class IterativeQuickSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return iterative_quick_sort


class SamplingQuickSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return sampling_quick_sort


class ThreewayQuickSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return threeway_quick_sort


class HeapSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return heap_sort


class SystemSortTest(unittest.TestCase, SortingTest):

	def get_sorter(self):
		return list.sort


if __name__ == "__main__":
	doubling_test(threeway_quick_sort, sample_size = 1)
