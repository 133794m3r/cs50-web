from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import *
from . import util
from django.utils.html import conditional_escape

def index(request):
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})

def random_page(request):
	pages = util.list_entries()
	print(len(pages))
	chosen_page = pages[randint(0,len(pages)-1)]
	return HttpResponseRedirect(f"wiki/{chosen_page}")

def show_page(request,page):
	page_rendered = util.get_entry(page)
	if page_rendered is None:
		return error(request,f"/wiki/{page}","Page wasn't found. Check your spelling or try to search for it.")
	else:
		page_rendered=markdown(page_rendered)
	return render(request,"encyclopedia/page.html",{
		"page_name": page,
		"page_content":page_rendered
	})

def error(request,page,msg):
	return render(request,"encyclopedia/error.html",{
		"msg":msg,
		"page":page
	})

def search_page(request,page=''):
	if page == '':
		if request.GET:
			page=request.GET.dict().get('query')
		elif request.POST:
			page = request.POST.dict().get('query')
		else:
			return render(request,"encyclopedia/search.html",{
				"entry":"No query given."
			})

	pages = util.list_entries()
	page_lower = page.lower()
	entry_lower = ''
	entries = []
	found = False
	for entry in pages:
		entry_lower = entry.lower()
		if page_lower == entry_lower:
			found = True
			break
		elif page_lower in entry_lower:
			entries.append(entry)
	else:
		if entries:
			return render(request,"encyclopedia/search.html",{
				"entries":entries
			})
		else:
			return render(request,"encyclopedia/search.html",{
				"entry":page
			})
	if found:
		return HttpResponseRedirect(f"wiki/{entry}")

def edit_page(request,name):
	if name:
		if request.method == "GET":
			content=util.get_entry(name)
			if content is None:
				return error(request,f'/edit/{name}','Article was not found, so editing is impossible.')

			return render(request,"encyclopedia/edit.html",{
				"contents":content,
				"page":name
			})
		elif request.method == "POST":
			title = request.POST['title']
			content = request.POST['content']
			util.save_entry(title,content)
			return render(request,"encyclopedia/edit.html",{
				"contents":content,
				"page":title
			})
	else:
		return error(request,f'/edit/{name}',"No name given, can't edit an article that doesn't have a name.")

def new_page(request):
	if request.method == "GET":
		return render(request,"encyclopedia/new.html",{
		})
	elif request.method == "POST":
		title = request.POST['title']
		content = request.POST['content']
		util.save_entry(title,content)
		return HttpResponseRedirect(f"wiki/{title}")
	else:
		return error(request,'/new',"Method no valid.")