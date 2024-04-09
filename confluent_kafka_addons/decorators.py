import time

from . import errors

class Retriable(object):
    """Hybrid decorator that implements a the Retry pattern with exponential backoff. 

    Waits $base**exp$ seconds before calling the decorated function 
    and returning the result.

    On error, the retry counter is incremented by one
    """

    def __init__(self, max_retries=10, upper_bound=6, base=2):
        """Instantiates and returns an instance of the Retriable decorator.

        Args:
            max_retries (int, optional): The maximum number of retries allowed. 
                Defaults to 10.

            upper_bound (int, optional): The upper limit for the exponent in 
                the exponential backoff calculation. This number must be less 
                than or equal to max_retries. Larger values cause more wait. 
                For example, with a base of 2, the largest wait time with the 
                exponential backoff algorithm would be 64 seconds or 
                approximately 1 minute. Defaults to 6.

            base (int, optional): The exponential backoff base. Smaller values 
                lead to less wait, larger values  more wait. Defaults to 2.
        """
        self.max_retries = max_retries
        self.upper_bound = upper_bound
        self.base = base
        self.retries = 0
        self.mode = "decorating"

    def __call__(self, *args, **kwargs):
        if self.mode == "decorating":
            self.func = args[0]
            self.mode = "calling"
            return self
        while self.retries < self.max_retries:
            try:
                if self.retries > self.upper_bound:
                    exp = self.upper_bound
                else:
                    exp = self.retries
                time.sleep(self.base*exp)
                return self.func(*args, **kwargs)
            except:
                self.max_retries += 1
        raise errors.RetriableException(self, args, kwargs)
