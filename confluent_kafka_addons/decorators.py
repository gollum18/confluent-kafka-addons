import threading
import time

from . import constants
from . import errors

class Retriable(object):
    """Hybrid decorator that implements the Retry pattern with exponential backoff. 

    Waits base**retries seconds before calling the decorated function 
    and returning the result.

    On error, the retry counter is incremented by one.

    This implementation is synchronous. The caller will be forced to wait 
    until the function completes successfully or a RetriableException is raised by the decorator. 
    """

    def __init__(self, 
                 max_retries: int=10, 
                 exponent_limit: int=6, 
                 base: int=2,
                 unit: constants.RetriableUnit=constants.RetriableUnit.SECONDS):
        """Instantiates and returns an instance of the Retriable decorator.

        Args:
            max_retries (int, optional): The maximum number of retries allowed. 
                Defaults to 10.
            exponent_limit (int, optional): The upper limit for the exponent in 
                the exponential backoff calculation. This number must be less 
                than or equal to max_retries. Larger values cause more wait. 
                For example, with a base of 2, the largest wait time with the 
                exponential backoff algorithm would be 64 seconds or 
                approximately 1 minute. Defaults to 6.
            base (int, optional): The exponential backoff base. Smaller values 
                lead to less wait, larger values  more wait. Defaults to 2.
            unit (constants.RetriableUnit): The unit for the wait period. 
                Defaults to constants.RetriableUnit.SECONDS.

        Raises:
            (errors.RetriableException): When the maximum number of retries
                has been exceeded.
        """
        if max_retries < 1:
            raise ValueError(
                "[confluent_kafka_addons.decorators.Retriable] - parameter "
                + "`max_retries` must be greater than or equal to one (1)!"
            )
        if exponent_limit > max_retries:
            raise ValueError(
                "[confluent_kafka_addons.decorators.Retriable] - parameter "
                + "`exponent_limit` must be less than or equal to parameter "
                + "`max_retries`!"
            )
        if base < 2:
            raise ValueError(
                "[confluent_kafka_addons.decorators.Retriable] - parameter "
                + "base must be greater than or equal to two (2)!"
            )
        self.max_retries = max_retries
        self.exponent_limit = exponent_limit
        self.base = base
        self.unit = unit
        self.retries = 0
        self.mode = "decorating"

    def __call__(self, *args, **kwargs):
        if self.mode == "decorating":
            self.func = args[0]
            self.mode = "calling"
            return self
        while self.retries <= self.max_retries:
            try:
                if self.retries > self.exponent_limit:
                    exp = self.exponent_limit
                else:
                    exp = self.retries
                if constants.RetriableUnit.is_seconds(self.unit):
                    sleep_period = self.base*exp
                elif constants.RetriableUnit.is_milliseconds(self.unit):
                    sleep_period = (self.base*exp) / 1000
                else:
                    raise ValueError(
                        "[decorators.Retriable] - parameter "
                        + f"'unit' must be one of {constants.RetriableUnit.format_str()}")
                time.sleep(sleep_period)
                return self.func(*args, **kwargs)
            except:
                self.retries += 1
        raise errors.RetriableException(self, args, kwargs)


class Timeout(object):
    """Hybrid decorator that implements the Timeout pattern. This is a extremely basic decorator that starts the target function in a threading.Thread object. It then joins against the thread and waits for the timeout.

    If the timeout occurred, an errors.TimeoutException is raised by the Timeout decorator.

    If you want to get values back out of the thread, a common pattern in Python is to pass in a mutable object such as a dictionary in the target functions argument or keywords arguments list and write to that.

    There are no return values from this decorator.
    """

    def __init__(self, timeout=30):
        self.mode = "decorating"
        self.timeout = timeout


    def __call__(self, *args, **kwargs):
        if self.mode == "decorating":
            self.func = args[0]
            self.mode = "calling"
            return self
        runner = threading.Thread(target=self.func,
                                  args=args,
                                  kwargs=kwargs)
        runner.start()
        runner.join(timeout=self.timeout)
        if runner.is_alive():
            raise errors.TimeoutException()
