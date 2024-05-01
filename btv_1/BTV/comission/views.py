from django.shortcuts import render
from .models import Comission_History

# Create your views here.

def commission_history_page(request):

    try:
        history = Comission_History.objects.filter(user=request.user).order_by('-date')
    except Comission_History.DoesNotExist:
        return render(request, 'authenticate/message.html', {'message': 'error while finding commission history'})

    if not history:
        print('no commission history')
        return render(request, 'authenticate/message.html', {'message': 'No history found .'})

    total_history = []
    for item in history:
        data = {
            'user_name': item.username_get_commission,
            'email': item.email_get_commission,
            'comission_amount': item.comission_amount,
            'product_name': item.purchased_product.product_name,
            'date': item.date
        }
        total_history.append(data)

    return render(request, 'comisson/comission_page.html',{'history': total_history})