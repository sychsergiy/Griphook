from typing import Type, Union

from griphook.api.graphite.target import Path, Target

# Type alias for base type of types
BuiltInOrTarget = Union[Type[Target], Type[str],
                        Type[bool], Type[int], Type[float]]


class Argument(object):
    """
    Wrapper for Function argument that renders it
    Every argument has it's type.

    string argument will be wrapped in double quotes.
    bool will be lowercased.
    any other type should implement __str__ method and will
    be rendered as result of __str__ call
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
    Class for building Graphite API functions as string.
    Before constructing function you have to declare it and
    its arguments types. Type specifies how argument will be treated and
    rendered to string.
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
        if not isinstance(name, str):
            raise TypeError('Function name should be str instance')
        self.name = name
        self._args = [Argument(t) for t in arg_types]

    def __call__(self, *args) -> str:
        """
        Constructs string representation of function call with arguments
        If argument count given less than declared - render only given, ignore
        others (assume them as defaults)

        :param arguments: function parameters values
        """
        # Fill function arguments with values
        for value, arg in zip(args, self._args):
            arg.value = value

        # Join all arguments with period
        arguments = Path(*self._args, sep=',')

        return '{func_name}({args})'.format(func_name=self.name,
                                            args=arguments)


if __name__ == "__main__":
    target = Path('foo', 'bar', 'spam', 'eggs')
    maximumAbove = Function('maximumAbove', Target, int)
    summarize = Function('summarize', Target)
    print(summarize(maximumAbove(target, 50)))
