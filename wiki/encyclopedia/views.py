
from django.shortcuts import render
from django import forms
from . import util
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from random import choice

class EditForm(forms.Form):
    forms.CharField(max_length = 1000)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries" : util.list_entries()})

def entry(request, title):
    if request.method=="POST":
        title_entry = request.POST.get('title')
        return edit(request, title_entry)
    if title not in util.list_entries():
        return HttpResponse("The requested page was not found.")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "text" : markdown2.markdown(util.get_entry(title))
        })

def randompage(request):
    randEntry = choice(util.list_entries())
    return HttpResponseRedirect(f"{randEntry}")

def create(request):
    if request.method=="POST":
        title = request.POST['title']
        text = request.POST['text']
        entries = util.list_entries()
        if title in entries:
            return HttpResponse("The page already exists.")
        else:
            util.save_entry(title, text)
            return HttpResponseRedirect(f"{title}")
    return render(request, 'encyclopedia/create.html', {
    })

def search(request):
    if request.method=="GET":
        query = request.GET['q']
        return render(request, "encyclopedia/entry.html", {
            "title" : query,
            "text" : markdown2.markdown(util.get_entry(query))
        })

def edit(request, name):
    context={}

    return render(request, 'encyclopedia/edit.html',{
        'title' : name,
        'text' : util.get_entry(name)
    })
