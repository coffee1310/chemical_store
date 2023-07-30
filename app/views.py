from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, ListView

from .forms import SearchForm, UserRegisterForm, UserLoginForm, UserProfileForm
from .models import *


# Create your views here.

class HomePage(TemplateView):
    template_name = "app/index.html"
    model = Product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        context["category"] = Category.objects.annotate(num_products=Count('product')).filter(num_products__gt=0)
        context["categories"] = Category.objects.annotate(num_products=Count('product')).filter(num_products__gt=0)
        context["search_form"] = SearchForm()
        context["title"] = "Reactive Mart"
        context["method"] = "POST"
        return context

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            context = super().get_context_data(**kwargs)
            query = form.cleaned_data['query']
            results = Product.objects.filter(product_name__icontains=query)
            context["products"] = results
            context["category"] = set([r.cat for r in results])
            context["categories"] = Category.objects.annotate(num_products=Count('product')).filter(num_products__gt=0)
            context["search_form"] = form
            context["title"] = "Reactive Mart"
            context["method"] = "POST"
            return self.render_to_response(context)
        return render(request, self.template_name, self.get_context_data(form=form))

class CategoryProduct(ListView):
    model = Product
    context_object_name = "products"
    template_name = "app/index.html"
    def get_queryset(self):
        cat_slug = self.kwargs["cat_slug"]
        print(Product.objects.filter(cat__cat_slug=cat_slug))
        return Product.objects.filter(cat__cat_slug=cat_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_slug = self.kwargs["cat_slug"]
        context["category"] = Category.objects.filter(cat_slug=cat_slug)
        context["categories"] = Category.objects.annotate(num_products=Count('product')).filter(num_products__gt=0)
        context["search_form"] = SearchForm()
        context["method"] = "GET"
        query = self.request.GET.get('query')
        if query:
            search_results = Product.objects.filter(product_name__icontains=query)
            context["products"] = search_results
        return context

class RegisterUser(FormView):
    template_name = 'app/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        context["categories"] = Category.objects.annotate(num_products=Count('product')).filter(num_products__gt=0)
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password1 = form.cleaned_data['password1']
        user_adress = form.cleaned_data['user_adress']
        user_birth_date = form.cleaned_data['user_birth_date']
        user = User(username=username, user_adress=user_adress, user_birth_date=user_birth_date)
        user.set_password(password1)
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect("register_user")

class LoginUser(LoginView):
    template_name = "app/login.html"
    form_class = UserLoginForm


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        context["categories"] = Category.objects.annotate(num_products=Count('product')).filter(num_products__gt=0)
        return context

    def get_success_url(self):
        return reverse_lazy("index_page")

class UserProfile(TemplateView):
    template_name = 'app/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(num_products=Count('product')).filter(num_products__gt=0)
        context["title"] = "Профиль"
        context["search_form"] = SearchForm()
        context["method"] = "POST"
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class EditProfile(FormView):
    template_name = 'app/edit_profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('user_profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class AboutAccount(TemplateView):
    template_name = "app/about_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["username"] = self.request.user.username
        context["created_at"] = self.request.user.created_at
        context["user_adress"] = self.request.user.user_adress
        context["user_birth_date"] = self.request.user.user_birth_date
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)  # Получить объект продукта по его идентификатору

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    cart_item.quantity += 1
    cart_item.save()

    cart_items_count = Cart.objects.filter(user=user).count()

    response_data = {
        'message': f'Продукт с ID {product_id} был успешно добавлен в корзину.',
        'cart_items_count': cart_items_count,
    }
    return JsonResponse(response_data)

def remove_from_cart(request, product_id):
    user = request.user
    cart_item, created = Cart.objects.get_or_create(user=user, product_id=product_id)
    cart_item.quantity -= 1
    cart_item.save()
    cart_items_count = Cart.objects.filter(user=user).count()
    response_data = {
        'message': f'Продукт с ID {product_id} был успешно добавлен в корзину.',
        'cart_items_count': cart_items_count,
    }
    print(response_data, cart_item.quantity)
    return JsonResponse(response_data)

def clear_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    cart.delete()
    response_data = {
        'message': 'Корзина успешно очищена.',
    }
    return JsonResponse(response_data)

def logout_user(request):
    logout(request)
    return redirect("index_page")

def order_history(request):
    pass