from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def show_products(request):
    products = Product.objects.prefetch_related("images").all()
    return render(request, 'products.html', {'products': products})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        images_ids = request.POST.getlist('images')

        if form.is_valid():
            product = form.save()
            # Зберігаємо картинки і пріоритет
            for idx, img_id in enumerate(images_ids):
                img = ProductImage.objects.get(id=img_id)
                img.product = product
                img.priority = idx
                img.save()

            return redirect("products:show_products")
    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})

@csrf_exempt
def upload_temp_image(request):
    if request.method == "POST":
        print("FILES:", request.FILES)
        file_key = list(request.FILES.keys())[0]  # беремо перший ключ
        image_file = request.FILES[file_key]
        img = ProductImage.objects.create(image=image_file, priority=0)
        return JsonResponse({"file_id": img.id})
    return JsonResponse({"error": "Нема файлу"}, status=400)
