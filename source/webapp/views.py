from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductForm,  ReviewForm
from webapp.models import Product, Review


class IndexView(ListView):
    model = Product
    template_name = 'index.html'


class ProductView(DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product/create.html'
    form_class = ProductForm
    permission_required = 'webapp.add_product'
    permission_denied_message = 'Доступ запрещен!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'product/update.html'
    context_object_name = 'product'
    form_class = ProductForm
    permission_required = 'webapp.change_product'
    permission_denied_message = 'Доступ запрещен!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'product'
    permission_required = 'webapp.delete_product'
    permission_denied_message = 'Доступ запрещен!'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review/create.html'
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        product_pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        product.review_product.create(author=self.request.user, product=product_pk, **form.cleaned_data)
        return redirect('webapp:product_detail', pk=product.pk)


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/update.html'
    form_class = ReviewForm
    context_object_name = 'review'
    permission_required = 'webapp.change_review'
    permission_denied_message = 'Доступ запрещен!'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author \
               or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.product.pk})


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    permission_required = 'webapp.delete_review'
    permission_denied_message = 'Доступ запрещен!'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author \
               or self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.product.pk})