from django.shortcuts import redirect
from django.shortcuts import render

# Create your views here.
from upload.forms import DocumentForm
from upload.models import Document
from django.db import connection, transaction

cursor = connection.cursor()
file_url = ''
context = {}


def upload(request):
    if request.user.is_authenticated:
        # Is it better to use @login_required ?
        username = request.user.username
        print(username)
        with connection.cursor() as cursor:
            query = """SELECT file FROM public.upload_document where username_id in (SELECT id FROM public.auth_user where 
            username = username) ; """
            cursor.execute(query)
            row = cursor.fetchone()
            print(row)
    else:
        username = ''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = username
            doc = form.save()
            file_url = doc.file.url
            print(file_url)
            return redirect('upload_list')
    else:
        form = DocumentForm()
    return render(request, 'upload/upload.html', {"form": form})


def upload_list(request):
    uploads = Document.objects.all()
    return render(request, 'upload/upload_list.html', {"uploads": uploads})


def data(request):
    if request.user.is_authenticated:
        # Is it better to use @login_required ?
        username = request.user.username
        print(username)
        with connection.cursor() as cursor:
            query = """SELECT file FROM public.upload_document where username_id in (SELECT id FROM public.auth_user where 
            username = username) ; """
            cursor.execute(query)
            row = cursor.fetchone()
            print(row)
    return render(request, 'upload/upload.html', {"row": row})
