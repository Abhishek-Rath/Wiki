from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown
import random

class CreateNewPage(forms.Form):
    title = forms.CharField(label = 'Title', max_length = 50)
    textarea = forms.CharField(widget=forms.Textarea, label = '')

    

#Get list of all entries
entries = util.list_entries()

#Create instance of Markdown
markdowner = Markdown() 

def index(request):
    if request.method == "POST":
        search_query = request.POST.get('q')

        found = 0
        for entry in entries:
            if search_query.lower() == entry.lower():
                found = 1
                break
            else:
                pass

        if found == 1:  
            # Get the decoded markdown file          
            get_md = util.get_entry(search_query)

            # Convert the md into html
            converted_page = markdowner.convert(get_md)

            return render(request, "encyclopedia/entry.html", {
                "converted_page":converted_page,
                "title":search_query,
            })
        else:
            return render(request, "encyclopedia/search.html",{
                "entries":entries,
                "message":"Sorry, the page you're looking for is not available. Here are some available entries."
            })

    return render(request, "encyclopedia/index.html", {
        "entries":entries,
    })


def entry(request, title):
    """ Function to display all the entries available.""" 

    #Check if the title is present in the entries
    if title in entries: 
        get_md = util.get_entry(title)
        converted_page = markdowner.convert(get_md)

        return render(request, "encyclopedia/entry.html", {
            "converted_page": converted_page,
            "title":title,
        })

    #title not present in entries
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Sorry, the page you're looking for isn't available."
        })


def create(request):
    """ Function to create new page """

    if request.method == "POST":
        # Create a form instance and populate it with data from the request.
        form =  CreateNewPage(request.POST)
        
        # Check if form is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            #Check if the title already exists
            if title in entries:
                
                return render(request, "encyclopedia/error.html", {
                    "message":"The page with this title already exists."
                })

            else:
                util.save_entry(title, textarea)
                get_page = util.get_entry(title) 
                converted_page = markdowner.convert(get_page)
                return render(request, "encyclopedia/entry.html", {
                    "converted_page": converted_page,
                    "title":title,
                })

    return render(request, "encyclopedia/create.html", {
        "form": CreateNewPage()
    })


def random_page(request):
    """ Function to random page"""

    get_random_page = random.choice(entries)  #Get random entry from the list of available entries
    get_md = util.get_entry(get_random_page)
    converted_page = markdowner.convert(get_md)
    return render(request, "encyclopedia/entry.html", {
        "converted_page": converted_page,
        # "title": get_random_page,
    })