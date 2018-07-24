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
    allowed_types = (int, bool, float, str, Target,)

    def __init__(self, type_: BuiltInOrTarget, *,
                 name: Optional[str] = None,
                 default: Optional[Any] = None) -> None:
        """
        Function Argument constructor

        :param type_: python type argument will be rendered as
        :type type_:  Target, str, bool, int or float
        """
        self.type_ = type_
        # Set initial argument value to None, as it is just declared
        self._value = None
        # If default is set - set value to default
        if default is not None:
            self.value = default
        self.name = name

    @property
    def type_(self):
        return self._type

    @type_.setter
    def type_(self, type_):
        # Check if type is allowed
        if type_ not in self.allowed_types:
            allowed_typenames = tuple(x.__name__ for x in self.allowed_types)
            raise ValueError(f"Not supported type of argument, "
                             f"argument type should be one of these types:\n"
                             f"{allowed_typenames}")
        self._type = type_

    @property
    def value(self):
        if self._value is None:
            raise ValueError("The value should be set!")
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        """
        Renders argument according to its type

        :returns: str
        :raises:  ValueError if self.value is not set
        """
        # Render according to type
        if self.type_ is str:
            # Wrap string argument value in double quotes
            return f'"{self.value}"'
        if self.type_ is bool:
            # Change 'True' to 'true', since Graphite uses lowercase bool
            return str(self.value).lower()
        else:
            return str(self.value)


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
