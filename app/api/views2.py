from django.http import JsonResponse

def custom_csrf_failure_view(request, reason=""):
    return JsonResponse({"error": "CSRF token missing or incorrect.", "reason": reason}, status=403)
