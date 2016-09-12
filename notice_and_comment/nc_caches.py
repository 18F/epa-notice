from regulations.url_caches import DailyCacheMiddleware
from django.utils.decorators import decorator_from_middleware_with_args

homepage_non_cache = decorator_from_middleware_with_args(DailyCacheMiddleware)(
    cache_timeout=0, cache_alias='eregs_longterm_cache')
