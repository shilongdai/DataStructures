import unittest


class Node:

	def __init__(self, value = None, after = None, prev = None):
		self.value = value
		self.after = after
		self.prev = prev

	def __eq__(self, other):
		try:
			if other is None:
				return False
			if self.value == other.value:
				return True
			if self.prev is None and other.prev is not None:
				return False
			prev_equal = self.prev == other.prev
			if self.after is None and other.after is not None:
				return False
			after_equal = self.after == other.after
			return prev_equal and after_equal
		except AttributeError:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)


class LinkedList:

	def __init__(self):
		self._start = None
		self._end = None
		self._size = 0
		self._cursor = None
		self._cursor_index = -1

	def append(self, value):
		if self._start is None:
			# if the list is empty, create the starting node
			self._start = Node(value)
			self._end = self._start
			self._cursor = self._start
			self._cursor_index = 0
		else:
			# otherwise, add a node to the end
			self._end.after = Node(value, prev = self._end)
			self._end = self._end.after
		self._size += 1

	def prepend(self, value):
		if self._start is None:
			# reuse append if list empty
			self.append(value)
		else:
			# add a new node before start node
			new_start = Node(value, after = self._start, prev = None)
			self._start.prev = new_start
			self._start = new_start
			self._size += 1
			self._cursor_index += 1

	def extend(self, other_list):
		# use the iteration protocol
		for i in other_list:
			self.append(i)

	def insert(self, i, value):
		i = self._normalize_boundaries(i)
		self._check_bound(i)
		if i == 0:
			self.prepend(value)
			return
		if i == self._size:
			self.append(value)
			return
		# insert a new node before the node of the given index
		self._shift_cursor(i)
		new_node = Node(value)
		self._merge_linked_list(self._cursor.prev, new_node)
		self._merge_linked_list(new_node, self._cursor)
		self._size += 1
		# update the cursor index to reflect the change
		self._cursor_index += 1

	def remove(self, value):
		if self._start is None:
			return
		current = self._start
		while current is not None:
			if current.value == value:
				if current is self._start:
					self.remove_first()
					return
				self._merge_linked_list(current.prev, current.after)
				self._size -= 1
				self._reset_cursor()
				return
			current = current.after

	def remove_first(self):
		if self._size == 0:
			return
		value = self._start.value
		self._start = self._start.after
		if self._start is not None:
			self._start.prev = None
		self._size -= 1
		self._reset_cursor()
		return value

	def clear(self):
		self.__init__()

	def index(self, value, start = None, end = None):
		# normalize boundaries
		if start is None:
			start = 0
		if end is None:
			end = self._size
		end = self._normalize_boundaries(end)
		start = self._normalize_boundaries(start)
		self._check_bound(end - 1)
		self._check_bound(start)
		if start > end:
			raise IndexError("The boundary provided does not create an interval with elements")
		i = start
		while i < end:
			self._shift_cursor(i)
			if self._cursor.value == value:
				return self._cursor_index
			i += 1
		return -1

	def count(self, value):
		count = 0
		current = self._start
		while current is not None:
			if current.value == value:
				count += 1
			current = current.after
		return count

	def copy(self):
		result = LinkedList()
		result.extend(self)
		return result

	def reverse(self):
		if self._start is None:
			return
		orig_end = self._end
		current = self._end.prev
		current_end = self._end
		while current is not self._start:
			next_current = current.prev
			self._merge_linked_list(current_end, current)
			current_end = current_end.after
			current = next_current
		self._merge_linked_list(current_end, current)
		self._start = orig_end
		self._end = current
		self._end.after = None
		self._start.prev = None
		self._reset_cursor()

	def __eq__(self, o: object) -> bool:
		for this_val, other_val in zip(self, o):
			if other_val is None:
				return False
			if this_val != other_val:
				return False
		return True

	def __ne__(self, o: object) -> bool:
		return not self.__eq__(o)

	def __len__(self):
		return self._size

	def __iter__(self):
		return self._generator_iter()

	def __repr__(self):
		result = "["
		for i in self:
			result = result + str(i) + ", "
		result = result[:-2]
		result += "]"
		return result

	def __setitem__(self, key, value):
		if type(key) != slice:
			index = self._normalize_boundaries(key)
			self._check_bound(key)
			self._shift_cursor(index)
			self._cursor.value = value
		else:
			start, end, step = self._normalize_slice(key)
			self._check_bound(start)
			self._check_bound(end - 1)
			if step == 1:
				delta = end - start
				self._shift_cursor(start)
				# insert added slice
				for i in value:
					self.insert(self._cursor_index, i)
				# remove previous slice
				start_cut = self._cursor
				self._shift_cursor(self._cursor_index + delta)
				self._merge_linked_list(start_cut.prev, self._cursor)
				self._size = self._size - delta + len(value)
				self._reset_cursor()
			else:
				if len(value) > (end - start) // step:
					raise IndexError("The replacement exceeds the slice to be replaced")
				self._shift_cursor(start)
				for i in value:
					self._cursor.value = i
					self._shift_cursor(self._cursor_index + step)

	def __getitem__(self, item):
		if type(item) != slice:
			item = self._normalize_boundaries(item)
			self._check_bound(item)
			self._shift_cursor(item)
			return self._cursor.value
		else:
			start, end, step = self._normalize_slice(item)
			self._check_bound(start)
			self._check_bound(end - 1)
			result = LinkedList()
			self._shift_cursor(start)
			while self._cursor_index < end:
				result.append(self._cursor.value)
				self._shift_cursor(self._cursor_index + step)
			return result

	def __delitem__(self, key):
		if type(key) != slice:
			key = self._normalize_boundaries(key)
			self._check_bound(key)
			if key == 0:
				self.remove_first()
			else:
				self._shift_cursor(key)
				self._merge_linked_list(self._cursor.prev, self._cursor.after)
				self._size -= 1
		else:
			start, end, step = self._normalize_slice(key)
			self._check_bound(start)
			self._check_bound(end - 1)
			self._shift_cursor(start)
			while self._cursor_index < end:
				self._merge_linked_list(self._cursor.prev, self._cursor.after)
				self._cursor = self._cursor.prev
				self._shift_cursor(self._cursor_index + step)
			self._reset_cursor()
			self._size -= (end - start) // step

	def _check_bound(self, index):
		if index >= self._size:
			raise IndexError("Index out of bound")

	def _reset_cursor(self):
		self._cursor_index = 0
		self._cursor = self._start

	def _generator_iter(self):
		current = self._start
		while current is not None:
			yield current.value
			current = current.after

	def _normalize_slice(self, slice_obj):
		start, end, step = slice_obj.start, slice_obj.stop, slice_obj.step
		if start is None:
			start = 0
		if end is None:
			end = self._size
		if step is None:
			step = 1
		start = self._normalize_boundaries(start)
		end = self._normalize_boundaries(end)
		return start, end, step

	def _normalize_boundaries(self, bound):
		if bound < 0:
			bound = self._size + bound
		return bound

	def _shift_cursor(self, position):
		if position == self._cursor_index:
			return
		if position > self._cursor_index:
			for i in range(position - self._cursor_index):
				self._cursor = self._cursor.after
		else:
			for i in range(self._cursor_index - position):
				self._cursor = self._cursor.prev
		self._cursor_index = position

	@staticmethod
	def _merge_linked_list(node_a, node_b):
		if node_b is None:
			node_a.after = None
			return
		if node_a is None:
			node_b.prev = None
			return
		node_a.after = node_b
		node_b.prev = node_a


