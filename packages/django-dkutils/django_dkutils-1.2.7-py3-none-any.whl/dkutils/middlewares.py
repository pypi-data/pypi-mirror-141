import waffle

from .exceptions import ServiceUnavailable


class PermissionFlagMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        self.switch_name = 'middleware'

    def __call__(self, request):
        if not waffle.switch_is_active(self.switch_name):
            raise ServiceUnavailable()
        response = self.get_response(request)
        return response
