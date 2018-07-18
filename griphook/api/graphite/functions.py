from typing import Type, Union

from griphook.api.graphite.target import Target, Path

# Type aliases
BuiltInOrTarget = Union[Type[Target], Type[str],
                        Type[bool], Type[int], Type[float]]


class Argument(object):
    """
    Graphite Function argument
    """

    def __init__(self, arg_type: BuiltInOrTarget) -> None:
        """
        Function Argument constructor

        :param arg_type: python type argument will be rendered as
        :type arg_type:  Target, str, bool, int or float
        """
        self.type = arg_type
        self.value = None

    def __str__(self):
        """
        Renders argument according to its type

        :returns: str
        :raises:  ValueError if self.value is not set
        """
        value = self.value
        if value is None:
            raise ValueError("The value should be set!")

        # Render according to type
        if self.type is str:
            # Wrap string argument value in double quotes
            return '"{}"'.format(value)
        if self.type is bool:
            # Change 'True' to 'true', since Graphite uses lowercase bool
            return str(value).lower()
        else:
            return str(value)

    def __repr__(self):
        return self.__str__()


class Function(Target):
    """
    Graphite Function for constructing api requests
    """

    def __init__(self,
                 name: str,
                 *arg_types: BuiltInOrTarget) -> None:
        """
        Function constructor.
        Creates Graphite function object, sets the name to function and
        declares function parameter types

        :param name:       name of the function
        :type name:        str
        :param *arg_types: list of type declarations for arguments
        :type *arg_types:  Target, str, bool, int or float
        """
        self.name = name
        self._args = [Argument(t) for t in arg_types]

    def __call__(self, *values) -> str:
        """
        Constructs string representation of function call with arguments

        :param values:
        """
        # TODO: refactor this
        for i in range(len(self._args)):
            self._args[i].value = values[i]

        # Join all arguments with period
        arguments = Path(*self._args, sep=',')

        return '{func_name}({args})'.format(func_name=self.name,
                                            args=arguments)


if __name__ == "__main__":
    target = Path('foo', 'bar', 'spam', 'eggs')
    maximumAbove = Function('maximumAbove', Target, int)
    summarize = Function('summarize', Target)
    print(summarize(maximumAbove(target, 50)))
