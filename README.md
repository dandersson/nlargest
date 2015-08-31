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
* `heapq.nlargest`: 1.53 seconds
* my fastest variation for this element count (`nlargest_list3`): 0.500 seconds

but there are large fluctuations between the algorithms depending on the number of input elements.

Note that the `heapq.nlargest` solution is expressed in native C code in the CPython interpreter, whereas `nlargest_list3` needs relatively slow Python function calls.


Outlook
-------
At a factor 3, the performance difference is not that practically noticeable, and the use case is probably not that large. I will not pursue this matter further, but it was interesting to think about the problem and architect different solutions.


Benchmarking
------------
In the exploratory vein, I thought it would be interesting to use the CLI for the built-in [`timeit`](https://docs.python.org/3/library/timeit.html) module for this purpose. An advantage of the CLI (through `python3 -m timeit`) as compared to its Python interface is that the CLI automatically performs an adaptive amount of runs depending on run time length.

I wrote a small benchmarking program that reads parameters from a configuration file and performs testing on all functions with a certain prefix imported from a configurable module.


Plotting
--------
I used [`matplotlib`](http://matplotlib.org/) to generate predefined comparison images. Scripts are included in the repository. Sample figures are shown below.

* Every tested function plotted at their full range. Not very readable (see later images for more clarity), but shown to illustrate the general tendencies.
  ![benchmark_output_2015-08-31_16_00_20__plot_all_series__axis_large](https://cloud.githubusercontent.com/assets/3901008/9583839/d0d09ea8-500d-11e5-8602-728cac6a642b.png)

* As above, but plotted to fewer elements.
  ![benchmark_output_2015-08-31_16_00_20__plot_all_series__axis_small](https://cloud.githubusercontent.com/assets/3901008/9583840/d0e3d928-500d-11e5-8447-e33dd4a00751.png)

* Comparison of initialization strategy 1 and 2 for the new functions.
  ![benchmark_output_2015-08-31_16_00_20__plot_init_1_against_init_2__axis_small](https://cloud.githubusercontent.com/assets/3901008/9583841/d0f6e20c-500d-11e5-83f9-7ac172ca2c29.png)

* Comparison of initialization strategy 1 and 3 for the new functions.
  ![benchmark_output_2015-08-31_16_00_20__plot_init_1_against_init_3__axis_small](https://cloud.githubusercontent.com/assets/3901008/9583843/d0fcafb6-500d-11e5-9488-d958564bf96e.png)

* Comparison of initialization strategy 2 and 3 for the new functions.
  ![benchmark_output_2015-08-31_16_00_20__plot_init_2_against_init_3__axis_small](https://cloud.githubusercontent.com/assets/3901008/9583844/d0fde57a-500d-11e5-8e63-c0d937afd6e0.png)

* Comparison of the reference functions and the new functions with initialization strategy 2.
  ![benchmark_output_2015-08-31_16_00_20__plot_ref_against_init_2__axis_small](https://cloud.githubusercontent.com/assets/3901008/9583842/d0fb0ec2-500d-11e5-9cf2-61e3559a594d.png)


License
-------
[Apache license, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
