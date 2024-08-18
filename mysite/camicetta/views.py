
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.views.generic import ListView, DetailView, CreateView
from django.http import Http404
# from django.urls import reverse_lazy 
# from .forms import RegisterUserForm


from .models import *
# Create your views here.

class Main(ListView):
    model = Category
    template_name = 'camicetta/index.html'
    context_object_name = 'categories'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная страница'
        return context
        

# def main(requests):
#     categories = Category.objects.all()
#     context = {
#         'categories': categories
#     }
#     return render(requests, 'camicetta/index.html', context=context)


class CategoryView(ListView):
    template_name = 'camicetta/category.html'
    model = Thing
    context_object_name = 'things'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(f"Категория - {Category.objects.get(slug=self.kwargs['cat_slug'])}")
        context['cat_slug'] = self.kwargs['cat_slug']
        return context
    
    def get_queryset(self):
        return Thing.objects.filter(cat__slug=self.kwargs['cat_slug'])

# def category(requests, cat_slug):
#     category = Category.objects.get(slug=cat_slug)
    # things = Thing.objects.filter(cat_id=category)
#     context = {
#         'cat_slug': cat_slug,
#         'things': things
#     }
#     return render(requests, 'camicetta/category.html', context=context)


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
        print()
        return Thing.objects.get(thing_slug=slug)
    

# def thing(requests, thing_slug):
#     thing = Thing.objects.get(thing_slug=thing_slug)
#     thing_sizes = thing.size.split('-')
#     thing_sizes = [i for i in range(int(thing_sizes[0]), int(thing_sizes[1]))]
#     context = {
#         'thing': thing,
#         'thing_sizes': thing_sizes
#         }
#     return render(requests, 'camicetta/thing.html', context=context)



# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'auth/register.html'
#     success_url = reverse_lazy('login')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs) 
#         context['title'] = 'Регистрация'
#         return context
    

def login(requests):
    if requests.method == 'POST':
        login = requests.POST.get('login')
        password = requests.POST.get('password')

        user = authenticate(requests, username=login, password=password)
        if user is not None:
            user_login(requests, user)
            return redirect('main')
        
        else:
            return render(requests, 'auth/login.html')


    
    else:
        return render(requests, 'auth/login.html')


def register(requests):
    return render(requests, 'auth/register.html')