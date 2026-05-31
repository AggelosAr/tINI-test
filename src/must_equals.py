import difflib


def must_equal(a, b) -> None:

    if a != b:
        a_str = str(a).splitlines(keepends=True)
        b_str = str(b).splitlines(keepends=True)

        diff = ''.join(
            difflib.unified_diff(
                a_str,
                b_str,
                fromfile='actual',
                tofile='expected',
            )
        )

        raise AssertionError(
            f'Values are not equal:\n{diff}'
        )
   