from django.shortcuts import render
from django.http import HttpResponse
from dashboard.decorators import login_required
from authenticate.models import User_Model
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from wallet.models import Wallet_Model
from .models import *
from recharge.models import account_details
# Create your views here.

@login_required
def withdraw(request):
    """
        wallet amount .

    """

    if request.method == "POST":

        amount = int(request.POST.get('amount'))
        confirm_amount = int(request.POST.get('confirm_amount'))
        print(amount)
        print(confirm_amount)

        if amount != confirm_amount:
            return render(request, 'withdraw/withdraw_page.html', {'message': 'amount and confirm amount do not match'})
        try:
            wallet = get_object_or_404(Wallet_Model, user=request.user)
            band_details = get_object_or_404(account_details, user=request.user)
        except Exception as error:
            return render(request, 'authenticate/message.html', {'message': error})

        if wallet.balance_amount < confirm_amount:
            return render(request, 'withdraw/withdraw_page.html', {'message': 'You do have enough balance .'})

        if confirm_amount < 500:
            return render(request, 'withdraw/withdraw_page.html', {'message': 'Cannot initiate payment below 500 .'})

        # if you did not refer account earlier
        try:
            referal_user = User_Model.objects.get(username=request.user)
            referance_id = referal_user.referal_id
            count = User_Model.objects.filter(refered_by=referance_id).count()
        except Exception as error:
            return render(request, 'authenticate/message.html', {'message': error})

        if count == 0:
            return render(request, 'withdraw/withdraw_page.html', {'message': 'Cannot initiate until you refer anyone .'})


        wallet.balance_amount -= confirm_amount
        withdraw_request = Withdraw_History(user=request.user, amount=confirm_amount, account_number=band_details.account_number,
                                            ifsc_code=band_details.ifsc_code)
        withdraw_request.save()
        wallet.save()

        return render(request, 'wallet/wallet.html', {'message': wallet.balance_amount})

    try:
        user_model = User_Model.objects.get(username=request.user)
        account_model = user_model.account_details
        print(account_model)
        if account_model.account_number == "":
            return redirect('/account/add-bank-detail/')
        if account_model.ifsc_code == "":
            return redirect('/account/add-bank-detail/')
    except Exception as error:
        return render(request, 'authenticate/message.html', {'message': error})

    user = request.user

    # getting the user account information
    try:
        user_model = User_Model.objects.get(username=user)
        user_account_model = user_model.account_details
        user_wallet_model = get_object_or_404(Wallet_Model, user=request.user)
    except User_Model.DoesNotExist:
        return render(request, 'authenticate/message.html',{'message': 'User Not Found .'})

    if user_account_model.account_number == "":
        return redirect('/account/add-bank-detail/')

    if user_account_model.ifsc_code == "":
        return redirect('/account/add-bank-detail/')

    wallet_amount = user_wallet_model.balance_amount
    return render(request, 'withdraw/withdraw_page.html', {'wallet_amount': wallet_amount})

@login_required
def history(request):
    user = request.user

    try:
        withdraw_history = Withdraw_History.objects.filter(user=user).order_by('-request_date')
    except Exception as error:
        return render(request, 'authenticate/message.html', {'message': error})

    if not withdraw_history.exists():
        return render(request, 'authenticate/message.html', {'message': 'No Withdraw History'})

    withdraw_details = []
    for withdraw in withdraw_history:
        data = {}
        data['withdraw_id'] = withdraw.withdraw_id
        data['amount'] = withdraw.amount
        data['account_number'] = withdraw.account_number
        data['ifsc_code'] = withdraw.ifsc_code
        data['request_date'] = withdraw.request_date
        data['status'] = withdraw.status
        withdraw_details.append(data)

    return render(request, 'withdraw/withdraw_history.html', {'withdraw_details': withdraw_details})
