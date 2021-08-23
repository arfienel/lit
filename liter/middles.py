from forum.services import *

class ViewsAddMiddleWare:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        views_add(request)
        response = self._get_response(request)
        print('end fist middleware')
        return response
