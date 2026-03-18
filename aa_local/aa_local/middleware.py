from django.utils.deprecation import MiddlewareMixin

class DisableClientCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            response["Cache-Control"] = "no-store, no-cache, must-revalidate, private, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
        return response