import random
import unittest


class KeyNode:

	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __repr__(self):
		return repr(self.__dict__)


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
		while k > 0 and self._less((k - 1) // 2, k):
			self._exchange(k, (k - 1) // 2)
			k = (k - 1) // 2

	def _demote(self, k):
		n = len(self._queue)
		while k * 2 + 1 < n:
			to_exchange = k * 2 + 1
			if to_exchange + 1 < n and self._less(to_exchange, to_exchange + 1):
				to_exchange += 1
			if self._less(k, to_exchange):
				self._exchange(k, to_exchange)
			else:
				break
			k = to_exchange

	def _less(self, node_a, node_b):
		return self._comparator(self._queue[node_a].key, self._queue[node_b].key)

	def _exchange(self, node_a, node_b):
		temp = self._queue[node_a]
		self._queue[node_a] = self._queue[node_b]
		self._queue[node_b] = temp


class HeapTest(unittest.TestCase):

	def test_order(self):
		random_data = []
		heap = BinaryHeap(int.__lt__)
		for i in range(10000):
			random_data.append(random.randint(0, 1000))
		for i in random_data:
			heap.add(i, i)
		random_data.sort(reverse = True)
		for i in random_data:
			self.assertEqual(i, heap.pop())
