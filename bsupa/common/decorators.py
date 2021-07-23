import traceback
from print_colors import cprint
# For testFunc
c = cprint()

# Static variable decorators
def static_variable(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def testFunc(someFunc):
    """
    Decorator used for custom testing
    """
    def insideCheck():
        if someFunc():
            c.prnt("Successful execution of %s"%someFunc.func_name, 'g')
            return True
        else:
            c.prnt("Failed execution of %s"%someFunc.func_name, 'r')
            return False

    return insideCheck

# If the function errs, then this logs the traceback
def logException(logI, logE, log_success):
    def wrap(f):
        def wrapperFunc(*args):
            try:
                f(*args)
                if log_success:
                    logI("Successful %s"%(f.__name__))
            except:
                logE("Failed %s\n-----------\n%s-----------"%(f.__name__, traceback.format_exc()))

        return wrapperFunc
    return wrap
