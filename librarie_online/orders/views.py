from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from .models import Order, OrderItem
from books.models import Books

def place_order(request):
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            order=form.save()
            cart=request.session.get('cart', {})
            for book_id, quantity in cart.items():
                book=Books.objects.get(id=book_id)
                if book.stock>=quantity:
                    total_price=book.price*quantity
                    order_item=OrderItem(order=order, book=book, quantity=quantity, total_price=total_price)
                    order_item.save()
                    book.stock-=quantity
                    book.save()
                    if book.stock==0:
                        book.delete()
                else:
                    return render(request, 'orders/place_order.html', {'form':form, 'error':f'Insufficient stock for {book.title}'})
            request.session['cart'] = {}
            return redirect('orders:order_success', order_id=order.id)

    else:
        form = OrderForm()
    
    return render(request, 'orders/place_order.html', {'form': form})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})

