import unittest

from structure.linkedList import LinkedStack


def check_parentheses(exp):
	parentheses_stack = LinkedStack()
	open_parentheses = "({["
	close_parentheses = ")}]"
	for index, value in enumerate(exp):
		if value in open_parentheses:
			parentheses_stack.push(value)
		if value in close_parentheses:
			last = parentheses_stack.pop()
			correct_index = close_parentheses.index(value)
			open_p = open_parentheses[correct_index]
			if last is None or last != open_p:
				return index
	return -1


class Operator:

	def __init__(self, symbol, priority, argument_count):
		self.symbol = symbol
		self.priority = priority
		self.argument_count = argument_count

	def __eq__(self, other):
		try:
			if self.argument_count != other.argument_count:
				return False
			if self.priority != other.priority:
				return False
			if self.symbol != other.symbol:
				return False
		except AttributeError:
			return False
		return True

	def __ne__(self, other):
		return not self.__eq__(other)

	def __repr__(self):
		return str(self.__dict__)

	def __gt__(self, other):
		return self.priority > other.priority

	def __lt__(self, other):
		return self.priority < other.priority

	def __ge__(self, other):
		return self.__gt__(other) or self.__eq__(other)

	def __le__(self, other):
		return self.__lt__(other) or self.__eq__(other)


class AdditionOperator(Operator):

	def __init__(self):
		Operator.__init__(self, "+", 1, 2)

	def __call__(self, *args, **kwargs):
		return float(args[0]) + float(args[1])


class SubtractionOperator(Operator):

	def __init__(self):
		Operator.__init__(self, "-", 1, 2)

	def __call__(self, *args, **kwargs):
		return float(args[0]) - float(args[1])


class MultiplicationOperator(Operator):

	def __init__(self):
		Operator.__init__(self, "*", 2, 2)

	def __call__(self, *args, **kwargs):
		return float(args[0]) * float(args[1])


class DivisionOperator(Operator):

	def __init__(self):
		Operator.__init__(self, "/", 2, 2)

	def __call__(self, *args, **kwargs):
		return float(args[0]) / float(args[1])


class ArithmeticEvaluator:
	open_parentheses = Operator("(", -1, 0)

	def __init__(self):
		self._operators = dict()

	def register_operator(self, operator):
		self._operators[operator.symbol] = operator

	def unregister_operator(self, symbol):
		del self._operators[symbol]

	def evaluate_infix(self, exp):
		# first, convert it to postfix
		post_fix_exp = self.infix_to_postfix(exp)
		return self.evaluate_postfix(post_fix_exp)

	def evaluate_postfix(self, exp):
		operands_stack = LinkedStack()
		tokenized = exp.split(" ")
		for symbol in tokenized:
			if symbol in self._operators:
				current_operator = self._operators[symbol]
				arguments = []
				for i in range(current_operator.argument_count):
					next_operand = operands_stack.pop()
					if next_operand is None:
						raise ValueError("More operand required for " + current_operator.symbol)
					arguments.insert(0, next_operand)
				result = current_operator(*arguments)
				operands_stack.push(result)
			else:
				operands_stack.push(symbol)
		if len(operands_stack) != 1:
			raise ValueError("Invalid Expression")
		return operands_stack.pop()

	def infix_to_postfix(self, exp):
		operator_buffer = LinkedStack()
		tokenized = exp.split(" ")
		result = []
		for index, symbol in enumerate(tokenized):
			if symbol in self._operators:
				current_operator = self._operators[symbol]
				while len(operator_buffer) != 0 and operator_buffer.peek() >= current_operator:
					result.append(operator_buffer.pop().symbol)
				operator_buffer.push(current_operator)
			else:
				if symbol == "(":
					operator_buffer.push(ArithmeticEvaluator.open_parentheses)
				else:
					if symbol == ")":
						while True:
							prev_operator = operator_buffer.pop()
							if prev_operator == ArithmeticEvaluator.open_parentheses:
								break
							if prev_operator is None:
								raise ValueError("Mismatched parentheses")
							result.append(prev_operator.symbol)
					else:
						result.append(symbol)

		while operator_buffer.peek() is not None:
			remaining_operator = operator_buffer.pop()
			if remaining_operator == ArithmeticEvaluator.open_parentheses:
				raise ValueError("Mismatched parentheses")
			result.append(remaining_operator.symbol)
		return " ".join(result)

	@staticmethod
	def fix_parentheses(exp):
		operand_indexes = LinkedStack()
		parentheses_index = []
		tokenized = exp.split(" ")
		result = []
		for index, artifact in enumerate(tokenized):
			if artifact.isdigit():
				operand_indexes.push(index)
			if artifact == ")":
				operand_indexes.pop()
				first_operand = operand_indexes.pop()
				if first_operand is None:
					raise ValueError("Invalid number of operands")
				parentheses_index.append(first_operand)
				operand_indexes.push(first_operand)
		if len(operand_indexes) != 1:
			raise ValueError("Parentheses mismatch")
		parentheses_index.sort()
		for index, value in enumerate(tokenized):
			count = 0
			for i in parentheses_index:
				if i == index:
					result.append("(")
					count += 1
				if i > index:
					break
			del parentheses_index[:count]
			result.append(value)
		return " ".join(result)


