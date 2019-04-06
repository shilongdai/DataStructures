import math

from structure.graph import *


class ParallelPrecedenceJobScheduler:

	def __init__(self):
		self._graph = DirectedEdgeWeightedGraph()
		self._graph.put_vertex("_start", "_start")
		self._graph.put_vertex("_end", "_end")
		self._jobs = set()

	def add_job(self, job_id, time):
		start_id = self._create_start_id(job_id)
		end_id = self._create_end_id(job_id)
		self._graph.put_vertex(start_id, job_id)
		self._graph.put_vertex(end_id, job_id)
		self._graph.add_edge(WeightedEdge("_start", start_id, 0))
		self._graph.add_edge(WeightedEdge(start_id, end_id, time))
		self._graph.add_edge(WeightedEdge(end_id, "_end", 0))
		self._jobs.add(job_id)

	def required_by(self, job, required_by):
		for i in required_by:
			self._graph.add_edge(WeightedEdge(self._create_end_id(job), self._create_start_id(i), 0))

	def schedule(self):
		lp = TopologicalAcyclicLongestPath("_start")
		self._graph.apply(lp)
		result_jobs = dict()
		for job in self._jobs:
			result_jobs[job] = lp.dist_to(self._create_start_id(job))
		return lp.dist_to("_end"), result_jobs

	@staticmethod
	def _create_start_id(jid):
		return str(jid) + "_start"

	@staticmethod
	def _create_end_id(jid):
		return str(jid) + "_end"


class ArbitrageCalculator:

	def __init__(self, currencies):
		self._graph = DirectedEdgeWeightedGraph()
		for currency, conversion in currencies.items():
			self._graph.put_vertex(currency, conversion)
			for c, rate in conversion.items():
				self._graph.add_edge(WeightedEdge(currency, c, -1 * math.log10(rate)))
		self._negative_cycle = QueueBellmanFordShortestPath(next(iter(currencies.keys())), True)
		self._graph.apply(self._negative_cycle)

	def convert(self, src, target):
		if self._negative_cycle.has_negative_cycle():
			raise ValueError("A negative cycle exists")
		shortest_path = QueueBellmanFordShortestPath(src)
		self._graph.apply(shortest_path)
		path = shortest_path.path_to(target)
		result = list()
		result.append(src)
		for edge in path:
			result.append(edge.dest)
		final_ratio = 1
		prev_table = self._graph.get_vertex(src)
		for p in result:
			final_ratio = final_ratio * prev_table[p]
			prev_table = self._graph.get_vertex(p)
		return final_ratio, result

	def has_opportunity(self):
		return self._negative_cycle.has_negative_cycle()

	def get_arbitrage_opportunity(self):
		result = []
		for edge in self._negative_cycle.cycle:
			result.append(edge.src)
		result.append(self._negative_cycle.cycle[-1].dest)
		return result


class TestJobScheduler(unittest.TestCase):

	@staticmethod
	def create_parallel_precedence_scheduler():
		scheduler = ParallelPrecedenceJobScheduler()
		scheduler.add_job(0, 41)
		scheduler.add_job(1, 51)
		scheduler.add_job(2, 50)
		scheduler.add_job(3, 36)
		scheduler.add_job(4, 38)
		scheduler.add_job(5, 45)
		scheduler.add_job(6, 21)
		scheduler.add_job(7, 32)
		scheduler.add_job(8, 32)
		scheduler.add_job(9, 29)

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


class TestArbitrageCalculator(unittest.TestCase):

	def test_calculator(self):
		currencies = {"USD": {"USD": 1, "EUR": 0.741, "GBP": 0.657, "CHF": 1.061, "CAD": 1.005},
		              "EUR": {"USD": 1.349, "EUR": 1, "GBP": 0.888, "CHF": 1.433, "CAD": 1.366},
		              "GBP": {"USD": 1.521, "EUR": 1.126, "GBP": 1, "CHF": 1.614, "CAD": 1.538},
		              "CHF": {"USD": 0.942, "EUR": 0.698, "GBP": 0.619, "CHF": 1, "CAD": 0.953},
		              "CAD": {"USD": 0.995, "EUR": 0.732, "GBP": 0.65, "CHF": 1.049, "CAD": 1}}
		calculator = ArbitrageCalculator(currencies)
		self.assertTrue(calculator.has_opportunity())
		self.assertListEqual(["USD", "CHF", "CAD", "USD"], calculator.get_arbitrage_opportunity())
