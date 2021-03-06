import random
import string
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


class RedBlackNode(BSTNode):

	def __init__(self, key, value, left = None, right = None, color = False):
		BSTNode.__init__(self, key, value, left, right)
		self.color = color


class BaseSymbolTable:

	def pop(self, key, default=None):
		result = self.get(key, default)
		if result is None:
			raise KeyError(repr(key))
		del self[key]
		return result

	def popitem(self):
		if len(self) == 0:
			raise KeyError("the dictionary is empty")
		next_set = next(self.items())
		del self[next_set[0]]
		return next_set

	def setdefault(self, key, default):
		if key not in self:
			self[key] = default

	def update(self, collection, **dictionary):
		for k, v in collection:
			self[k] = v
		for k, v in dictionary.items():
			self[k] = v

	def __contains__(self, item):
		return self.get(item) is not None

	def __eq__(self, other):
		try:
			for k, v in self.items():
				if v != other[k]:
					return False
		except KeyError:
			return False
		return True

	def __ne__(self, other):
		return not self.__eq__(other)

	def __getitem__(self, item):
		result = self.get(item)
		if result is None:
			raise KeyError(repr(item))
		return result

	def __repr__(self):
		if len(self) == 0:
			return "{}"
		result = "{"
		for k, v in self.items():
			result += repr(k) + ": " + repr(v) + ", "
		result = result[:-2]
		result += "}"
		return result


class BinarySearchTree(BaseSymbolTable):

	def __init__(self):
		self._root = None
		self._size = 0
		self._use_pre = False

	def get(self, key, default=None):
		result = self._seek(key)
		if result is None:
			return default
		return result.value

	def values(self):
		return self._value_iterator()

	def keys(self):
		return self._key_iterator()

	def items(self):
		return self._both_iterator()

	def copy(self):
		new_root = self._copy_recursive(self._root)
		result = BinarySearchTree()
		result._root = new_root
		result._size = self._size
		result._use_pre = self._use_pre
		return result

	def clear(self):
		self._root = None
		self._size = 0

	def min(self):
		if self._root is None:
			raise ValueError("The tree is empty")
		root = self._root
		while root.left is not None:
			root = root.left
		return root.key, root.value

	def max(self):
		if self._root is None:
			raise ValueError("The tree is empty")
		root = self._root
		while root.right is not None:
			root = root.right
		return root.key, root.value

	def __delitem__(self, key):
		self._root = self._recursive_delete(self._root, key)

	def __iter__(self):
		return self._key_iterator()

	def __len__(self):
		return self._size

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

	def _seek(self, key):
		current = self._root
		while current is not None and current.key != key:
			if key < current.key:
				current = current.left
			else:
				current = current.right
		return current

	def _delete_max(self, root):
		while root.right.right is not None:
			root = root.right
		result = root.right
		root.right = result.left
		return result

	def _delete_min(self, root):
		while root.left.left is not None:
			root = root.left
		result = root.left
		root.left = result.right
		return result

	def _recursive_delete(self, root, key):
		if root is None:
			raise KeyError(repr(key))
		if root.key == key:
			self._size -= 1
			if root.left is None:
				return root.right
			if root.right is None:
				return root.left
			if self._use_pre:
				self._use_pre = False
				if root.left.right is None:
					result = root.left
				else:
					result = self._delete_max(root.left)
				result.right = root.right
				result.left = root.left
				return result
			else:
				self._use_pre = True
				if root.right.left is None:
					result = root.right
				else:
					result = self._delete_min(root.right)
				result.left = root.left
				result.right = root.right
				return self._delete_min(root.right)
		if key < root.key:
			root.left = self._recursive_delete(root.left, key)
		else:
			root.right = self._recursive_delete(root.right, key)
		return root

	def _node_generator(self, root):
		if root is None:
			return iter([])
		if root.left is not None:
			yield from self._node_generator(root.left)
		yield root
		if root.right is not None:
			yield from self._node_generator(root.right)

	def _key_iterator(self):
		node_gen = self._node_generator(self._root)
		for node in node_gen:
			yield node.key

	def _value_iterator(self):
		node_gen = self._node_generator(self._root)
		for node in node_gen:
			yield node.value

	def _both_iterator(self):
		node_gen = self._node_generator(self._root)
		for node in node_gen:
			yield node.key, node.value

	def _copy_recursive(self, root):
		if root is None:
			return None
		new_root = KeyNode(root.key, root.value)
		new_root.left = self._copy_recursive(root.left)
		new_root.right = self._copy_recursive(root.right)
		return new_root


