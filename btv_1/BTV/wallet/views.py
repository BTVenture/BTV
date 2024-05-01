from django.shortcuts import render
from dashboard.decorators import login_required
from .models import Wallet_Model
from authenticate.models import User_Model
from django.shortcuts import get_object_or_404

@login_required
def wallet_page(request):
    # try:
    #     user = request.user
    #     user = User_Model.objects.get(username=user)
    # except User_Model.DoesNotExist:
    #     print('user not found')
    #
    # try:
    #     wallet = Wallet_Model.objects.get(user=user.id)
    # except Exception as e :
    #     print(e)
    # print(wallet.balance_amount)


    user = request.user
    try:
        wallet = get_object_or_404(Wallet_Model, user=user)
    except Exception as error:
        return render(request, 'wallet/wallet.html', {'message': error})

    amount = wallet.balance_amount
    return render(request, 'wallet/wallet.html', {'message': amount})

