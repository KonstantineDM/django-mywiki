import os
import random

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from markdown2 import Markdown

from . import util
from .forms import EntryForm


def index(request):
    # Render main page
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Render the chosen wiki entry; if it does not exist: display warning
    try:
        # Convert markdown to HTML before rendering
        entry_html = Markdown().convert(util.get_entry(title))
    except TypeError:
        return render(request, "encyclopedia/entry.html", {
        "entry": "Entry not found",
        "title": title,
    })
    return render(request, "encyclopedia/entry.html", {
        "entry": entry_html,
        "title": title,
    })

def search(request):
    """
    Search for entry in the wiki (case-insensitive);
    searches for any matches between search string and entry name strings;
    if at least some characters match - returns a list of matching entries;
    else displays a warning
    """
    all_entries = [entry for entry in util.list_entries()]
    request_text = request.GET.get("q", "")
    matches = [match for match in all_entries if request_text in match or request_text in match.lower()]
    if request_text and request_text in [entry.lower() for entry in all_entries]:
        return entry(request, request_text)
    elif matches:
        return render(request, "encyclopedia/results.html", {
            "matches": matches,
        })
    else:
        return render(request, "encyclopedia/entrynotfound.html", {
        "entry": "Entry not found",
        "title": request_text,
    })


def newpage(request):
    # Create a new entry; save entry's .md file to "entries" directory
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            if os.path.isfile(f"./entries/{form.cleaned_data['title']}.md".lower()):
                return render(request, "encyclopedia/newpageexists.html", {
                })
            else:
                with open(f"./entries/{form.cleaned_data['title']}.md", "w+") as entry_file:
                    entry_file.write("# " + form.cleaned_data['title'])
                    entry_file.write("\n")
                    entry_file.write(form.cleaned_data['entry'])
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={
                    "title": form.cleaned_data['title']
                }))
        else:render(request, "encyclopedia/newpage.html", {
        "form": form,
        })

    return render(request, "encyclopedia/newpage.html", {
        "form": EntryForm()
    })

def editpage(request, title):
    # Edit existing page; accessed through visiting entry's view
    original_title = title
    original_content = util.get_entry(title)
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_content = form.cleaned_data["entry"]
            # After editing save entry to "entries" directory
            util.save_entry(original_title, entry_title, entry_content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={
                "title": entry_title,
            }))
        else:
            return render(request, "encyclopedia/editpage.html", {
                "form": form,
                "title": title,
            })
            
    return render(request, "encyclopedia/editpage.html", {
        "form": EntryForm(initial={"title": original_title, "entry": original_content}),
        "title": original_title
    })

def randompage(request):
    # Display random existing wiki page
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={
        "title": entry,
    }))
