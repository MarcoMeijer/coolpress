from django.http import HttpResponse

# Create your views here.
def index(_):
    return HttpResponse("Hello world!")
