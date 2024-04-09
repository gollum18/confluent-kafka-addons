import time

import pytest

from confluent_kafka_addons import decorators, errors


def test_retriable_all_defaults():
    @decorators.Retriable()
    def _test_function(a: int, b: int) -> int:
        """Returns the sum of a and b.

        Args:
            a (int): The left operand.
            b (int): The right operand.

        Returns:
            int: The sum of a and b.
        """
        return a + b

    assert _test_function(2, 2) == 4


def test_retriable_backoff_one_retry():
    @decorators.Retriable(max_retries=1, exponent_limit=1)
    def _test_function():
        """Intentionally raises an Exception to trigger backoff.

        Raises:
            Exception: Raised when the function is called.
        """
        raise Exception

    pytest.raises(errors.RetriableException, _test_function)


def test_timeout_one_second():
    @decorators.Timeout(1)
    def _test_timeout():
        """Sleeps for two seconds to trigger an errors.TimeoutException."""
        time.sleep(2)

    pytest.raises(errors.TimeoutException, _test_timeout)


def test_timeout_one_second_callback():
    def _callback_func(*args, **kwargs):
        """Sets a `result` key in the `return_values` dict received from
        `kwargs to True.
        """
        return_values = kwargs["return_values"]
        return_values["result"] = True

    @decorators.Timeout(1, timeout_callback=_callback_func)
    def _test_timeout_with_callback(return_values):
        time.sleep(2)

    rvalues = dict()
    _test_timeout_with_callback(return_values=rvalues)
    assert "result" in rvalues
    assert rvalues["result"]
