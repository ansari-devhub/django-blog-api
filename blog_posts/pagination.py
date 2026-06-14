from rest_framework.pagination import PageNumberPagination, CursorPagination

class PostPagination(PageNumberPagination):
    max_page_size = 3
    page_size = 2
    page_size_query_param = 'size'
    page_query_param = 'pagenum'
    
    
class CategoryPagination(PageNumberPagination):
    max_page_size = 3
    page_size = 2
    page_size_query_param = 'size'
    page_query_param = 'pagenum'
    

class CategoryCursorPagination(CursorPagination):
    ordering = '-created_at'
    page_size_query_param = 'limit'
    max_page_size = 3
    page_size = 2