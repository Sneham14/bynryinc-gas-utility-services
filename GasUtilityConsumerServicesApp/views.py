from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  
from .forms import *
from django.contrib import messages
from .models import *
from django.contrib import auth


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect('customerlogin')  # Redirect to the login page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def customerlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_details = authenticate(username=username, password=password)
            if user_details is not None:
                login(request, user_details)
                print("User authenticated:", user_details)
                return redirect('accountinfo')  # Redirect to the account information page or any other desired page
            else:
                messages.error(request, 'Invalid login credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def accountinfo(request):
    data=CustomerModel.objects.all()
    return render(request, 'accountinfo.html',{"data":data})
    
def customerlogout(request):
    logout(request)
    return redirect("customerlogin")

@login_required
def servicerequests(request):
    service_requests = ServiceRequestModel.objects.all()
    return render(request, 'servicerequests.html', {'service_requests': service_requests})

@login_required
def submitservicerequest(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)

            user = User.objects.get(username=request.user.username)

            customer, created = CustomerModel.objects.get_or_create(user=user, defaults={'email': user.email, 'username': user.username})

            service_request.customer = customer
            service_request.save()
            
            return redirect('servicerequests')
    else:
        form = ServiceRequestForm()
    return render(request, 'submitservicerequest.html', {'form': form})



def viewdetails(request):
    service_request = get_object_or_404(ServiceRequestModel)
    return render(request, 'viewdetails.html', {'service_request': service_request})



def stafflogin(request):
    if request.method == 'POST':
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_data = auth.authenticate(username=username, password=password)

            if user_data is not None and user_data.is_superuser:
                auth.login(request, user_data)
                return redirect('staffui')
            else:
                messages.info(request, 'Please enter the correct username and password for an admin account.')
                return redirect('stafflogin')
        else:
            messages.info(request, 'Please enter valid login credentials.')
            return redirect('stafflogin')
    else:
        form = StaffLoginForm()

    return render(request, 'stafflogin.html', {'form': form})


