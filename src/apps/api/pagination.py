from collections import OrderedDict

from rest_framework.pagination import CursorPagination as _CursorPagination
from rest_framework.response import Response


# Copied from https://github.com/HackSoftware/Django-Styleguide#filters--pagination
def get_paginated_response(pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()
    page = paginator.paginate_queryset(queryset, request, view=view)

    context = {"request": request}
    if page is not None:
        serializer = serializer_class(page, many=True, context=context)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True, context=context)
    return Response(data=serializer.data)


class CursorPagination(_CursorPagination):
    ordering = "pub_date"
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("count", len(data)),
                    ("results", data),
                ]
            )
        )
