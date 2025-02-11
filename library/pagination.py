from rest_framework.pagination import PageNumberPagination

class HundredItemsPagination(PageNumberPagination):
    page_size = 100  # Limit to 100 items per page
    page_size_query_param = 'page_size'  # Allow clients to override the page size
    max_page_size = 100  # Maximum limit of 100 items per page