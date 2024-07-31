# middlewares.py
import json
from datetime import datetime, timedelta

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class RateLimitMiddleware(MiddlewareMixin):
    RATE_LIMIT = {
        "default": (5, 60),  # Defaultní limit: 5 požadavků za 60 sekund
        "sendInvitation": (3, 120),  # Limit pro sendInvitation: 3 požadavky za 120 sekund
    }

    def process_request(self, request):
        if request.content_type == "application/json":
            try:
                body = json.loads(request.body)
                operation_name = body.get("operationName")
                if operation_name:
                    identifier = self.get_identifier(request)
                    rate_limit, time_period = self.get_rate_limit(operation_name)

                    if identifier and rate_limit and time_period:
                        if not self.is_rate_limited(identifier, rate_limit, time_period):
                            return JsonResponse({"error": "Rate limit exceeded"}, status=429)
            except json.JSONDecodeError:
                pass

    def get_identifier(self, request):
        if request.user.is_authenticated:
            return f"user:{request.user.id}"
        else:
            return f"ip:{self.get_client_ip(request)}"

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def get_rate_limit(self, operation_name):
        return self.RATE_LIMIT.get(operation_name, self.RATE_LIMIT["default"])

    def is_rate_limited(self, identifier, rate_limit, time_period):
        cache_key = f"rl:{identifier}"
        requests = cache.get(cache_key, [])

        now = datetime.now()
        requests = [req for req in requests if req > now - timedelta(seconds=time_period)]

        if len(requests) >= rate_limit:
            return False

        requests.append(now)
        cache.set(cache_key, requests, timeout=time_period)
        return True
