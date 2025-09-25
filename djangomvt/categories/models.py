from django.db import models
import uuid

def image_upload_to(instance, filename):
    ext = "webp"
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f'images/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

