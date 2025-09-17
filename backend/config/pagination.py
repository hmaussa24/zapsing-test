from rest_framework.pagination import PageNumberPagination


class DefaultPageNumberPagination(PageNumberPagination):
    # Usa PAGE_SIZE de settings para el tamaño por defecto
    page_size_query_param = 'page_size'
    max_page_size = 100