class TestParentheses(unittest.TestCase):

	def test_correct_expression(self):
		exp = "{([])({}){[]}}[()]"
		result = check_parentheses(exp)
		self.assertEqual(-1, result, "check parentheses did not work as expected")

	def test_incorrect_expression(self):
		exp = "{([])({}){[}}[()]"
		result = check_parentheses(exp)
		self.assertEqual(11, result, "check parentheses did not return the correct index")


class TestEvaluator(unittest.TestCase):

	def test_fix_parentheses(self):
		exp = "1 + 2 ) * 3 - 4 ) * 5 - 6 ) ) )"
		fixed = ArithmeticEvaluator.fix_parentheses(exp)
		self.assertEqual("( ( 1 + 2 ) * ( ( 3 - 4 ) * ( 5 - 6 ) ) )", fixed)

	def test_infix_to_postfix_with_parentheses(self):
		exp = "( ( 1 + 2 ) * ( ( 3 - 4 ) * ( 5 - 6 ) ) )"
		post_fix = "1 2 + 3 4 - 5 6 - * *"
		evaluator = TestEvaluator._get_default_evaluator()
		self.assertEqual(post_fix, evaluator.infix_to_postfix(exp))

	def test_infix_to_postfix_natural(self):
		exp = "1 + 2 * 3 - 4 * 5 - 6"
		post_fix = "1 2 3 * 4 5 * - 6 - +"
		evaluator = TestEvaluator._get_default_evaluator()
		self.assertEqual(post_fix, evaluator.infix_to_postfix(exp))

	def test_infix_to_postfix_partial(self):
		exp = "3 + 4 * 2 / ( 1 - 5 )"
		post_fix = "3 4 2 1 5 - / * +"
		evaluator = TestEvaluator._get_default_evaluator()
		self.assertEqual(post_fix, evaluator.infix_to_postfix(exp))

	def test_evaluate_postfix(self):
		exp = "1 2 + 3 4 - 5 6 - * *"
		evaluator = TestEvaluator._get_default_evaluator()
		self.assertEqual(3, evaluator.evaluate_postfix(exp))

	def test_evaluate_infix(self):
		exp = "1 + ( 100 * 20 ) / 5 + ( 11 + 12 ) * 2"
		evaluator = TestEvaluator._get_default_evaluator()
		self.assertEqual(447, evaluator.evaluate_infix(exp))

	@staticmethod
	def _get_default_evaluator():
		evaluator = ArithmeticEvaluator()
		evaluator.register_operator(AdditionOperator())
		evaluator.register_operator(SubtractionOperator())
		evaluator.register_operator(MultiplicationOperator())
		evaluator.register_operator(DivisionOperator())
		return evaluator
