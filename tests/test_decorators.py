from confluent_kafka_addons import decorators, errors



def test_retriable_no_exceptions():
    @decorators.Retriable()
    def _test_function(a, b):
        return a + b
    
    assert _test_function(2, 2) == 4


def test_retriable_backoff():
    pass


def test_retriable_backoff_postconditions():
    pass


def test_retriable_max_retries():
    pass