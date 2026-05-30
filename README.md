


cli tool 

can be used from the command line with 

small_test [-VERBOCITY] [-d | -f] [ -func ]

-d directory
-f file
-t specific test 

VERBOCITY
-NORMAL
-SORT
-MINIMAL
-MINIMAL_NO_STACK


This test framework ? was tested on it self

directory will be used as relative from terminal current dir

if directory is provided it will find all the tests in that dir and run them 
e.g. it will try to connect the current dir to the requested dir
edge case is that if multiple same nested sub dirs exists it will only collect one it finds


if test file is provided it will search the entire project for that test file
and run all the tests of that specific file
The test file can be given with or without the extension

if test is provided it will search the entire project for that sepecific test if not d or f is provided 
else it will search for the test file in all the project . in case multiple same test files exists it will only find the first one it finds
e.g. if you want to run only def testing_something(*args, **kwargs): ...
you should run something lke this -t testing_something

if no search flags are provided the test suite will search 
for all the tests in the current directory 


Discovery works as follows 

the files that have a prefix of <test_> and are python files 
thaty are inside a folder with the name <tests>

e.g.


small_test -NORMAL -d src/test_folder

small_test -SORT -f test_concurrency

small_test -MINIMAL -t function_that_tests_something


The test suite will collect functions that are decorated with <>

the decorator accepts at most 2 arguments which should be lambda with a setup or cleanup

The setup will wun before the test 
The cleanup will run after test finishes.

In case the setup or the main function fails and a setup is provided 
an attempt will be made to run the cleanup


Modes
-----

In NORMAL mode the full flow excecution of the test will be shown with details and stacktraces

In SORT mode the results will be shown in a sorted fashion and the failuer will appear last 
In NORMAL and SORT mode prints work isnide the functions calling.

In MINIMAL mode the tests will run and only the stacktraces of failed tests will be shown 
In MINIMAL_NO_STACK which is the same as MINIMAL mode there will be no stacktraces in case the test fails



GROUPS
------
...


ROADMAP
-------
# TODO add config for colors and maybe formatting
# TODO calculate coverage
# TODO update sort to sort based on category of failure instead of simple fail
# TODO make correclty failing tests to pass using small_test