from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from oops.settings import REST_FRAMEWORK

User = get_user_model()

class MyPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_page_size(self, request):
        page_size_val = request.query_params.get(self.page_size_query_param,10)
        if page_size_val != 'all':
            return super(MyPagination,self).get_page_size(request)
        else:
            return None

    # def get_paginated_response(self, data):
    #     ret = {
    #         'count': self.page.paginator.count,
    #         'next': self.get_next_link(),
    #         'previous': self.get_previous_link(),
    #         'role_list': dict(User.ROLE_CHOICES),
    #         'results': data
    #     }
    #     return Response(ret)