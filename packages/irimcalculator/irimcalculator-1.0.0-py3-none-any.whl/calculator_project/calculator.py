class Calculator:
    """
    Module Calculator proceeds the ability to calculate numbers (float), given by user.
    Attribute: 
    - memory(float)

    Methods of this class:

    - Addition;
    - Subtraction;
    - Multiplication;
    - Division;
    - Take (n) root of a number (memory);
    - Reset memory to 0.0;
    - Start memory with chosen number (float);
    - Print out the final answer (memory).

    Calculator has its own memory and manipulates its starting number 0.0 until it is reseted.
    User can set the starting calculator memory to it's own value(float) with `start_memory_with` method.
    In all Calcuator methods using `try` and `if` statement is checked if the users input is certainly a `float`.

    For example:

        >>> my_calc = Calculator()
        >>> print(my_calc.add(2.0))
        2.0
        >>> print(my_calc.add(2.0))
        4.0
        >>> print(my_calc.sub(1.0))
        3.0
        >>> print(my_calc.multiply(9.0))
        27.0
        >>> print(my_calc.multiply(-1.0))
        -27.0
        >>> print(my_calc.divide(3.0))
        -9.0
        >>> print(my_calc.reset_memory())
        0.0
        >>> print(my_calc.add(6.0))
        6.0
        >>> print(my_calc.multiply(6.0))
        36.0
        >>> print(my_calc.root(2.0))
        6.0
        >>> print(my_calc.add(2))
        8.0
        >>> my_calc.answer()
        8.0
        """

    def __init__(self) -> None:
        """Sets attribute: `memory` - of the calculator to 0.0."""
        self._memory = 0.0

    def add(self, num: float) -> float:
        """Adds to the `memory` the number(float), entered by user.

        With `if` statment, escaping complex numbers, as 
        TypeError doesn't include those.
        """

        if type(num) == complex:
            print("Please enter a float")
        else:
            try:
                self._memory += num
            except TypeError:
                print("Please enter a float")
        return self._memory

    def sub(self, num: float) -> float:
        """ Subtracts from `memory` users entered nuber(float)"""

        if type(num) == complex:
            print("Please enter a float")
        else:
            try:
                self._memory -= num
            except TypeError:
                print("Please enter a float")
        return self._memory

    def multiply(self, num: float) -> float:
        """Multiplies `memory` by users entered number(float)"""

        if type(num) == complex:
            print("Please enter a float")
        else:
            try:
                self._memory *= num
            except TypeError:
                print("Please enter a float")
        return self._memory

    def divide(self, num: float) -> float:
        """Divides `memory` by users entered float"""

        if type(num) == complex:
            print("Please enter a float")
        else:
            try:
                self._memory /= num
            except ZeroDivisionError:
                print("Division by zero is impossible.")
            except TypeError:
                print("Please enter a float")
        return self._memory

    def root(self, num: float) -> float:
        """Takes users entered n-th (num) root of the `memory`.
        param: num (float), must be a positive float
        """

        if type(num) == complex:
            print("Please enter a float")
        else:
            try:
                if num > 0.0 and self._memory > 0.0:
                    self._memory = self._memory ** (1 / num)
                else:
                    print("The root cannot be taken")
            except (TypeError, ZeroDivisionError, ValueError):
                print("Please enter a positive float")

        return self._memory

    def reset_memory(self):
        """Resets `memory` to 0.0"""

        self._memory = 0.0
        return self._memory

    def start_memory_with(self, num: float) -> float:
        """Resets `memory` to the chosen number by user.

        Method takes as an argument a float and sets it as
        the `memory` of the calculator. In that way, for 
        egzample, user can instantly after this method apply 
        the 'root' method and get the (n)th root of his chosen 
        number, also user can do all other calculations
        starting not from 0.0, but from his own chosen number.
        """

        if type(num) == complex:
            print("Please enter a float")
        else:
            try:
                self._memory = float(num)
            except (TypeError, ValueError):
                print("Please enter a float")

        return self._memory

    def answer(self):
        """Prints the `memory`"""
        print(self._memory)


if __name__ == "__main__":
    Calculator()
