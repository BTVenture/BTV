from django.utils import timezone

from django.shortcuts import render
from django.http import HttpResponse
from wallet.models import Buyed_Products
from authenticate.models import User_Model
# Create your views here.
from dashboard.decorators import login_required
from .models import Generated_Amount_History
from django.shortcuts import redirect


@login_required
def income_page(request):

    try:
        user_instance = User_Model.objects.get(username=request.user)
        buyed_products = Buyed_Products.objects.filter(user=user_instance)
    except Buyed_Products.DoesNotExist:
        return render(request, 'authenticate/message.html', {'message': 'No Purchased Product Found.'})

    try:
        generated_amount_history = Generated_Amount_History.objects.filter(user=request.user).order_by('-request_at').first()
    except Generated_Amount_History.DoesNotExist:
        return render(request, 'authenticate/message.html', {'message': 'Error Generating Amount History.'})

    if generated_amount_history == None:
        total_amount = 0
        for product_in_id in buyed_products:
            purchased_at = (product_in_id.purchased_date).date()
            current_date = timezone.now().date()
            print(f'{purchased_at}, {current_date}')
            difference_in_days = (current_date - purchased_at).days
            total_production_amount = 0
            total_production_amount = difference_in_days * product_in_id.product.generate_per_day
            total_amount += total_production_amount

        product_list = []

        for buyed_product in buyed_products:
            data = {
                'product_name': buyed_product.product.product_name,
                'product_image': buyed_product.product.product_image,
                'product_purchase_date': buyed_product.purchased_date,
                'product_price': buyed_product.product.product_price,
                'generate_per_day': buyed_product.product.generate_per_day
            }
            product_list.append(data)
        return render(request, 'income/income_page.html', {'product_list': product_list,
                                                           'generated_amount': total_amount})

    total_amount = 0
    for product_in_id in buyed_products:
        total_production = 0
        purchased_at = (generated_amount_history.request_at).date()
        current_date = timezone.now().date()
        difference_in_days = (current_date - purchased_at).days

        total_production = difference_in_days * product_in_id.product.generate_per_day
        total_amount += total_production


    product_list = []

    for buyed_product in buyed_products:
        data = {
            'product_name': buyed_product.product.product_name,
            'product_image': buyed_product.product.product_image,
            'product_purchase_date': buyed_product.purchased_date,
            'product_price': buyed_product.product.product_price,
            'generate_per_day': buyed_product.product.generate_per_day
        }
        product_list.append(data)
    return render(request, 'income/income_page.html', {'product_list': product_list,
                                                       'generated_amount': total_amount })



@login_required
def transfer_amount(request, transfer_amount):

    if transfer_amount == 0:
        return redirect('/income/')

    try:
        user_model = User_Model.objects.get(username=request.user)
    except User_Model.DoesNotExist:
        return render(request, 'authenticate/message.html', {'message': 'user not found .'})
    history = Generated_Amount_History(user=user_model, amount=transfer_amount)
    history.save()
    return redirect('/income/')