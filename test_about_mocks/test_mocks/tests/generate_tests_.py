import os
import random

# ============================================================
# CONFIGURATION
# ============================================================

INCLUDE_ALL_REQUIRED_ARGS_IN_MOCK = True

ARG_NAMES = ['a', 'b', 'c', 'd', 'e']
KWARG_NAMES = ['p', 'w', 'x', 'y', 'z']
TYPES = ['int', 'str', 'float', 'list', 'dict']

TYPE_VALUES = {
    'int': [1, 2, 3, 10, 20],
    'str': ['1', '2', '3', '10'],
    'float': [1.5, 2.5, 3.5],
    'list': [[1, 2], [3, 4], [5]],
    'dict': [
        {'a': 1, 'b': 2},
        {'x': 3, 'y': 4},
        {'a': 10},
    ],
}


# ============================================================
# HELPERS
# ============================================================

def save_tests(name: str, tests: list):
    with open(os.path.join(os.getcwd(), name), 'w') as f:
        f.write('\n\n')
        f.write('\n\n'.join(tests))


def value_for_type(type_name, index=0):
    values = TYPE_VALUES[type_name]
    return values[index % len(values)]


def value_to_sum(value):
    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return value

    if isinstance(value, str):
        return int(value)

    if isinstance(value, list):
        return sum(value)

    if isinstance(value, dict):
        return sum(value.values())

    raise TypeError(value)


def expected_sum(values):
    return sum(value_to_sum(value) for value in values)


def different_value(type_name, original, seed):
    values = TYPE_VALUES[type_name]

    for offset in range(len(values) + 10):
        candidate = values[(seed + offset) % len(values)]

        if candidate != original:
            return candidate

    if type_name == 'int':
        return original + 100

    if type_name == 'float':
        return original + 100.5

    if type_name == 'str':
        return str(int(original) + 100)

    if type_name == 'list':
        return list(original) + [100]

    if type_name == 'dict':
        result = dict(original)
        result['_different'] = 100
        return result

    raise TypeError(type_name)


# ============================================================
# FUNCTION GENERATION
# ============================================================

def generate_function_metadata(index):
    name = 'generated_function_%d' % index

    positional_count = random.randint(1, 3)
    keyword_count = random.randint(0, 2)

    positional = []
    keyword = []

    for i in range(positional_count):
        arg_name = ARG_NAMES[i]
        type_name = TYPES[(index + i) % len(TYPES)]

        positional.append(
            (arg_name, type_name)
        )

    for i in range(keyword_count):
        arg_name = KWARG_NAMES[i]
        type_name = TYPES[
            (index + positional_count + i) % len(TYPES)
        ]

        default = value_for_type(
            type_name,
            index + i
        )

        keyword.append(
            (arg_name, type_name, default)
        )

    return {
        'name': name,
        'positional': positional,
        'keyword': keyword,
    }


def generate_function_definition(function):
    params = []

    for name, type_name in function['positional']:
        params.append(name)

    for name, type_name, default in function['keyword']:
        params.append(
            '%s=%r' % (name, default)
        )

    lines = []

    lines.append(
        'def %s(%s):' % (
            function['name'],
            ', '.join(params)
        )
    )

    lines.append(
        '    print(%r)' % function['name']
    )

    expressions = []

    for name, type_name in function['positional']:
        expressions.append(
            'value_to_sum(%s)' % name
        )

    for name, type_name, default in function['keyword']:
        expressions.append(
            'value_to_sum(%s)' % name
        )

    lines.append(
        '    return %s' % ' + '.join(expressions)
    )

    return '\n'.join(lines)


# ============================================================
# MOCK GENERATION
# ============================================================

