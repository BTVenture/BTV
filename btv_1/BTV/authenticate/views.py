from django.shortcuts import render, redirect
from .models import User_Model
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
import uuid

# Create your views here.

def login_page(request):

    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        """
            method to check the login .
        """
        username = request.POST.get('username')

        if username == '':
            # if username is empty .
            message = {
                'error_message': 'Username Field is required'
            }
            return render(request, 'authenticate/login.html', message)

        password = request.POST.get('password')
        if password == '':
            # if password is empty
            message = {
                'error_message': 'Password field is required'
            }
            return render(request, 'authenticate/login.html', message)

        try:
            # check weather the user exist
            user = User_Model.objects.get(username=username)
        except User_Model.DoesNotExist:
            user = None

        if user:
            # if user is not None
            authenticated_user = authenticate(request, username=username, password=password)
            if user.is_verified :
                if authenticated_user is not None:
                    # if the user if found then login
                    login(request, authenticated_user)
                    return redirect('/dashboard')  # Redirect to the panel page
                else:
                    message = {
                        'error_message': 'Invalid password'
                    }
            else:
                message = {
                    'error_message': 'Account is not activated .',
                    'account_activaton_status' : False
                }

                return render(request, 'authenticate/login.html', message)
        else:
            # if user is not None
            message = {
                'error_message': 'User does not exist'
            }
        return render(request, 'authenticate/login.html', message)

    return render(request, 'authenticate/login.html')


