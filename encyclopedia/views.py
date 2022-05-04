'''
 Views are the functions that are called by the URL,
 and are responsible for rendering the HTML pages.
'''
from django.shortcuts import render
from django import forms
from . import util
import markdown2

'''
    Class for create a form to search entries
'''
class SearchForm(forms.Form):
    search = forms.CharField(label="",max_length=100,widget= forms.TextInput(attrs={'placeholder': 'Search Encyclopedia','class':'form-control'}))
'''
    Class for create a form to create/edit entries
'''
class NewEntryForm(forms.Form):
    title = forms.CharField(label="",max_length=100,widget= forms.TextInput(attrs={'placeholder': 'Title','class':'form-control m-3'}))
    content = forms.CharField(label="",widget= forms.Textarea(attrs={'placeholder': 'Content','rows': 15, 'class': 'form-control m-3'}))
'''
    Function to render the a list of all the entries
'''
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
    })
'''
    Function to render the page of an entry
'''
def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": markdown2.markdown(util.get_entry(entry)),
        "form": SearchForm(),
    })
'''
    Function to render a search page with a list of entries
'''
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            entries = util.list_entries()
            searchList = []
            for entry in entries:
                if search.lower() in entry.lower():
                    searchList.append(entry)

            return render(request, "encyclopedia/search.html", {
                "searchList": searchList,
                "form": SearchForm(),
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "form": SearchForm(),
            })
'''
    Function to render a page to create a new entry
'''
def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) != None:
                return render(request, "encyclopedia/create.html", {
                    "formulary": NewEntryForm(),
                    "form": SearchForm(),
                    "error": "Entry already exists",
                })
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": markdown2.markdown(util.get_entry(title)),
                    "form": SearchForm(),
                })
        else:
            return render(request, "encyclopedia/create.html", {
                "formulary": NewEntryForm(),
                "form": SearchForm(),
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "formulary": NewEntryForm(),
            "form": SearchForm(),
        })
'''
    Function to render a page to edit an entry pre loaded
    with the content of the entry in the form
'''
def edit(request, entry):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(util.get_entry(title)),
                "form": SearchForm(),
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "formulary": NewEntryForm(),
                "form": SearchForm(),
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            # Creating a new formulary pre-filled with the data of the entry using "initial"
            "formulary": NewEntryForm(initial={'title': entry, 'content': util.get_entry(entry)}),
            "form": SearchForm(),
            'title': entry,
        })
'''
    Function to render a random entry page
'''
def random(request):
    entries = util.list_entries()
    import random
    randomEntry = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
        "title": randomEntry,
        "entry": markdown2.markdown(util.get_entry(randomEntry)),
        "form": SearchForm(),
    })