class RedBlackTree(BinarySearchTree):

	def __init__(self):
		BinarySearchTree.__init__(self)

	def __setitem__(self, key, value):
		self._root = self._recursive_put(self._root, key, value)
		self._root.color = False

	def __delitem__(self, key):
		if self._root is None:
			return
		if not self._is_red(self._root.left) and not self._is_red(self._root.right):
			self._root.color = True
		self._root = self._delete_recursive(self._root, key)
		if self._root is not None:
			self._root.color = False

	def _recursive_put(self, root, key, value):
		if root is None:
			self._size += 1
			return RedBlackNode(key, value, color = True)
		if root.key == key:
			root.value = value
		else:
			if key < root.key:
				root.left = self._recursive_put(root.left, key, value)
			else:
				root.right = self._recursive_put(root.right, key, value)
		if self._is_red(root.right) and not self._is_red(root.left):
			root = self._rotate_left(root)
		if self._is_red(root.left) and self._is_red(root.left.left):
			root = self._rotate_right(root)
		if self._is_red(root.left) and self._is_red(root.right):
			self._flip_color(root)
		return root

	def _is_red(self, node):
		if node is None:
			return False
		return node.color

	def _rotate_left(self, root):
		new_root = root.right
		root.right = new_root.left
		new_root.left = root
		new_root.color = root.color
		root.color = True
		return new_root

	def _rotate_right(self, root):
		new_root = root.left
		root.left = new_root.right
		new_root.right = root
		new_root.color = root.color
		root.color = True
		return new_root

	def _flip_color(self, root):
		root.left.color = not root.left.color
		root.right.color = not root.right.color
		root.color = not root.color

	def _move_red_left(self, node):
		self._flip_color(node)
		if self._is_red(node.right.left):
			node.right = self._rotate_right(node.right)
			node = self._rotate_left(node)
			self._flip_color(node)
		return node

	def _balance(self, node):
		if self._is_red(node.right):
			node = self._rotate_left(node)
		if self._is_red(node.left) and self._is_red(node.left.left):
			node = self._rotate_right(node)
		if self._is_red(node.left) and self._is_red(node.right):
			self._flip_color(node)
		return node

	def _delete_min_recursive(self, node):
		if node.left is None:
			return None
		if not self._is_red(node.left) and not self._is_red(node.left.left):
			node = self._move_red_left(node)
		node.left = self._delete_min_recursive(node.left)
		return self._balance(node)

	def _min(self, root):
		while root.left is not None:
			root = root.left
		return root

	def _move_red_right(self, node):
		self._flip_color(node)
		if self._is_red(node.left.left):
			node = self._rotate_right(node)
			self._flip_color(node)
		return node

	def _delete_recursive(self, node, key):
		if key < node.key:
			if not self._is_red(node.left) and not self._is_red(node.left.left):
				node = self._move_red_left(node)
			node.left = self._delete_recursive(node.left, key)
		else:
			if self._is_red(node.left):
				node = self._rotate_right(node)
			if key == node.key and node.right is None:
				self._size -= 1
				return None
			if not self._is_red(node.right) and not self._is_red(node.right.left):
				node = self._move_red_right(node)
			if key == node.key:
				self._size -= 1
				min_node = self._min(node.right)
				node.key = min_node.key
				node.value = min_node.value
				node.right = self._delete_min_recursive(node.right)
			else:
				node.right = self._delete_recursive(node.right, key)
		return self._balance(node)


