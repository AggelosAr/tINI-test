
import os
from itertools import permutations

# TODO add more variants of mock and test decorator(s)

headers = '''
# from test_mocks_and_shared.tests.test_imports import add_args_function
from tini_test.mock import Mock
# from tini_test.must_equals import must_equal
from tini_test.test_utils import Test
'''


body = '''
def test_order_works_%s():
    print('works')

'''

def save_tests(name: str, tests: list):
    with open(os.path.join(os.getcwd(), name), 'w') as f:
        f.write(headers)
        f.write('\n\n')
        f.write('\n\n'.join(tests))



def get_body_from_arrangement(arrangement: list, idx: int) -> str:
    return ('%s%s' 
            % (
                '\n'.join(arrangement), 
                body % (idx,), 
                )
            )


def generate_incremental_tests():

    tests = []

    idx = 0
    
    for root in ['@Test.case', '@Test.case()', ]:

        for base in ['@Mock.mock', '@Mock.mock()', ]:
            
            current = [root, base]    
            all_arrangements = list(permutations(current))

            for arrangement in all_arrangements:
                test = get_body_from_arrangement(arrangement, idx)
                tests.append(test)
                idx += 1


    for root in ['@Test.case', '@Test.case()', ]:
    
        for base in ['@Mock.mock', '@Mock.mock()', ]:
            
            more = ['@Mock.mock()', '@Mock.mock', ]

            current = [root, base]    

            while more:

                current.append(more.pop())
                
                all_arrangements = list(permutations(current))

                for arrangement in all_arrangements:
                    test = get_body_from_arrangement(arrangement, idx)
                    tests.append(test)
                    idx += 1


    name = 'test_ordering_of_mock_with_test_%d.py' % (len(tests), )
    save_tests(name, tests)





if __name__ == "__main__":

    # generate_incremental_tests()
    ...

