from django.http import HttpResponse

def IndexView(request):
    return HttpResponse('<h1>Runing ... <h1/>')