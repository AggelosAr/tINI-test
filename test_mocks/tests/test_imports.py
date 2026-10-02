

def add_args_function(*args, k_val_1: int = 0, k_val_2: int = 0) -> int:
    return sum(args) + k_val_1 + k_val_2



def f1():
    print('f1 called')



def f2():
    print('f2 called')



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



def generated_function_16(a, b):
    print('generated_function_16')
    return value_to_sum(a) + value_to_sum(b)


def generated_function_17(a, b):
    print('generated_function_17')
    return value_to_sum(a) + value_to_sum(b)
