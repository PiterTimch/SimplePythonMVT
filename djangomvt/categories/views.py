from django.shortcuts import render
from .models import Category
from .forms import CategoryForm
from django.shortcuts import redirect

# Create your views here.

def show_categories(request):
    categories = Category.objects.all()

    return render(request, 'categories.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categories:show_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'add_category.html', {'form': form})