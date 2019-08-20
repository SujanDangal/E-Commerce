from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from acereadymade_app.models import *
from .models import Cart, CartItem, Order
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from .forms import OrderForm






#
# class DetailView(TemplateView):
#     template_name = 'cart/detail.html'


class CartView(ListView):
    template_name = 'cart/cart.html'


class ProceedCheckoutView(TemplateView):
    form_class = OrderForm
    template_name = 'cart/proceed_checkout.html'
    model = Cart

    def get_context_data(self, **kwargs):
        context = super(ProceedCheckoutView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Cart.objects.get(user=self.request.user)
            context['carts'] = CartItem.objects.filter(cart=cart)

        context['categories'] = Category.objects.all()
        context['form'] = self.form_class()
        total = 0
        counter = 0
        for cart_item in CartItem.objects.all():
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
        context['total'] = total
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        print(55555555555,request.POST)
        cart = Cart.objects.get(user=self.request.user)
        cart_item = CartItem.objects.filter(cart=cart)
        if form.is_valid():
            form_data = request.POST
            for item in cart_item:
                print(13333333333333333333333333333333333333)
                order = Order.objects.create(
                    user=self.request.user,
                    product=item.product,
                    f_name=form_data['f_name'],
                    l_name=form_data['l_name'],
                    country=form_data['country'],
                    street_add=form_data['street_add'],
                    apartment=form_data['apartment'],
                    town=form_data['town'],
                    state=form_data['state'],
                    postcode=form_data['postcode'],
                    phone=form_data['phone'],
                    email=form_data['email'],
                    information=form_data['information'],
                )
                if form_data['company_name']:
                    order.company_name = form_data['company_name']

                if form_data['apartment']:
                    order.apartment = form_data['apartment']

                if form_data['postcode']:
                    order.apartment = form_data['postcode']

                if form_data['information']:
                    order.apartment = form_data['information']

                order.save()
                item.delete()
            return redirect('cart:order_list')

        return render(request, 'cart/proceed_checkout.html')


class ViewCartView(TemplateView):
    template_name = 'cart/viewfinish.html'


class OrderView(TemplateView):
    template_name = 'cart/ordersummery.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        print(222222222222222222222222222222222222222222222222)
        context['categories'] = Category.objects.all()
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context






# def _cart_id(request):  # checking if a session id has been created on the customer browser
#     cart = request.session.session_key
#     if not cart:
#         cart = request.session.create()
#     return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    print(11111111111111111111111111111111111111111, request.user)
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('acereadymade_app:login')

    try:  # getting a cart by id and if it does'nt exist then we will create the cart
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            user=request.user,
            cart_id=request.user.id
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)  # adding product to cart
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):  # this method is used to display cart
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        # products = Product.objects.get(price=price(request))

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY  # processing payments using stripe api
    stripe_total = int(total * 100)
    description = 'Perfect Cushion Store - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':  # doing this to get the stripe token and email address in order to create the customer record and the charge
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']  # to get Billing Name from stripe payment form
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingState = request.POST['stripeBillingAddressState']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingState = request.POST['stripeShippingAddressState']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='gbp',
                description=description,
                customer=customer.id
            )
            ''' Creating the Order '''
            try:
                order_details = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingState=billingState,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingState=shippingState,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )
                order_details.save()
                for order_item in cart_items:  # every time the for loop runs a cart item is assigned to the order item variable
                    oi = OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )  # oi variable is getting the value of each order item in order to create the order item record
                    oi.save()
                    '''Reduce stock when order is placed or saved'''
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()
                    '''The terminal will print this message when the order is saved'''
                    print('The order has been created')
                try:
                    ''' Calling the sendEmail function '''
                    sendEmail(order_details.id)
                    print('The order email has been sent to the customer.')
                except IOError as e:
                    return e
                return redirect('order:thanks', order_details.id)
            except ObjectDoesNotExist:
                pass
        except stripe.error.CardError as e:
            return False, e

    return render(request, 'cart/viewfinish.html', dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key,
                                             stripe_total=stripe_total, description=description))


def cart_remove(request, product_id):  # to remove a quantity product from cart
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def full_remove(request, product_id):  # to remove the entire stock of a product from cart
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


def sendEmail(order_id):
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)
    try:
        '''Sending the order'''
        subject = "Perfect Cushion Store - New Order #{}".format(
            transaction.id)  # using the transaction method to interpolate the transaction id in the curly brackets of the subject
        to = ['{}'.format(transaction.emailAddress)]
        from_email = "orders@perfectcushionstore.com"
        order_information = {
            'transaction': transaction,
            'order_items': order_items
        }
        message = get_template('email/email.html').render(order_information)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
    except IOError as e:
        return e
