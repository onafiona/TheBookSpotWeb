# Generated by Django 5.1.7 on 2025-03-11 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_category_books_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='category',
        ),
    ]