class SeparateChainingHashTable(BaseSymbolTable):

	def __init__(self, table_size=17):
		self._table = [[]]
		self._size = 0
		self._table_size = table_size
		self._resize(table_size)
		self._initial_table_size = table_size

	def get(self, key, default=None):
		index = self._hash(key)
		chain = self._table[index]
		probed_index = self._sequential_search(key, chain)
		if probed_index == -1:
			return default
		return chain[probed_index][1]

	def values(self):
		for k, v in self.items():
			yield v

	def keys(self):
		for k, v in self.items():
			yield k

	def items(self):
		for st in self._table:
			for k, v in st:
				yield k, v

	def copy(self):
		new_table = []
		for i in range(self._table_size):
			new_table.append([])
		for i in range(self._table_size):
			for item in self._table[i]:
				new_table[i].append(item)
		result = SeparateChainingHashTable()
		result._table = new_table
		result._table_size = self._table_size
		result._initial_table_size = self._initial_table_size
		result._size = self._size
		return result

	def clear(self):
		self._table = []
		for i in range(self._initial_table_size):
			self._table.append([])
		self._size = 0
		self._table_size = self._initial_table_size

	def __delitem__(self, key):
		index = self._hash(key)
		chain = self._table[index]
		probed_index = self._sequential_search(key, chain)
		if probed_index == -1:
			raise KeyError(probed_index)
		del chain[probed_index]
		self._size -= 1
		if self._size <= 2 * self._table_size:
			new_size = self._table_size // 2
			if new_size >= self._initial_table_size:
				self._resize(self._table_size // 2)

	def __iter__(self):
		return self.keys()

	def __len__(self):
		return self._size

	def __setitem__(self, key, value):
		index = self._hash(key)
		chain = self._table[index]
		probed_index = self._sequential_search(key, chain)
		if probed_index == -1:
			chain.append((key, value))
			self._size += 1
		else:
			chain[probed_index] = key, value
		if self._size >= 8 * self._table_size:
			self._resize(2 * self._table_size)

	def _resize(self, m):
		old_table = self._table
		self._table = []
		for i in range(m):
			self._table.append([])
		self._table_size = m
		self._size = 0
		for st in old_table:
			for k, v in st:
				self[k] = v

	def _hash(self, k):
		hash_val = abs(hash(k))
		hash_val = hash_val % self._table_size
		return hash_val

	def _sequential_search(self, k, st):
		for i in range(len(st)):
			if st[i][0] == k:
				return i
		return -1


class OpenAddressHashTable(BaseSymbolTable):

	def __init__(self, table_size=17):
		self._table = []
		self._size = 0
		self._table_size = table_size
		self._resize(table_size)
		self._initial_table_size = table_size

	def get(self, key, default=None):
		index = self._hash(key)
		probed_index = self._linear_probe(key, index)
		if not probed_index[1]:
			return default
		return self._table[probed_index[0]][1]

	def values(self):
		for k, v in self.items():
			yield v

	def keys(self):
		for k, v in self.items():
			yield k

	def items(self):
		for item in self._table:
			if item is not None:
				yield item

	def copy(self):
		new_table = []
		for i in range(self._size):
			new_table.append(self._table[i])
		result = OpenAddressHashTable()
		result._table = new_table
		result._table_size = self._table_size
		result._initial_table_size = self._initial_table_size
		result._size = self._size
		return result

	def clear(self):
		self._table.clear()
		for i in range(self._initial_table_size):
			self._table.append(None)
		self._size = 0
		self._table_size = self._initial_table_size

	def __delitem__(self, key):
		index = self._hash(key)
		probed_index = self._linear_probe(key, index)
		if not probed_index[1]:
			raise KeyError(key)
		self._table[probed_index[0]] = None
		self._size -= 1
		index = probed_index[0]
		index = (index + 1) % self._table_size
		while self._table[index] is not None:
			k, v = self._table[index]
			self._table[index] = None
			self._size -= 1
			self[k] = v
			index = (index + 1) % self._table_size
		if self._table_size // 8 >= self._size:
			new_size = self._table_size // 2
			if new_size >= self._initial_table_size:
				self._resize(self._table_size // 2)

	def __iter__(self):
		return self.keys()

	def __len__(self):
		return self._size

	def __setitem__(self, key, value):
		index = self._hash(key)
		probed_index = self._linear_probe(key, index)
		if not probed_index[1]:
			self._table[probed_index[0]] = (key, value)
			self._size += 1
		else:
			self._table[probed_index[0]] = key, value
		if self._size * 2 >= self._table_size:
			self._resize(2 * self._table_size)

	def _resize(self, m):
		old_table = self._table
		self._table = []
		for i in range(m):
			self._table.append(None)
		self._table_size = m
		self._size = 0
		for k, v in old_table:
			if k is not None:
				self[k] = v

	def _hash(self, k):
		hash_val = abs(hash(k))
		hash_val = hash_val % self._table_size
		return hash_val

	def _linear_probe(self, k, start_index):
		i = start_index
		while i < self._table_size:
			if self._table[i] is None:
				return i, False
			if self._table[i][0] == k:
				return i, True
			i = (i + 1) % self._table_size


class TrieNode:

	def __init__(self, val, size):
		self.val = val
		self.next = [None for i in range(size)]


class Trie(BaseSymbolTable):

	def __init__(self, alphabet):
		self._alphabet = {}
		self._reverse_alphabet = {}
		for i, v in enumerate(alphabet):
			self._alphabet[v] = i
			self._reverse_alphabet[i] = v
		self._root = TrieNode(None, len(self._alphabet))
		self._count = 0

	def get(self, key, default=None):
		node = self._recursive_get(self._root, key, 0)
		val = node.val
		if val is None:
			val = default
		return val

	def values(self):
		for k, v in self.items():
			yield v

	def keys(self):
		for k, v in self.items():
			yield k

	def items(self):
		yield from self._traversal_generator(self._root, "")

	def copy(self):
		result = Trie(self._reverse_alphabet.keys())
		for k, v in self.items():
			result[k] = v
		return result

	def clear(self):
		self._root = TrieNode(None, len(self._alphabet))
		self._count = 0

	def with_prefix(self, prefix):
		yield from self._traversal_generator(self._root, prefix)

	def __delitem__(self, key):
		self._recursive_delete(self._root, key, 0)

	def __iter__(self):
		return self.keys()

	def __len__(self):
		return self._count

	def __setitem__(self, key, value):
		self._root = self._recursive_put(self._root, key, 0, value)

	def _recursive_get(self, node, key, index):
		if node is None:
			return None
		if index == len(key):
			return node
		node = node.next[self._alphabet[key[index]]]
		return self._recursive_get(node, key, index + 1)

	def _recursive_put(self, node, key, index, val):
		if node is None:
			node = TrieNode(None, len(self._alphabet))
		if index == len(key):
			if node.val is None:
				self._count += 1
			node.val = val
			return node
		next_node = node.next[self._alphabet[key[index]]]
		next_node = self._recursive_put(next_node, key, index + 1, val)
		node.next[self._alphabet[key[index]]] = next_node
		return node

	def _traversal_generator(self, root, prefix):
		if root is None:
			return iter([])
		if root.val is not None:
			yield prefix, root.val
		for i, n in enumerate(root.next):
			yield from self._traversal_generator(n, prefix + self._reverse_alphabet[i])

	def _recursive_delete(self, root, key, current):
		if root is None:
			return None
		if current == len(key):
			if root.val is not None:
				self._count -= 1
			root.val = None
		else:
			next_char = key[current]
			index = self._alphabet[next_char]
			self._recursive_delete(root.next[index], key, current + 1)
		if root.val is not None:
			return root
		for i in root.next:
			if i is not None:
				return root
		return None


class DictionaryTest:

	def test_frequency(self):
		n = 10000
		random_set = random_array(n, 0, 100)
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
		set_from_rand = set(random_set)
		self.assertEqual(len(set_from_rand), len(dict_to_test))
		for i in set_from_rand:
			self.assertEqual(working_dict[i], dict_to_test[i])
		for k in dict_to_test.keys():
			self.assertEqual(working_dict[k], dict_to_test[k])
		for k, v in dict_to_test.items():
			self.assertEqual(working_dict[k], dict_to_test[k])
		for i in set(random_set):
			self.assertEqual(working_dict.pop(i), dict_to_test.pop(i))
		self.assertEqual(0, len(dict_to_test))


class BSTTest(DictionaryTest, unittest.TestCase):

	def get_dictionary(self):
		return BinarySearchTree()


class RBTreeTest(DictionaryTest, unittest.TestCase):

	def get_dictionary(self):
		return RedBlackTree()


class SeparateChainingHashTableTest(DictionaryTest, unittest.TestCase):

	def get_dictionary(self):
		return SeparateChainingHashTable(997)


class OpenAddressHashTableTest(DictionaryTest, unittest.TestCase):

	def get_dictionary(self):
		return OpenAddressHashTable(997)


class StdDictTest(unittest.TestCase, DictionaryTest):

	def get_dictionary(self):
		return dict()


class RegularTrieTest(unittest.TestCase):

	def test_trie_symbol_table(self):
		n = 100
		charset = string.ascii_letters
		strings = set()
		for i in range(n):
			s = []
			for j in range(random.randint(0, 16)):
				s.append(charset[random.randint(0, len(charset) - 1)])
			strings.add("".join(s))
		trie = Trie(charset)
		for i in strings:
			trie[i] = 1
		for i in strings:
			self.assertTrue(i in trie)
		self.assertEqual(len(strings), len(trie))
		copy = set(strings)
		for i in copy:
			strings.remove(i)
			trie.pop(i)
			for i in strings:
				self.assertTrue(i in trie)
			for i in trie:
				self.assertTrue(i in strings)
		self.assertEqual(0, len(trie))
