from rest_framework import pagination
from django.conf import settings


class CustomPagnation(pagination.PageNumberPagination):
    page_size = settings.DEFAULT_PAGE_SIZE
    page_size_query_param = 'limit'
