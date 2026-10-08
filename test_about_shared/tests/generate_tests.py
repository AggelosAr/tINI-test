from itertools import combinations, permutations

HEADERS = '''
from tini_test.test_utils import Test
from tini_test.mock import Mock
from tini_test.shared import SharedVar, Shared, var, NotInitialized
from tini_test.must_equals import must_equal

'''

body = '''
def test_function_%d():
    must_equal(True, True)
'''



test = ['@Test.case', '@Test.case()']
mock = ['@Mock.mock', '@Mock.mock()']
shared = ['@Shared', '@Shared()']

# extra_shared = [
#     '@Shared(var.a)', 
#     '@Shared(var.a, var.b_b)', 
#     '@Shared(var.a, var.b_b, var.c_c_c)'
# ]

all_permutations = []


for t in test:
    base = [t]

    for s in shared:

        base.append(s)
        all_permutations.extend(permutations(base))

        for m in mock:

            base.append(m)
            all_permutations.extend(permutations(base))
            base.pop()
        base.pop()


       
# for extra_share in extra_shared:
    # all_permutations.extend(permutations([*base, extra_share]))



print(len(all_permutations))
with open('test_decorator_schema.py', 'w') as f:
    f.write(HEADERS)
    f.write('\n')
    f.write('\n')
    f.write('\n')

    for i, p in enumerate(all_permutations, start=2400):
        f.write('\n'.join(p))
        f.write(body % i)
        
        f.write('\n')
        f.write('\n')



# import time


# def empty():
#     pass

# start = time.perf_counter()

# for _ in range(len(all_permutations)):
#     empty()

# end = time.perf_counter()

# print(f"Time taken: {end - start:.9f} seconds")
# print(f"Time taken: {(end - start) * 1000:.6f} ms")