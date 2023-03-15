from django.conf import settings
from rest_framework import pagination


class CustomPagnation(pagination.PageNumberPagination):
    page_size = settings.DEFAULT_PAGE_SIZE
    page_size_query_param = 'limit'
