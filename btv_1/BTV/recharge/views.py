from django.shortcuts import render
from django.http import HttpResponse
from dashboard.decorators import login_required
from authenticate.models import User_Model
from django.shortcuts import redirect
from wallet.models import Admin_Payment_Id
from wallet.models import Payment_Details

# Create your views here.

@login_required
def recharge(request):

    if request.method == 'POST':
        upi_id = request.POST.get('upi_id')
        utr_id = request.POST.get('utr_id')
        payment_amount = request.POST.get('payment_amount')
        # print(payment_amount)
        #
        # print(f'{upi_id} : {utr_id}')
        if upi_id == "":
            return render(request, 'recharge/recharge.html', {'message': 'UPI ID is required'})
        if utr_id == "":
            return render(request, 'recharge/recharge.html', {'message': 'UTR ID is required'})

        if len(upi_id) < 3 or len(upi_id) > 50:
            return render(request, 'recharge/recharge.html', {'message': 'UPI ID must be between 3 and 50'})
        if len(utr_id) < 12 or len(utr_id) > 12:
            return render(request, 'recharge/recharge.html', {'message': 'UTR ID should be equal to 12 digit'})

        try:
            utr_found = Payment_Details.objects.get(utr_id=utr_id)
            print(utr_found)
            if utr_found != "":
                return render(request, 'recharge/recharge.html', {'message': 'UTR ID already exist'})
        except Payment_Details.DoesNotExist:
            pass

        try:
            payment = Payment_Details.objects.create(user= request.user, payment_amount=payment_amount, upi_id=upi_id, utr_id=utr_id)
            payment.save()
        except Exception as error:
            return render(request, 'authenticate/message.html', {'message': error})

        return redirect('/wallet/')

    try:
        user_model = User_Model.objects.get(username=request.user)
        user_account_model = user_model.account_details
    except Exception as error:
        print(error)
        return render(request, 'authenticate/message.html', {'message': error})

    if user_account_model.account_number == "":
        return redirect('/account/add-bank-detail/')

    if user_account_model.ifsc_code == "":
        return redirect('/account/add-bank-detail/')

    try:
        admin_upi_id = Admin_Payment_Id.objects.all().first()
    except Exception as error:
        print(error)
        return render(request, 'authenticate/message.html', {'message': error})

    return render(request, 'recharge/recharge.html', {'admin_upi':admin_upi_id.upi_id})

@login_required
def recharge_history(request):
    try:
        payments_history = Payment_Details.objects.filter(user=request.user).order_by('-payment_request_time')
    except Payment_Details.DoesNotExist:
        return render(request, 'authenticate/message.html', {'message': 'Unable to fetch Payment history .'})

    if not payments_history.exists():
        return render(request, 'authenticate/message.html', {'message': 'No Recharge History'})

    payment_details = []
    for payment in payments_history:
        data = {}
        data['user_name'] = payment.user.username
        data['payment_amount'] = payment.payment_amount
        data['upi_id'] = payment.upi_id
        data['utr_id'] = payment.utr_id
        data['status'] = payment.payment_completed
        data['payment_request_time'] = payment.payment_request_time
        payment_details.append(data)

    return render(request, 'recharge/recharge_history.html', {'payment_details': payment_details})