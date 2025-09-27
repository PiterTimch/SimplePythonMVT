from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Category.objects.filter(name__iexact=name)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Категорія з такою назвою вже існує.")
        return name
