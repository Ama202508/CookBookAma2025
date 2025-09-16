from django.contrib import admin

# Register your models here.
# recipes/admin.py
from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "created_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)

