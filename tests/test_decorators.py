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
    pytest.raises(errors.RetriableException, 
                  _test_function)
