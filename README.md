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
Note that a `precision` of `exact` is the same as setting the precision to `0.0`. `example.inp` and `example.pqr` are both in the `inputs/` directory, as noted above.
### Input/PQR Files
If you're writing tests for MPMC, you should know what these are. Nonetheless, you can look at examples in `sample_configs/`  contained in the main `mpmc` directory if you want some inspiration.
