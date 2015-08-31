#!/usr/bin/env python3
import functools
import heapq
import itertools


def nlargest_ref_sorted(n, iterable):
    """Full list sorting for reference."""
    return sorted(iterable)[-n:]


def nlargest_ref_heapq(n, iterable):
    """Vanilla implementation from the heapq module."""
    return heapq.nlargest(n, iterable)[::-1]


def nlargest_list(n, iterable):
    """Return the n largest items in the given iterable. O(N) performance for
    small n, where N is the length of the list.
    """
    # Quite naïve method, keeping its own list of the n largest numbers at
    # every time and keeping track of the smallest item and its index in the
    # list for future replacement.
    get_min_index_value = functools.partial(min, key=lambda x: x[1])
    largest = n * [float('-inf')]
    min_index, min_value = 0, largest[0]
    for i in iterable:
        if i > min_value:
            largest[min_index] = i
            min_index, min_value = get_min_index_value(enumerate(largest))
    largest.sort()
    return largest


def nlargest_heapreplace(n, iterable):
    """Return the n largest items in the given iterable. O(N) performance for
    small n, where N is the length of the list.
    """
    # Uses the heapq.heapify structure for the list of largest numbers, to
    # replace the search for the minimal number at every turn. The search is
    # replaced by maintaining the heap invariant after insertion, which should
    # be a O(log n) operation rather than O(n) for an exhaustive search, with
    # the drawback of having to do more internal list element movements when
    # the new item is sifted into the structure.
    largest = n * [float('-inf')]
    push_larger = functools.partial(heapq.heapreplace, largest)
    for i in iterable:
        if i > largest[0]:
            push_larger(i)
    largest.sort()
    return largest


def nlargest_heappushpop(n, iterable):
    """Return the n largest items in the given iterable. O(N) performance for
    small n, where N is the length of the list.
    """
    # Like nlargest_heapreplace, but using the built-in heappushpop function
    # which only performs the addition of the new element in case it is larger
    # than the root (which is the smallest element). In practice, this offloads
    # the comparison to the heapq module. Performance takes a hit since there
    # is a function call for every item in the iterable.
    largest = n * [float('-inf')]
    push_larger = functools.partial(heapq.heappushpop, largest)
    for i in iterable:
        push_larger(i)
    largest.sort()
    return largest


def nlargest_manual_heapreplace(n, iterable):
    """Return the n largest items in the given iterable. O(N) performance for
    small n, where N is the length of the list.
    """
    # A test using a "manual" heapq.heapreplace equivalent through its internal
    # heapq._siftup function. The idea is that this should avoid some extra
    # tests performed by heapq.heapreplace, but in practice the same tests are
    # performed by heapq._siftup, so there is generally no speedup.
    largest = n * [float('-inf')]
    siftup = functools.partial(heapq._siftup, largest, 0)
    for i in iterable:
        if i > largest[0]:
            largest[0] = i
            siftup()
    largest.sort()
    return largest


# The functions with suffix "2" use a slightly modified initialization and
# iteration which avoids creating the float('inf') values just to shift them
# out at first opportunity. This gives a speedup for small lists, but for some
# reason tends to produce slowdowns for large lists. I would expect the
# corresponding functions to asymptotically approach each other, but there
# seems to be some slowdown in letting the iterator pass through
# itertools.islice().

# 13 % slowdown for large iterables.
def nlargest_list2(n, iterable):
    """Return the n largest items in the given iterable."""
    # Quite naïve method, keeping its own list of the n largest numbers at
    # every time and keeping track of the smallest item and its index in the
    # list for future replacement.
    get_min_index_value = functools.partial(min, key=lambda x: x[1])
    largest = iterable[:n]
    min_index, min_value = get_min_index_value(enumerate(largest))
    for i in itertools.islice(iterable, n, None):
        if i > min_value:
            largest[min_index] = i
            min_index, min_value = get_min_index_value(enumerate(largest))
    largest.sort()
    return largest


# 8 % slowdown for large iterables.
def nlargest_heapreplace2(n, iterable):
    """Return the n largest items in the given iterable."""
    # Uses the heapq.heapify structure for the list of largest numbers, to
    # replace the search for the minimal number at every turn. The search is
    # replaced by maintaining the heap invariant after insertion, which should
    # be a O(log n) operation rather than O(n) for an exhaustive search, with
    # the drawback of having to do more internal list element movements when
    # the new item is sifted into the structure.
    largest = iterable[:n]
    heapq.heapify(largest)
    push_larger = functools.partial(heapq.heapreplace, largest)
    for i in itertools.islice(iterable, n, None):
        if i > largest[0]:
            push_larger(i)
    largest.sort()
    return largest


