#!/usr/bin/env python3
import heapq
import random
import unittest

import nlargest


random.seed(42)
unsorted = [random.randrange(0, 99) for i in range(10)]


class TestSequence(unittest.TestCase):
    functions = (
        getattr(nlargest, fun)
        for fun in dir(nlargest) if fun.startswith('nlargest_')
    )

    def test_get_largest(self):
        N = 5
        verify = sorted(heapq.nlargest(N, unsorted))
        message = ('{{}} should return the largest {} numbers from the given '
                   'list').format(N)
        for f in self.functions:
            with self.subTest(msg=message.format(f.__name__)):
                self.assertEqual(f(N, unsorted), verify)


if __name__ == '__main__':
    unittest.main()
