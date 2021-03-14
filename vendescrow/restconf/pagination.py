from rest_framework import pagination


class LoansAPIPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