def sign_up(request):
    if request.method == 'POST':
        """
            This method is required to create the user .
        """

        """
            username, email, password fields could not remain empty .
        """
        refered_by = request.POST.get('refered_by')

        if refered_by != '':
            if is_valid_uuid(refered_by):
                try:
                    user = User_Model.objects.get(referal_id=refered_by)
                except User_Model.DoesNotExist:
                    user = None
                    message = {
                        'error_message': 'Refered by does not associate with any account'
                    }
                    return render(request, 'authenticate/signup.html', message)
            else:
                message = {
                    'error_message': 'Enter a valid refered by .'
                }
                return render(request, 'authenticate/signup.html', message)
        else:
            refered_by = None

        user_name = request.POST.get('username')
        if user_name == '':
            # if user_name field is empty
            message = {
                'error_message': 'Username Field is required'
            }
            return render(request, 'authenticate/signup.html', message)

        email = request.POST.get('email')
        if email == '':
            # if password is none
            message = {
                'error_message': 'Email Field is required'
            }
            return render(request, 'authenticate/signup.html', message)

        password = request.POST.get('password')
        if password == '':
            # if password is None
            message = {
                'error_message': 'Password field is required'
            }
            return render(request, 'authenticate/signup.html', message)


        """
            1. check weather the email exist in the database .
            2. check weather the username exist in the database .
            3. checking the lenght of the password
        """
        user = None
        if user_name != '':
            try:
                user = User_Model.objects.get(username=user_name)
                message = {
                    'error_message': 'User Already Exist'
                }
                return render(request, 'authenticate/signup.html', message)
            except User_Model.DoesNotExist:
                user = None

        if email != '':
            try:
                user = User_Model.objects.get(email=email)
                message = {
                    'error_message': 'Email Already exist'
                }
                return render(request, 'authenticate/signup.html', message)
            except User_Model.DoesNotExist:
                user = None

        if password != '':
            if len(password) < 8:
                message = {
                    'error_message': 'Password length must be at least 8 characters'
                }
                return render(request, 'authenticate/signup.html', message)
            elif len(password) > 10:
                message = {
                    'error_message': 'Password length must be of 8-10 character '
                }
                return  render(request,'authenticate/signup.html', message)

        try:
            email_token = uuid.uuid4()
            user = User_Model(username=user_name, email=email, email_token=email_token, refered_by=refered_by)
            user.set_password(password)
            send_confirmation_email(email, user_name, email_token)
            user.save()
            message = {
                'error_message': 'activation link has successfully been sent to your email.'
            }
            return render(request, 'authenticate/login.html', message)

        except Exception as error :
            return render(request, 'authenticate/signup',{'error_message': str(error)})

    return render(request, 'authenticate/signup.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User_Model.objects.get(email=email)
        except User_Model.DoesNotExist:
            user = None

        if user is None:
            # email does not exist
            msg = {
                'message': 'email does not exist'
            }
            return render(request, 'authenticate/reset_password.html', msg)
        else:
            # email do exist
            email_token = uuid.uuid4()
            user.email_token = email_token
            user_name = user.username
            user.save()
            send_reset_password_email(email, user_name, email_token)
            msg = {
                'message':'reset link sent to your email address .'
            }
            return render(request, 'authenticate/reset_password.html', msg)

    return render(request, 'authenticate/reset_password.html')


def change_password(request, param1, param2):
    try:
        user = User_Model.objects.get(username=param1)
    except User_Model.DoesNotExist:
        user = None

    if user is not None:
        # user found
        if user.email_token == param2:
            # email token is valid
            message = {
                'user': user.username
            }
            return render(request, 'authenticate/change_password.html', message)
        else:
            # email token is not valid
            msg = {
                'message': 'Invalid link to reset password'
            }
            return render(request, 'auth/message.html', msg)
    else:
        # user not found
        msg = {
            'message': 'Invalid link to reset password'
        }
        return render(request, 'auth/message.html', msg)


def confirm_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_password')
        username = request.POST.get('username')
        print(username)
        if password == confirm_pass:
            # both the password match with each other
            if len(password) < 8:
                # oass
                message = {
                    'user': username,
                    'error_message': 'Password must be at least 8 characters long'
                }
                return render(request, 'authenticate/change_password.html', message)
            elif len(password) > 10:
                message = {
                    'user': username,
                    'error_message': 'Password must be at most 8-10 characters long'
                }
                return render(request, 'authenticate/change_password.html', message)
            else:
                try:
                    user = User_Model.objects.get(username=username)
                except User_Model.DoesNotExist:
                    message = {
                        'message': 'Error 404 : User not found'
                    }
                    return render(request, 'authenticate/message.html', message)

                message = {
                    'message': 'password successfully changed .'
                }
                user.set_password(password)
                user.save()
                return render(request, 'authenticate/message.html', message)
        else:
            # both the password did not match
            message = {
                'user': username,
                'error_message': 'password and confirm password did not match .'
            }
            print(message)
            return render(request, 'authenticate/change_password.html', message)
    print("helo world")

def verify_account(request, param1, param2):
    # print(param1) # user_name
    # print(param2)  # email_token

    msg = {
        'message': 'Congratulations, Your account is successfully activated ..'
    }

    try:
        user = User_Model.objects.get(username=param1)
    except User_Model.DoesNotExist:
        # username is not found
        msg = {
            'message': 'Sorry, Unable to find your account ...'
        }
        return render(request,'authenticate/message.html', msg)

    if user.email_token == param2:
        # user found
        # token is valid
        user.is_verified = True
        user.save()
        return render(request, 'authenticate/message.html', msg)
    else:
        # user found
        # email token is invalid
        msg = {
            'message': 'Sorry, Unable to find your account ...'
        }
        return render(request, 'authenticate/message.html',msg)

def resend_activation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User_Model.objects.get(email=email)
        except User_Model.DoesNotExist:
            message = {
                'message':'Sorry invalid email address'
            }
            return render(request, 'authenticate/activation_link.html', message)

        activation_token = uuid.uuid4()
        user.email_token = activation_token
        user.save()
        send_confirmation_email(user.email, user.username, activation_token)
        message = {
            'error_message': 'activation link successfully sent to your email.'
        }
        return render(request, 'authenticate/login.html', message)
    return render(request, 'authenticate/activation_link.html')

def send_confirmation_email(email, user_name, token):
    subject = 'Account Activation Email'
    message = f'Thank you for registering on our website. Please click here to activate your account .!\n https://btv.pythonanywhere.com//auth/verify-account/{user_name}/{token}'
    from_email = settings.EMAIL_HOST_USER  # Replace with your email address
    send_mail(subject, message, from_email, [email])

def send_reset_password_email(email, user_name, token):
    subject = 'Reset Password'
    message = f'Reset your password . Please click here to reset your account password .!\n https://btv.pythonanywhere.com//auth/change-password/{user_name}/{token}'
    from_email = settings.EMAIL_HOST_USER  # Replace with your email address
    send_mail(subject, message, from_email, [email])

def is_valid_uuid(string):
    try:
        uuid.UUID(string, version=4)
        return True
    except ValueError:
        return False