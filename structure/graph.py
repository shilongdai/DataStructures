import unittest


class Graph:

	def __init__(self):
		self._adjacency_lists = dict()
		self._vertices = dict()
		self._edge_count = 0

	def adjacent(self, vertex_name):
		if vertex_name not in self._adjacency_lists:
			raise KeyError(str(vertex_name) + " not in graph")
		for vertex in self._adjacency_lists[vertex_name]:
			yield vertex, self._vertices[vertex]

	def put_vertex(self, vertex_name, vertex):
		if vertex_name not in self._adjacency_lists:
			self._adjacency_lists[vertex_name] = []
		self._vertices[vertex_name] = vertex

	def add_edge(self, vertex_a, vertex_b):
		if vertex_a not in self._adjacency_lists or vertex_b not in self._adjacency_lists:
			raise KeyError("vertex not added to the graph")
		self._adjacency_lists[vertex_a].append(vertex_b)
		self._adjacency_lists[vertex_b].append(vertex_a)
		self._edge_count += 1

	def vertex_count(self):
		return len(self._vertices)

	def edge_count(self):
		return self._edge_count

	def degree(self, vertex_name):
		if vertex_name not in self._adjacency_lists:
			raise KeyError(str(vertex_name) + " not in graph")
		return len(self._adjacency_lists[vertex_name])

	def max_degree(self):
		max_count = 0
		for vertex in self._adjacency_lists:
			if self.degree(vertex) > max_count:
				max_count = self.degree(vertex)
		return max_count

	def avg_degree(self):
		return 2 * self.edge_count() / self.vertex_count()

	def self_loop_count(self):
		count = 0
		for vertex_name in self._adjacency_lists:
			for adj_name, adj_vertex in self.adjacent(vertex_name):
				if adj_name == vertex_name:
					count += 1
		# each edge counted twice because it is added twice to the adjacency list
		return count / 2

	def apply(self, operation):
		operation.do(self)

	def vertices(self):
		for k, v in self._vertices.items():
			yield k, v


class DepthFirstSearch:

	def __init__(self, vertex_name):
		self.vertex_name = vertex_name
		self._marked = dict()

	def do(self, graph):
		self._recursive_search(graph, self.vertex_name)

	def count(self):
		return len(self._marked)

	def marked(self, vertex_name):
		return self._marked.get(vertex_name, False)

	def _recursive_search(self, graph, vertex_name):
		self._marked[vertex_name] = True
		for name, vertex in graph.adjacent(vertex_name):
			if not self._marked.get(name, False):
				self._recursive_search(graph, name)


class PathSearch:

	def has_path(self, other_vertex):
		return other_vertex in self._get_path_tree()

	def path_to(self, other_vertex):
		if other_vertex not in self._get_path_tree():
			raise KeyError(str(other_vertex) + " not connected")
		path = []
		next_vertex = self._get_path_tree()[other_vertex]
		while True:
			path.append(next_vertex)
			prev = next_vertex
			next_vertex = self._get_path_tree()[next_vertex]
			if prev == next_vertex:
				break
		path.reverse()
		path.append(other_vertex)
		return path

	def connected(self):
		for k in self._get_path_tree():
			yield k


class DepthFirstPaths(PathSearch):

	def __init__(self, vertex_name):
		self.vertex_name = vertex_name
		self._marked = dict()
		self._path_tree = dict()

	def do(self, graph):
		self._recursive_path_find(graph, self.vertex_name)
		self._path_tree[self.vertex_name] = self.vertex_name

	def _recursive_path_find(self, graph, vertex_name):
		self._marked[vertex_name] = True
		for name, vertex in graph.adjacent(vertex_name):
			if not self._marked.get(name, False):
				self._path_tree[name] = vertex_name
				self._recursive_path_find(graph, name)

	def _get_path_tree(self):
		return self._path_tree


class BreadthFirstPaths(PathSearch):

	def __init__(self, vertex_name):
		self.vertex_name = vertex_name
		self._marked = dict()
		self._parent_tree = dict()

	def do(self, graph):
		processing_queue = [self.vertex_name]
		self._marked[self.vertex_name] = True
		self._parent_tree[self.vertex_name] = self.vertex_name
		while len(processing_queue) != 0:
			next_vertex = processing_queue.pop(0)
			for name, vertex in graph.adjacent(next_vertex):
				if not self._marked.get(name, False):
					self._marked[next_vertex] = True
					self._parent_tree[name] = next_vertex
					processing_queue.append(name)

	def _get_path_tree(self):
		return self._parent_tree


