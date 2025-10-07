# submissions/middleware.py
import time, math
from django.http import JsonResponse
from django.core.cache import caches
from django.conf import settings

cache = caches['default']

class RateLimitMiddleware:
    def __init__(self, get_response):
        # This is called once when the server starts
        self.get_response = get_response
        cfg = getattr(settings, "RATE_LIMIT", {}) or {}
        self.rate = float(cfg.get("RATE", 5))
        self.window = float(cfg.get("WINDOW", 60))
        self.burst = float(cfg.get("BURST", max(self.rate, 1)))
        self.key_prefix = cfg.get("KEY_PREFIX", "rl:")
        self.block_status = cfg.get("BLOCK_STATUS", 429)
        self.fill_per_sec = self.rate / self.window if self.window else 0.0

    def __call__(self, request):
        # This is run for every request before view
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            identifier = self._get_identifier(request)
            if not self._allow_request(identifier):
                return JsonResponse(
                    {"detail": "Rate limit exceeded. Try again later."},
                    status=self.block_status
                )
        # Continue to view
        response = self.get_response(request)
        return response

    def _get_identifier(self, request):
        if request.user.is_authenticated:
            return f"user:{request.user.pk}"
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            ip = xff.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "unknown")
        return f"ip:{ip}"

    def _allow_request(self, identifier):
        now = time.time()
        key = f"{self.key_prefix}{identifier}"

        data = cache.get(key)
        if data is None:
            tokens, last = self.burst, now
        else:
            tokens, last = data

        # refill tokens
        elapsed = max(0, now - last)
        tokens = min(self.burst, tokens + elapsed * self.fill_per_sec)
        last = now

        if tokens >= 1:
            tokens -= 1
            cache.set(key, (tokens, last), timeout=int(self.window * 4))
            return True
        else:
            return False
