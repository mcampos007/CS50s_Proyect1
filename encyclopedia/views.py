from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django import forms

import markdown2
import random

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    # content = forms.CharField(widget=forms.Textarea, label="Content")
    content = forms.CharField(
    widget=forms.Textarea(attrs={'rows': '10', 'cols': '80', 'style': 'width: 50%; height: 300px;'}),
    label="Content"
)
    
class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': '10', 'cols': '80', 'style': 'width: 50%; height: 300px;'}),
    label="Content")    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):    
    # Utiliza la función get_entry desde util para obtener el contenido en Markdown
    markdown_content = util.get_entry(title)
    
    if markdown_content is None:
        # # Si no se encuentra la entrada, devuelve un error 404
        # raise Http404("Entry not found.")
    # Renderiza 404.html manualmente para verificar que funciona
        return render(request, "encyclopedia/404.html", status=404)
    
    # Convierte el contenido Markdown a HTML
    html_content = markdown2.markdown(markdown_content)
    
    # Renderiza la plantilla con el contenido HTML
    # html_content
    return render(request, "encyclopedia/title.html", {
        "title": title,
         "content": html_content 
    })

def search(request):
     if request.method == "POST":
        query = request.POST.get("q")
        entries = util.list_entries()

        # Si la búsqueda coincide exactamente con una entrada, redirige a esa página
        if query in entries:
            return redirect("title", title=query)
        
        # Filtra entradas que contengan la consulta
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

        # Renderiza una página con los resultados
        return render(request, "encyclopedia/search_results.html", {
            "entries": matching_entries,
            "query": query
        })
     else:
        return redirect("index")
     
def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)            
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            #verificar si existe una entrada con el titulo
            if util.get_entry(title):
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": "A page with this title already exist!"
                })
            
            #Guarda la nueva entrada
            util.save_entry(title, content)

            #Redirigue a la nueva pagina
            return redirect("title", title=title)
    else:
        form = NewPageForm()

    return render(request,"encyclopedia/new_page.html", {"form":form})

def edit_page(request, title):
    
    if request.method == "POST" :

        form = EditEntryForm(request.POST)
    
        if form.is_valid():
            # Utiliza form.cleaned_data para obtener el contenido
            new_content = form.cleaned_data['content']
            util.save_entry(title, new_content)
            
            # Redirige a la página de la entrada una vez guardada
            return redirect("title", title=title)
    else:
        # Si es GET, inicializa el formulario con el contenido actual
        content = util.get_entry(title)
        # Convierte el contenido Markdown a HTML
        # html_content = markdown2.markdown(content)
        form = EditEntryForm(initial={'content': content})

    # Renderiza el formulario con el contenido actual del text area
    return render(request, "encyclopedia/edit_page.html", {
        "form": form,
        "title": title,
        "content":content
    })

    
def random_page(request):
# Obtén la lista de todas las entradas disponibles
    entries = util.list_entries()

# Selecciona una entrada aleatoria
    random_entry = random.choice(entries)

# Redirige a la vista de la entrada aleatoria
    return redirect("title", title=random_entry)