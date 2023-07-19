import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from uncertainty.utypes import *

def equals(o, e):
    if hasattr(o, 'uEquals'):
        func = getattr(o, 'uEquals')
        return func(e)
    elif hasattr(o, 'equals'):
        func = getattr(o, 'equals')
        return func(e)
    else:
        return o == e

def err_msg(o, e):
    return 'Obtained: ' + str(o) + ' | Expected: ' + str(e)

def t(o, e):
    r = equals(o, e)
    assert r.tobool(0.98) if is_ubool(r) else r, err_msg(o, e)