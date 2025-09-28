from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.show_products, name='show_products'),
    path('add/', views.add_product, name='add_product'),
    path("upload_temp_image/", views.upload_temp_image, name="upload_temp_image"),
    # path('delete/<int:products_id>/', views.delete_products, name='delete_products'),
    # path('edit/<int:products_id>/', views.edit_products, name='edit_products'),
]
