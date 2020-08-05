
from django.shortcuts import render
from django import forms
from . import util
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from random import choice

class EditForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
        'cols': 6,
        'rows': 20,
        'style': 'resize:none; width:600px; height:526px; margin-top: 20px;'
    }), initial='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries" : util.list_entries()})

def entry(request, title):
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

def edit(request, title):
    content = util.get_entry(title);
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            form = EditForm(initial={content})
    return render(request, 'encyclopedia/edit.html',{
        'title': title,
        'form': form
    })
