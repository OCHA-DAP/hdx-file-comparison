#!/usr/bin/env python
# encoding: utf-8

"""A decorator, @run_with_timer, which limits the time a function can run for, raising an
exception if it exceeds that time.

Copied from:
https://towardsdatascience.com/limiting-a-python-functions-execution-time-using-a-decorator-and-multiprocessing-6fcfe01da6f8
By Chris Knorowski with a small modification: using multprocess instead of multiprocessing because
multiprocessing gives a "can't pickle" error.


Raises:
    TimeExceededException: _description_
    result: _description_

Returns:
    _type_ -- _description_
"""

import multiprocess
from functools import wraps


class TimeExceededException(Exception):
    pass


def function_runner(*args, **kwargs):
    """Used as a wrapper function to handle
    returning results on the multiprocessing side"""

    send_end = kwargs.pop("__send_end")
    function = kwargs.pop("__function")
    try:
        result = function(*args, **kwargs)
    except Exception as e:
        send_end.send(e)
        return
    send_end.send(result)


def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parameterized
def run_with_timer(func, max_execution_time):
    @wraps(func)
    def wrapper(*args, **kwargs):
        recv_end, send_end = multiprocess.Pipe(False)
        kwargs["__send_end"] = send_end
        kwargs["__function"] = func

        p = multiprocess.Process(target=function_runner, args=args, kwargs=kwargs)
        p.start()
        p.join(max_execution_time)
        if p.is_alive():
            p.terminate()
            p.join()
            raise TimeExceededException("Exceeded Execution Time")
        result = recv_end.recv()

        if isinstance(result, Exception):
            raise result

        return result

    return wrapper
