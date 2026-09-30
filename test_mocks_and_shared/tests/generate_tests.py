
import os
from itertools import permutations

headers = '''
from test_mocks_and_shared.tests.test_imports import add_args_function
from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test
'''


items = [
    '@Test.case',
    '@Mock.mock',
    '@Mock.mock()',
    '@Mock.mock(add_args_function, args=(1,))',
]


body = '''
def test_order_works_%s():
    must_equal(1, add_args_function(100))
    print('works')

'''


# TODO add more variants of mock and test decorator(s)

if __name__ == "__main__":
    all_arrangements = list(permutations(items))

    tests = []
    for idx, arrangement in enumerate(all_arrangements):
        test = '%s%s' % ('\n'.join(arrangement), body % (idx,), )
        # print(test)
        tests.append(test)


    with open(os.path.join(os.getcwd(), 'test_ordering_of_mock_with_test.py'), 'w') as f:
        f.write(headers)
        f.write('\n\n')
        f.write('\n\n'.join(tests))