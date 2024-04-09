class RetriableException(Exception):
    def __init__(self, retriable, func_args, func_kwargs, *args):
        Exception.__init__(self, *args)
        self.retriable = retriable
        self.func_args = func_args
        self.func_kwargs = func_kwargs


class TimeoutException(Exception):
    def __init__(self, *args)
        Exception.__init__(self, *args)
