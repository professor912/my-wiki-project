from django.shortcuts import render, redirect
from . import util
import random
import markdown

def index(request):
    """
    Display a list of all available encyclopedia entries on the homepage.
    """
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})

def entry(request, title):
    """
    Display a specific entry with rendered Markdown content.
    """
    content = util.get_entry(title)
    
    if content is None:
        message = f"The page '{title}' was not found."
        return render(request, "encyclopedia/error.html", {"message": message})
    
    # Convert the Markdown content to HTML
    content_html = markdown.markdown(content)
    
    return render(request, "encyclopedia/entry.html", {"title": title, "content": content_html})

def search(request):
    """
    Search for entries based on the query string provided by the user.
    """
    query = request.GET.get('q', '').lower()
    
    if query:
        entries = util.list_entries()
        matching_entries = [entry for entry in entries if query in entry.lower()]
        
        if len(matching_entries) == 1 and matching_entries[0].lower() == query:
            return redirect('entry', title=matching_entries[0])

        if matching_entries:
            return render(request, "encyclopedia/search.html", {
                'query': query,
                'matching_entries': matching_entries
            })

        message = f"No page found for '{query}'."
        return render(request, "encyclopedia/error.html", {"message": message})
    
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {'entries': entries})

def create(request):
    """
    Create a new encyclopedia page. Only allow creation if the title doesn't already exist.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            if util.get_entry(title):
                message = f"A page with the title '{title}' already exists."
                return render(request, "encyclopedia/error.html", {"message": message})

            util.save_entry(title, content)
            return redirect('entry', title=title)

        error_message = 'Both title and content are required.'
        return render(request, "encyclopedia/create.html", {'error': error_message})
    
    return render(request, "encyclopedia/create.html")

def random_page(request):
    """
    Redirect to a random encyclopedia entry.
    """
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect('entry', title=random_title)

def edit(request, title):
    """
    Edit an existing encyclopedia page.
    """
    content = util.get_entry(title)
    
    if content is None:
        message = f"The page '{title}' does not exist and cannot be edited."
        return render(request, "encyclopedia/error.html", {"message": message})

    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_content = request.POST.get('content')

        if new_title and new_content:
            util.save_entry(new_title, new_content)
            return redirect('entry', title=new_title)

        error_message = 'Both title and content are required.'
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'content': content,
            'error': error_message
        })
    
    return render(request, "encyclopedia/edit.html", {'title': title, 'content': content})
