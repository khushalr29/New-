from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'perPage'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'data': data
        })

def paginate_queryset(queryset, request, serializer_class=None, view=None):
    paginator = CustomPagination()
    paginated_data = paginator.paginate_queryset(queryset, request, view=view)
    if serializer_class is not None:
        serializer = serializer_class(paginated_data, many=True)
        return paginator.get_paginated_response(serializer.data)
    return paginator.get_paginated_response(paginated_data)