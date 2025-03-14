from django.db import models
from books.models import Books

class Order(models.Model):
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    email=models.EmailField(max_length=200)
    address=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('cash_on_delivery', 'Cash on Delivery')
    ])

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"
        
    def calculate_total(self):
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save()

class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book=models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    total_price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} x{self.quantity}"

    def save(self, *args, **kwargs):
        self.total_price = self.book.price * self.quantity 
        super().save(*args, **kwargs)
        self.order.calculate_total()