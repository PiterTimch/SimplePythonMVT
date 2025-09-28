from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Product, ProductImage
from .forms import ProductForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

def show_products(request):
    products = Product.objects.prefetch_related("images").all()
    return render(request, 'products.html', {'products': products})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        images_ids = request.POST.getlist('images')

        if form.is_valid():
            product = form.save()
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
        file_key = list(request.FILES.keys())[0]
        image_file = request.FILES[file_key]
        img = ProductImage.objects.create(image=image_file, priority=0)
        return JsonResponse({"file_id": img.id})
    return JsonResponse({"error": "Нема файлу"}, status=400)

@csrf_exempt
def delete_temp_image(request):
    if request.method == "DELETE":
        import json
        data = json.loads(request.body)
        file_id = data.get("file_id")
        if file_id:
            try:
                img = ProductImage.objects.get(id=file_id, product__isnull=True)
                if img.image:
                    if os.path.isfile(img.image.path):
                        os.remove(img.image.path)
                img.delete()
                return JsonResponse({"status": "ok"})
            except ProductImage.DoesNotExist:
                return JsonResponse({"error": "File not found"}, status=404)
        return JsonResponse({"error": "No file_id provided"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)