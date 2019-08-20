from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView, ListView, DetailView
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerSignupForm, CustomerLogInForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponseRedirect
from django.utils.encoding import force_text
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from cart.models import *




# Create your views here.

class IndexView(ListView):
    template_name = 'acereadymade/index.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(available=True).order_by('-created')[0:4]
        context['featured_products'] = Product.objects.filter(available=True, featured=True).order_by('-created')[0:5]
        context['latest_products'] = Product.objects.filter(available=True, latest=True).order_by('-created')[0:4]
        context['topkurtha_products'] = Product.objects.filter(available=True, topkurtha=True).order_by('-created')[0:4]
        context['topfeatured_products'] = Product.objects.filter(available=True, topfeatured=True).order_by('-created')[0:4]
        context['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(user=self.request.user)
            cart_item_count = CartItem.objects.filter(cart=cart).count
            context['total_item'] = cart_item_count
        return context



class CustomerSignUpView(View):
    form_class = CustomerSignupForm
    template_name = 'acereadymade/create-new.html'

    def get(self, request):
        form = self.form_class()
        categories = Category.objects.all()
        return render(request, self.template_name, {'form': form, 'categories': categories})

    def post(self, request):
        print("print method called")
        form = self.form_class(request.POST)

        print(form.is_valid(), request.POST)

        if form.is_valid():
            print("Inside form.isvalid111")
            user = form.save(commit=False)
            user.is_active = False
            user.username = user.first_name
            user.save()


            Customer.objects.create(user=user).save()
            # Cart.objects.create(user=user)

            print(type(user), '111111111', 's', '222222222', type('s'))
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            print("after saving user.......................")
            message = render_to_string('acereadymade/account_activation_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': account_activation_token.make_token(user),
                                       })

            to_email = form.cleaned_data.get('email')

            email = EmailMessage(
                subject, message, to=[to_email]

            )
            email.send()

            return HttpResponse('Please Click the link to activate in your Gmail Inbox')

        return render(request, 'acereadymade/create-new.html')

class LogoutView(View):
    success_url = reverse_lazy('acereadymade_app:login')

    def get(self, request):
        logout(request)
        return redirect(self.success_url)


def account_activation_sent(request):
    return render(request, 'acereadymade/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # user.email_confirmed = True
        # user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('acereadymade_app:index')
    else:
        return render(request, 'account_activation_invalid.html')


#
# class LogInView(ListView):
#     template_name = 'acereadymade/myaccount.html'
#     model = Category
#
#     def get_context_data(self, **kwargs):
#         context = super(LogInView, self).get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         return context


class LogInView(View):
    success_url = reverse_lazy('acereadymade_app:index')
    template_name = 'acereadymade/myaccount.html'
    form_class = CustomerLogInForm

    # template_name = 'myshop_app/login.html'
    def get(self, request):
        categories = Category.objects.all()
        form = self.form_class()
        return render(request, self.template_name, {'login_error': 'Please Login to Continue', 'categories': categories, 'form': form})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = User.objects.get(email=str(email)).username
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(self.success_url)
        else:
            form = self.form_class()
            return render(request, 'acereadymade/myaccount.html', {'form': form})


class DetailsView(TemplateView):
    template_name = 'cart/viewfinish.html'


class ShopView(TemplateView):
    template_name = 'acereadymade/shop.html'

class BaseView(ListView):
    template_name = 'acereadymade/base.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ContactView(TemplateView):
    template_name = 'acereadymade/contact.html'

class MyAccoutView(TemplateView):
    template_name = 'acereadymade/myaccount.html'

class WishListView(TemplateView):
    template_name = 'acereadymade/wishlist.html'


class ProductList(ListView):
    template_name = 'acereadymade/shop.html'
    model = Product


    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        products = Product.objects.filter(available=True)
        context['topfeatured_products'] = Product.objects.filter(available=True, topfeatured=True)
        print(11111111111111111111, products)
        context['categories'] = Category.objects.all()
        try:
            category_slug = self.kwargs['category_slug']
        except KeyError:
            category_slug = None

        context['products'] = products
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            context['products'] = products.filter(category=category)
        return context


class ProductDetail(DetailView):
    template_name = 'cart/detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['product'] = Product.objects.get(slug=self.kwargs['product_slug'])
        context['categories'] = Category.objects.all()
        return context




