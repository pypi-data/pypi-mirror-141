import waffle

from .exceptions import ServiceUnavailable


class PermissionFlagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.switch_name = 'middleware'

    def __call__(self, request):
        whitelisted_paths = ['dkutils', 'switches', 'debug']
        response = self.get_response(request)
        if not waffle.switch_is_active(self.switch_name):
            for path in whitelisted_paths:
                if request.path in path:
                    return response
            raise ServiceUnavailable()
        return response
