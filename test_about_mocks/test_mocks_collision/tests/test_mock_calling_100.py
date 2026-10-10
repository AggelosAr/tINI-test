from tini_test import Mock, Test, must_equal


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



def generated_function_0(a, p='1'):
    print('generated_function_0')
    return value_to_sum(a) + value_to_sum(p)



def generated_function_1(a, b, p=[3, 4], w={'a': 10}):
    print('generated_function_1')
    return value_to_sum(a) + value_to_sum(b) + value_to_sum(p) + value_to_sum(w)



def generated_function_2(a, b, p={'a': 10}, w=10):
    print('generated_function_2')
    return value_to_sum(a) + value_to_sum(b) + value_to_sum(p) + value_to_sum(w)



def generated_function_3(a, b, c, p='10', w=2.5):
    print('generated_function_3')
    return value_to_sum(a) + value_to_sum(b) + value_to_sum(c) + value_to_sum(p) + value_to_sum(w)



def generated_function_4(a, p=20):
    print('generated_function_4')
    return value_to_sum(a) + value_to_sum(p)



def generated_function_5(a, b, p=3.5):
    print('generated_function_5')
    return value_to_sum(a) + value_to_sum(b) + value_to_sum(p)



def generated_function_6(a, b, c, p={'a': 1, 'b': 2}):
    print('generated_function_6')
    return value_to_sum(a) + value_to_sum(b) + value_to_sum(c) + value_to_sum(p)



def generated_function_7(a, p=[3, 4], w={'a': 10}):
    print('generated_function_7')
    return value_to_sum(a) + value_to_sum(p) + value_to_sum(w)



def generated_function_8(a, b, c, p='1', w=1.5):
    print('generated_function_8')
    return value_to_sum(a) + value_to_sum(b) + value_to_sum(c) + value_to_sum(p) + value_to_sum(w)



def generated_function_9(a, p=20):
    print('generated_function_9')
    return value_to_sum(a) + value_to_sum(p)



@Mock.mock(generated_function_2, args=(2.5, [5]), kwargs={'p': {'a': 10}})
@Mock.mock(generated_function_8, args=([5], {'a': 1, 'b': 2}, 20), kwargs={'p': '2', 'w': 2.5})
@Test.case()
def test_generated_0():
    must_equal(
        27.5 + 32.5,
        generated_function_2(3.5, [1, 2], p={'a': 1, 'b': 2}, w=2)
        + generated_function_8([1, 2], {'x': 3, 'y': 4}, 10, p='3', w=3.5)
    )




@Mock.mock(generated_function_1, args=('2', 1.5))
@Test.case()
def test_generated_1():
    must_equal(
        20.5,
        generated_function_1('1', 2.5, p=[1, 2], w={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_9, args=({'a': 1, 'b': 2},), kwargs={'p': 1})
@Test.case
def test_generated_2():
    must_equal(
        4,
        generated_function_9({'x': 3, 'y': 4}, p=2)
    )




@Mock.mock(generated_function_0, args=(2,), kwargs={'p': '1'})
@Test.case()
def test_generated_3():
    must_equal(
        3,
        generated_function_0(1, p='2')
    )




@Mock.mock(generated_function_3, args=([5], {'a': 1, 'b': 2}, 10), kwargs={'p': '1'})
@Test.case()
def test_generated_4():
    must_equal(
        21.5,
        generated_function_3([1, 2], {'x': 3, 'y': 4}, 3, p='2', w=2.5)
    )




@Mock.mock(generated_function_3, args=([1, 2], {'x': 3, 'y': 4}, 10), kwargs={'p': '1', 'w': 3.5})
@Mock.mock(generated_function_0, args=(3,), kwargs={'p': '2'})
@Test.case
def test_generated_5():
    must_equal(
        24.5 + 5,
        generated_function_3([3, 4], {'a': 10}, 3, p='2', w=1.5)
        + generated_function_0(2, p='3')
    )




@Mock.mock(generated_function_3, args=([3, 4], {'a': 10}, 10), kwargs={'p': '1', 'w': 1.5})
@Test.case
def test_generated_6():
    must_equal(
        29.5,
        generated_function_3([5], {'a': 1, 'b': 2}, 3, p='2', w=2.5)
    )




@Mock.mock(generated_function_8, args=([5], {'a': 1, 'b': 2}, 10))
@Test.case()
def test_generated_7():
    must_equal(
        20.5,
        generated_function_8([1, 2], {'x': 3, 'y': 4}, 3, p='1', w=2.5)
    )




@Mock.mock(generated_function_0, args=(2,))
@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},))
@Mock.mock(generated_function_6, args=('10', 1.5, [3, 4]))
@Test.case
def test_generated_8():
    must_equal(
        3 + 27 + 21.5,
        generated_function_0(1, p='1')
        + generated_function_4({'a': 10}, p=2)
        + generated_function_6('3', 2.5, [5], p={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},))
