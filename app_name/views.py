from django.shortcuts import get_object_or_404, render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum

def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'create_expense.html', {'form': form})

def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

def expense_report(request):
     category_totals = Expense.objects.values('category').annotate(total_amount=Sum('amount'))
     total_expenses = Expense.objects.aggregate(total=Sum('amount'))

     return render(request, 'expense_report.html', {
        'category_totals': category_totals,
        'total_expenses': total_expenses['total'],
      })

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    
    return redirect('expense_list')