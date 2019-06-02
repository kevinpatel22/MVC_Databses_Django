from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from photogur.models import Picture, Comment
from photogur.forms import LoginForm

def pictures_page(request):
    pic_links = Picture.objects.all()
    context = {'db_pictures': pic_links }
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def root(request):
    return HttpResponseRedirect('/pictures')

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(artist=query)
    context = {'pictures': search_results, 'query': query}
    response = render(request, 'search.html', context)
    return HttpResponse(response)

@require_http_methods(['POST'])
def create_comment(request):
    user_name = request.POST['name']
    user_message = request.POST['message']
    user_select_picture = request.POST['picture']
    select_picture = Picture.objects.get(id=user_select_picture)
    comment = Comment(name=user_name, picture=select_picture, message=user_message)
    comment.save()
    return redirect("picture_details", id=user_select_picture)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else: 
        form = LoginForm()
    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)