# 29 % (!) slowdown for large iterables.
def nlargest_heappushpop2(n, iterable):
    """Return the n largest items in the given iterable."""
    # Like nlargest_heapreplace, but using the built-in heappushpop function
    # which only performs the addition of the new element in case it is larger
    # than the root (which is the smallest element). In practice, this offloads
    # the comparison to the heapq module. Performance takes a hit since there
    # is a function call for every item in the iterable.
    largest = iterable[:n]
    heapq.heapify(largest)
    push_larger = functools.partial(heapq.heappushpop, largest)
    for i in itertools.islice(iterable, n, None):
        push_larger(i)
    largest.sort()
    return largest


# 7 % slowdown for large iterables.
def nlargest_manual_heapreplace2(n, iterable):
    """Return the n largest items in the given iterable."""
    # A test using a "manual" heapq.heapreplace equivalent through its internal
    # heapq._siftup function. The idea is that this should avoid some extra
    # tests performed by heapq.heapreplace, but in practice the same tests are
    # performed by heapq._siftup, so there is generally no speedup.
    largest = iterable[:n]
    heapq.heapify(largest)
    siftup = functools.partial(heapq._siftup, largest, 0)
    for i in itertools.islice(iterable, n, None):
        if i > largest[0]:
            largest[0] = i
            siftup()
    largest.sort()
    return largest


# The functions with suffix "3" explicitly converts the incoming argument to an
# iterator, which is then consumed up to n before the loop is started. This
# keeps the idea of the "2" functions without resorting to itertools.islice().
# These versions are faster than the vanilla functions for small iterable sizes
# and seem to asymptotically approach them for large iterables, as expected.

def nlargest_list3(n, iterable):
    """Return the n largest items in the given iterable."""
    # Quite naïve method, keeping its own list of the n largest numbers at
    # every time and keeping track of the smallest item and its index in the
    # list for future replacement.
    iterator = iter(iterable)
    largest = [next(iterator) for i in range(n)]
    get_min_index_value = functools.partial(min, key=lambda x: x[1])
    min_index, min_value = get_min_index_value(enumerate(largest))
    for i in iterator:
        if i > min_value:
            largest[min_index] = i
            min_index, min_value = get_min_index_value(enumerate(largest))
    largest.sort()
    return largest


def nlargest_heapreplace3(n, iterable):
    """Return the n largest items in the given iterable."""
    # Uses the heapq.heapify structure for the list of largest numbers, to
    # replace the search for the minimal number at every turn. The search is
    # replaced by maintaining the heap invariant after insertion, which should
    # be a O(log n) operation rather than O(n) for an exhaustive search, with
    # the drawback of having to do more internal list element movements when
    # the new item is sifted into the structure.
    iterator = iter(iterable)
    largest = [next(iterator) for i in range(n)]
    heapq.heapify(largest)
    push_larger = functools.partial(heapq.heapreplace, largest)
    for i in iterator:
        if i > largest[0]:
            push_larger(i)
    largest.sort()
    return largest


def nlargest_heappushpop3(n, iterable):
    """Return the n largest items in the given iterable."""
    # Like nlargest_heapreplace, but using the built-in heappushpop function
    # which only performs the addition of the new element in case it is larger
    # than the root (which is the smallest element). In practice, this offloads
    # the comparison to the heapq module. Performance takes a hit since there
    # is a function call for every item in the iterable.
    iterator = iter(iterable)
    largest = [next(iterator) for i in range(n)]
    heapq.heapify(largest)
    push_larger = functools.partial(heapq.heappushpop, largest)
    for i in iterator:
        push_larger(i)
    largest.sort()
    return largest


def nlargest_manual_heapreplace3(n, iterable):
    """Return the n largest items in the given iterable."""
    # A test using a "manual" heapq.heapreplace equivalent through its internal
    # heapq._siftup function. The idea is that this should avoid some extra
    # tests performed by heapq.heapreplace, but in practice the same tests are
    # performed by heapq._siftup, so there is generally no speedup.
    iterator = iter(iterable)
    largest = [next(iterator) for i in range(n)]
    heapq.heapify(largest)
    siftup = functools.partial(heapq._siftup, largest, 0)
    for i in iterator:
        if i > largest[0]:
            largest[0] = i
            siftup()
    largest.sort()
    return largest
