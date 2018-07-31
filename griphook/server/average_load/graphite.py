from griphook.api.graphite.target import Target
from griphook.api.graphite.functions import Function, Argument

average = Function('avg', Argument(Target, name='seriesLists'))

summarize = Function('summarize',
                     Argument(Target, name='seriesList'),
                     Argument(str, name='time', default='1hour', ),
                     Argument(str, name='func', default='sum', ),
                     Argument(bool, name='AlignToFrom', default=False))
