# MPMC Tests
This repository contains the tests, test inputs, and test runner (`test.py`) 
for [MPMC](https://github.com/mpmccode/mpmc).

The only dependencies are Python 3.6, and, of course, MPMC itself.
### How to Write Tests
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

`example.inp` and `example.pqr` are both in the `inputs/` directory, as noted 
above.

### Notes on Test Options
A `precision` of `exact` is the same as setting the precision to `0.0`.

For comparisons, use `less`(<), `lesser`(<=), `more`(>), or `greater`(>=) as 
needed.

If you want to find the LAST occurrence of your search string, use `search 
reverse` in your input. This 
is useful for testing properties at equilibrium.

### Running Tests
The test runner expects the `mpmc_testing` directory to be inside the main 
`mpmc` directory, with
the `mpmc` executable itself being in `mpmc/build/`.

`mpmc` must be compiled for `Release` before running the tests. Just run `bash 
compile.sh` from
the MPMC directory root to accomplish this.

Then, from the `mpmc_testing` directory: `python3 run_tests.py`

### Running Tests in Parallel
`mpmc_testing` supports running tests in parallel using Python's
[joblib](https://pypi.org/project/joblib/) library. Use `pip3 install joblib` 
(with appropriate
flags as necessary for your environment) to get access to it.

### Canaries
`mpmc_testing` comes with a few "canary" tests which are intended to always 
fail. These are there as checks 
on `run_tests.py` itself and so are not ran by default. To use them, supply 
`canaries` as an argument to the
script.

### Testing All MPMC Commits
(Only tested on USF's CIRCE Cluster; please edit `test_all_commits.sh` to make 
sure it works on your environment.)
The provided script (`test_all_commits.sh`) runs the test suite on the MPMC 
commits in a file,
mpmc_commits.txt. To generate this file, `cd` into your local MPMC install, and 
then:

    git rev-list master > mpmc_commits.txt

We recommend copying `test_all_commits.sh` and `mpmc_commits.txt` into your 
home directory, and
then run `bash test_all_commits.sh`. This will execute two `git clone`s and run 
the entire
test suite for each MPMC commit; expect it to take some time.

