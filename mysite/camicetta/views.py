from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.views.generic import ListView, DetailView, CreateView
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy 
from .forms import *
from .other_func import handle_uploaded_file, validate_password
import os

from .models import *


class Main(ListView):
    model = Category
    template_name = 'camicetta/index.html'
    context_object_name = 'categories'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная страница'

        if self.request.user.is_authenticated:
            basket = Basket.objects.filter(user=self.request.user, is_ordered=False)
            context["basket_len"] = sum([i.quantity for i in basket])
        return context
        


class CategoryView(ListView):
    template_name = 'camicetta/category.html'
    model = Thing
    context_object_name = 'things'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(f"Категория - {Category.objects.get(slug=self.kwargs['cat_slug'])}")
        context['cat_slug'] = self.kwargs['cat_slug']
        if self.request.user.is_authenticated:
            basket = Basket.objects.filter(user=self.request.user, is_ordered=False)
            context["basket_len"] = sum([i.quantity for i in basket])
        return context
    
    def get_queryset(self):
        return Thing.objects.filter(cat__slug=self.kwargs['cat_slug'])


class ThingView(DetailView):
    model = Thing
    template_name = 'camicetta/thing.html'
    slug_url_kwarg = 'thing_slug'


    def get_context_data(self, **kwargs):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        context = super().get_context_data(**kwargs)
        thing = Thing.objects.get(thing_slug=slug)
        thing_sizes = thing.size

        context['title'] = f'{thing.name} - {thing.brand}'
        context['thing'] = thing 

        if self.request.user.is_authenticated:
            basket = Basket.objects.filter(user=self.request.user, is_ordered=False)
            context["basket_len"] = sum([i.quantity for i in basket])

        if not thing_sizes:      
            context['thing_sizes'] = None

        elif len(thing_sizes.split(', ')) > 1:
            context['thing_sizes'] = thing_sizes.split(', ')

        elif thing_sizes.split(', ')     == 1:
            context['thing_sizes'] = [thing_sizes]

        else:
            raise Http404()
        
        return context
    

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        return Thing.objects.get(thing_slug=slug)
    

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Регистрация'
        return context
    

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'auth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Авторизация'
        return context



@login_required
def profile(requests):
    if requests.method == 'POST':
        user = User.objects.get(pk=requests.user.pk)
        photo = requests.FILES['image']
        
        if user.image:
            os.remove(user.image.path)
        
        handle_uploaded_file(photo)
        user.image = f'photos/photos_users/{photo.name}'
        user.save()
        
        return redirect('profile')

    context = {
        'orders': Order.objects.filter(user=requests.user),
        'form': LoadPhoto,
    }
    return render(requests, 'camicetta/profile.html', context=context)


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = User
    context_object_name = 'user'
    template_name = 'camicetta/profile.html'
    queryset = model.objects.all().select_related('user')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context
    
    def get_queryset(self):
        return User.objects.get(pk=self.request.user.pk)



@login_required
def bakset(requests):
    basket = Basket.objects.filter(user=requests.user, is_ordered=False)
    context = {
        'basket': basket,
        'title': 'Корзина',
        'basket_len': sum([i.quantity for i in basket]),
    }

    for el in context['basket']:
        el.thing.price *= el.quantity
        el.thing.discount *= el.quantity  

    return render(requests, 'camicetta/basket.html', context=context)


@login_required
def basket_update(request, basket_id, action):
    basket_item = get_object_or_404(Basket, id=basket_id)
    
    if action == 'increase':
        basket_item.quantity += 1
        basket_item.save()
    elif action == 'decrease':
        if basket_item.quantity > 1:
            basket_item.quantity -= 1
            basket_item.save()
        else:
            basket_item.delete()
            return JsonResponse({'success': True, 'deleted': True})

    return JsonResponse({'success': True, 'quantity': basket_item.quantity})


def add_to_basket(request, thing_slug, size):
    thing = Thing.objects.get(thing_slug=thing_slug)
    basket = Basket.objects.filter(thing=thing, user=request.user, is_ordered=False)
    basket_sizes = [i.size for i in basket]
    thing_sizes = thing.size.split(', ')

    if str(size) in basket_sizes:
        basket = basket.get(size=size)
        basket.quantity += 1
        basket.save()
        return redirect('basket')
    
    else:
        if str(size) in thing_sizes:
            Basket.objects.create(thing=thing, user=request.user, size=size, quantity=1)
            return redirect('basket')
        

@login_required
def clean_basket(requests):
    Basket.objects.filter(user=requests.user, is_ordered=False).delete()
    return redirect('basket')
    
        
    
    

@login_required
def logout_user(request):
    logout(request)
    return redirect('main')




@login_required
def formalization(requests):
    if requests.method == 'POST':
        things = Basket.objects.filter(user=requests.user, is_ordered=False)
        total_price = []
        for el in things:
            if el.thing.discount == 0:
                total_price.append(el.thing.price * el.quantity)
            else:
                total_price.append(el.thing.discount * el.quantity)

        total_price = sum(total_price)

        order = Order.objects.create(
            user=requests.user,
            first_name=requests.POST['first_name'],
            last_name=requests.POST['last_name'], 
            phone=requests.POST['phone'], 
            address=requests.POST['address'],
            delivery_type=requests.POST['delivery_type'], 
            comments=requests.POST['comments'], 
            total_cost=total_price,
        )

        order.things.set(things)
        order.save()

        for thing in things:
            thing.is_ordered = True
            print(thing.is_ordered)
            thing.save()

        return redirect('main')

        
    else:
        context = {
            'form': OrderForm
        }
        return render(requests, 'camicetta/formalization.html', context=context)
 

@login_required
def profile_settings(request):
    context = {
    }
    if request.method == 'POST':
        if 'form1' in request.POST:
            form = UserSettingsForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')
            else:
                form = UserSettingsForm
                context = {
                    'form': form
                }
        
        elif 'form2' in request.POST:
            current_password = request.POST.get('current_password')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            is_valid_password, message = validate_password(password1)
            if password1 == password2:
                if is_valid_password:
                    if check_password(current_password, request.user.password):
                        user = User.objects.get(pk=request.user.id)
                        user = authenticate(request, username=user.username)
                        request.user.set_password(password1)
                        request.user.save()
                        login(request, user)
                    else:
                        messages.warning(request, 'Текущий пароль неверен')
                else:
                    messages.warning(request, message)
            else:
                messages.warning(request, 'Пароли не сопадают')
    return render(request, 'camicetta/settings.html', context=context)
