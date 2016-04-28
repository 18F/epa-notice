from django.conf import settings

from regcore_write.views.security import basic_auth


class BasicAuthMiddleware(object):
    """Wrap all requests in the same basic auth we're using in regcore"""
    def process_request(self, request):
        if settings.HTTP_AUTH_USER and settings.HTTP_AUTH_PASSWORD:
            # "None" means success; basic_auth is a decorator
            thunk = basic_auth(lambda req: None)
            return thunk(request)
