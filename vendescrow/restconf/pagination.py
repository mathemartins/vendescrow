from rest_framework import pagination


class DataAPIPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
