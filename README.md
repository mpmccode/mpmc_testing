# MPMC Tests
This directory contains the tests, test inputs, and test runner (`test.py`) for the MPMC program. This program should run fine on any modern python installation.

## How to write tests
Each test needs three files:

 - A *description file*, in the `tests/` directory, 
 - An *MPMC input file*, in the `inputs/` directory, and
 - A *pqr file*, also in the `inputs/` directory.
 
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
For comparisons, use `less` or `greater` as needed. These are respectively
equivalent to "less than" and "greater than."
If you want to find the LAST occurrence of your search string, use `search reverse` in your input. This 
is useful for testing properties at equilibrium or for tests that require simulations to be run for some
amount of time before the result we want will pop out.

### Input/PQR Files
If you're writing tests for MPMC, you should know what these are. Nonetheless, you can look at examples in `sample_configs/`  contained in the main `mpmc` directory if you want some inspiration.

### Running tests
The test runner expects the mpmc_testing directory to be inside the main `mpmc` directory, with
the `mpmc` executable itself being in `mpmc/build/`.

`mpmc` must be compiled for `Release` before running the tests. Just run `bash compile.sh` from
the MPMC directory root to accomplish this.
