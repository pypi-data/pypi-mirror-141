from calculator_project import calculator
import unittest

# 1. Printed and checked `help` to see and evaluate
# the DocStrings.

# 2. pyflakes was used, showed no errors.

# 3. mypy was used:
# PS C:\Users\ikirs\Desktop\Calculator_project> mypy calculator_project.py
# Success: no issues found in 1 source file

# 4. DOCTEST

if __name__ == "__main__":
    import doctest

    calculator.Calculator()
    print(doctest.testmod())

# Output:
# TestResults(failed=0, attempted=13)
# Doctest - no errors (tested in the module, don't know how in testfile).

# 5. Unittest


class TestCalculator(unittest.TestCase):
    def test_print_memory(self) -> None:
        self.calculator = calculator.Calculator()
        self.assertEqual(self.calculator._memory, 0.0)

    def test_add(self) -> None:
        self.calculator = calculator.Calculator()
        self.assertEqual(self.calculator.add(1.0), 1.0)
        self.assertEqual(self.calculator.add(-6.0), -5.0)
        self.assertEqual(self.calculator.add(1000.0), 995.0)
        self.assertEqual(self.calculator.add(0.0), 995.0)
        # Trying 'complex' input, print's 'Please enter a float',
        # returns self._memory.
        self.assertEqual(self.calculator.add(8j), 995.0)
        # Trying 'str' input, print's out 'Please enter a float'
        # and returns self._memory.
        self.assertEqual(self.calculator.add("a"), 995.0)

    def test_sub(self) -> None:
        self.calculator = calculator.Calculator()
        self.assertEqual(self.calculator.sub(1.0), -1.0)
        self.assertEqual(self.calculator.sub(-6.0), 5.0)
        self.assertEqual(self.calculator.sub(1000.0), -995.0)
        self.assertEqual(self.calculator.sub(0.0), -995.0)
        # Trying 'complex' input, print's 'Please enter a float',
        # returns self._memory.
        self.assertEqual(self.calculator.add(8j), -995.0)
        # Trying a string input, prints 'Please enter a float',
        # returns self._memory.
        self.assertEqual(self.calculator.add("a"), -995.0)

    def test_multiply(self) -> None:
        self.calculator = calculator.Calculator()
        self.assertEqual(self.calculator.add(1.0), 1.0)
        self.assertEqual(self.calculator.multiply(1.0), 1.0)
        self.assertEqual(self.calculator.multiply(-6.0), -6.0)
        self.assertEqual(self.calculator.multiply(1000.0), -6000.0)
        self.assertEqual(self.calculator.multiply(0.0), 0.0)
        # Trying 'complex' input, print's 'Please enter a float', returns self._memory.
        self.assertEqual(self.calculator.multiply(8j), 0.0)
        # Trying 'str' input, print's out 'Please enter a float' and returns self._memory.
        self.assertEqual(self.calculator.multiply("a"), 0.0)

    def test_divide(self) -> None:
        self.calculator = calculator.Calculator()
        self.assertEqual(self.calculator.start_memory_with(10.0), 10.0)
        self.assertEqual(self.calculator.divide(1.0), 10.0)
        # Handled ZerroDivisionError.
        self.assertEqual(self.calculator.divide(0.0), 10.0)
        self.assertEqual(self.calculator.divide(-2.0), -5.0)
        self.assertEqual(self.calculator.divide(5.0), -1.0)
        # Trying 'str' input, print's out 'Please enter a float'
        # and returns self._memory.
        self.assertEqual(self.calculator.divide("a"), -1.0)
        # Trying 'complex' input, print's 'Please enter a float',
        # returns self._memory.
        self.assertEqual(self.calculator.divide(8j), -1.0)

    def test_root(self) -> None:
        self.calculator = calculator.Calculator()
        self.assertEqual(self.calculator.start_memory_with(36.0), 36.0)
        self.assertEqual(self.calculator.root(2.0), 6.0)
        self.assertEqual(self.calculator.start_memory_with(27.0), 27.0)
        self.assertEqual(self.calculator.root(3.0), 3.0)
        self.assertEqual(self.calculator.start_memory_with(9.0), 9.0)
        # Trying a negative number as the (n) th. Print's out 'The root
        # cannot be taken', returns self._memory
        self.assertEqual(self.calculator.root(-2.0), 9.0)
        # Trying 'str' input, print's out 'Please enter a float'
        # and returns self._memory.
        self.assertEqual(self.calculator.root("a"), 9.0)
        # Trying 'complex' input, print's 'Please enter a float',
        # returns self._memory.
        self.assertEqual(self.calculator.root(8j), 9.0)
        self.assertEqual(self.calculator.start_memory_with(-36.0), -36.0)
        # Trying a negative float as self._memory. Print out 'the root
        #  cannot be taken', returns self._memory.
        self.assertEqual(self.calculator.root(2.0), -36.0)

    def test_start_memory_with(self) -> None:
        self.calculator = calculator.Calculator()
        self.assertEqual(self.calculator.start_memory_with(36.0), 36.0)
        self.assertEqual(self.calculator.start_memory_with(-8.0), -8.0)
        self.assertEqual(self.calculator.start_memory_with(9.0), 9.0)
        #  Trying 'str' input, print's out 'Please enter a float' and
        # returns self._memory.
        self.assertEqual(self.calculator.start_memory_with("a"), 9.0)
        # Trying 'complex' input, print's 'Please enter a float', returns
        #  self._memory.
        self.assertEqual(self.calculator.start_memory_with(6j), 9.0)


if __name__ == "__main__":
    unittest.main()

# ANSWER:
# .
# ----------------------------------------------------------------------
# Ran 7 tests in 0.004s
#
# OK
