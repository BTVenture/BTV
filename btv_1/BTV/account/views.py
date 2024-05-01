from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from dashboard.decorators import login_required
from authenticate.models import User_Model
from recharge.models import account_details
# Create your views here.


@login_required
def account_page(request):

    try:
        # trying to find the user details
        user_model = User_Model.objects.get(username=request.user)
        user_account_details = user_model.account_details

    except User_Model.DoesNotExist:
        print('error')
        return render(request, 'authenticate/message.html', {'message': 'User not found'})

    details = {
        'user_id': user_model.id,
        'username': user_model.username,
        'email': user_model.email,
        'referal_id': user_model.referal_id,
    }

    if user_account_details.account_number == "" or user_account_details.ifsc_code == "":
        details['account_number'] = "No Information Available"
        details['ifsc_code'] = 'No Information Available'
    else:
        details['account_number'] = user_account_details.account_number
        details['ifsc_code'] = user_account_details.ifsc_code

    return render(request, 'account/account.html', details)


@login_required
def add_bank_account_information(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')
        print(f'{account_number} : {ifsc_code}')

        # the method id post
        try:
            user_model = User_Model.objects.get(username=request.user)
            user_account_details = user_model.account_details
        except Exception as error:
            print('error')
            return render(request, 'authenticate/message.html', {'message': error})

        if account_number == '':
            return render(request, 'account/add_account_details.html', {'message': 'Account Number Not Found .'})

        if ifsc_code == "":
            return render(request, 'account/add_account_details.html', {'message': 'IFSC code not Found .'})

        if len(account_number) < 11:
            return render(request, 'account/add_account_details.html', {'message': 'Account Number cannot be less than 11 digits'})
        elif len(account_number) > 16:
            return render(request, 'account/add_account_details.html', {'message': 'Account Number must be between 11-16 digits'})

        if len(ifsc_code) > 11 or len(ifsc_code) < 11:
            return render(request, 'account/add_account_details.html', {'message': 'IFSC code must be of 11 digits .'})

        user_account_details.account_number = account_number
        user_account_details.ifsc_code = ifsc_code

        user_account_details.save()
        return redirect('/wallet/')

    return render(request, 'account/add_account_details.html')