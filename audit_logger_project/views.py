from django.shortcuts import render

def homepage(request):
    """
    View untuk menampilkan homepage
    """
    return render(request, 'home/index.html') 