class ConnectedComponents:

	def __init__(self):
		self._count = 0
		self._connected_marker = dict()

	def do(self, graph):
		for vertex_name, vertex in graph.vertices():
			if vertex_name not in self._connected_marker:
				dfp = DepthFirstPaths(vertex_name)
				graph.apply(dfp)
				for k in dfp.connected():
					self._connected_marker[k] = self._count
				self._count += 1

	def count(self):
		return self._count

	def connected(self, a, b):
		return self._connected_marker[a] == self._connected_marker[b]

	def id(self, vertex_name):
		if vertex_name not in self._connected_marker:
			raise KeyError(vertex_name)
		return self._connected_marker[vertex_name]

	def component(self, id):
		for k, v in self._connected_marker.items():
			if v == id:
				yield k


class CycleDetection:

	def __init__(self, impossible):
		self._marked = {}
		self._has_cycle = False
		self.impossible = impossible

	def do(self, graph):
		for vertex_name, vertex in graph.vertices():
			if vertex_name not in self._marked:
				self._recursive_dfs(graph, vertex_name, self.impossible)

	def has_cycle(self):
		return self._has_cycle

	def cycles(self):
		pass

	def _recursive_dfs(self, graph, current, parent):
		self._marked[current] = True
		for vertex_name, vertex in graph.adjacent(current):
			if vertex_name not in self._marked:
				self._recursive_dfs(graph, vertex_name, current)
			else:
				if parent != vertex_name:
					self._has_cycle = True


class BiparteDetection:

	def __init__(self):
		self._marked = {}
		self._color = {}
		self._is_biparte = True

	def do(self, graph):
		for vertex_name, vertex in graph.vertices():
			if vertex_name not in self._marked:
				self._color[vertex_name] = False
				self._recursive_dfs(graph, vertex_name)

	def is_biparte(self):
		return self._is_biparte

	def _recursive_dfs(self, graph, current):
		self._marked[current] = True
		for vertex_name, vertex in graph.adjacent(current):
			if vertex_name not in self._marked:
				self._color[vertex_name] = not self._color[current]
				self._recursive_dfs(graph, vertex_name)
			else:
				if self._color[vertex_name] == self._color[current]:
					self._is_biparte = False



