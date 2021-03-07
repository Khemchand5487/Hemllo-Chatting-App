from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("<h1>Welcome</h1>")
    context = {
        'var':"Just testing!"
    }
    return render(request, 'index.html', context=context)

