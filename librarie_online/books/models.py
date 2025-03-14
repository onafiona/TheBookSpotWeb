from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Books(models.Model):
    title=models.CharField(max_length=250)
    author=models.CharField(max_length=250)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    stock=models.PositiveIntegerField()
    publication_date=models.DateField()
    categoryid = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    
    def __str__(self):
        return self.title

