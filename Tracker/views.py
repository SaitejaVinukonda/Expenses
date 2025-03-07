from django.shortcuts import render,redirect
from .models import TrackingHistory, currentbalance

# Create your views here.
def index(request):
    if request.method ==  "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        current_balance,_=currentbalance.objects.get_or_create(id=1)
        expense_type="credit"
        if float(amount) < 0:
            expense_type="debit"
        tracking_history = TrackingHistory.objects.create(
            amount=amount,
            expense_type=expense_type,
            current_balance=current_balance,
            description=description)
        current_balance.current_balance += float(tracking_history.amount) 
        current_balance.save()        
        print(description,amount)
        return redirect('/')
    current_balance,_=currentbalance.objects.get_or_create(id=1)
    income=0
    expense=0
    for tracking_history in TrackingHistory.objects.all():
        if tracking_history.expense_type == 'credit':
            income+=tracking_history.amount
        else:
            expense+=tracking_history.amount

    
    context = {'income':income,'expense':expense,
    'transactions':TrackingHistory.objects.all(),
    'current_balance':current_balance
    }                 
    return render(request,'index.html', context)


