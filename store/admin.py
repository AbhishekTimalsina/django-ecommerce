from django.contrib import admin
from .models import Category, Book,BookImage
# Register your models here.


class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1 
    fields = ['image', 'is_primary']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_price', 'category']
    # prepopulated_fields = {'slug': ('name',)}
    inlines = [BookImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
