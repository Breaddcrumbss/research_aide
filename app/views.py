from django.shortcuts import render
from .forms import SearchForm
from .utils import classify, find_cases

# Create your views here.
def index(request):
    return render(request, 'app/index.html', {
                    
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(data=request.POST)
        if form.is_valid():
            tag = classify(request.POST.get('input'))       # Pass tag into the function to find cases
            cases = find_cases(tag)
            return render(request, 'app/search.html', {
                'cases': cases,       # To change to cases
                'search': False
            })

    else:
        form = SearchForm()

        return render(request, 'app/search.html', {
            'form':form,
            'search': True
        })