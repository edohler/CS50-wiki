from django.shortcuts import render
from . import util
from random import randrange
import markdown2

mark = markdown2.Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
	entries = util.list_entries()
	new_entries = []
	try:
		return render(request, "encyclopedia/entry.html", {
		"entry": mark.convert(util.get_entry(title)), "title": title
		})
	except TypeError:
		for entry in entries:
			if title.lower() in entry.lower():
				new_entries += [entry]
		return render(request, "encyclopedia/search.html", {
			"entries": new_entries, "input": title
    	})
	

def search(request):
	title = request.POST['q']
	entries = util.list_entries()
	new_entries = []
	if util.get_entry(title) == None:
		for entry in entries:
			if title.lower() in entry.lower():
				new_entries += [entry]
		return render(request, "encyclopedia/search.html", {
			"entries": new_entries, "input": title
    	})	
	else:
		return render(request, "encyclopedia/entry.html", {
		"entry": mark.convert(util.get_entry(title)), "title": title
		})

def new(request):
	return render(request, "encyclopedia/new.html")

def add(request):
	title = request.POST['title']
	maintext = request.POST['maintext']
	entries = util.list_entries()
	newEntry = request.POST['source']
	if newEntry == 'new':
		for i in range(len(entries)):
			entries[i] = entries[i].lower()
		if title.lower() in entries:
			return render(request, "encyclopedia/error.html", {
				"title": title
				})
		elif not title:
			return render(request, "encyclopedia/new.html")
		else:
			util.save_entry(title, maintext)
			return render(request, "encyclopedia/entry.html", {
				"entry": mark.convert(util.get_entry(title)), "title": title
				})
	elif newEntry == 'edit':
		util.save_entry(title, maintext)
		return render(request, "encyclopedia/entry.html", {
				"entry": mark.convert(util.get_entry(title)), "title": title
				})

def edit(request, title):
	return render(request, "encyclopedia/edit.html", {
		"entry": util.get_entry(title), "title": title
		})

def random(request):
	entries = util.list_entries()
	i = randrange(0, len(entries))
	title = entries[i]
	return render(request, "encyclopedia/entry.html", {
		"entry": mark.convert(util.get_entry(title)), "title": title
		})
