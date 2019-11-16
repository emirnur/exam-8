from django import forms

from webapp.models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'photo']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'mark']


