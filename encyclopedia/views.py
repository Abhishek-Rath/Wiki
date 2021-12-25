from django.shortcuts import render, redirect
from . import util
from markdown2 import Markdown
import random
from .forms import CreateNewPage

#Get list of all entries
entries = util.list_entries()

#Create instance of Markdown
markdowner = Markdown() 

def index(request):

    substring_results = []
    substring_search = False

    # Search for the entry in the available entries
    if request.method == "POST":
        search_query = request.POST.get('q')

        found = 0

        for entry in entries:
            if search_query.lower() == entry.lower():
                found = 1
                break
            elif search_query.lower() in entry.lower():
                substring_results.append(entry)
                substring_search = True
            else:
                pass

        if found == 1:  
            # Get markdown file          
            get_md = util.get_entry(search_query)

            # Convert the md into html
            converted_page = markdowner.convert(get_md)

            return render(request, "encyclopedia/entry.html", {
                "converted_page":converted_page,
                "title":search_query,
            })


        elif substring_search == True:
            message = f"Here are some search results matching your query:- {search_query} "
            return render(request, "encyclopedia/index.html", {
                "substring_search":True,
                "substring_results": substring_results,
                "message": message,
            })
        else:
            return render(request, "encyclopedia/search.html",{
                "entries":entries,
                "message":"Sorry, the page you're looking for is not available. Here are some available entries."
            })

    return render(request, "encyclopedia/index.html", {
        "entries":entries,
    })


# def search(request):      
#     substring_results = []
#     search = False

#     #Search for the entry in the available entries
#     if request.method == "POST":
#         search_query = request.POST.get('q')

#         found = 0

#         for entry in entries:
#             if search_query.lower() == entry.lower():
#                 found = 1
#                 break
#             else:
#                 search_query.lower() in entry.lower()
#                 substring_results.append(entry)
#                 search = True

#         if found == 1:  
#             # Get markdown file          
#             get_md = util.get_entry(search_query)

#             # Convert the md into html
#             converted_page = markdowner.convert(get_md)

#             return render(request, "encyclopedia/entry.html", {
#                 "converted_page":converted_page,
#                 "title":search_query,
#             })

#         elif search == True:
#             message = "Here are some search results matching your query"
#             return render(request, "encyclopedia/index.html", {
#                 "search": True,
#                 "substring_results": substring_results
#             })

#         else:
#             return render(request, "encyclopedia/search.html",{
#                 "entries":entries,
#                 "message":"Sorry, the page you're looking for is not available. Here are some available entries."
#             })

    

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
    """ Function to get any random page"""

    get_random_page = random.choice(entries)  #Get random entry from the list of available entries
    get_md = util.get_entry(get_random_page)
    converted_page = markdowner.convert(get_md)
    return render(request, "encyclopedia/entry.html", {
        "converted_page": converted_page,
        "title": get_random_page,
    })


def edit(request, entry):

    """ Function to edit the requested page """

    if request.method == "GET":
        title = entry
        textarea = util.get_entry(title)

        # Pre-populate the form with existing content
        form = CreateNewPage({"title": title, "textarea": textarea})

        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title":title
        })

    if request.method == "POST":
        
        # after editing, save the contents
        form = CreateNewPage(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]

            util.save_entry(title, textarea)
            return redirect("entry", title)
