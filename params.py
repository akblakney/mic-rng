# contains methods used to read params from command line arguments

from my_exception import MyException


# args is args list
# target is string to search for in args list
# if target in args list, return the value set in args
# otherwise return the default value
def set_param_int(args, target, default_value):
    if not target in args:
        return default_value
    msg1 = 'The flag {} requires an integer argument. Try something like '.format(target)
    msg2 = '{} <int>'.format(target)
    msg = msg1 + msg2
    try:
        return int(args[args.index(target) + 1])
    except:
        raise MyException(msg)

def set_param_gen(args, target, default_value, msg):
    if not target in args:
        return default_value
    try:
        return args[args.index(target) + 1]
    except:
        raise MyException(msg)


# args is the args list
# target is string to search for in args list
# if target in list, return True, else False
def set_param_bool(args, target):
    return target in args
