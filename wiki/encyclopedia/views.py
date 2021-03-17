
from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from random import choice

class EditForm(forms.Form):
    titlearea = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'resize: none; width: 400px; height: 30px; margin-top: 10px; padding-left: 5px; padding-top: 2px; position: absolute;'}), label='')
    textarea = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'resize: none; width: 650px; height: 500px; margin-top: 50px;'}), label='')

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        content = "## Page was not found"
    content = Markdown().convert(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {'text': content, 'title': title})

def randompage(request):
    randEntry = choice(util.list_entries())
    return HttpResponseRedirect(f"{randEntry}")

def create(request):
    if request.method == "POST":
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
    entries = util.list_entries()
    query = request.GET.get("q", "")
    if query in entries:
        return HttpResponseRedirect(reverse("wiki:entry", args=(query,)))
    else:
        return render(request, "encyclopedia/search.html", {"entries": util.search(query), "query": query})

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            changetitle = form.cleaned_data['titlearea']
            text = form.cleaned_data['textarea']
            util.save_entry(changetitle, text)
            return HttpResponseRedirect(reverse("wiki:entry", args=(changetitle,)))
    return render(request, 'encyclopedia/edit.html', {
        'title': title,
        'form': EditForm(initial={"textarea": util.get_entry(title), "titlearea": title})
    })
