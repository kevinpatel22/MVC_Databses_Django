from django.http import HttpResponse
from django.shortcuts import render
from photogur.models import Picture, Comment

def pictures_page(request):
    pic_links = Picture.objects.all()
    context = {'db_pictures': pic_links }
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)
    