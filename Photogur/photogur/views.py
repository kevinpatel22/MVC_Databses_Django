from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from photogur.models import Picture, Comment
from photogur.forms import LoginForm, PictureForm

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
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)


@login_required
def add_picture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            add_pic = form.save(commit=False)
            add_pic.user = request.user
            form.save()
            return redirect('picture_details', id=add_pic.id)
    else:
        form = PictureForm()
    html_response = render(request, 'new_pic.html', {'form': form})
    return HttpResponse(html_response)


@login_required
def edit_picture(request, id):
    picture = get_object_or_404(Picture, pk=id, user=request.user.pk)
    if request.method == 'POST':
        form = PictureForm(request.POST, instance=picture)
        if form.is_valid():
            form.save()
            return redirect('picture_details', id=picture.id)
    else:
        form = PictureForm(instance=picture)

    html_response = render(request, 'edit_pic.html', {
                           'form': form, 'picture': picture})
    return HttpResponse(html_response)
