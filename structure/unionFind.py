import random
import unittest


class Node:

	def __init__(self, group_id, data):
		self.group_id = group_id
		self.data = data


class ForestTreeNode(Node):

	def __init__(self, parent, group_id, data):
		Node.__init__(self, group_id, data)
		self.parent = parent


class UnionFind:

	def connected(self, id_1, id_2):
		return self.find(id_1) == self.find(id_2)


class QuickFind(UnionFind):

	def __init__(self):
		self._nodes = {}
		self._group_count = 0

	def add_node(self, id_num, data):
		node = Node(id_num, data)
		if id_num not in self._nodes:
			self._nodes[id_num] = node
			self._group_count += 1

	def find(self, id_num):
		if id_num not in self._nodes:
			raise IndexError("The id " + id_num + " does not exists")
		return self._nodes[id_num].group_id

	def union(self, id_1, id_2):
		node_1 = self.find(id_1)
		node_2 = self.find(id_2)
		if node_1 == node_2:
			return
		for key, node in self._nodes.items():
			if node.group_id == node_1:
				node.group_id = node_2
		self._group_count -= 1

	def group_count(self):
		return self._group_count

	def __contains__(self, item):
		return item in self._nodes


class QuickUnion(UnionFind):

	def __init__(self):
		self._nodes = {}
		self._group_count = 0

	def add_node(self, id_num, data):
		if id_num not in self:
			node = ForestTreeNode(id_num, id_num, data)
			self._nodes[id_num] = node
			self._group_count += 1

	def find(self, id_num):
		return self._find_root(id_num).group_id

	def union(self, id_1, id_2):
		root_1 = self._find_root(id_1)
		root_2 = self._find_root(id_2)
		if root_1.group_id == root_2.group_id:
			return
		root_1.parent = root_2.group_id
		self._group_count -= 1

	def group_count(self):
		return self._group_count

	def _find_root(self, id_num):
		current = self._nodes[id_num]
		while current.group_id != self._nodes[current.parent].group_id:
			current = self._nodes[current.parent]
		return current

	def __contains__(self, item):
		return item in self._nodes


class BalancedQuickUnion(QuickUnion):

	def __init__(self):
		QuickUnion.__init__(self)
		self._counts = {}

	def add_node(self, id_num, data):
		if id_num not in self:
			QuickUnion.add_node(self, id_num, data)
			self._counts[id_num] = 1

	def union(self, id_1, id_2):
		root_1 = self._find_root(id_1)
		root_2 = self._find_root(id_2)
		if root_1.group_id == root_2.group_id:
			return
		root_1_size = self._counts[root_1.group_id]
		root_2_size = self._counts[root_2.group_id]
		if root_1_size >= root_2_size:
			root_2.parent = root_1.group_id
			self._counts[root_1.group_id] += root_2_size
		else:
			root_1.parent = root_2.group_id
			self._counts[root_2.group_id] += root_1_size
		self._group_count -= 1


def _compressed_find_root(self, id_num):
	current = self._nodes[id_num]
	to_link = []
	while current.group_id != self._nodes[current.parent].group_id:
		to_link.append(current)
		current = self._nodes[current.parent]
	for node in to_link:
		node.parent = current.group_id
	return current


class PathCompressedQuickUnion(QuickUnion):

	def __init__(self):
		QuickUnion.__init__(self)

	_find_root = _compressed_find_root


class PathCompressedBalancedQuickUnion(BalancedQuickUnion):

	def __init__(self):
		BalancedQuickUnion.__init__(self)

	_find_root = _compressed_find_root


class UnionFindTest:

	def test_erdos_renyi(self):
		finder = self._get_union_find()
		n = 1000
		for i in range(n):
			finder.add_node(i, i)
		random.seed(n)
		while finder.group_count() != 1:
			id_1 = random.randint(0, n - 1)
			id_2 = random.randint(0, n - 1)
			if not finder.connected(id_1, id_2):
				finder.union(id_1, id_2)
		for i in range(n):
			self.assertTrue(finder.connected(0, i))


class QuickFindTest(unittest.TestCase, UnionFindTest):

	def _get_union_find(self):
		return QuickFind()


class QuickUnionTest(unittest.TestCase, UnionFindTest):

	def _get_union_find(self):
		return QuickUnion()


class BalancedQuickUnionTest(unittest.TestCase, UnionFindTest):

	def _get_union_find(self):
		return BalancedQuickUnion()


class PathCompressedQuickUnionTest(unittest.TestCase, UnionFindTest):

	def _get_union_find(self):
		return PathCompressedQuickUnion()


class PathCompressedBalancedQuickUnionTest(unittest.TestCase, UnionFindTest):

	def _get_union_find(self):
		return PathCompressedBalancedQuickUnion()
