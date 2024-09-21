from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', "name", 'photo',)
    list_display_links = ('id', "name")
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ThingAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'name', 'price', 'discount', 'image', 'size',)
    list_filter = ('brand',)
    search_fields = ("name", 'brand',)
    list_display_links = ('id', "name",)
    prepopulated_fields = {'thing_slug': ('name',)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'first_name', 'last_name', 'phone', 'date')
    list_filter = ('status',)
    search_fields = ("first_name", 'status', 'phone', 'date')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Thing, ThingAdmin)
admin.site.register(Basket)
admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserAdmin)