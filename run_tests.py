#!/usr/bin/python3

"""
Runs MPMC tests as defined in the README
"""

import os
import os.path
import re
import subprocess
import sys
import time
import multiprocessing
import argparse

RUN_PARALLEL = True
try:
    import joblib
except ImportError:
    RUN_PARALLEL = False


class Test:
    def __init__(self):
        self.name = ""
        self.folder = ""
        self.input_file = ""
        self.pqr = ""
        self.search_string = ""
        self.expected_result = None
        self.precision = None
        self.search = ""
        self.duration = 0.0
        self.start = None

    '''
    Run the test. We choose only the first match of a search string and find the
    first floating point number after the match as result due to how MPMC is built: we can't
    run 0 steps (i.e, output the initial system without outputting the first move after.)
    '''

    def run(self, args):
        if not args.canaries and "canary" in self.name:
            return self.duration
        # ok so what's the deal with this canary business? Basically, they're tests that should *always* fail
        # unless there's a bug in run_tests.py itself. The only person that would ever want them to run is
        # me, so we hide them for the good of the end user
        test_dir = 'inputs'
        input_file = self.input_file
        cwd = os.getcwd()
        os.chdir(test_dir)
        os.chdir(self.folder)
        mpmc_exe = '../../../build/mpmc'  # it should always be here
        self.start = time.perf_counter()
        try:
            out = subprocess.check_output([mpmc_exe, input_file])
        except subprocess.CalledProcessError:
            print("subprocess returned an error for test {}".format(self.name))
            os.chdir(cwd)
            return None
        _end = time.perf_counter()
        self.duration = round((_end - self.start), 3)

        out = out.decode("ascii", errors="ignore")
        # stole this next line from SO, I can't read regex yet so all I know is it gets the numbers from the goop
        numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
        # probably doesn't need to be done each time this function is called
        rx = re.compile(numeric_const_pattern, re.VERBOSE)
        output = out.splitlines()
        result = None
        if self.search == "reverse":
            output.reverse()
        for line in output:
            term = self.search_string
            if term in line:
                result = rx.findall(line)[0]
                break
        check_result(self, result)
        os.chdir(cwd)
        return self.duration


def read_test_parameters():
    tests = []
    tests_dir = 'tests'
    for test in os.listdir(tests_dir):
        path = tests_dir + "/" + test
        temp_test = Test()
        for line in open(path, "r"):
            if line[0] == '#' or line.isspace():
                continue
            if len(line.split()) == 1:
                print("Missing option or syntax error in this line:")
                print(line)
                exit(
                    1
                )  # don't try to handle groups of tests that include a broken one
            if re.search("name", line):
                temp_test.name = line.split(' ', 1)[1].strip()
            elif re.search("folder", line):
                temp_test.folder = line.split(' ', 1)[1].strip()
            elif re.search("input", line):
                temp_test.input_file = line.split(' ', 1)[1].strip()
            elif re.search("pqr", line):
                temp_test.pqr = line.split(' ', 1)[1]
            elif re.search("term", line):
                temp_test.search_string = line.split(' ', 1)[1].strip()
            elif re.search("output", line):
                temp_test.expected_result = line.split(' ', 1)[1].strip()
            elif re.search("precision", line):
                temp_test.precision = line.split(' ', 1)[1].strip()
            elif re.search("search", line):
                temp_test.search = line.split(' ', 1)[1].strip()
            else:
                print(f"Found unsupported option {line} in file {path}:")
                print(line)
        tests.append(temp_test)
    return tests


def test_passed(test):
    green = '\33[32m'
    end = '\033[0m'
    print(f"{green}Test {test.name.strip()} passed in {test.duration}s!{end}")


def test_failed(test, answer):
    red = '\033[91m'
    end = '\033[0m'
    output = "Test " + test.name + " failed in " + str(test.duration) + "s.\n"
    output += "Expected answer: " + test.expected_result
    if test.precision not in {"less", "more", "lesser",
                              "greater"}:  # numerical precision
        output += " with precision of " + str(test.precision)
    output += "\nActual answer: " + answer
    print(f"{red}{output}{end}")


'''
handle_non_exact_answer() deals with tests whose precision is not set to "exact"
or a numerical value.
return True if we handled a test with this function (i.e. test.precision was set
to an allowed non-"exact" value, false otherwise
'''


def handle_non_exact_answer(test, answer):
    if test.precision not in {"less", "more", "lesser", "greater"}:
        return False
    else:
        if test.precision == "less" and answer < test.expected_result:
            test_passed(test)
        elif test.precision == "more" and answer > test.expected_result:
            test_passed(test)
        elif test.precision == "lesser" and answer <= test.expected_result:
            test_passed(test)
        elif test.precision == "greater" and answer >= test.expected_result:
            test_passed(test)
        else:
            test_failed(test, answer)
    return True


def check_result(test, answer):
    if not handle_non_exact_answer(test, answer):
        delta = (float(answer) - float(test.expected_result))
        if test.precision == "exact":
            precision = 0.0
        else:
            precision = float(test.precision)

        if abs(delta) <= precision:
            test_passed(test)
        else:
            test_failed(test, answer)


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


@run_once
def check_mpmc_exists(executable):
    blue = '\033[94m'
    red = '\033[91m'
    end = '\033[0m'
    if os.path.isfile(os.path.realpath(executable)):
        print(f"{blue}MPMC executable found, continuing...{end}")
    else:
        print(
            f"{red}MPMC executable not found, halting program execution.{end}")
        sys.exit()

def make_test(test, args):
    return test.run(args)


def main():
    mpmc_exe = '../build/mpmc'  # it should always be here
    check_mpmc_exists(
        mpmc_exe)  # exit here if MPMC executable provided is not correct
    blue = '\033[94m'
    yellow = '\033[33m'
    end = '\033[0m'

    parser = argparse.ArgumentParser(description='Run MPMC Tests...')
    parser.add_argument(
        '--canaries',
        action='store_true',
        help='a flag to ask for the run_tests.py canaries to be ran',
        default=False)
    parser.add_argument(
        '--serial',
        action='store_true',
        help='force run_tests.py to run in serial',
        default=False)

    args = parser.parse_args()

    global RUN_PARALLEL
    if args.serial:
        RUN_PARALLEL = False

    tests = read_test_parameters()

    if RUN_PARALLEL:
        num_cores = multiprocessing.cpu_count()
        print(
            f"{yellow}Running tests in parallel with {num_cores} cores available...{end}"
        )
        jobs = joblib.Parallel(n_jobs=num_cores)(
            joblib.delayed(make_test)(test, args) for test in tests)
        total_time = round(sum((job if job!=None else 0.) for job in jobs), 3)
    else:
        print(f"{yellow}Running tests serially...{end}")
        for test in tests:
            make_test(test, args)
        total_time = round(sum(test.duration for test in tests), 3)

    print(f"{blue}All done! This run took {total_time} seconds.{end}")


if __name__ == '__main__':
    main()
