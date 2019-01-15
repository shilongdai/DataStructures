import random
import unittest

from algorithms.sort import random_array


class KeyNode:

	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __repr__(self):
		return repr(self.__dict__)


class BSTNode(KeyNode):

	def __init__(self, key, value, left=None, right=None):
		KeyNode.__init__(self, key, value)
		self.right = right
		self.left = left


class BinaryHeap:

	def __init__(self, comparator):
		self._comparator = comparator
		self._queue = []

	def add(self, key, val):
		self._queue.append(KeyNode(key, val))
		self._rise_up(len(self._queue) - 1)

	def pop(self):
		result = self.peep()
		self._queue[0] = self._queue[len(self._queue) - 1]
		self._queue.pop()
		self._demote(0)
		return result

	def peep(self):
		if len(self._queue) > 0:
			return self._queue[0].value
		raise IndexError("Heap is empty")

	def __len__(self):
		return len(self._queue)

	def _rise_up(self, k):
		temp = self._queue[k]
		while k > 0 and self._less(self._queue[(k - 1) // 2], temp):
			self._queue[k] = self._queue[(k - 1) // 2]
			k = (k - 1) // 2
		self._queue[k] = temp

	def _demote(self, k):
		n = len(self._queue)
		if n == 0:
			return
		temp = self._queue[k]
		while k * 2 + 1 < n:
			to_exchange = k * 2 + 1
			if to_exchange + 1 < n and self._less(self._queue[to_exchange], self._queue[to_exchange + 1]):
				to_exchange += 1
			if self._less(temp, self._queue[to_exchange]):
				self._queue[k] = self._queue[to_exchange]
			else:
				break
			k = to_exchange
		self._queue[k] = temp

	def _less(self, node_a, node_b):
		return self._comparator(node_a.key, node_b.key)

	def _exchange(self, node_a, node_b):
		temp = self._queue[node_a]
		self._queue[node_a] = self._queue[node_b]
		self._queue[node_b] = temp


class BinarySearchTree:

	def __init__(self):
		self._root = None
		self._size = 0
		self._use_pre = False

	def get(self, key, default=None):
		result = self._seek(key)
		if result is None:
			return default
		return result.value

	def pop(self, key, default=None):
		pass

	def popitem(self):
		pass

	def setdefault(self, key, default=None):
		pass

	def update(self, collection, **dictionary):
		pass

	def values(self):
		pass

	def keys(self):
		pass

	def items(self):
		pass

	def copy(self):
		pass

	def clear(self):
		pass

	def __contains__(self, item):
		return self.get(item) is None

	def __delitem__(self, key):
		self._recursive_delete(self._root, key)

	def __eq__(self, other):
		pass

	def __ne__(self, other):
		pass

	def __getitem__(self, item):
		result = self.get(item)
		if result is None:
			raise KeyError(repr(item))
		return result

	def __iter__(self):
		pass

	def __len__(self):
		pass

	def __setitem__(self, key, value):
		if self._root is None:
			self._root = BSTNode(key, value)
			self._size += 1
		current = self._root
		while True:
			if key == current.key:
				current.value = value
				return
			if key < current.key:
				if current.left is None:
					current.left = BSTNode(key, value)
					self._size += 1
					return
				else:
					current = current.left
			else:
				if current.right is None:
					current.right = BSTNode(key, value)
					self._size += 1
					return
				else:
					current = current.right

	def __repr__(self):
		pass

	def _seek(self, key):
		current = self._root
		while current is not None and current.key != key:
			if key < current.key:
				current = current.left
			else:
				current = current.right
		return current

	def _delete_min(self, root):
		parent = None
		while root.left is not None:
			parent = root
			root = root.left
		parent.left = root.right
		return root

	def _delete_max(self, root):
		parent = None
		while root.right is not None:
			parent = root
			root = root.right
		parent.right = root.left
		return root

	def _recursive_delete(self, root, key):
		if root is None:
			raise KeyError(repr(key))
		if root.key == key:
			if root.left is None:
				return root.right
			if root.right is None:
				return root.left
			if self._use_pre:
				return self._delete_max(root.left)



class HeapTest(unittest.TestCase):

	def test_order(self):
		random_data = []
		heap = BinaryHeap(int.__lt__)
		random.seed(10000)
		for i in range(10000):
			random_data.append(random.randint(0, 1000))
		for i in random_data:
			heap.add(i, i)
		random_data.sort(reverse = True)
		for i in random_data:
			self.assertEqual(i, heap.pop())


class DictionaryTest:

	def test_frequency(self):
		n = 10000
		random_set = random_array(n, 0, 10)
		dict_to_test = self.get_dictionary()
		working_dict = {}
		for i in random_set:
			if i in dict_to_test:
				dict_to_test[i] = dict_to_test[i] + 1
			else:
				dict_to_test[i] = 1
			if i in working_dict:
				working_dict[i] = working_dict[i] + 1
			else:
				working_dict[i] = 1
		for i in random_set:
			self.assertEqual(working_dict[i], dict_to_test[i])
			self.assertEqual(working_dict.pop(i), dict_to_test.pop(i))


class BSTTest(DictionaryTest, unittest.TestCase):

	def get_dictionary(self):
		return BinarySearchTree()
