from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown

class CreateNewPage(forms.Form):
    title = forms.CharField(label = 'Title', max_length = 50)
    # content = forms.Textarea(widget = forms.Textarea, label = '')
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":20}), label = '')


def index(request):

    #Get list of all the entries
    entries = util.list_entries()

    markdowner = Markdown()

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

    #Get list of all the entries
    entries = util.list_entries() 

    markdowner = Markdown()  

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
    if request.method == "POST":
        # Create a form instance and populate it with data from the request.
        form =  CreateNewPage(request.POST)
        markdowner =  Markdown()
        entries = util.list_entries()
        # Check if form is valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            #Check if the title already exists
            if title in entries:
                
                return render(request, "encyclopedia/error.html", {
                    "message":"The page with this title already exists."
                })

            else:
                util.save_entry(title, content)
                get_page = util.get_entry(title) 
                converted_page = markdowner.convert(get_page)
                return render(request, "encyclopedia/entry.html", {
                    "converted_page": converted_page,
                    "title":title,
                })


    
    return render(request, "encyclopedia/create.html", {
        "form": CreateNewPage()
    })