@Mock.mock(generated_function_1, args=('3', 1.5))
@Test.case()
def test_generated_9():
    must_equal(
        27 + 21.5,
        generated_function_4({'a': 10}, p=1)
        + generated_function_1('2', 2.5, p=[1, 2], w={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_8, args=([5], {'a': 1, 'b': 2}, 10), kwargs={'p': '1'})
@Mock.mock(generated_function_1, args=('3', 2.5), kwargs={'p': [3, 4]})
@Mock.mock(generated_function_7, args=(2.5,), kwargs={'p': [5]})
@Test.case
def test_generated_10():
    must_equal(
        20.5 + 22.5 + 17.5,
        generated_function_8([1, 2], {'x': 3, 'y': 4}, 3, p='2', w=2.5)
        + generated_function_1('2', 3.5, p=[5], w={'a': 10})
        + generated_function_7(3.5, p=[1, 2], w={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_1, args=('2', 2.5), kwargs={'p': [3, 4], 'w': {'a': 10}})
@Mock.mock(generated_function_5, args=(3, '10'))
@Test.case()
def test_generated_11():
    must_equal(
        21.5 + 16.5,
        generated_function_1('1', 3.5, p=[5], w={'a': 1, 'b': 2})
        + generated_function_5(2, '3', p=3.5)
    )




@Mock.mock(generated_function_7, args=(2.5,), kwargs={'p': [5]})
@Test.case()
def test_generated_12():
    must_equal(
        17.5,
        generated_function_7(3.5, p=[1, 2], w={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_1, args=('2', 1.5))
@Mock.mock(generated_function_4, args=({'a': 1, 'b': 2},), kwargs={'p': 2})
@Test.case
def test_generated_13():
    must_equal(
        20.5 + 5,
        generated_function_1('1', 2.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_4({'x': 3, 'y': 4}, p=3)
    )




@Mock.mock(generated_function_8, args=([1, 2], {'x': 3, 'y': 4}, 10), kwargs={'p': '1', 'w': 3.5})
@Mock.mock(generated_function_6, args=('3', 3.5, [1, 2]))
@Mock.mock(generated_function_9, args=({'a': 10},))
@Test.case
def test_generated_14():
    must_equal(
        24.5 + 12.5 + 30,
        generated_function_8([3, 4], {'a': 10}, 3, p='2', w=1.5)
        + generated_function_6('2', 1.5, [3, 4], p={'a': 10})
        + generated_function_9({'a': 1, 'b': 2}, p=3)
    )




@Mock.mock(generated_function_2, args=(2.5, [5]), kwargs={'p': {'a': 10}})
@Mock.mock(generated_function_0, args=(3,), kwargs={'p': '2'})
@Mock.mock(generated_function_6, args=('10', 2.5, [5]))
@Test.case()
def test_generated_15():
    must_equal(
        27.5 + 5 + 20.5,
        generated_function_2(3.5, [1, 2], p={'a': 1, 'b': 2}, w=2)
        + generated_function_0(2, p='3')
        + generated_function_6('3', 3.5, [1, 2], p={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_7, args=(3.5,), kwargs={'p': [1, 2], 'w': {'x': 3, 'y': 4}})
@Mock.mock(generated_function_2, args=(1.5, [3, 4]), kwargs={'p': {'x': 3, 'y': 4}})
@Mock.mock(generated_function_6, args=('10', 3.5, [1, 2]))
@Test.case()
def test_generated_16():
    must_equal(
        13.5 + 25.5 + 19.5,
        generated_function_7(1.5, p=[3, 4], w={'a': 10})
        + generated_function_2(2.5, [5], p={'a': 10}, w=3)
        + generated_function_6('3', 1.5, [3, 4], p={'a': 10})
    )




@Mock.mock(generated_function_3, args=([1, 2], {'x': 3, 'y': 4}, 10))
@Mock.mock(generated_function_8, args=([3, 4], {'a': 10}, 20), kwargs={'p': '2'})
@Test.case
def test_generated_17():
    must_equal(
        32.5 + 40.5,
        generated_function_3([3, 4], {'a': 10}, 3, p='1', w=3.5)
        + generated_function_8([5], {'a': 1, 'b': 2}, 10, p='3', w=1.5)
    )




@Mock.mock(generated_function_6, args=('2', 3.5, [1, 2]))
@Mock.mock(generated_function_0, args=(3,), kwargs={'p': '2'})
@Test.case
def test_generated_18():
    must_equal(
        11.5 + 5,
        generated_function_6('1', 1.5, [3, 4], p={'a': 10})
        + generated_function_0(2, p='3')
    )




@Mock.mock(generated_function_4, args=({'a': 10},))
@Test.case()
def test_generated_19():
    must_equal(
        30,
        generated_function_4({'a': 1, 'b': 2}, p=1)
    )




@Mock.mock(generated_function_2, args=(1.5, [3, 4]), kwargs={'p': {'x': 3, 'y': 4}, 'w': 2})
@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},))
@Test.case
def test_generated_20():
    must_equal(
        17.5 + 27,
        generated_function_2(2.5, [5], p={'a': 10}, w=3)
        + generated_function_4({'a': 10}, p=2)
    )




@Mock.mock(generated_function_6, args=('2', 3.5, [1, 2]))
@Mock.mock(generated_function_5, args=(3, '10'))
@Mock.mock(generated_function_9, args=({'a': 1, 'b': 2},), kwargs={'p': 3})
@Test.case()
def test_generated_21():
    must_equal(
        11.5 + 16.5 + 6,
        generated_function_6('1', 1.5, [3, 4], p={'a': 10})
        + generated_function_5(2, '3', p=1.5)
        + generated_function_9({'x': 3, 'y': 4}, p=10)
    )




@Mock.mock(generated_function_4, args=({'a': 10},), kwargs={'p': 1})
@Mock.mock(generated_function_1, args=('3', 2.5), kwargs={'p': [3, 4]})
@Test.case()
def test_generated_22():
    must_equal(
        11 + 22.5,
        generated_function_4({'a': 1, 'b': 2}, p=2)
        + generated_function_1('2', 3.5, p=[5], w={'a': 10})
    )




@Mock.mock(generated_function_4, args=({'a': 1, 'b': 2},))
@Mock.mock(generated_function_3, args=([3, 4], {'a': 10}, 20), kwargs={'p': '2', 'w': 1.5})
@Test.case
def test_generated_23():
    must_equal(
        23 + 40.5,
        generated_function_4({'x': 3, 'y': 4}, p=1)
        + generated_function_3([5], {'a': 1, 'b': 2}, 10, p='3', w=2.5)
    )




@Mock.mock(generated_function_9, args=({'x': 3, 'y': 4},), kwargs={'p': 1})
@Mock.mock(generated_function_1, args=('3', 1.5), kwargs={'p': [1, 2], 'w': {'x': 3, 'y': 4}})
@Mock.mock(generated_function_0, args=(10,), kwargs={'p': '3'})
@Test.case()
def test_generated_24():
    must_equal(
        8 + 14.5 + 13,
        generated_function_9({'a': 10}, p=2)
        + generated_function_1('2', 2.5, p=[3, 4], w={'a': 10})
        + generated_function_0(3, p='10')
    )




@Mock.mock(generated_function_6, args=('2', 1.5, [3, 4]), kwargs={'p': {'a': 1, 'b': 2}})
@Mock.mock(generated_function_1, args=('3', 2.5), kwargs={'p': [3, 4], 'w': {'a': 10}})
@Test.case()
def test_generated_25():
    must_equal(
        13.5 + 22.5,
        generated_function_6('1', 2.5, [5], p={'x': 3, 'y': 4})
        + generated_function_1('2', 3.5, p=[5], w={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_5, args=(2, '3'))
@Mock.mock(generated_function_7, args=(2.5,), kwargs={'p': [5], 'w': {'a': 1, 'b': 2}})
@Mock.mock(generated_function_6, args=('10', 1.5, [3, 4]))
@Test.case
def test_generated_26():
    must_equal(
        8.5 + 10.5 + 21.5,
        generated_function_5(1, '2', p=2.5)
        + generated_function_7(3.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_6('3', 2.5, [5], p={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_1, args=('2', 3.5), kwargs={'p': [5], 'w': {'a': 1, 'b': 2}})
@Mock.mock(generated_function_6, args=('3', 1.5, [3, 4]))
@Test.case()
def test_generated_27():
    must_equal(
        13.5 + 14.5,
        generated_function_1('1', 1.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_6('2', 2.5, [5], p={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_1, args=('2', 1.5), kwargs={'p': [1, 2], 'w': {'x': 3, 'y': 4}})
@Test.case
def test_generated_28():
    must_equal(
        13.5,
        generated_function_1('1', 2.5, p=[3, 4], w={'a': 10})
    )




@Mock.mock(generated_function_1, args=('2', 2.5), kwargs={'p': [3, 4]})
@Mock.mock(generated_function_2, args=(2.5, [5]))
@Mock.mock(generated_function_5, args=(10, '1'))
@Test.case()
def test_generated_29():
    must_equal(
        21.5 + 27.5 + 14.5,
        generated_function_1('1', 3.5, p=[5], w={'a': 10})
        + generated_function_2(3.5, [1, 2], p={'a': 10}, w=3)
        + generated_function_5(3, '10', p=1.5)
    )




@Mock.mock(generated_function_6, args=('2', 3.5, [1, 2]), kwargs={'p': {'a': 10}})
@Mock.mock(generated_function_2, args=(3.5, [1, 2]))
@Mock.mock(generated_function_1, args=('10', 2.5), kwargs={'p': [3, 4], 'w': {'a': 10}})
@Test.case()
def test_generated_30():
    must_equal(
        18.5 + 26.5 + 29.5,
        generated_function_6('1', 1.5, [3, 4], p={'a': 1, 'b': 2})
        + generated_function_2(1.5, [3, 4], p={'a': 1, 'b': 2}, w=3)
        + generated_function_1('3', 3.5, p=[5], w={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_7, args=(3.5,), kwargs={'p': [1, 2]})
@Test.case()
def test_generated_31():
    must_equal(
        16.5,
        generated_function_7(1.5, p=[3, 4], w={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_7, args=(1.5,), kwargs={'p': [3, 4], 'w': {'a': 10}})
@Mock.mock(generated_function_0, args=(3,), kwargs={'p': '2'})
@Mock.mock(generated_function_3, args=([5], {'a': 1, 'b': 2}, 1), kwargs={'p': '3', 'w': 2.5})
@Test.case
def test_generated_32():
    must_equal(
        18.5 + 5 + 14.5,
        generated_function_7(2.5, p=[5], w={'a': 1, 'b': 2})
        + generated_function_0(2, p='3')
        + generated_function_3([1, 2], {'x': 3, 'y': 4}, 20, p='10', w=3.5)
    )




@Mock.mock(generated_function_1, args=('2', 3.5), kwargs={'p': [5]})
@Mock.mock(generated_function_3, args=([5], {'a': 1, 'b': 2}, 20), kwargs={'p': '2'})
@Mock.mock(generated_function_7, args=(1.5,), kwargs={'p': [3, 4]})
@Test.case()
def test_generated_33():
    must_equal(
        20.5 + 32.5 + 18.5,
        generated_function_1('1', 1.5, p=[1, 2], w={'a': 1, 'b': 2})
        + generated_function_3([1, 2], {'x': 3, 'y': 4}, 10, p='3', w=2.5)
        + generated_function_7(2.5, p=[5], w={'a': 10})
    )




@Mock.mock(generated_function_7, args=(3.5,))
@Mock.mock(generated_function_1, args=('3', 2.5), kwargs={'p': [3, 4]})
@Mock.mock(generated_function_8, args=([3, 4], {'a': 10}, 1), kwargs={'p': '3'})
@Test.case
def test_generated_34():
    must_equal(
        20.5 + 22.5 + 22.5,
        generated_function_7(1.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_1('2', 3.5, p=[5], w={'a': 10})
        + generated_function_8([5], {'a': 1, 'b': 2}, 20, p='10', w=1.5)
    )




@Mock.mock(generated_function_6, args=('2', 2.5, [5]))
@Mock.mock(generated_function_2, args=(2.5, [5]))
@Test.case()
def test_generated_35():
    must_equal(
        12.5 + 27.5,
        generated_function_6('1', 3.5, [1, 2], p={'x': 3, 'y': 4})
        + generated_function_2(3.5, [1, 2], p={'a': 10}, w=3)
    )




@Mock.mock(generated_function_2, args=(2.5, [5]), kwargs={'p': {'a': 10}, 'w': 2})
@Mock.mock(generated_function_7, args=(3.5,), kwargs={'p': [1, 2], 'w': {'x': 3, 'y': 4}})
@Mock.mock(generated_function_8, args=([1, 2], {'x': 3, 'y': 4}, 1), kwargs={'p': '3', 'w': 3.5})
@Test.case
def test_generated_36():
    must_equal(
        19.5 + 13.5 + 17.5,
        generated_function_2(3.5, [1, 2], p={'a': 1, 'b': 2}, w=3)
        + generated_function_7(1.5, p=[3, 4], w={'a': 10})
        + generated_function_8([3, 4], {'a': 10}, 20, p='10', w=1.5)
    )




@Mock.mock(generated_function_4, args=({'a': 10},), kwargs={'p': 1})
@Mock.mock(generated_function_8, args=([1, 2], {'x': 3, 'y': 4}, 20), kwargs={'p': '2', 'w': 3.5})
@Mock.mock(generated_function_1, args=('10', 3.5))
@Test.case
def test_generated_37():
    must_equal(
        11 + 35.5 + 30.5,
        generated_function_4({'a': 1, 'b': 2}, p=2)
        + generated_function_8([3, 4], {'a': 10}, 10, p='3', w=1.5)
        + generated_function_1('3', 1.5, p=[5], w={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_2, args=(1.5, [3, 4]), kwargs={'p': {'x': 3, 'y': 4}, 'w': 2})
@Mock.mock(generated_function_8, args=([3, 4], {'a': 10}, 20))
@Test.case()
def test_generated_38():
    must_equal(
        17.5 + 39.5,
        generated_function_2(2.5, [5], p={'a': 10}, w=3)
        + generated_function_8([5], {'a': 1, 'b': 2}, 10, p='2', w=1.5)
    )




@Mock.mock(generated_function_2, args=(2.5, [5]))
@Test.case
def test_generated_39():
    must_equal(
        27.5,
        generated_function_2(3.5, [1, 2], p={'a': 10}, w=2)
    )




@Mock.mock(generated_function_1, args=('2', 1.5), kwargs={'p': [1, 2]})
@Mock.mock(generated_function_6, args=('3', 2.5, [5]))
@Test.case()
def test_generated_40():
    must_equal(
        16.5 + 13.5,
        generated_function_1('1', 2.5, p=[3, 4], w={'x': 3, 'y': 4})
        + generated_function_6('2', 3.5, [1, 2], p={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_3, args=([1, 2], {'x': 3, 'y': 4}, 10), kwargs={'p': '1'})
@Mock.mock(generated_function_6, args=('3', 3.5, [1, 2]), kwargs={'p': {'a': 10}})
@Test.case
def test_generated_41():
    must_equal(
        23.5 + 19.5,
        generated_function_3([3, 4], {'a': 10}, 3, p='2', w=3.5)
        + generated_function_6('2', 1.5, [3, 4], p={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_8, args=([3, 4], {'a': 10}, 10), kwargs={'p': '1'})
@Test.case()
def test_generated_42():
    must_equal(
        29.5,
        generated_function_8([5], {'a': 1, 'b': 2}, 3, p='2', w=1.5)
    )




@Mock.mock(generated_function_6, args=('2', 1.5, [3, 4]), kwargs={'p': {'a': 1, 'b': 2}})
@Test.case()
def test_generated_43():
    must_equal(
        13.5,
        generated_function_6('1', 2.5, [5], p={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_5, args=(2, '3'))
@Mock.mock(generated_function_7, args=(2.5,))
@Test.case
def test_generated_44():
    must_equal(
        8.5 + 19.5,
        generated_function_5(1, '2', p=2.5)
        + generated_function_7(3.5, p=[5], w={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},))
@Mock.mock(generated_function_5, args=(3, '10'))
@Test.case
def test_generated_45():
    must_equal(
        27 + 16.5,
        generated_function_4({'a': 10}, p=1)
        + generated_function_5(2, '3', p=1.5)
    )




@Mock.mock(generated_function_0, args=(2,), kwargs={'p': '1'})
@Mock.mock(generated_function_6, args=('3', 2.5, [5]))
@Mock.mock(generated_function_2, args=(2.5, [5]), kwargs={'p': {'a': 10}})
@Test.case
def test_generated_46():
    must_equal(
        3 + 13.5 + 27.5,
        generated_function_0(1, p='2')
        + generated_function_6('2', 3.5, [1, 2], p={'x': 3, 'y': 4})
        + generated_function_2(3.5, [1, 2], p={'a': 1, 'b': 2}, w=10)
    )




@Mock.mock(generated_function_0, args=(2,))
@Mock.mock(generated_function_8, args=([3, 4], {'a': 10}, 20), kwargs={'p': '2'})
@Test.case()
def test_generated_47():
    must_equal(
        3 + 40.5,
        generated_function_0(1, p='1')
        + generated_function_8([5], {'a': 1, 'b': 2}, 10, p='3', w=1.5)
    )




@Mock.mock(generated_function_8, args=([3, 4], {'a': 10}, 10))
@Test.case()
def test_generated_48():
    must_equal(
        29.5,
        generated_function_8([5], {'a': 1, 'b': 2}, 3, p='1', w=1.5)
    )




@Mock.mock(generated_function_3, args=([5], {'a': 1, 'b': 2}, 10))
@Test.case
def test_generated_49():
    must_equal(
        30.5,
        generated_function_3([1, 2], {'x': 3, 'y': 4}, 3, p='1', w=2.5)
    )




@Mock.mock(generated_function_2, args=(1.5, [3, 4]))
@Mock.mock(generated_function_6, args=('3', 3.5, [1, 2]), kwargs={'p': {'a': 10}})
@Mock.mock(generated_function_5, args=(10, '1'))
@Test.case()
def test_generated_50():
    must_equal(
        28.5 + 19.5 + 14.5,
        generated_function_2(2.5, [5], p={'x': 3, 'y': 4}, w=2)
        + generated_function_6('2', 1.5, [3, 4], p={'a': 1, 'b': 2})
        + generated_function_5(3, '10', p=1.5)
    )




@Mock.mock(generated_function_9, args=({'x': 3, 'y': 4},), kwargs={'p': 1})
@Test.case
def test_generated_51():
    must_equal(
        8,
        generated_function_9({'a': 10}, p=2)
    )




@Mock.mock(generated_function_7, args=(3.5,))
@Mock.mock(generated_function_5, args=(3, '10'))
@Test.case
def test_generated_52():
    must_equal(
        20.5 + 16.5,
        generated_function_7(1.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_5(2, '3', p=2.5)
    )




@Mock.mock(generated_function_4, args=({'a': 1, 'b': 2},))
@Mock.mock(generated_function_3, args=([3, 4], {'a': 10}, 20), kwargs={'p': '2', 'w': 1.5})
@Test.case()
def test_generated_53():
    must_equal(
        23 + 40.5,
        generated_function_4({'x': 3, 'y': 4}, p=1)
        + generated_function_3([5], {'a': 1, 'b': 2}, 10, p='3', w=2.5)
    )




@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},))
@Test.case()
def test_generated_54():
    must_equal(
        27,
        generated_function_4({'a': 10}, p=1)
    )




@Mock.mock(generated_function_1, args=('2', 1.5))
@Mock.mock(generated_function_2, args=(1.5, [3, 4]), kwargs={'p': {'x': 3, 'y': 4}, 'w': 3})
@Mock.mock(generated_function_0, args=(10,), kwargs={'p': '3'})
@Test.case
def test_generated_55():
    must_equal(
        20.5 + 18.5 + 13,
        generated_function_1('1', 2.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_2(2.5, [5], p={'a': 10}, w=10)
        + generated_function_0(3, p='10')
    )




@Mock.mock(generated_function_9, args=({'a': 1, 'b': 2},), kwargs={'p': 1})
@Mock.mock(generated_function_1, args=('3', 3.5), kwargs={'p': [5], 'w': {'a': 1, 'b': 2}})
@Mock.mock(generated_function_8, args=([5], {'a': 1, 'b': 2}, 1))
@Test.case
def test_generated_56():
    must_equal(
        4 + 14.5 + 11.5,
        generated_function_9({'x': 3, 'y': 4}, p=2)
        + generated_function_1('2', 1.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_8([1, 2], {'x': 3, 'y': 4}, 20, p='3', w=2.5)
    )




@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},), kwargs={'p': 1})
@Mock.mock(generated_function_1, args=('3', 1.5), kwargs={'p': [1, 2]})
@Mock.mock(generated_function_8, args=([1, 2], {'x': 3, 'y': 4}, 1), kwargs={'p': '3', 'w': 3.5})
@Test.case
def test_generated_57():
    must_equal(
        8 + 17.5 + 17.5,
        generated_function_4({'a': 10}, p=2)
        + generated_function_1('2', 2.5, p=[3, 4], w={'x': 3, 'y': 4})
        + generated_function_8([3, 4], {'a': 10}, 20, p='10', w=1.5)
    )




@Mock.mock(generated_function_8, args=([5], {'a': 1, 'b': 2}, 10), kwargs={'p': '1', 'w': 2.5})
@Mock.mock(generated_function_6, args=('3', 2.5, [5]))
@Test.case
def test_generated_58():
    must_equal(
        21.5 + 13.5,
        generated_function_8([1, 2], {'x': 3, 'y': 4}, 3, p='2', w=3.5)
        + generated_function_6('2', 3.5, [1, 2], p={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_4, args=({'a': 1, 'b': 2},))
@Test.case()
def test_generated_59():
    must_equal(
        23,
        generated_function_4({'x': 3, 'y': 4}, p=1)
    )




@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},))
@Mock.mock(generated_function_0, args=(3,))
@Mock.mock(generated_function_2, args=(1.5, [3, 4]), kwargs={'p': {'x': 3, 'y': 4}, 'w': 10})
@Test.case
def test_generated_60():
    must_equal(
        27 + 4 + 25.5,
        generated_function_4({'a': 10}, p=1)
        + generated_function_0(2, p='2')
        + generated_function_2(2.5, [5], p={'a': 10}, w=20)
    )




@Mock.mock(generated_function_4, args=({'a': 10},))
@Mock.mock(generated_function_2, args=(1.5, [3, 4]), kwargs={'p': {'x': 3, 'y': 4}, 'w': 3})
@Test.case
def test_generated_61():
    must_equal(
        30 + 18.5,
        generated_function_4({'a': 1, 'b': 2}, p=1)
        + generated_function_2(2.5, [5], p={'a': 10}, w=10)
    )




@Mock.mock(generated_function_0, args=(2,), kwargs={'p': '1'})
@Mock.mock(generated_function_5, args=(3, '10'))
@Test.case
def test_generated_62():
    must_equal(
        3 + 16.5,
        generated_function_0(1, p='2')
        + generated_function_5(2, '3', p=3.5)
    )




@Mock.mock(generated_function_2, args=(2.5, [5]))
@Mock.mock(generated_function_6, args=('3', 1.5, [3, 4]))
@Test.case
def test_generated_63():
    must_equal(
        27.5 + 14.5,
        generated_function_2(3.5, [1, 2], p={'a': 10}, w=2)
        + generated_function_6('2', 2.5, [5], p={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_3, args=([5], {'a': 1, 'b': 2}, 10), kwargs={'p': '1'})
@Test.case
def test_generated_64():
    must_equal(
        21.5,
        generated_function_3([1, 2], {'x': 3, 'y': 4}, 3, p='2', w=2.5)
    )




@Mock.mock(generated_function_8, args=([1, 2], {'x': 3, 'y': 4}, 10), kwargs={'p': '1'})
@Test.case
def test_generated_65():
    must_equal(
        22.5,
        generated_function_8([3, 4], {'a': 10}, 3, p='2', w=3.5)
    )




@Mock.mock(generated_function_1, args=('2', 3.5), kwargs={'p': [5], 'w': {'a': 1, 'b': 2}})
@Test.case()
def test_generated_66():
    must_equal(
        13.5,
        generated_function_1('1', 1.5, p=[1, 2], w={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_6, args=('2', 1.5, [3, 4]))
@Test.case()
def test_generated_67():
    must_equal(
        13.5,
        generated_function_6('1', 2.5, [5], p={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_9, args=({'a': 1, 'b': 2},), kwargs={'p': 1})
@Mock.mock(generated_function_6, args=('3', 3.5, [1, 2]))
@Test.case
def test_generated_68():
    must_equal(
        4 + 12.5,
        generated_function_9({'x': 3, 'y': 4}, p=2)
        + generated_function_6('2', 1.5, [3, 4], p={'a': 10})
    )




@Mock.mock(generated_function_3, args=([3, 4], {'a': 10}, 10), kwargs={'p': '1'})
@Mock.mock(generated_function_0, args=(3,))
@Test.case
def test_generated_69():
    must_equal(
        30.5 + 4,
        generated_function_3([5], {'a': 1, 'b': 2}, 3, p='2', w=1.5)
        + generated_function_0(2, p='2')
    )




@Mock.mock(generated_function_4, args=({'a': 10},), kwargs={'p': 1})
@Test.case
def test_generated_70():
    must_equal(
        11,
        generated_function_4({'a': 1, 'b': 2}, p=2)
    )




@Mock.mock(generated_function_3, args=([1, 2], {'x': 3, 'y': 4}, 10))
@Mock.mock(generated_function_7, args=(2.5,))
@Test.case
def test_generated_71():
    must_equal(
        32.5 + 19.5,
        generated_function_3([3, 4], {'a': 10}, 3, p='1', w=3.5)
        + generated_function_7(3.5, p=[5], w={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_0, args=(2,))
@Mock.mock(generated_function_7, args=(3.5,), kwargs={'p': [1, 2]})
@Test.case()
def test_generated_72():
    must_equal(
        3 + 16.5,
        generated_function_0(1, p='1')
        + generated_function_7(1.5, p=[3, 4], w={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_9, args=({'a': 10},), kwargs={'p': 1})
@Mock.mock(generated_function_5, args=(3, '10'), kwargs={'p': 2.5})
@Mock.mock(generated_function_6, args=('10', 3.5, [1, 2]), kwargs={'p': {'a': 10}})
@Test.case()
def test_generated_73():
    must_equal(
        11 + 15.5 + 26.5,
        generated_function_9({'a': 1, 'b': 2}, p=2)
        + generated_function_5(2, '3', p=3.5)
        + generated_function_6('3', 1.5, [3, 4], p={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_3, args=([1, 2], {'x': 3, 'y': 4}, 10), kwargs={'p': '1'})
@Mock.mock(generated_function_5, args=(3, '10'), kwargs={'p': 3.5})
@Test.case()
def test_generated_74():
    must_equal(
        23.5 + 16.5,
        generated_function_3([3, 4], {'a': 10}, 3, p='2', w=3.5)
        + generated_function_5(2, '3', p=1.5)
    )




@Mock.mock(generated_function_6, args=('2', 3.5, [1, 2]), kwargs={'p': {'a': 10}})
@Mock.mock(generated_function_0, args=(3,))
@Mock.mock(generated_function_9, args=({'a': 1, 'b': 2},))
@Test.case()
def test_generated_75():
    must_equal(
        18.5 + 4 + 23,
        generated_function_6('1', 1.5, [3, 4], p={'a': 1, 'b': 2})
        + generated_function_0(2, p='2')
        + generated_function_9({'x': 3, 'y': 4}, p=3)
    )




@Mock.mock(generated_function_8, args=([5], {'a': 1, 'b': 2}, 10), kwargs={'p': '1', 'w': 2.5})
@Mock.mock(generated_function_9, args=({'a': 1, 'b': 2},))
@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},))
@Test.case
def test_generated_76():
    must_equal(
        21.5 + 23 + 27,
        generated_function_8([1, 2], {'x': 3, 'y': 4}, 3, p='2', w=3.5)
        + generated_function_9({'x': 3, 'y': 4}, p=2)
        + generated_function_4({'a': 10}, p=3)
    )




@Mock.mock(generated_function_2, args=(1.5, [3, 4]))
@Mock.mock(generated_function_9, args=({'x': 3, 'y': 4},))
@Test.case
def test_generated_77():
    must_equal(
        28.5 + 27,
        generated_function_2(2.5, [5], p={'x': 3, 'y': 4}, w=2)
        + generated_function_9({'a': 10}, p=2)
    )




@Mock.mock(generated_function_6, args=('2', 3.5, [1, 2]))
@Mock.mock(generated_function_4, args=({'a': 10},))
@Test.case
def test_generated_78():
    must_equal(
        11.5 + 30,
        generated_function_6('1', 1.5, [3, 4], p={'a': 10})
        + generated_function_4({'a': 1, 'b': 2}, p=2)
    )




@Mock.mock(generated_function_1, args=('2', 1.5))
@Mock.mock(generated_function_0, args=(3,), kwargs={'p': '2'})
@Test.case
def test_generated_79():
    must_equal(
        20.5 + 5,
        generated_function_1('1', 2.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_0(2, p='3')
    )




@Mock.mock(generated_function_6, args=('2', 2.5, [5]), kwargs={'p': {'x': 3, 'y': 4}})
@Mock.mock(generated_function_1, args=('3', 3.5), kwargs={'p': [5], 'w': {'a': 1, 'b': 2}})
@Test.case
def test_generated_80():
    must_equal(
        16.5 + 14.5,
        generated_function_6('1', 3.5, [1, 2], p={'a': 10})
        + generated_function_1('2', 1.5, p=[1, 2], w={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},), kwargs={'p': 1})
@Mock.mock(generated_function_0, args=(3,))
@Mock.mock(generated_function_5, args=(10, '1'), kwargs={'p': 2.5})
@Test.case()
def test_generated_81():
    must_equal(
        8 + 4 + 13.5,
        generated_function_4({'a': 10}, p=2)
        + generated_function_0(2, p='2')
        + generated_function_5(3, '10', p=3.5)
    )




@Mock.mock(generated_function_3, args=([5], {'a': 1, 'b': 2}, 10), kwargs={'p': '1'})
@Mock.mock(generated_function_6, args=('3', 2.5, [5]))
@Mock.mock(generated_function_7, args=(2.5,), kwargs={'p': [5]})
@Test.case
def test_generated_82():
    must_equal(
        21.5 + 13.5 + 17.5,
        generated_function_3([1, 2], {'x': 3, 'y': 4}, 3, p='2', w=2.5)
        + generated_function_6('2', 3.5, [1, 2], p={'x': 3, 'y': 4})
        + generated_function_7(3.5, p=[1, 2], w={'a': 1, 'b': 2})
    )




@Mock.mock(generated_function_9, args=({'a': 1, 'b': 2},))
@Mock.mock(generated_function_6, args=('3', 3.5, [1, 2]))
@Test.case
def test_generated_83():
    must_equal(
        23 + 12.5,
        generated_function_9({'x': 3, 'y': 4}, p=1)
        + generated_function_6('2', 1.5, [3, 4], p={'a': 10})
    )




@Mock.mock(generated_function_5, args=(2, '3'))
@Mock.mock(generated_function_7, args=(3.5,), kwargs={'p': [1, 2], 'w': {'x': 3, 'y': 4}})
@Test.case
def test_generated_84():
    must_equal(
        8.5 + 13.5,
        generated_function_5(1, '2', p=3.5)
        + generated_function_7(1.5, p=[3, 4], w={'a': 10})
    )




@Mock.mock(generated_function_5, args=(2, '3'), kwargs={'p': 1.5})
@Mock.mock(generated_function_6, args=('3', 2.5, [5]), kwargs={'p': {'x': 3, 'y': 4}})
@Test.case()
def test_generated_85():
    must_equal(
        6.5 + 17.5,
        generated_function_5(1, '2', p=2.5)
        + generated_function_6('2', 3.5, [1, 2], p={'a': 10})
    )




@Mock.mock(generated_function_4, args=({'a': 1, 'b': 2},), kwargs={'p': 1})
@Mock.mock(generated_function_3, args=([3, 4], {'a': 10}, 20), kwargs={'p': '2', 'w': 1.5})
@Mock.mock(generated_function_8, args=([5], {'a': 1, 'b': 2}, 1), kwargs={'p': '3', 'w': 2.5})
@Test.case()
def test_generated_86():
    must_equal(
        4 + 40.5 + 14.5,
        generated_function_4({'x': 3, 'y': 4}, p=2)
        + generated_function_3([5], {'a': 1, 'b': 2}, 10, p='3', w=2.5)
        + generated_function_8([1, 2], {'x': 3, 'y': 4}, 20, p='10', w=3.5)
    )




@Mock.mock(generated_function_5, args=(2, '3'))
@Mock.mock(generated_function_9, args=({'a': 10},), kwargs={'p': 2})
@Mock.mock(generated_function_3, args=([1, 2], {'x': 3, 'y': 4}, 1), kwargs={'p': '3'})
@Test.case()
def test_generated_87():
    must_equal(
        8.5 + 12 + 16.5,
        generated_function_5(1, '2', p=3.5)
        + generated_function_9({'a': 1, 'b': 2}, p=3)
        + generated_function_3([3, 4], {'a': 10}, 20, p='10', w=3.5)
    )




@Mock.mock(generated_function_9, args=({'a': 10},))
@Mock.mock(generated_function_6, args=('3', 2.5, [5]), kwargs={'p': {'x': 3, 'y': 4}})
@Mock.mock(generated_function_0, args=(10,))
@Test.case()
def test_generated_88():
    must_equal(
        30 + 17.5 + 11,
        generated_function_9({'a': 1, 'b': 2}, p=1)
        + generated_function_6('2', 3.5, [1, 2], p={'a': 10})
        + generated_function_0(3, p='3')
    )




@Mock.mock(generated_function_2, args=(1.5, [3, 4]), kwargs={'p': {'x': 3, 'y': 4}, 'w': 2})
@Mock.mock(generated_function_9, args=({'x': 3, 'y': 4},), kwargs={'p': 2})
@Mock.mock(generated_function_7, args=(3.5,))
@Test.case
def test_generated_89():
    must_equal(
        17.5 + 9 + 20.5,
        generated_function_2(2.5, [5], p={'a': 10}, w=3)
        + generated_function_9({'a': 10}, p=3)
        + generated_function_7(1.5, p=[1, 2], w={'x': 3, 'y': 4})
    )




@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},), kwargs={'p': 1})
@Mock.mock(generated_function_5, args=(3, '10'), kwargs={'p': 1.5})
@Mock.mock(generated_function_7, args=(1.5,))
@Test.case
def test_generated_90():
    must_equal(
        8 + 14.5 + 18.5,
        generated_function_4({'a': 10}, p=2)
        + generated_function_5(2, '3', p=2.5)
        + generated_function_7(2.5, p=[3, 4], w={'a': 10})
    )




@Mock.mock(generated_function_9, args=({'a': 10},))
@Mock.mock(generated_function_1, args=('3', 2.5), kwargs={'p': [3, 4], 'w': {'a': 10}})
@Mock.mock(generated_function_8, args=([3, 4], {'a': 10}, 1))
@Test.case
def test_generated_91():
    must_equal(
        30 + 22.5 + 20.5,
        generated_function_9({'a': 1, 'b': 2}, p=1)
        + generated_function_1('2', 3.5, p=[5], w={'a': 1, 'b': 2})
        + generated_function_8([5], {'a': 1, 'b': 2}, 20, p='3', w=1.5)
    )




@Mock.mock(generated_function_1, args=('2', 2.5), kwargs={'p': [3, 4], 'w': {'a': 10}})
@Mock.mock(generated_function_5, args=(3, '10'))
@Mock.mock(generated_function_9, args=({'a': 10},))
@Test.case
def test_generated_92():
    must_equal(
        21.5 + 16.5 + 30,
        generated_function_1('1', 3.5, p=[5], w={'a': 1, 'b': 2})
        + generated_function_5(2, '3', p=3.5)
        + generated_function_9({'a': 1, 'b': 2}, p=3)
    )




@Mock.mock(generated_function_8, args=([3, 4], {'a': 10}, 10))
@Test.case()
def test_generated_93():
    must_equal(
        29.5,
        generated_function_8([5], {'a': 1, 'b': 2}, 3, p='1', w=1.5)
    )




@Mock.mock(generated_function_9, args=({'a': 10},))
@Mock.mock(generated_function_6, args=('3', 2.5, [5]), kwargs={'p': {'x': 3, 'y': 4}})
@Test.case()
def test_generated_94():
    must_equal(
        30 + 17.5,
        generated_function_9({'a': 1, 'b': 2}, p=1)
        + generated_function_6('2', 3.5, [1, 2], p={'a': 10})
    )




@Mock.mock(generated_function_0, args=(2,))
@Mock.mock(generated_function_7, args=(2.5,), kwargs={'p': [5], 'w': {'a': 1, 'b': 2}})
@Mock.mock(generated_function_3, args=([5], {'a': 1, 'b': 2}, 1))
@Test.case
def test_generated_95():
    must_equal(
        3 + 10.5 + 21.5,
        generated_function_0(1, p='1')
        + generated_function_7(3.5, p=[1, 2], w={'x': 3, 'y': 4})
        + generated_function_3([1, 2], {'x': 3, 'y': 4}, 20, p='3', w=2.5)
    )




@Mock.mock(generated_function_6, args=('2', 3.5, [1, 2]), kwargs={'p': {'a': 10}})
@Mock.mock(generated_function_0, args=(3,))
@Mock.mock(generated_function_4, args=({'a': 1, 'b': 2},), kwargs={'p': 3})
@Test.case
def test_generated_96():
    must_equal(
        18.5 + 4 + 6,
        generated_function_6('1', 1.5, [3, 4], p={'a': 1, 'b': 2})
        + generated_function_0(2, p='2')
        + generated_function_4({'x': 3, 'y': 4}, p=10)
    )




@Mock.mock(generated_function_1, args=('2', 1.5), kwargs={'p': [1, 2], 'w': {'x': 3, 'y': 4}})
@Mock.mock(generated_function_0, args=(3,), kwargs={'p': '2'})
@Test.case()
def test_generated_97():
    must_equal(
        13.5 + 5,
        generated_function_1('1', 2.5, p=[3, 4], w={'a': 10})
        + generated_function_0(2, p='3')
    )




@Mock.mock(generated_function_5, args=(2, '3'), kwargs={'p': 2.5})
@Mock.mock(generated_function_3, args=([3, 4], {'a': 10}, 20))
@Mock.mock(generated_function_7, args=(3.5,), kwargs={'p': [1, 2], 'w': {'x': 3, 'y': 4}})
@Test.case()
def test_generated_98():
    must_equal(
        7.5 + 49.5 + 13.5,
        generated_function_5(1, '2', p=3.5)
        + generated_function_3([5], {'a': 1, 'b': 2}, 10, p='2', w=1.5)
        + generated_function_7(1.5, p=[3, 4], w={'a': 10})
    )




@Mock.mock(generated_function_4, args=({'x': 3, 'y': 4},), kwargs={'p': 1})
@Mock.mock(generated_function_3, args=([5], {'a': 1, 'b': 2}, 20), kwargs={'p': '2'})
@Mock.mock(generated_function_1, args=('10', 2.5), kwargs={'p': [3, 4]})
@Test.case
def test_generated_99():
    must_equal(
        8 + 32.5 + 29.5,
        generated_function_4({'a': 10}, p=2)
        + generated_function_3([1, 2], {'x': 3, 'y': 4}, 10, p='3', w=2.5)
        + generated_function_1('3', 3.5, p=[5], w={'a': 10})
    )