class LinkedStack(LinkedList):

	def __init__(self):
		LinkedList.__init__(self)

	def push(self, value):
		self.prepend(value)

	def pop(self):
		return self.remove_first()

	def peek(self):
		if len(self) == 0:
			return None
		result = self._start.value
		return result


class LinkedQueue(LinkedList):

	def __init__(self):
		LinkedList.__init__(self)

	def enqueue(self, value):
		self.append(value)

	def dequeue(self):
		return self.remove_first()

	def peek(self):
		if len(self) == 0:
			return None
		return self._start.value


class TestLinkedList(unittest.TestCase):

	def test_append(self):
		linked_list = LinkedList()
		for i in range(1000):
			linked_list.append(i)
		self.assertEqual(1000, len(linked_list), "List has wrong size")
		working_list = [i for i in range(1000)]
		self.assertEqual(linked_list, working_list, "Linked List does not work against python list implementation")

	def test_prepend(self):
		linked_list = LinkedList()
		for i in range(1000):
			linked_list.prepend(i)
		self.assertEqual(1000, len(linked_list), "List has wrong size")
		working_list = [999 - i for i in range(1000)]
		self.assertEqual(linked_list, working_list, "Linked List does not match the expected list")

	def test_extension(self):
		linked_list = LinkedList()
		for i in range(500):
			linked_list.append(i)
		working_list = [i for i in range(500, 1000)]
		linked_list.extend(working_list)
		expected_list = [i for i in range(1000)]
		self.assertEqual(1000, len(linked_list), "Length should be 500 + 500")
		self.assertEqual(linked_list, expected_list, "Values does not match expectation")

	def test_iteration(self):
		linked_list = LinkedList()
		for i in range(1000):
			linked_list.append(i)
		working_list = [i for i in range(1000)]
		for a, b in zip(linked_list, working_list):
			self.assertEqual(a, b, "iterator does not return correct result")

	def test_indexing(self):
		linked_list = LinkedList()
		for i in range(1000):
			linked_list.append(i)
		for i in range(1000):
			self.assertEqual(linked_list[i], i, "index does not return correct result")

	def test_insert(self):
		linked_list = LinkedList()
		for i in range(10):
			linked_list.append(i)
		linked_list.insert(8, 1)
		self.assertEqual(11, len(linked_list), "insertion did not affect the size")
		self.assertEqual(1, linked_list[8], "insertion did not insert at right place")

	def test_remove_value(self):
		linked_list = LinkedList()
		for i in range(20):
			linked_list.append(i)
		for i in range(10):
			linked_list.append(i)
		linked_list.remove(5)
		self.assertEqual(29, len(linked_list), "linked list did not remove just one element")
		self.assertEqual(6, linked_list[5], "linked list did not remove the right element")

	def test_remove_first(self):
		linked_list = LinkedList()
		for i in range(20):
			linked_list.append(i)
		linked_list.remove_first()
		self.assertEqual(19, len(linked_list), "linked list did not change size properly")
		self.assertEqual(1, linked_list[0], "linked list did not remove the right element")

	def test_clear(self):
		linked_list = LinkedList()
		for i in range(100000):
			linked_list.append(i)
		linked_list.clear()
		self.assertEqual(0, len(linked_list), "linked list did not clear all elements")

	def test_get_index_of_value(self):
		linked_list = LinkedList()
		for i in range(100):
			linked_list.append(i)
		for i in range(20):
			linked_list.append(i)
		self.assertEqual(11, linked_list.index(11), "linked list did not get the index of first 11")
		self.assertEqual(111, linked_list.index(11, 100, -1), "linked list did not interpret slice")

	def test_count(self):
		linked_list = LinkedList()
		for i in range(100):
			linked_list.append(i)
		for i in range(50):
			linked_list.append(i)
		for i in range(10):
			linked_list.append(i)
		self.assertEqual(1, linked_list.count(99), "linked list failed to count")
		self.assertEqual(2, linked_list.count(49), "linked list failed to count")
		self.assertEqual(3, linked_list.count(9), "linked list failed to count")

	def test_copy(self):
		linked_list_a = LinkedList()
		for i in range(100):
			linked_list_a.append(i)
		linked_list_b = linked_list_a.copy()
		self.assertEqual(linked_list_a, linked_list_b, "copy did not return duplicate list")
		linked_list_a.remove(1)
		linked_list_a.remove(4)
		linked_list_a.remove(3)
		self.assertNotEqual(linked_list_a, linked_list_b, "copy did not even shallow copy")

	def test_reverse(self):
		linked_list = LinkedList()
		for i in range(10):
			linked_list.append(i)
		reverse_list = [9 - i for i in range(10)]
		linked_list.reverse()
		self.assertEqual(reverse_list, linked_list, "failed to reverse linked list")

	def test_index_set(self):
		linked_list = LinkedList()
		for i in range(100):
			linked_list.append(i)
		linked_list[10] = 10.5
		self.assertEqual(10.5, linked_list[10], "linked list did not set the value")
		self.assertEqual(100, len(linked_list), "insertion performed instead of modification")

	def test_index_splice_assignment(self):
		linked_list = LinkedList()
		for i in range(10):
			linked_list.append(i)
		to_insert = [1, 2, 3, 4, 5]
		linked_list[0:2] = to_insert
		expected_list = [1, 2, 3, 4, 5, 2, 3, 4, 5, 6, 7, 8, 9]
		self.assertEqual(expected_list, linked_list, "slice assignment without step did not perform as expected")
		linked_list[1:5:2] = ['a', 'b']
		expected_list[1] = 'a'
		expected_list[3] = 'b'
		self.assertEqual(expected_list, linked_list, "slice step assignment with step did not perform as expected")
		try:
			linked_list[1:5:2] = ['a', 'b', 'c']
			self.fail("Did not through index out of bound exception")
		except IndexError:
			pass

	def test_index_splice_getitem(self):
		linked_list = LinkedList()
		for i in range(10):
			linked_list.append(i)
		sub_list_1 = linked_list[1:4]
		expected_1 = [1, 2, 3]
		self.assertEqual(expected_1, sub_list_1, "did not get the right slice")
		sub_list_2 = linked_list[1:5:2]
		expected_2 = [1, 3]
		self.assertEqual(expected_2, sub_list_2, "did not get the right slice with the right step")

	def test_index_delete_index(self):
		linked_list = LinkedList()
		for i in range(10):
			linked_list.append(i)
		del linked_list[5]
		expected_list = [0, 1, 2, 3, 4, 6, 7, 8, 9]
		self.assertEqual(expected_list, linked_list, "did not delete the right index")

	def test_index_delete_slice(self):
		linked_list = LinkedList()
		for i in range(10):
			linked_list.append(i)
		del linked_list[2:4]
		expected_list = [0, 1, 4, 5, 6, 7, 8, 9]
		self.assertEqual(expected_list, linked_list, "did not delete the right slice")
		self.assertEqual(8, len(linked_list))
		del linked_list[1:-3:2]
		expected_list = [0, 4, 6, 7, 8, 9]
		self.assertEqual(6, len(linked_list))
		self.assertEqual(expected_list, linked_list)


class TestLinkedStack(unittest.TestCase):

	def test_stack_operations(self):
		stack = LinkedStack()
		for i in range(10):
			stack.push(i)
		current = 9
		while len(stack) != 0:
			self.assertEqual(current, stack.pop())
			current -= 1

	def test_stack_iterator(self):
		stack = LinkedStack()
		for i in range(10):
			stack.push(i)
		current = 9
		iterator = iter(stack)
		while True:
			try:
				self.assertEqual(current, next(iterator))
				current -= 1
			except StopIteration:
				break
		self.assertEqual(-1, current)


class TestLinkedQueue(unittest.TestCase):

	def test_queue_methods(self):
		linked_queue = LinkedQueue()
		for i in range(10):
			linked_queue.enqueue(i)
		current = 0
		while len(linked_queue) != 0:
			self.assertEqual(current, linked_queue.dequeue())
			current += 1
