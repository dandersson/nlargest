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

Some benchmarking images I looked at during this process:

* The two “native functions” plotted agains the `nlargest_*3` functions created for this task:
  ![elements_1e1__1e4_nlargest3](https://cloud.githubusercontent.com/assets/3901008/9471122/2f73282c-4b4f-11e5-8d68-90b6d4f62b52.png)

* As above, but plotted for more elements:
  ![elements_1e1__1e7_nlargest3](https://cloud.githubusercontent.com/assets/3901008/9471123/2f7f5ade-4b4f-11e5-8b62-8dedb083c1d9.png)

* `nlargest_*3` plotted against the initial `nlargest_*` ideas:
  ![elements_1e1__1e4_nlargest2_against_nlargest3](https://cloud.githubusercontent.com/assets/3901008/9471124/2fad2180-4b4f-11e5-95fc-b8bdbf6a4b30.png)

* `nlargest_*3` plotted against the initial `nlargest_*` ideas:
  ![elements_1e1__1e4_nlargest_against_nlargest3](https://cloud.githubusercontent.com/assets/3901008/9471121/2f64deac-4b4f-11e5-9920-3ea86cea8d8e.png)


License
-------
[Apache license, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
