import sys
def trace(frame, event, arg):
    if event == "call":
        filename = frame.f_code.co_filename
        if filename == "path/to/myfile.py":
            lineno = frame.f_lineno
            # Here I'm printing the file and line number,
            # but you can examine the frame, locals, etc too.
            print(f"{filename} @ {lineno}")
    return trace
sys.settrace(trace)
call_my_function()
sys.settrace(None)