from flask import request, abort

from typing import Iterable


class QueryParametersMixin(object):
    """
    Mixin to check query parameters on existing and save them to self.parameters
    provide required_parameters and optional_parameters variables
    Just inherit this mixin before View:
        class FooView(QueryParametersMixin, View):
            required_parameters = ('param1', 'param2')
            optional_parameters = ('param3',)

            def dispatch_request(self):
                self.parameters['param1']
                self.parameters['param1']

                self.parameters.get('param3', None)
                ...
    """

    required_parameters: tuple = tuple()
    optional_parameters: tuple = tuple()

    def __init__(self, *args, **kwargs):
        super(QueryParametersMixin, self).__init__(*args, **kwargs)
        self.parameters = {}

    def dispatch_request(self, *args, **kwargs):
        self.save_parameters(self.required_parameters, self.optional_parameters)
        return super(QueryParametersMixin, self).dispatch_request(*args, **kwargs)

    def save_parameters(
        self, required_parameters: Iterable[str], optional_parameters: Iterable[str]
    ):
        self.validate_and_save_params(*required_parameters)
        self.validate_and_save_params(*optional_parameters, required=False)

    def validate_and_save_params(self, *arguments, required=True):
        for argument in arguments:
            value = request.args.get(argument)
            if required and not value:
                abort(400)
            self.parameters.update({argument: value})


class QueryParametersForMethodMixin(QueryParametersMixin):
    """
    Mixin to provide query parameters for each HTTP method
    Just inherit this mixin before MethodView
    and provide {prefix}_optional_parameters and  {prefix}_required_parameters
    where prefix is the name of method:

        class FooView(QueryParametersForMethodMixin, MethodView):
            get_required_parameters = ('param1',)
            get_options_parameters = ('param2',)

            post_required_parameters = ('param3',)
            post_optional_parameters = ('param4',)

            def get(self):
                self.parameters['param1']
                self.parameters.get('param2', None)
                ...

            def post(self):
                self.parameters['param3']
                self.parameters.get('param4', None)
                ...

    """

    def dispatch_request(self, *args, **kwargs):
        optional_params = getattr(
            self, request.method.lower() + "_optional_parameters", tuple()
        )
        required_params = getattr(
            self, request.method.lower() + "_required_parameters", tuple()
        )
        self.save_parameters(required_params, optional_params)

        return super(QueryParametersForMethodMixin, self).dispatch_request(
            *args, **kwargs
        )
