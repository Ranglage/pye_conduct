import json


def exception_para_conduct(new_para: dict, hst_error: Exception, ExceptionClass, is_top=False):
    '''
    Append the error parameters of the new exception to the error parameters of the lower-level exception and structure them (in the form of a list of dictionaries, arranged from top to bottom), then pass them upward. When the error is already the top-level error, return the exception value without raising it again and directly proceed to the email sending process.
    Each usage of this function to pass exceptions needs to include the following code:
    import sys
    import os
    
    filename = os.path.basename(__file__)
    func_name = gf().f_code.co_name
    For usage within a class:
    func_name = self.__class__.__name__ + '.' + gf().f_code.co_name
    
    except_key = filename + '->' + func_name
    
    :param new_para: Parameters of the new error, format:
        {except_key: 'no para'}
        exception_para_conduct({except_key: {'a': a}}, e, Exception)
    :param hst_error: The caught exception
    :param ExceptionClass: The exception class to be raised
    :param is_top: Whether it is the top-level exception; if so, it needs to log, serialize, and persist the parameters, then proceed to the email error reporting process.
    :return:
    Example return value:
    [{"test_exception_para_conduct.py->test": {"a": 10}}, {"test_exception_para_conduct.py->test1": "no para", "except": "(\"1 isn't equal to 2\",)"}]
    The order is: top-level function -> bottom-level function
    '''
    assert isinstance(new_para, dict)
    assert isinstance(hst_error, Exception)
    his_para = []
    try:
        if len(hst_error.args) > 1:
            new_e_info = ', '.join(hst_error.args)
            hst_error = type(hst_error)(new_e_info)
        his_para = json.loads(hst_error.args[0])
    except (IndexError, json.JSONDecodeError):
        # The previous exception has no return value, or cannot be parsed
        his_para = []
        new_para['except'] = str(hst_error.args)
    except Exception as e:
        # The issues here are all related to JSON
        # Normally, the program should not reach this point
        # Correctly upload the previous error
        # exit1
        if is_top:
            return e.args[0]
        raise type(e)(e.args[0], type(e))
    finally:
        # exit2
        new_para['exception'] = hst_error.__class__.__name__
        total_para = json.dumps([new_para] + his_para)
        if is_top:
            return total_para
        raise ExceptionClass(total_para)
