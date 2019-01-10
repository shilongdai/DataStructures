import random
import unittest

from sequence.sort import exchange


class KeyNode:

	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __repr__(self):
		return repr(self.__dict__)


class BinaryHeap:

	def __init__(self, comparator):
		self._comparator = comparator
		self._queue = [None]

	def add(self, key, val):
		self._queue.append(KeyNode(key, val))
		self._rise_up(len(self._queue) - 1)

	def pop(self):
		result = self.peep()
		self._queue[1] = self._queue[len(self._queue) - 1]
		self._queue.pop()
		self._demote(1)
		return result

	def peep(self):
		if len(self._queue) > 1:
			return self._queue[1].value
		raise IndexError("Heap is empty")

	def __len__(self):
		return len(self._queue)

	def _rise_up(self, k):
		while k > 1 and self._less(self._queue[k // 2], self._queue[k]):
			exchange(self._queue, k, k // 2)
			k = k // 2

	def _demote(self, k):
		n = len(self._queue)
		while k * 2 < n:
			to_exchange = k * 2
			if to_exchange + 1 < n and self._less(self._queue[to_exchange], self._queue[to_exchange + 1]):
				to_exchange += 1
			if self._less(self._queue[k], self._queue[to_exchange]):
				exchange(self._queue, k, to_exchange)
			else:
				break
			k = to_exchange

	def _less(self, node_a, node_b):
		return self._comparator(node_a.key, node_b.key)


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
