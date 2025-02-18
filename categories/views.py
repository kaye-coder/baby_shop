from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, SemiCategory
from .forms import CategoryForm, SemiCategoryForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})

def semi_category_list(request):
    semi_categories = SemiCategory.objects.all()
    return render(request, "semi_category_list.html", {"semi_categories": semi_categories})

def add_category(request):
    semi_categories = SemiCategory.objects.all()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the category without checking for duplicates
            return redirect("category_list")
    else:
        form = CategoryForm()

    return render(
        request,
        "category_form.html",
        {"form": form, "semi_categories": semi_categories}
    )

def add_semi_category(request):
    if request.method == "POST":
        form = SemiCategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new semi-category
            return redirect("add_category")
    else:
        form = SemiCategoryForm()

    return render(
        request,
        "semi_category_form.html",
        {"form": form}
    )

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("category_list")

def delete_semi_category(request, pk):
    semi_category = get_object_or_404(SemiCategory, pk=pk)
    semi_category.delete()
    return redirect("semi_category_list")
