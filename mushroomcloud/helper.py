import inspect

def cname():
    ret_name = ""
    stack = inspect.stack()
    # Attach class name to the ret_name
    ret_name = type(stack[1][0].f_locals['self']).__name__
    for frame_info in stack:
        frame = frame_info[0]
        f_locals = frame.f_locals
        if "name" in f_locals.keys() and isinstance(f_locals["name"], str):
            ret_name = f_locals["name"] + "." + ret_name
    return ret_name
