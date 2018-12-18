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

	def add_node(self, id_num, data):
		node = Node(id_num, data)
		self._nodes[id_num] = node

	def find(self, id_num):
		if id_num > len(self._nodes):
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

	def __getitem__(self, item):
		return self._nodes[item]


class QuickUnion(UnionFind):

	def __init__(self):
		self._nodes = {}

	def add_node(self, id_num, data):
		node = ForestTreeNode(id_num, id_num, data)
		self._nodes[id_num] = node

	def find(self, id_num):
		return self._find_root(id_num).group_id

	def union(self, id_1, id_2):
		root_1 = self._find_root(id_1)
		root_2 = self._find_root(id_2)
		if root_1.group_id == root_2.group_id:
			return
		root_1.parent = root_2.group_id

	def _find_root(self, id_num):
		current = self._nodes[id_num]
		while current.group_id != self._nodes[current.parent].group_id:
			current = self._nodes[current.parent]
		return current


class BalancedQuickUnion(QuickUnion):

	def __init__(self):
		QuickUnion.__init__(self)
		self._counts = {}

	def add_node(self, id_num, data):
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


class UnionFindTest:

	def test_ungrouped_find(self):
		finder = self._get_union_find()
		for i in range(10000):
			finder.add_node(i, i)
		for i in range(10000):
			self.assertEqual(i, finder.find(i), "Failed to return the right group id")

	def test_union(self):
		finder = self._get_union_find()
		for i in range(10000):
			finder.add_node(i, i)
		finder.union(1, 3)
		finder.union(2, 4)
		finder.union(2, 3)
		finder.union(5, 8)
		self.assertTrue(finder.connected(1, 3))
		self.assertTrue(finder.connected(1, 2))
		self.assertFalse(finder.connected(1, 5))


class QuickFindTest(unittest.TestCase, UnionFindTest):

	def _get_union_find(self):
		return QuickFind()


class QuickUnionTest(unittest.TestCase, UnionFindTest):

	def _get_union_find(self):
		return QuickUnion()


class BalancedQuickUnionTest(unittest.TestCase, UnionFindTest):

	def _get_union_find(self):
		return BalancedQuickUnion()
