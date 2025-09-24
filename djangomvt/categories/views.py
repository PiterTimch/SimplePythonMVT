from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm
from django.utils.text import slugify

def show_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.name)
            category.save()
            return redirect('categories:show_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'add_category.html', {'form': form})

def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
    except Category.DoesNotExist:
        pass
    return redirect('categories:show_categories')
