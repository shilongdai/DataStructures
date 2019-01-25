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