def generate_mock(function, seed):
    """
    Generate mock values.

    When INCLUDE_ALL_REQUIRED_ARGS_IN_MOCK is True:
        Every required positional argument is included.

    When False:
        Required arguments may be partially omitted.
    """

    positional = function['positional']
    keyword = function['keyword']

    args = []
    kwargs = {}

    # --------------------------------------------------------
    # REQUIRED POSITIONAL ARGUMENTS
    # --------------------------------------------------------

    required_count = len(positional)

    if INCLUDE_ALL_REQUIRED_ARGS_IN_MOCK:
        # ALL required positional arguments must be mocked.
        positional_count = required_count
    else:
        # Allow partial mocking of required arguments.
        positional_count = random.randint(
            0,
            required_count
        )

    for index in range(positional_count):
        name, type_name = positional[index]

        args.append(
            value_for_type(
                type_name,
                seed + index + 1
            )
        )

    # --------------------------------------------------------
    # OPTIONAL / DEFAULT ARGUMENTS
    # --------------------------------------------------------

    if keyword:
        keyword_count = random.randint(
            0,
            len(keyword)
        )

        for index in range(keyword_count):
            name, type_name, default = keyword[index]

            kwargs[name] = value_for_type(
                type_name,
                seed + index + 20
            )

    # --------------------------------------------------------
    # GUARANTEE THAT THE MOCK IS NOT EMPTY
    # --------------------------------------------------------

    if not args and not kwargs:

        if positional:
            name, type_name = positional[0]

            args.append(
                value_for_type(
                    type_name,
                    seed + 1
                )
            )

        elif keyword:
            name, type_name, default = keyword[0]

            kwargs[name] = value_for_type(
                type_name,
                seed + 20
            )

    return args, kwargs


def render_mock(function, args, kwargs):
    pieces = []

    if args:
        pieces.append(
            'args=%r' % (tuple(args),)
        )

    if kwargs:
        pieces.append(
            'kwargs=%r' % (kwargs,)
        )

    if pieces:
        return '@Mock.mock(%s, %s)' % (
            function['name'],
            ', '.join(pieces)
        )

    return '@Mock.mock(%s)' % function['name']


# ============================================================
# EXPECTED RESULT
# ============================================================

def calculate_mock_expected(function, args, kwargs):
    """
    Calculate the effective value of the mocked function.

    Rules:

    1. Explicitly mocked positional values are used.
    2. Explicitly mocked keyword values are used.
    3. Missing optional/default arguments use their defaults.
    4. If INCLUDE_ALL_REQUIRED_ARGS_IN_MOCK is False and a
       required argument was omitted, it is NOT included in
       the expected value.
    """

    values = []

    # --------------------------------------------------------
    # Positional arguments
    # --------------------------------------------------------

    for index, (name, type_name) in enumerate(
        function['positional']
    ):
        if index < len(args):
            # Explicitly mocked.
            values.append(args[index])

        elif INCLUDE_ALL_REQUIRED_ARGS_IN_MOCK:
            # This should never happen in normal generation,
            # because all required args are included.
            raise ValueError(
                'Required argument %s was not mocked' % name
            )

        else:
            # Required argument intentionally omitted.
            #
            # It is NOT part of the mock expectation.
            continue

    # --------------------------------------------------------
    # Keyword/default arguments
    # --------------------------------------------------------

    for name, type_name, default in function['keyword']:

        if name in kwargs:
            # Explicitly mocked.
            values.append(kwargs[name])

        else:
            # Not mocked -> function default is used.
            values.append(default)

    return expected_sum(values)


# ============================================================
# ACTUAL FUNCTION CALL
# ============================================================

def generate_call(function, mock_args, mock_kwargs, seed):
    args_text = []
    kwargs_text = []

    # --------------------------------------------------------
    # Positional arguments
    # --------------------------------------------------------

    for index, (name, type_name) in enumerate(
        function['positional']
    ):

        if index < len(mock_args):

            # This argument was mocked.
            # Actual value must be different.
            actual_value = different_value(
                type_name,
                mock_args[index],
                seed + index + 100
            )

        else:

            # Not mocked.
            # Generate a normal actual value.
            actual_value = value_for_type(
                type_name,
                seed + index + 100
            )

        args_text.append(
            repr(actual_value)
        )

    # --------------------------------------------------------
    # Keyword/default arguments
    # --------------------------------------------------------

    for index, (name, type_name, default) in enumerate(
        function['keyword']
    ):

        if name in mock_kwargs:

            # Explicitly mocked.
            actual_value = different_value(
                type_name,
                mock_kwargs[name],
                seed + index + 200
            )

        else:

            # Not mocked.
            actual_value = value_for_type(
                type_name,
                seed + index + 200
            )

        kwargs_text.append(
            '%s=%r' % (
                name,
                actual_value
            )
        )

    arguments = args_text + kwargs_text

    return '%s(%s)' % (
        function['name'],
        ', '.join(arguments)
    )


