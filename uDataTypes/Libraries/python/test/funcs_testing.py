import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

def equals(o, e):
    funcname = 'uEquals'
    if hasattr(o, funcname):
        func = getattr(o, funcname)
        return func(e)
    else:
        return o.equals(e)

def err_msg(o, e):
    return 'Obtained: ' + str(o) + ' | Expected: ' + str(e)

def t(o, e):
    assert equals(o, e).tobool(0.98), err_msg(o, e)