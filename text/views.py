from django.shortcuts import render
from django.views.generic import TemplateView


def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['documents']
        print(uploaded_file.name)
    return render(request, 'text/home.html')


# Create your views here.