class UndirectedGraphTest(unittest.TestCase):

	@staticmethod
	def create_connected_graph():
		graph = Graph()
		graph.put_vertex("a", "a")
		graph.put_vertex("b", "b")
		graph.put_vertex("c", "c")
		graph.put_vertex("d", "d")
		graph.put_vertex("e", "e")
		graph.put_vertex("f", "f")
		graph.put_vertex("g", "g")
		graph.put_vertex("h", "h")
		graph.put_vertex("i", "i")
		graph.put_vertex("j", "j")
		graph.put_vertex("k", "k")
		graph.add_edge("a", "b")
		graph.add_edge("a", "d")
		graph.add_edge("d", "f")
		graph.add_edge("b", "f")
		graph.add_edge("b", "e")
		graph.add_edge("c", "e")
		graph.add_edge("e", "f")
		graph.add_edge("d", "j")
		graph.add_edge("f", "g")
		graph.add_edge("g", "h")
		graph.add_edge("j", "g")
		graph.add_edge("k", "i")
		graph.add_edge("j", "k")
		graph.add_edge("g", "i")
		return graph

	@staticmethod
	def create_disconnected_graph():
		nodes = "abcdefghijklm"
		graph = Graph()
		for i in nodes:
			graph.put_vertex(i, i)
		graph.add_edge("a", "e")
		graph.add_edge("a", "d")
		graph.add_edge("a", "c")
		graph.add_edge("a", "b")
		graph.add_edge("c", "g")
		graph.add_edge("b", "f")
		graph.add_edge("g", "f")
		graph.add_edge("h", "i")
		graph.add_edge("j", "m")
		graph.add_edge("h", "j")
		graph.add_edge("h", "k")
		graph.add_edge("l", "i")
		return graph

	@staticmethod
	def create_acyclic_graph():
		nodes = "hijklm"
		graph = Graph()
		for i in nodes:
			graph.put_vertex(i, i)
		graph.add_edge("h", "i")
		graph.add_edge("h", "j")
		graph.add_edge("h", "k")
		graph.add_edge("i", "l")
		graph.add_edge("j", "m")
		return graph

	@staticmethod
	def create_biparte_graph():
		graph = Graph()
		graph.put_vertex("movie_a", "a")
		graph.put_vertex("movie_b", "b")
		graph.put_vertex("movie_c", "c")
		graph.put_vertex("movie_d", "d")
		graph.put_vertex("actor_a", "e")
		graph.put_vertex("actor_b", "f")
		graph.put_vertex("actor_c", "g")
		graph.put_vertex("actor_d", "h")
		graph.put_vertex("actor_e", "i")
		graph.add_edge("movie_a", "actor_a")
		graph.add_edge("movie_b", "actor_b")
		graph.add_edge("movie_c", "actor_c")
		graph.add_edge("movie_d", "actor_d")
		graph.add_edge("movie_d", "actor_e")
		graph.add_edge("actor_a", "movie_b")
		graph.add_edge("actor_c", "movie_a")
		graph.add_edge("actor_c", "movie_b")
		graph.add_edge("actor_d", "movie_a")
		graph.add_edge("actor_e", "movie_b")
		return graph

	def test_adjacency(self):
		graph = UndirectedGraphTest.create_connected_graph()
		neighbors = {"d", "b", "e", "g"}
		for name, vertex in graph.adjacent("f"):
			self.assertTrue(name in neighbors)

	def test_stats(self):
		graph = UndirectedGraphTest.create_connected_graph()
		self.assertEqual(4, graph.degree("f"))
		self.assertEqual(4, graph.degree("g"))
		self.assertEqual(3, graph.degree("e"))
		self.assertEqual(4, graph.max_degree())
		self.assertEqual(11, graph.vertex_count())
		self.assertEqual(14, graph.edge_count())
		self.assertEqual(0, graph.self_loop_count())

	def test_depth_first_search(self):
		searcher = DepthFirstSearch("f")
		graph = UndirectedGraphTest.create_connected_graph()
		graph.apply(searcher)
		self.assertEqual(graph.vertex_count(), searcher.count())
		vertices = "abcdefghijk"
		for c in vertices:
			self.assertTrue(searcher.marked(c))

	def test_depth_first_path(self):
		searcher = DepthFirstPaths("f")
		graph = UndirectedGraphTest.create_connected_graph()
		graph.apply(searcher)
		vertices = "abcdefghijk"
		for c in vertices:
			self.assertTrue(searcher.has_path(c))
		sequence = searcher.path_to("c")
		self.assertEqual("fdabec", "".join(sequence))
		connected = set(searcher.connected())
		self.assertEqual(set("abcdefghijk"), connected)

	def test_breadth_first_path(self):
		searcher = BreadthFirstPaths("f")
		graph = UndirectedGraphTest.create_connected_graph()
		graph.apply(searcher)
		vertices = "abcdefghijk"
		for c in vertices:
			self.assertTrue(searcher.has_path(c))
		sequence = searcher.path_to("c")
		self.assertEqual("fbec", "".join(sequence))
		connected = set(searcher.connected())
		self.assertEqual(set("abcdefghijk"), connected)

	def test_connected_component(self):
		searcher = ConnectedComponents()
		graph = UndirectedGraphTest.create_disconnected_graph()
		graph.apply(searcher)
		self.assertEqual(2, searcher.count())
		connected = set(searcher.component(0))
		self.assertEqual(set("abcdefg"), connected)
		connected = set(searcher.component(1))
		self.assertEqual(set("hijklm"), connected)
		self.assertTrue(searcher.connected("h", "m"))
		self.assertTrue(searcher.connected("a", "g"))
		self.assertEqual(0, searcher.id("a"))

	def test_cycle_detection(self):
		searcher = CycleDetection("-1")
		graph = UndirectedGraphTest.create_connected_graph()
		graph.apply(searcher)
		self.assertTrue(searcher.has_cycle())
		searcher = CycleDetection("-1")
		graph = UndirectedGraphTest.create_acyclic_graph()
		graph.apply(searcher)
		self.assertFalse(searcher.has_cycle())

	def test_biparte_detection(self):
		searcher = BiparteDetection()
		graph = UndirectedGraphTest.create_biparte_graph()
		graph.apply(searcher)
		self.assertTrue(searcher.is_biparte())
		graph = UndirectedGraphTest.create_connected_graph()
		searcher = BiparteDetection()
		graph.apply(searcher)
		self.assertFalse(searcher.is_biparte())
