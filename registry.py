# registry.py

COMMANDS = {}


def register(name):
    def decorator(func_or_cls):
        # if isinstance(func_or_cls, type):
        #     COMMANDS[name] = func_or_cls()
        # else:
        #     COMMANDS[name] = func_or_cls
        # return func_or_cls
        COMMANDS[name] = func_or_cls
        return func_or_cls

    return decorator
