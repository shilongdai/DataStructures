import heapq
import random

from algorithms.sort import exchange
from algorithms.sort import inversions


def a_algorithm(start_config, end_config):
	config_queue = [start_config]
	closed_set = set()
	while True:
		next = heapq.heappop(config_queue)
		if next == end_config:
			return next
		possibilities = next.next()
		for i in possibilities:
			if i in closed_set:
				continue
			heapq.heappush(config_queue, i)
		closed_set.add(next)


class EightPuzzle:

	@staticmethod
	def completed_puzzle():
		return EightPuzzle([1, 2, 3, 4, 5, 6, 7, 8, -1])

	def __init__(self, numbers = (), x = 0, y = 0):
		space_pos = self._2d_to_index(x, y)
		if len(numbers) == 9:
			self._numbers = list(numbers)
		else:
			self._numbers = []
			for i in range(8):
				self._numbers.append(i + 1)
			random.shuffle(self._numbers)
			self._numbers.insert(space_pos, -1)
		self._x = x
		self._y = y

	def solved(self):
		return self.distance_to_solved() == 0

	def solvable(self):
		tester = list(self._numbers)
		tester.remove(-1)
		return inversions(tester) % 2 == 0

	def distance_to_solved(self):
		distance = 0
		completed = self.completed_puzzle()
		for i in range(9):
			if self._numbers[i] != completed._numbers[i]:
				distance += 1
		return distance

	def move_up(self):
		return self._move_to_position(self._x, self._y + 1)

	def move_down(self):
		return self._move_to_position(self._x, self._y - 1)

	def move_right(self):
		return self._move_to_position(self._x + 1, self._y)

	def move_left(self):
		return self._move_to_position(self._x - 1, self._y)

	def can_move_up(self):
		return self._y < 2

	def can_move_down(self):
		return self._y > 0

	def can_move_right(self):
		return self._x < 2

	def can_move_left(self):
		return self._x > 0

	def _move_to_position(self, x, y):
		if not self._can_move_to_pos(x, y):
			raise IndexError("Cannot move to the coordinate")
		index = self._2d_to_index(x, y)
		numbers = list(self._numbers)
		exchange(numbers, index, self._2d_to_index(self._x, self._y))
		return EightPuzzle(numbers, x, y)

	def _can_move_to_pos(self, x, y):
		index = self._2d_to_index(x, y)
		return index >= 0 and index < 9

	def _2d_to_index(self, x, y):
		return 3 * y + x

	def __eq__(self, other):
		return self._numbers == other._numbers

	def __hash__(self):
		return hash("".join([str(i) for i in self._numbers]))

	def __repr__(self):
		result = ""
		for i in range(3):
			for j in range(3):
				result += str(self._numbers[self._2d_to_index(j, i)]) + " "
			result += "\n"
		return result


class EightPuzzleConfiguration:

	def __init__(self, puzzle, move_count, parent):
		self._puzzle = puzzle
		self.parent = parent
		self._move_count = move_count

	def next(self):
		result = []
		if self._puzzle.can_move_right():
			result.append(EightPuzzleConfiguration(self._puzzle.move_right(), self._move_count + 1, self))
		if self._puzzle.can_move_left():
			result.append(EightPuzzleConfiguration(self._puzzle.move_left(), self._move_count + 1, self))
		if self._puzzle.can_move_up():
			result.append(EightPuzzleConfiguration(self._puzzle.move_up(), self._move_count + 1, self))
		if self._puzzle.can_move_down():
			result.append(EightPuzzleConfiguration(self._puzzle.move_down(), self._move_count + 1, self))
		return result

	def __eq__(self, other):
		return self._puzzle == other._puzzle

	def __lt__(self, other):
		return self._priority() < other._priority()

	def _priority(self):
		return self._move_count + self._puzzle.distance_to_solved()

	def __repr__(self):
		return repr(self._puzzle)

	def __hash__(self):
		return hash(self._puzzle)


if __name__ == "__main__":
	puzzle = EightPuzzle()
	while not puzzle.solvable():
		puzzle = EightPuzzle()
	print(puzzle)
	start_config = EightPuzzleConfiguration(puzzle, 0, None)
	end_config = EightPuzzleConfiguration(EightPuzzle.completed_puzzle(), -1, None)
	end_config = a_algorithm(start_config, end_config)
	in_order = []
	while end_config.parent is not None:
		in_order.insert(0, end_config)
		end_config = end_config.parent
	for i in in_order:
		print(i)
