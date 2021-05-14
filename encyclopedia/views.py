from django.shortcuts import render

from . import util
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    #Get list of all the entries
    entries = util.list_entries() 

    markdowner = Markdown()  

    #Check if the title is present in the entries
    if title in entries: 

        # Get the decoded markdown file
        get_md = util.get_entry(title)

        # Convert the md into html
        page_converted = markdowner.convert(get_md)

        return render(request, "encyclopedia/entry.html",{
            "page_converted": page_converted,
            "title":title,
        })

    #title not present in entries
    else:
        return render(request, "encyclopedia/error.html")



