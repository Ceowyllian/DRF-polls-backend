"""
Copied from https://github.com/HackSoftware/Django-Styleguide#filters--pagination
"""

from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response


def get_paginated_response(pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()
    page = paginator.paginate_queryset(queryset, request, view=view)

    context = {'request': request}
    if page is not None:
        serializer = serializer_class(page, many=True, context=context)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True, context=context)
    return Response(data=serializer.data)


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 20
    max_limit = 20

    def get_paginated_data(self, data):
        return OrderedDict(
            [
                ("limit", self.limit),
                ("offset", self.offset),
                ("count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("limit", self.limit),
                    ("offset", self.offset),
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
