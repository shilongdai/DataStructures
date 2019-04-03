import unittest

from structure.graph import *


class ParallelPrecedenceJobScheduler:

	def __init__(self):
		self._graph = DirectedEdgeWeightedGraph()
		self._graph.put_vertex("_start", "_start")
		self._graph.put_vertex("_end", "_end")
		self._jobs = set()

	def add_job_by_val(self, job_id, time):
		start_id = self._create_start_id(job_id)
		end_id = self._create_end_id(job_id)
		self._graph.put_vertex(start_id, job_id)
		self._graph.put_vertex(end_id, job_id)
		self._graph.add_edge(WeightedEdge("_start", start_id, 0))
		self._graph.add_edge(WeightedEdge(start_id, end_id, time * -1))
		self._graph.add_edge(WeightedEdge(end_id, "_end", 0))
		self._jobs.add(job_id)

	def required_by(self, job, required_by):
		for i in required_by:
			self._graph.add_edge(WeightedEdge(self._create_end_id(job), self._create_start_id(i), 0))

	def schedule(self):
		lp = TopologicalAcyclicShortestPath("_start")
		self._graph.apply(lp)
		result_jobs = dict()
		for job in self._jobs:
			result_jobs[job] = lp.dist_to(self._create_start_id(job)) * -1
		return lp.dist_to("_end") * -1, result_jobs

	@staticmethod
	def _create_start_id(jid):
		return str(jid) + "_start"

	@staticmethod
	def _create_end_id(jid):
		return str(jid) + "_end"


class TestJobScheduler(unittest.TestCase):

	@staticmethod
	def create_parallel_precedence_scheduler():
		scheduler = ParallelPrecedenceJobScheduler()
		scheduler.add_job_by_val(0, 41)
		scheduler.add_job_by_val(1, 51)
		scheduler.add_job_by_val(2, 50)
		scheduler.add_job_by_val(3, 36)
		scheduler.add_job_by_val(4, 38)
		scheduler.add_job_by_val(5, 45)
		scheduler.add_job_by_val(6, 21)
		scheduler.add_job_by_val(7, 32)
		scheduler.add_job_by_val(8, 32)
		scheduler.add_job_by_val(9, 29)

		scheduler.required_by(0, (1, 7, 9))
		scheduler.required_by(1, [2])
		scheduler.required_by(9, (4, 6))
		scheduler.required_by(8, [2])
		scheduler.required_by(7, (3, 8))
		scheduler.required_by(6, (3, 8))
		return scheduler

	def test_parallel_precedence_scheduler(self):
		scheduler = self.create_parallel_precedence_scheduler()
		total_time, jobs = scheduler.schedule()
		self.assertAlmostEqual(173, total_time)
		self.assertAlmostEqual(0, jobs[0])
		self.assertAlmostEqual(41, jobs[1])
		self.assertAlmostEqual(123, jobs[2])
		self.assertAlmostEqual(91, jobs[3])
		self.assertAlmostEqual(70, jobs[4])
		self.assertAlmostEqual(0, jobs[5])
		self.assertAlmostEqual(70, jobs[6])
		self.assertAlmostEqual(41, jobs[7])
		self.assertAlmostEqual(91, jobs[8])
		self.assertAlmostEqual(41, jobs[9])
