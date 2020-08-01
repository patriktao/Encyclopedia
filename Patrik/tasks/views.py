from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewTaskForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

             # Isolate the task from the 'cleaned' version of form data
            task = form.cleaned_data["task"]

            # Add the new task to our list of tasks
            request.session["tasks"] += [task]

            return HttpResponseRedirect(reverse("tasks:index"))

        else:
             # If the form is invalid, re-render the page with existing information.
            return render(request, "tasks/add.html", {
            "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })
