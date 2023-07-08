from django.shortcuts import get_object_or_404, render, redirect
from .models import Expense,ExpenseCategory
from .forms import ExpenseForm
from django.db.models import Sum

import matplotlib.pyplot as plt
import io
import base64


def create_expense(request):
    categories = ExpenseCategory.objects.all()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'create_expense.html', {'form': form,'categories':categories})

def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

def expense_report(request):
    # Calculate category-wise total amount
    category_totals = Expense.objects.values('category__name').annotate(total_amount=Sum('amount'))

    # Calculate total expenses
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))

    # Generate the bar chart
    categories = [category_total['category__name'] for category_total in category_totals]
    amounts = [category_total['total_amount'] for category_total in category_totals]
    bar_width = 0.4
    gap_width = 0.6


    total_width = bar_width + gap_width 

    bar_positions = [i * total_width for i in range(len(categories))]
    
    plt.bar(categories, amounts,width=bar_width)
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.title('Monthly Expense Report')
    plt.xticks(bar_positions,categories,rotation=45)
    plt.tight_layout()

    # Save the chart to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    categories = ExpenseCategory.objects.all()

    # Get budget notifications
    budget_notifications = check_budget_notifications()
    
    return render(request, 'expense_report.html', {
        'category_totals': category_totals,
        'total_expenses': total_expenses['total'],
        'chart_image': chart_image,
        'categories': categories,
        'budget_notifications': budget_notifications,
    })

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    
    return redirect('expense_list')



def clear_expenses(request):
    Expense.objects.all().delete()
    return redirect('expense_list')


def save_budget_limits(request):
    if request.method == 'POST':
        for category in ExpenseCategory.objects.all():
            budget_limit = request.POST.get(f'budget_limit_{category.id}')
            category.budget_limit = budget_limit
            category.save()
    
    return redirect('expense_list')

def check_budget_notifications():
    categories_exceeded_limit = []
    categories = ExpenseCategory.objects.all()
    for category in categories:
        total_expenses = Expense.objects.filter(category=category).aggregate(total=Sum('amount'))['total']
        if total_expenses and total_expenses > category.budget_limit:
            categories_exceeded_limit.append(category)
    return categories_exceeded_limit
