from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Recipe


def recipe_list(request):
    recipes = Recipe.objects.order_by('title')
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'page_title': 'Rețete (alfabetic)',
    })


def recipe_list_by_date(request):
    recipes = Recipe.objects.order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'page_title': 'Rețete (după data creării)',
    })


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Adaugă rețetă',
    })


@login_required
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    if recipe.owner != request.user:
        raise PermissionDenied("Nu poți edita rețetele altor utilizatori.")
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES or None, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Editează rețetă',
    })


@login_required
def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    if recipe.owner != request.user:
        raise PermissionDenied("Nu poți șterge rețetele altor utilizatori.")
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})
