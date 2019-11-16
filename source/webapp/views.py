from django.contrib.auth.mixins import LoginRequiredMixin
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


class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/create.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/update.html'
    context_object_name = 'product'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'product'


# class ReviewListView(ListView):
#     template_name = 'review/list.html'
#     model = Review
#     context_object_name = 'reviews'


# class ReviewForProductCreateView(LoginRequiredMixin, CreateView):
#     model = Product
#     template_name = 'review/create.html'
#     form_class = ReviewProductForm
#
#     def dispatch(self, request, *args, **kwargs):
#         self.article = self.get_article()
#         if self.article.is_archived:
#             raise Http404
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         self.object = self.rev.create(
#             author=self.request.user,
#             **form.cleaned_data
#         )
#         return redirect('webapp:product_detail', pk=self.article.pk)
#
#     def get_article(self):
#         pr_pk = self.kwargs.get('pk')
#         return get_object_or_404(Review, pk=review_pk)


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


class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'review/update.html'
    form_class = ReviewForm
    context_object_name = 'review'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author \
               or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.product.pk})


class ReviewDeleteView(DeleteView):
    model = Review

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author \
               or self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.product.pk})