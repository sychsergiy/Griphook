from typing import Union


class Target(object):
    pass


class DotPath(Target):
    """
    Class for constructing path with custom rules
    Converts every path part to string before joining them

    Example:
            >>> p = DotPath('foo', 'bar', 'spam')
            >>> str(p)
            >>> 'foo.bar.spam'
    """

    def __init__(self, *chunks: str) -> None:
        self.chunks = list(chunks)

    def __str__(self) -> str:
        """
        Builds string of chunks joined with separator and returns it.
        Any object with __str__ method implemented is suitable
        """
        return ".".join(map(str, self.chunks))

    def __add__(self, other: Union[str, "DotPath"]) -> "DotPath":
        """
        Overloaded plus operator

        :returns: DotPath object with copy of chunks from both operands
        """
        chunks = self.chunks.copy()
        if isinstance(other, DotPath):
            chunks += other.chunks
        else:
            chunks.append(other)

        return DotPath(*chunks)


class MultipleValues(object):
    """
    Graphite API allows to get data from multiple sources in one request
    using curly brace notation, for example:
        'my_server.{my_instance1,my_instance2}.cpu'
    This class defines interface for building that value list

    Example:
        >>> values = GraphiteMultipleValue('foo', bar', 'spam')
        >>> str(values)
        >>> '{foo,bar,spam}'
    """

    def __init__(self, *values: str) -> None:
        if not values:
            raise ValueError("values cannot be empty")
        self.values = values

    def __str__(self) -> str:
        """
        Converts each value to string and joins them with comma symbol

        :returns: string of comma-separated values wrapped in curly braces
        """
        return f'{{{",".join(self.values)}}}'
