from django.shortcuts import render


def index(request):
    """Landing page introducing the system developer."""
    return render(request, 'index.html')