# ============================================================
# TEST GENERATION
# ============================================================

def generate_test(functions, test_index):

    mock_count = random.randint(
        1,
        min(3, len(functions))
    )

    # Different function for every mock.
    mocked_functions = random.sample(
        functions,
        mock_count
    )

    decorators = []
    actual_calls = []
    expected_results = []

    for mock_index, function in enumerate(
        mocked_functions
    ):

        # ----------------------------------------------------
        # Generate mock
        # ----------------------------------------------------

        mock_args, mock_kwargs = generate_mock(
            function,
            test_index * 100 + mock_index
        )

        decorators.append(
            render_mock(
                function,
                mock_args,
                mock_kwargs
            )
        )

        # ----------------------------------------------------
        # Expected result
        # ----------------------------------------------------

        expected = calculate_mock_expected(
            function,
            mock_args,
            mock_kwargs
        )

        expected_results.append(
            expected
        )

        # ----------------------------------------------------
        # Actual call
        # ----------------------------------------------------

        actual_call = generate_call(
            function,
            mock_args,
            mock_kwargs,
            test_index * 1000 + mock_index
        )

        actual_calls.append(
            actual_call
        )

    # ========================================================
    # RENDER TEST
    # ========================================================

    lines = []

    # All mocks first.
    lines.extend(decorators)

    # Exactly one Test.case.
    lines.append(
        random.choice([
            '@Test.case',
            '@Test.case()'
        ])
    )

    lines.append(
        'def test_generated_%d():' % test_index
    )

    lines.append(
        '    must_equal('
    )

    expected_expression = ' + '.join(
        repr(value)
        for value in expected_results
    )

    lines.append(
        '        %s,' % expected_expression
    )

    actual_expression = '\n        + '.join(
        actual_calls
    )

    lines.append(
        '        %s' % actual_expression
    )

    lines.append(
        '    )'
    )

    return '\n'.join(lines)


# ============================================================
# COMPLETE TEST FILE
# ============================================================

def generate_incremental_tests(
    function_count=20,
    tests_per_function=20
):
    functions = []

    for index in range(function_count):
        functions.append(
            generate_function_metadata(index)
        )

    tests = []
    test_index = 0

    for _ in range(tests_per_function):

        for _ in range(function_count):

            test = generate_test(
                functions,
                test_index
            )

            tests.append(test)
            tests.append('\n')

            test_index += 1

    source = []

    # --------------------------------------------------------
    # value_to_sum
    # --------------------------------------------------------

    source.append(
        'def value_to_sum(value):'
    )

    source.append(
        '    if isinstance(value, int):'
    )
    source.append(
        '        return value'
    )

    source.append(
        '    if isinstance(value, float):'
    )
    source.append(
        '        return value'
    )

    source.append(
        '    if isinstance(value, str):'
    )
    source.append(
        '        return int(value)'
    )

    source.append(
        '    if isinstance(value, list):'
    )
    source.append(
        '        return sum(value)'
    )

    source.append(
        '    if isinstance(value, dict):'
    )
    source.append(
        '        return sum(value.values())'
    )

    source.append('')

    # --------------------------------------------------------
    # Generated functions
    # --------------------------------------------------------

    for function in functions:

        source.append(
            generate_function_definition(function)
        )

        source.append('')

    # --------------------------------------------------------
    # Generated tests
    # --------------------------------------------------------

    source.extend(tests)

    name = (
        'test_mock_calling_%d.py'
        % test_index
    )

    save_tests(
        name,
        ['\n\n'.join(source)]
    )


# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':

    generate_incremental_tests(
        function_count=25,
        tests_per_function=25
    )
