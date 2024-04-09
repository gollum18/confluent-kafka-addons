import enum
import typing

class RetriableUnit(enum.Enum):
    SECONDS = 0
    MILLISECONDS = 1

    @staticmethod
    def is_seconds(unit: typing.Union[int, "RetriableUnit"]) -> bool:
        """Determines if `unit` is constants.RetriableUnit.SECONDS.

        Args:
            unit (typing.Union[int, RetriableUnit]): An int or 
                constants.RetriableUnit.SECONDS instance.

        Raises:
            TypeError: If `unit` is not an int or 
                constants.RetriableUnit.SECONDS instance.

        Returns:
            (bool): True if `unit` is constants.RetriableUnit.SECONDS, 
                False otherwise.
        """
        if isinstance(unit, int):
            return unit == RetriableUnit.SECONDS.value
        elif isinstance(unit, RetriableUnit):
            return unit == RetriableUnit.SECONDS
        else:
            raise TypeError(
                "[constants.RetriableUnit.is_seconds] - parameter "
                + "'unit' must be one of the following types: [int, "
                + "RetriableUnit]!")


    @staticmethod
    def is_milliseconds(unit: typing.Union[int, "RetriableUnit"]) -> bool:
        """Determines if `unit` is constants.RetriableUnit.MILLISECONDS.

        Args:
            unit (typing.Union[int, RetriableUnit]): An int or 
                constants.RetriableUnit.MILLISECONDS instance.

        Raises:
            TypeError: If `unit` is not an int or 
                constants.RetriableUnit.MILLISECONDS instance.

        Returns:
            (bool): True if `unit` is constants.RetriableUnit.MILLISECONDS, 
                False otherwise.
        """
        if isinstance(unit, int):
            return unit == RetriableUnit.MILLISECONDS.value
        elif isinstance(unit, RetriableUnit):
            return unit == RetriableUnit.MILLISECONDS
        else:
            raise TypeError(
                "[constants.RetriableUnit.is_milliseconds] - parameter "
                + "'unit' must be one of the following types: [int, "
                + "RetriableUnit]!")


    @staticmethod
    def is_valid(unit: typing.Union[int, "RetriableUnit"]):
        if isinstance(unit, int):
            return unit in [e.value for e in RetriableUnit]
        elif isinstance(unit, RetriableUnit):
            return unit in RetriableUnit
        else:
            raise TypeError(
                "[constants.RetriableUnit.valid] - parameter "
                + "'unit' must be one of the following types: [int, "
                + "RetriableUnit]!")    


    @staticmethod
    def format_str() -> str:
        """Returns a string containing the names of the Enumeration names specified by the Retriable Enum.

        This string takes the format of a comma separated list surrounded by brackets.

        Returns:
            str: A bracketed, comma separated list of Enumeration names.
        """
        enum_names = [str(e) for e in RetriableUnit]
        return f"[{', '.join([enum_names])}]"