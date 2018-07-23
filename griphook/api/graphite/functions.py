from typing import Any, Optional, Type, Union

from griphook.api.graphite.target import Target

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

    def __init__(self, type_: BuiltInOrTarget, *,
                 name: Optional[str] = None,
                 default: Optional[Any] = None) -> None:
        """
        Function Argument constructor

        :param type_: python type argument will be rendered as
        :type type_:  Target, str, bool, int or float
        """
        self.type_ = type_
        self.value = None
        self.default = default
        self.name = name

    def __str__(self):
        """
        Renders argument according to its type

        :returns: str
        :raises:  ValueError if self.value is not set
        """
        # Set value to default if not set
        value = self.value if self.value is not None else self.default
        if value is None:
            raise ValueError("The value should be set!")

        # Render according to type
        if self.type_ is str:
            # Wrap string argument value in double quotes
            return f'"{value}"'
        if self.type_ is bool:
            # Change 'True' to 'true', since Graphite uses lowercase bool
            return str(value).lower()
        else:
            return str(value)


class Function(Target):
    """
    Class for building Graphite API functions as string.
    Before constructing function you have to declare it and
    its arguments types. Type specifies how argument will be treated and
    rendered to string.
    """

    def __init__(self,
                 name: str,
                 *arg_types: Union[BuiltInOrTarget, Argument]) -> None:
        """
        Function constructor.
        Creates Graphite function object, sets the name to function and
        declares function parameter types
        First declare function and it arg types, then call it.

        Example:
            >>> pow = Function('pow', int, Argument(int, default=2))
            >>> print(pow(2))
            >>> 'pow(2,2)'
            >>> print(pow(2, 3))
            >>> 'pow(2,3)'

        :param name:       name of the function
        :type name:        str
        :param *arg_types: list of type declarations for arguments
        :type *arg_types:  Argument, Target, str, bool, int or float,
        """
        if not isinstance(name, str):
            raise TypeError('Function name should be str instance')
        self.name = name
        self._args = [self._type_to_argument(t) for t in arg_types]

    @staticmethod
    def _type_to_argument(type_: Union[BuiltInOrTarget, Argument]):
        if isinstance(type_, Argument):
            return type_
        return Argument(type_)

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
        arguments = ','.join(map(str, self._args))

        return f'{self.name}({arguments})'


# Built-in functions
summarize = Function('summarize',
                     Argument(Target, name='seriesList'),
                     Argument(str, name='func', default='sum',),
                     Argument(bool, name='AlignToFrom', default=False))
