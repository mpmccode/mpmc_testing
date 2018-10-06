# MPMC Tests
This repository contains the tests, test inputs, and test runner (`test.py`) for [MPMC](https://github.com/mpmccode/mpmc).

The only dependencies are Python 3, and, of course, MPMC itself.
### How to write tests
Each test needs three files:

 - A *description file* placed in the `tests/` directory, 
 - An *MPMC input file* placed in the `inputs/` directory, and
 - A *pqr file* also placed in the `inputs/` directory.
 
### Description Files 
 The following would be found in `tests/example.txt`:
 
    name example
    input example.inp
    pqr example.pqr
    term OUTPUT: example energy
    output 12345.6789
    precision exact

`example.inp` and `example.pqr` are both in the `inputs/` directory, as noted above.

### Notes on test options
A `precision` of `exact` is the same as setting the precision to `0.0`.

For comparisons, use `less`(<), `lesser`(<=), `more`(>), or `greater`(>=) as needed.

If you want to find the LAST occurrence of your search string, use `search reverse` in your input. This 
is useful for testing properties at equilibrium.

### Running tests
The test runner expects the `mpmc_testing` directory to be inside the main `mpmc` directory, with
the `mpmc` executable itself being in `mpmc/build/`.

`mpmc` must be compiled for `Release` before running the tests. Just run `bash compile.sh` from
the MPMC directory root to accomplish this.

Then, from the `mpmc_testing` directory: `python3 run_tests.py`

### Canaries
`mpmc_testing` comes with a few "canary" tests which are intended to always fail. These are there as checks 
on `run_tests.py` itself and so are not ran by default. To use them, supply `canaries` as an argument to the
script.
