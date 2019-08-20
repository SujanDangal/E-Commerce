from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, View, FormView, ListView, DetailView, DeleteView
from django.views.generic.edit import UpdateView
from acereadymade_app.models import *
from cart.models import *
from .forms import AddCategoryForm, AddProductForm, EditCategoryForm
from django.urls import reverse_lazy
from PIL import Image
import os


# Create your views here.

class dashboard(TemplateView):
    template_name = 'dashboard/index.html'


class base(TemplateView):
    template_name = 'dashboard/base.html'

class categories(TemplateView):
    template_name = 'dashboard/m_categories.html'

    def get_context_data(self, **kwargs):
        context = super(categories, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context


class add_categories(TemplateView):
    success_url = reverse_lazy('dashboard:categories')
    form_class = AddCategoryForm
    template_name = 'dashboard/modals.html'

    def get_context_data(self, **kwargs):
        context = super(add_categories, self).get_context_data()
        context['add_categories'] = Category.objects.all()
        context['form'] = self.form_class()
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        print(11111111111111111, request.POST)
        if form.is_valid():
            Category.objects.create(name=request.POST['name'], slug=request.POST['slug']).save()

        else:
            return render(request, 'dashboard/m_categories.html')

        return redirect(self.success_url)


class order(TemplateView):
    template_name = 'dashboard/m_orders.html'

    def get_context_data(self, **kwargs):
        context = super(order, self).get_context_data(**kwargs)
        # print(222222222222222222222222222222222222222222222222)
        # context['categories'] = Category.objects.all()
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context




class users(TemplateView):
    template_name = 'dashboard/m_users.html'

    def get_context_data(self, **kwargs):
        context = super(users, self).get_context_data()
        context['users'] = User.objects.all()
        return context

class products(TemplateView):
    template_name = 'dashboard/m_products.html'

    def get_context_data(self, **kwargs):
        context = super(products, self).get_context_data()
        context['products'] = Product.objects.all()
        return context


class add_products(TemplateView):
    success_url = reverse_lazy('dashboard:products')
    form_class = AddProductForm
    template_name = 'dashboard/add_products.html'

    def get_context_data(self, **kwargs):
        context = super(add_products, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['form'] = self.form_class()
        return context

    def post(self, request):
        category = Category.objects.get(id=request.POST['category'])
        print(request.POST)
        product = Product.objects.create(category=category, name=request.POST['name'], slug=request.POST['slug'],
                               description=request.POST['description'], price=request.POST['price'],
                               image=request.FILES['image'], stock=request.POST['stock'])
        try:
            featured = request.POST['featured']
            product.featured = True
        except KeyError:
            product.featured = False

        try:
            available = request.POST['available']
            product.available = True
        except KeyError:
            product.available = False

        try:
            topkurtha = request.POST['topkurtha']
            product.topkurtha = True
        except KeyError:
            product.topkurtha = False

        try:
            latest = request.POST['latest']
            product.latest = True
        except KeyError:
            product.latest = False

        try:
            topfeatured = request.POST['topfeatured']
            product.topfeatured = True
        except KeyError:
            product.topfeatured = False

        product.save()
        return redirect(self.success_url)

        # size_300 = (255, 399)
        # size_700 = (600, 938)
        #
        # for f in os.listdir('.'):
        #     if f.endswith('.jpg'):
        #         i = Image.open(f)
        #         fn, fext = os.path.splitext(f)
        #
        #         i.thumbnail(size_300)
        #         i.save('small/{}_small{}'.format(fn, fext))
        #
        #         i.thumbnail(size_700)
        #         i.save('large/{}_large{}'.format(fn, fext))




    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     print(11111111111111111, request.POST)
    #     if form.is_valid():
    #         Category.objects.create(name=request.POST['name'], slug=request.POST['slug']).save()
    #
    #     else:
    #         return render(request, 'dashboard/m_categories.html')
    #
    #     return redirect(self.success_url)

class DeleteProduct(View):

    def post(self, request, **kwargs):
        product_id = kwargs['product_id']
        Product.objects.get(id=product_id).delete()
        return redirect('dashboard:products')


class DeleteCategory(View):

    def post(self, request, **kwargs):
        category_id = kwargs['category_id']
        Category.objects.get(id=category_id).delete()
        return redirect('dashboard:categories')

class DeleteUser(View):

    def post(self, request, **kwargs):
        user_id = kwargs['user_id']
        User.objects.get(id=user_id).delete()
        return redirect('dashboard:users')


class EditCategory(View):
    success_url = reverse_lazy('dashboard:categories')

    def get(self, request, **kwargs):
        form = EditCategoryForm
        category = Category.objects.get(id=kwargs['category_id'])
        return render(request, 'dashboard/editmodals.html', {'category': category, 'form': form})

    def post(self, request, **kwargs):
        form_data = request.POST
        print(22222222222222222222,form_data)
        category = Category.objects.get(id=kwargs['category_id'])
        category.name = form_data['name']
        category.slug = form_data['slug']
        category.save()
        return redirect('dashboard:categories')