#Runs MPMC tests as defined in the README

import os
import os.path
import re
import subprocess

class Test():
    def __init__(self):
        self.name = ""
        self.input_file = ""
        self.pqr = ""
        self.search_string = ""
        self.expected_result = None
        self.precision = None


#Get our params and strip newlines wherever they broke other code 

def read_test_parameters():
    tests = []
    tests_dir = 'tests'
    for test in os.listdir(tests_dir):
        path = tests_dir + "/" + test
        temp_test = Test()
        for line in open(path, "r"):
            if line[0] == '#':
                continue
            if re.search("name", line):
                temp_test.name = line.split(' ', 1)[1].strip()
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
            else:
                print "Found unsupported option in file ", path
                print line
        tests.append(temp_test)
    return tests


def check_result(test, answer):
    if test.precision == "exact":
        precision = 0.0
    else:
        precision = float(test.precision)

    CGREEN  = '\33[32m'
    CRED = '\033[91m'
    CEND = '\033[0m'
    if abs(float(answer) - float(test.expected_result)) <= precision:
        output = "Test " + test.name.strip() + " passed!"
        print CGREEN + output + CEND
    else:
        output = "Test " + test.name + " failed.\n"
        output += "Expected answer: " + test.expected_result + " with precision of " + str(
                precision) + "\n"
        output += "Actual answer: " + answer
        print  CRED + output + CEND


#Run the tests. We choose only the first match of a search string and find the
#first floating point number after the match as result due to how MPMC is built: we can't
#run 0 steps (i.e, output the initial system without outputting the first move after.)


def run_test(test):
    #TODO: generate these paths dynamically
    #exe is two directories up because when we cd down we're one dir further from the exe
    mpmc_exe = '../../build/mpmc'
    test_dir = 'inputs/'
    input_file = test.input_file
    cwd = os.getcwd()
    os.chdir(test_dir)
    out = subprocess.check_output([mpmc_exe, input_file])
    out = out.decode("ascii", errors="ignore")
    #stole this next line from SO, I can't read regex yet so all I know is it gets the numbers from the goop
    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    #probably doesn't need to be done each time this function is called
    rx = re.compile(numeric_const_pattern, re.VERBOSE)
    for line in out.splitlines():
        term = test.search_string
        if term in line:
            result = rx.findall(line)[0]
            break
    check_result(test, result)
    os.chdir(cwd)


#remove garbage in case the test writer forgets to redirect MPMC output to /dev/null in their input script
def cleanup():
    test_dir = 'inputs/'
    cwd = os.getcwd()
    os.chdir(test_dir)
    #using shell=True is a bit dangerous here, but it's the only way (as far as I can tell) to
    #have subprocess evaluate wildcards properly -L 
    subprocess.call("rm *.dat *.last *.restart.* *.traj* *.energy* *.final*", shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    os.chdir(cwd)

def main():
    tests = read_test_parameters()
    for test in tests:
        run_test(test)
    cleanup()#clean up, everybody clean up!


if __name__ == '__main__':
    main()
