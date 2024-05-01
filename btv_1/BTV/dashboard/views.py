from django.shortcuts import redirect
from django.shortcuts import render
from .decorators import login_required
from django.contrib.auth import logout
from .models import Product

@login_required
def dashboard(request):
    products = Product.objects.all()
    message = {
        'products': products
    }
    return render(request, 'dashboard/dashboard.html', message)


def logout_user_account(request):
    logout(request)
    return redirect('/auth/login')



