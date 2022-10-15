from django.core.cache import cache
from django.http import HttpResponse

NO_ASSOCIATED_EXPIRE  = -2
NOT_EXIST = -1

class LimitRequest:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        print(cache.ttl(ip))
        if cache.ttl(ip) in (NO_ASSOCIATED_EXPIRE, NOT_EXIST, 0):
            cache.set(ip, 1, 30)
        elif cache.get(ip) >= 5:
            return HttpResponse("Quá số lần request")
        else:
            cache.incr(ip)
        response = self.get_response(request)

        return response
