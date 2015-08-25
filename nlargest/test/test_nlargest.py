#!/usr/bin/env python3
import heapq
import random
import unittest

import nlargest


random.seed(42)
unsorted = [random.randrange(0, 99) for i in range(10)]


class TestSequence(unittest.TestCase):
    functions = (
        nlargest.nlargest_list,
        nlargest.nlargest_list2,
        nlargest.nlargest_list3,
        nlargest.nlargest_heapreplace,
        nlargest.nlargest_heapreplace2,
        nlargest.nlargest_heapreplace3,
        nlargest.nlargest_heappushpop,
        nlargest.nlargest_heappushpop2,
        nlargest.nlargest_heappushpop3,
        nlargest.nlargest_manual_heapreplace,
        nlargest.nlargest_manual_heapreplace2,
        nlargest.nlargest_manual_heapreplace3,
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
