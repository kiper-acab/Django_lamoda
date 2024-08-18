from django.contrib import admin
from .models import *

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

admin.site.register(Category, CategoryAdmin)
admin.site.register(Thing, ThingAdmin)