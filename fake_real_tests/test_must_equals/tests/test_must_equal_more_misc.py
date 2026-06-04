from small_test.context_manager import WillRaise
from small_test.misc.exceptions import (ComperatorWasNotProvided,
                                        ExpectedWasDifferentFromActual)
from small_test.must_equals import must_equal
from small_test.test_utils import Test

# These are actual seperate cases ....

@Test.case
def test_must_equal_different_objects() -> None:

    obj1 = 1
    obj2 = 'a'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: type mismatch
expected: <class 'int'>
actual:   <class 'str'>
''', str(context.exception))



@Test.case
def test_must_equal_different_objects_different_order() -> None:

    obj1 = 1
    obj2 = 'a'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: type mismatch
expected: <class 'int'>
actual:   <class 'str'>
''', str(context.exception))



@Test.case
def test_must_equal_alien_object() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

 
    obj1 = A(11)
    obj2 = A(21)

    with WillRaise(ComperatorWasNotProvided) as context:
        must_equal(obj1, obj2)

    must_equal('Unknown type encountered and a comperator was not provided.', str(context.exception))



@Test.case
def test_must_equal_alien_object_different_order() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

    obj1 = A(21)
    obj2 = A(11)

    with WillRaise(ComperatorWasNotProvided) as context:
        must_equal(obj1, obj2)

    must_equal('Unknown type encountered and a comperator was not provided.', str(context.exception))


@Test.case
def test_must_equal_alien_object_with_eq() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return self.a == other.a
        
    obj1 = A(11)
    obj2 = A(21)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equal_alien_object_with_eq_different_order() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return self.a == other.a
        
    obj1 = A(21)
    obj2 = A(11)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equal_alien_object_with_cumtom_comp() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

    def custom_comperator(a: A, b: A):
        return a.a == b.a
        
    obj1 = A(11)
    obj2 = A(21)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2, comperator=custom_comperator)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equal_alien_object_with_cumtom_comp_different_order() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

    def custom_comperator(a: A, b: A):
        return a.a == b.a
    
    obj1 = A(21)
    obj2 = A(11)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2, comperator=custom_comperator)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



@Test.case
def test_must_equals_auto_discovers_eq_and_returns_false_format_case() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return self.a == other.a
 
    obj1 = A(a=10)
    obj2 = A(a=20)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))



def cosmic_entropy_engine(v, seed=42):
    import hashlib
    import itertools
    import math
    import random
    from collections import deque
    random.seed(seed)

    class X:
        def __init__(self):
            ...

    # Generate a strange universe
    universe = {
        f'sector_{i}': {
            'mass': random.random() * 1000,
            'particles': [random.randint(-9999, 9999) for _ in range(random.randint(5, 20))]
        }
        for i in range(30)
    }

    value = v
    # Build a meaningless graph
    graph = {
        k: random.sample(list(universe.keys()), random.randint(1, 5))
        for k in universe
    }


    # Recursive nonsense
    def quantum_fold(x, depth):
        if depth <= 0:
            return x
        return quantum_fold(
            math.sin(x) + math.cos(x * depth) + depth,
            depth - 1
        )

    class Y:
        def __init__(self):
            ...

    # Rotate through sectors
    sector_queue = deque(universe.keys())

    for cycle in range(50):

        sector_queue.rotate(random.randint(-5, 5))
        current = sector_queue[0]

        values = universe[current]['particles']

        transformed = [
            quantum_fold(abs(v) % 100 + 1, 6)
            for v in values
        ]

        checksum = hashlib.sha256(
            ','.join(f'{x:.5f}' for x in transformed).encode()
        ).hexdigest()

        universe[current]['checksum'] = checksum

        # Pointless mutation
        if checksum[0] in 'abcdef':
            universe[current]['mass'] *= 1.03
        else:
            universe[current]['mass'] *= 0.97

        class Z:
            def __init__(self):
                ...

        # Random graph wandering
        visited = set()
        stack = [current]

        while stack and len(visited) < 10:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            neighbors = graph.get(node, [])

            stack.extend(
                random.sample(
                    neighbors,
                    min(len(neighbors), random.randint(0, len(neighbors)))
                )
            )

        # Build useless matrices
        matrix = [
            [
                ((i * j) ^ random.randint(0, 255)) % 97
                for j in range(12)
            ]
            for i in range(12)
        ]

        diagonal_energy = sum(matrix[i][i] for i in range(12))

        # Artificially expensive operation
        combinations = list(
            itertools.islice(
                itertools.combinations(range(20), 3),
                500
            )
        )

        entropy_score = sum(
            sum(combo) * random.random()
            for combo in combinations
        )

        universe[current]['entropy'] = entropy_score + diagonal_energy

    # Build an absurd report nobody uses
    report = []

    for name, info in sorted(universe.items()):

        signature = hashlib.md5(
            (
                name
                + str(info['mass'])
                + info.get('checksum', '')
            ).encode()
        ).hexdigest()

        report.append({
            'name': name,
            'signature': signature,
            'mass': round(info['mass'], 3),
            'entropy': round(info.get('entropy', 0), 3)
        })

    # for important in report:
    #     print(report)

    # Sort it for no reason
    report.sort(
        key=lambda x: (
            x['entropy'],
            len(x['signature']),
            x['mass']
        )
    )

    # More pointless processing
    ghost_value = 0

    for item in report:
        for ch in item['signature']:
            ghost_value ^= ord(ch)
            ghost_value = ((ghost_value << 1) | (ghost_value >> 7)) & 0xFF

    # Compute a number and immediately discard it
    _ = math.sqrt(ghost_value + 1) * math.pi

    # Return absolutely nothing
    return value



@Test.case
def test_must_equals_auto_discovers_truly_works_and_returns_true() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented

            return cosmic_entropy_engine(self.a==other.a)
 
    obj1 = A(a=10)
    obj2 = A(a=10)

    must_equal(obj1, obj2, comperator=A.__eq__)



@Test.case
def test_must_equals_auto_discovers_truly_works_and_returns_false() -> None:

    class A:

        def __init__(self, a: int) -> None:
            self.a = a

        def __eq__(self, other: object) -> bool:

            if not isinstance(other, A):
                return NotImplemented
            
            return cosmic_entropy_engine(self.a==other.a)
 
    obj1 = A(a=10)
    obj2 = A(a=20)

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(obj1, obj2)

    must_equal('''
ITEM: <Object A at %s> != <Object A at %s>
''' % (hex(id(obj1)), hex(id(obj2)), ), str(context.exception))
    


@Test.case
def test_must_equal_different_objects_bytes() -> None:

    expected = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    actual = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'

    with WillRaise(ExpectedWasDifferentFromActual) as context:
        must_equal(expected, actual)

    must_equal('''
ITEM: <Object bytes at %s> != <Object bytes at %s>
''' % (hex(id(expected)), hex(id(actual)), ), str(context.exception))
