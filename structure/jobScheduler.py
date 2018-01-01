from structure.graph import *


class Job:

	def __init__(self, name, start_time):
		self.name = name
		self.start_time = start_time

	def __eq__(self, other):
		if self.name != other.name:
			return False
		if abs(self.start_time - other.start_time) > 0.0000001:
			return False
		return True

	def __ne__(self, other):
		return not self == other

	def __hash__(self):
		hash_code = 7
		hash_code = 31 * hash_code + hash(self.name)
		hash_code = 31 * hash_code + hash()


class ParallelPrecedenceJobScheduler:

	def __init__(self):
		self._graph = EdgeWeightedGraph()
		self._graph.put_vertex("_start", "_start")
		self._graph.put_vertex("_end", "_end")
		self._jobs = set()

	def add_job_by_val(self, job_id, time, dependencies=()):
		start_id = str(job_id) + "_start"
		end_id = str(job_id) + "_end"
		self._graph.put_vertex(start_id, job_id)
		self._graph.put_vertex(end_id, job_id)
		self._graph.add_edge(WeightedEdge("_start", start_id, 0))
		self._graph.add_edge(WeightedEdge(start_id, end_id, time * -1))
		self._graph.add_edge(WeightedEdge(end_id, "_end", 0))
		self._jobs.add(job_id)

	def schedule(self):
		lp = TopologicalAcyclicShortestPath("_start")
		self._graph.apply(lp)
		result_jobs = []
		for job in self._jobs:
			result_jobs.append(Job(job, lp.dist_to(job) * -1))
		return lp.dist_to("_end"), result_jobs


class TestJobScheduler:
	pass
