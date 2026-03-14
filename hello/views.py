from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Hello from Django Docker App"
    })

def health(request):
    return JsonResponse({
        "status": "ok"
    })