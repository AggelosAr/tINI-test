

def add_args_function(*args, k_val_1: int = 0, k_val_2: int = 0) -> int:
    return sum(args) + k_val_1 + k_val_2


def proxy(*args, **kwargs):
    return 1_000_000


def f1():
    print('f1 called')


def f2():
    print('f2 called')

