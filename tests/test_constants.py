import pytest

from confluent_kafka_addons import constants

def test_retriable_seconds():
    test_inputs = [
        constants.RetriableUnit.SECONDS,
        constants.RetriableUnit.SECONDS.value
    ]
    expected_output = True
    for test_input in test_inputs:
        actual_output = constants.RetriableUnit.is_seconds(test_input)
        assert expected_output == actual_output


def test_retriable_milliseconds():
    test_inputs = [
        constants.RetriableUnit.MILLISECONDS,
        constants.RetriableUnit.MILLISECONDS.value
    ]
    expected_output = True
    for test_input in test_inputs:
        actual_output = constants.RetriableUnit.is_milliseconds(test_input)
        assert expected_output == actual_output


def test_retriable_seconds_invalid_value():
    test_inputs = [-1, 1]
    expected_value = False
    for test_input in test_inputs:
        actual_value = constants.RetriableUnit.is_seconds(test_input)
        assert expected_value == actual_value


def test_retriable_seconds_invalid_type():
    test_input = "abc"
    pytest.raises(
        TypeError, 
        constants.RetriableUnit.is_seconds, 
        test_input
    )


def test_retriable_milliseconds_invalid_type():
    test_inputs = [0, 2]
    expected_value = False
    for test_input in test_inputs:
        actual_value = constants.RetriableUnit.is_milliseconds(test_input)
        assert expected_value == actual_value


def test_retriable_milliseconds_invalid_value():
    test_input = "abc"
    pytest.raises(
        TypeError, 
        constants.RetriableUnit.is_milliseconds, 
        test_input
    )


def test_is_valid():
    test_inputs = [0, 1]
    expected_output = True
    for test_input in test_inputs:
        actual_output = constants.RetriableUnit.is_valid(test_input)
        expected_output == actual_output


def test_is_value_invalid_type():
    test_input = "abc"
    pytest.raises(
        TypeError, 
        constants.RetriableUnit.is_valid, 
        test_input
    )


def test_is_valid_invalid_value():
    test_inputs = [-1, 2]
    expected_output = False
    for test_input in test_inputs:
        actual_output = constants.RetriableUnit.is_valid(test_input)
        expected_output == actual_output