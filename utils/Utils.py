import random
import string

from tests.constants import BearType


class Utils(object):

    @staticmethod
    def get_random_string(add_string='', size=6, chars=string.ascii_lowercase):
        """Generate random string with given length.

        Args:
            add_string: start string.
            size: length of random string.
            chars: array of chars.

        Returns: Random string.

        """
        return add_string + ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def get_random_int(size=2):
        """Get random integer.

        Args:
            size: number og digits for result random integer.

        Returns: random integer with given number of digits.

        """
        range_start = 10 ** (size - 1)
        range_end = (10 ** size) - 1
        return random.randint(range_start, range_end)

    @staticmethod
    def get_random_bear_type():
        """Get random bear type."""
        return random.choice(list(BearType)).value
