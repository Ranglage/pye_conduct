import os
from sys import _getframe as gf
from econduct import exception_para_conduct

filename = os.path.basename(__file__)


def test(a):
    func_name = gf().f_code.co_name
    except_key = filename + '->' + func_name
    try:
        test1()
    except Exception as e:
        exception_para_conduct({except_key: {'a': a}}, e, Exception)


def test1():
    func_name = gf().f_code.co_name
    except_key = filename + '->' + func_name
    try:
        assert 1 == 2, '1 isn\'t equal to 2'
    except Exception as e:
        exception_para_conduct({except_key: 'no para'}, e, Exception)


if __name__ == '__main__':
    try:
        test(10)
    except Exception as e:
        print(e.args[0])
