
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import RecipeForm
from .models import Recipe


def recipe_list(request):
    recipes = Recipe.objects.order_by('title')
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'page_title': 'Retete (alfabetic)',
    })


def recipe_list_by_date(request):
    recipes = Recipe.objects.order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'page_title': 'Retete (dupa data crearii)',
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
            messages.success(request, 'Reteta a fost creata.')
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Adauga reteta',
    })


@login_required
def recipe_edit(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    if recipe.owner != request.user:
        raise PermissionDenied("Nu poti edita retetele altor utilizatori.")
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES or None, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reteta a fost actualizata.')
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Editeaza reteta',
    })


@login_required
def recipe_delete(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    if recipe.owner != request.user:
        raise PermissionDenied("Nu poti sterge retetele altor utilizatori.")
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Reteta a fost stearsa.')
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cont creat si autentificat.')
            return redirect('recipe_list')
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

