from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirects to the main dashboard
        else:
            return render(request, "users/login.html", {"error": "Invalid credentials"})
    return render(request, "users/login.html")

@login_required
def dashboard_view(request):
    return render(request, "users/customer_dashboard.html")  # Use a single dashboard

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "users/customer_dashboard.html")


@login_required
def add_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        role = request.POST.get("role", None)

        try:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return render(request, "users/add_user.html", {"error": "Username already exists."})

            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)

            # If a role is provided, assign it; "manager" replaces "customer" as a role
            if role:
                if role == "manager":
                    group, created = Group.objects.get_or_create(name="Manager")
                elif role == "admin":
                    group, created = Group.objects.get_or_create(name="Admin")
                elif role == "employee":
                    group, created = Group.objects.get_or_create(name="Employee")

                user.groups.add(group)

            user.save()
            return redirect("dashboard")

        except IntegrityError:
            return render(request, "users/add_user.html", {"error": "Error while creating the user."})

    return render(request, "users/add_user.html")

@login_required
def dashboard(request):
    if request.user.groups.filter(name="Admin").exists():
        return render(request, "users/admin_dashboard.html")
    elif request.user.groups.filter(name="Employee").exists():
        return render(request, "users/employee_dashboard.html")
    else:
        return render(request, "users/customer_dashboard.html")


@login_required
def add_user_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        messages.success(request, "User added successfully!")
        return redirect("dashboard")  # Redirect to dashboard after adding a user

    return render(request, "users/add_user.html")  # Render the add user page


@login_required
def add_user_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        messages.success(request, "User added successfully!")
        return redirect("dashboard")  # Redirect to dashboard after adding a user

    return render(request, "users/add_user.html")  # Render the add user page

@permission_required('auth.view_user', raise_exception=True)
def user_list(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'users/user_list.html', {'users': users})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Fetch user by ID
    return render(request, 'users/user_detail.html', {'user': user})