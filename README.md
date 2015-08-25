nlargest – exploring different algorithms for finding the _n_ largest items in an iterable
==========================================================================================

Why?
----
I initially had a Python need for finding the lexically “largest” files in a directory with many files, and solved it by

1. reading the directory contents into a list with [`os.listdir`](https://docs.python.org/3/library/os.html#os.listdir) (currently waiting for [`os.scandir`](https://www.python.org/dev/peps/pep-0471/) coming in Python 3.5)
2. sorting this list
3. slicing out the last _n_ elements.

This was straightforward, but conceptually it did not quite feel right to have to sort the entire list, when many elements could be discarded immediately when only the largest _n_ were of interest.

I started to try different approaches and benchmarking these to see if there were any speed-ups to gain from different approaches. It was certainly “fast enough” already for my purposes, so the motivation was pure curiosity.

The included [`heapq.nlargest`](https://docs.python.org/3/library/heapq.html#heapq.nlargest) method from the native [`heapq` module](https://docs.python.org/3/library/heapq.html) initially seemed to be exactly what I was looking for, but digging through the implementation, it still felt like there should be a more efficient way. The [min-heap structure](https://en.wikipedia.org/wiki/Heap_(data_structure)) was certainly interesting to explore further in this context, though.

For picking the 5 largest numbers in the largest list tested, consisting of 10^7 randomly distributed positive integers, the times (on a certain computer) were distributed approximately like:

* initial naïve solution described above: 16.2 seconds
* `heapq.nlargest`: 1.56 seconds
* My fastest variation (`nlargest_list3`): 0.51 seconds

Note that the `heapq.nlargest` solution is expressed in native C code in the CPython interpreter, whereas `nlargest_list3` needs relatively slow Python function calls.


Outlook
-------
The performance difference is not that practically noticeable, and the use case is probably not that large. I will not pursue this matter further, but it was interesting to think about the problem and architect different solutions.

I might clean up the graphing solution I used to compare the solutions and include it in the repository; currently it is just a Matlab script to which I copy+pasted measurement data.


Benchmarking
------------
In the exploratory vein, I thought it would be interesting to use the CLI for the built-in [`timeit`](https://docs.python.org/3/library/timeit.html) module for this purpose. An advantage of the CLI (through `python3 -m timeit`) as compared to its Python interface is that the CLI automatically performs an adaptive amount of runs depending on run time length.

I wrote a small benchmarking program that reads parameters from a configuration file and performs testing on all functions with a certain prefix imported from a configurable module.


License
-------
[Apache license, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
