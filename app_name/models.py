from django.db import models


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    
    
    def __str__(self):
        return self.name
    
class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.title
    


