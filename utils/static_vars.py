def static_vars(**kwargs):
    """Define static variables for a decorated function."""
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate