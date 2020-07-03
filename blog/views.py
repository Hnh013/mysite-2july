from django.db.models import F
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm , ProfileForm, AstroProfileForm, RechargeForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .models import User, Profile, Wallet
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

import stripe

stripe.api_key = ('sk_test_51GzwicFlMZrJNY0xzkbFfyuVlnGK2Fuu77qFgpsCdMjTuDT8aCTeh9bIUxmXMZmFCRSx0WLtnGQb7598hFFXcldp00xF0KKieG')

def Convert(string):
	li = list(string.split(" "))
	return li

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST)
        recharge_form = RechargeForm(request.POST)

        if form.is_valid() and profile_form.is_valid() and recharge_form.is_valid():

            user = form.save(commit=True)
            user.is_active = False
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            recharge = recharge_form.save(commit=False)
            recharge.user = user

            recharge.save()



            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })

            to_email = Convert(form.cleaned_data.get('email'))
            print(to_email)
            send_mail('test', message ,'najay357@gmail.com', to_email, fail_silently=False)
            
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
        profile_form = ProfileForm()
        recharge_form = RechargeForm()
    return render(request, 'signup.html', {'form': form, 'profile_form':profile_form, 'recharge_form':recharge_form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        pro = user
        user.save()
        login(request, user)


        return redirect('confirmed_account')


        
    else:
        return HttpResponse('Activation link is invalid!')

def confirmed_account(request):
    if request.method == 'POST':
        data_form = AstroProfileForm(request.POST)

        if data_form.is_valid():
            data = data_form.save(commit=False)
            data = request.user.profile

            data.save()
                                     
            return redirect('logout')
    else:
        data_form = AstroProfileForm()
    return render(request, 'account.html', {'data_form': data_form})

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('logout')

@login_required
def recharge(request):

    return render(request, 'recharge.html')

@login_required
def charge(request):
    if request.method == "POST":
        amount = int(request.POST['amount'])

        print('Data:', request.POST)

        amount = int(request.POST['amount'])

        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
            source=request.POST['stripeToken']
            )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='INR',
            description="Donation"
            )

        Wallet.objects.filter(balance=request.user.wallet.balance).update(balance=F('balance')+ amount)

        return redirect('recharge')
    return redirect('recharge')


