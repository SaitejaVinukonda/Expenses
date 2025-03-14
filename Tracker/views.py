from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import TrackingHistory, currentbalance
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.success(request, "Username not found") 
            return redirect('/login/')
        
        user = authenticate(username = username , password = password)
        if not user:
            messages.success(request, "Incorrect password") 
            return redirect('/login/')        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')
  
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.success(request, "Username is already taken") 
            return redirect('/register/')
        
        user = User.objects.create(
            username = username,
            first_name = first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created") 
        return redirect('/register/')
    return render(request , 'register.html')

@login_required(login_url="/login/")
def index(request):
    if request.method ==  "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        current_balance,_=currentbalance.objects.get_or_create(id=1)
        expense_type="credit"
        if float(amount) < 0:
            expense_type="debit"
        if not TrackingHistory.objects.filter(description=description, amount=amount, expense_type=expense_type).exists():
            tracking_history = TrackingHistory.objects.create(
                amount=amount,
                expense_type=expense_type,
                current_balance=current_balance,
                description=description
            )
            current_balance.current_balance += amount  # Update balance
            current_balance.save()

        return HttpResponseRedirect(reverse('index'))  
    current_balance, _ = currentbalance.objects.get_or_create(id=1)
    income = sum(t.amount for t in TrackingHistory.objects.filter(expense_type='credit'))
    expense = sum(t.amount for t in TrackingHistory.objects.filter(expense_type='debit'))
    expected_balance = income + expense  
    if current_balance.current_balance != expected_balance:
        current_balance.current_balance = expected_balance  
        current_balance.save()

    context = {
        'income': income,
        'expense': expense,
        'transactions': TrackingHistory.objects.all(),
        'current_balance': current_balance
    }
    return render(request, 'index.html', context)


@login_required(login_url="/login/")
def delete_transaction(request, id):
    tracking_history = TrackingHistory.objects.filter(id=id)
    if tracking_history.exists():
        current_balance, _ = currentbalance.objects.get_or_create(id=1)
        tracking_history = tracking_history.first()
        
        current_balance.current_balance -= tracking_history.amount  # Deduct amount from balance
        current_balance.save()

        tracking_history.delete()
    return HttpResponseRedirect(reverse('index'))  # Redirect to index
