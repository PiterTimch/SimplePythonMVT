import os
import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            filename = f"{uuid.uuid4().hex}.webp"

            buffer = BytesIO()
            img.save(buffer, format='WEBP')
            buffer.seek(0)

            self.image.save(filename, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

