from .static_vars import static_vars

@static_vars(is_verbose=False)
def log(*args, **kwargs):
    """Print each argument to stdout if `is_verbose` is true."""
    end = '\n'
    if 'is_verbose' in kwargs:
        log.is_verbose = kwargs['is_verbose']
    if 'end' in kwargs:
        end = kwargs['end']
    if log.is_verbose:
        for arg in args:
            print(arg, end=end)