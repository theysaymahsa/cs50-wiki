from django.shortcuts import render, redirect
import markdown
from . import util
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = convert_md_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {"message": "Page Not Found!"})
    return render(request, "encyclopedia/entry.html", {"title": title, "content": content})


def search(request):
    query=request.GET.get("q","")
    entries=util.list_entries()

    for entry in entries:
        if entry.lower() == query.lower():
            return redirect("entry", title=entry)

    results=[]
    for entry in entries:
        if query.lower() in entry.lower():
            results.append(entry)
    return render(request, "encyclopedia/search.html" , {
            "query": query,
            "results": results
        })

def create(request):
    if request.method == "POST":
        title=request.POST.get("title")
        content= request.POST.get("content")

        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {"message": "Page already exists."})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    content=util.get_entry(title)
    if request.method=="POST":
        new_content=request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {"title":title, "content":content})

def random_page(request):
    entries=util.list_entries()
    entry=random.choice(entries)
    return redirect("entry", title=entry)

