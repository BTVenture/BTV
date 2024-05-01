from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Product
from dashboard.decorators import login_required
from authenticate.models import User_Model
from django.shortcuts import get_object_or_404
from wallet.models import Wallet_Model
from wallet.models import Buyed_Products
from django.shortcuts import redirect
# Create your views here.

@login_required
def confirm_product(request, item_id):
    try:
        product = Product.objects.get(product_id=item_id)
    except Exception as error:
        return render(request, 'authenticate/message.html', {'message': error})

    try:
        user_model = User_Model.objects.get(username=request.user)
        # Get the associated Wallet_Model instance
        wallet_model = get_object_or_404(Wallet_Model, user=user_model)
    except Exception as error:
        return render(request, 'authenticate/message.html', {'message': 'user not found .'})

    if wallet_model.balance_amount < product.product_price:
        return render(request, 'add_item/add_item_confirmation.html', {'product': product, 'info': 'You do not have enough money in wallet . ' })
    else:
        return render(request, 'add_item/add_item_confirmation.html',
                      {'product': product})

@login_required
def confirm_payment(request, item_id):
    try:
        user = User_Model.objects.get(username=request.user)
    except User_Model.DoesNotExist:
        return render(request, 'authenticate/message.html', {'message': " User not found ."})

    try:
        product_get = Product.objects.get(product_id=item_id)
    except Product.DoesNotExist:
        return render(request, 'authenticate/message.html', {'message': 'Product not found .'})

    try:
        wallet = Wallet_Model.objects.get(user=request.user)
    except Wallet_Model.DoesNotExist:
        return render(request, 'authenticate/message.html', {'message', 'wallet not found .'})

    wallet.balance_amount = wallet.balance_amount - product_get.product_price
    wallet.save()

    item = Buyed_Products(user=user, product=product_get)
    item.save()
    return redirect('/dashboard/')