import socket

from contextlib import contextmanager


@contextmanager
def socketcontext(*args, **kwds):
    """
    Context manager for the UDP client.

    args:
        args follow from socket documentation

    kwds:
        kwds follow from socket documentation

    """
    grab = lambda x: socket.__dict__[kwds[x]]

    skwds = {kwd:grab(kwd) for kwd in kwds}

    s = socket.socket(*args,**skwds)
    try:
        yield s
    except:
        pass ## Not sure what type of errors can happen here
    finally:
        s.close()


if __name__ == "__main__":
    
    pass
