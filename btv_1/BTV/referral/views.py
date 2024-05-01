from django.shortcuts import render
from django.http import HttpResponse
from authenticate.models import User_Model

# Create your views here.


def referrals_page(request):

    try:
        user = User_Model.objects.get(username=request.user)
    except User_Model.DoesNotExist:
        print("user not found")
        return render(request, 'authenticate/message.html', {'message': 'user not found'})
    referral_id = user.referal_id

    try:
        referred_accounts = User_Model.objects.filter(refered_by=referral_id).order_by('-date_time')
    except User_Model.DoesNotExist:
        print("error while fetching")
        return render(request, 'authenticate/message.html', {'message': 'error while fetching referred account .'})

    referred_account_details = []
    for account in referred_accounts:
        data = {}
        data['username'] = account.username
        data['email'] = account.email
        data['date_time'] = account.date_time
        referred_account_details.append(data)
    print(referred_account_details)

    return render(request, 'referral/referral_page.html', {'referral_id': referral_id, 'referred_account_details': referred_account_details})