from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Books, Category
from django.db.models import Q

class BooksListView(generic.ListView):
    model=Books
    template_name='books/book_list.html'
    context_object_name='books'

    def get_queryset(self):
        queryset=Books.objects.all().order_by('title')
        query=self.request.GET.get('q')
        category_id=self.request.GET.get('category')
        if query:
            queryset=queryset.filter(Q(title__icontains=query) | Q(author__icontains=query))
        
        if category_id:
            queryset=queryset.filter(categoryid__id=category_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()
        return context

class BooksDetailView(generic.DetailView):
    model=Books
    template_name='books/book_detail.html'
    context_object_name='book'

def add_to_cart(request, book_id):
    book=get_object_or_404(Books, id=book_id)
    quantity=int(request.POST.get('quantity', 1))

    cart=request.session.get('cart', {})
    book_id_str=str(book_id)

    if book_id_str in cart:
        cart[book_id_str]+=quantity
    else:
            cart[book_id_str]=quantity

    request.session['cart']=cart
    return redirect('books:book_detail', pk=book_id)

def view_cart(request):
    cart=request.session.get('cart', {})
    books_in_cart=[]
    total_price=0
    for book_id, quantity in cart.items():
        book=Books.objects.get(id=book_id)
        total_price+=book.price*quantity
        books_in_cart.append({
            'book':book,
            'quantity':quantity,
            'total_price': book.price*quantity
        })
    return render(request, 'books/cart.html', {'cart_items':books_in_cart, 'total_price':total_price})

def change_quantity(request, book_id):
    book=get_object_or_404(Books, id=book_id)
    action=request.POST.get('action')
    cart=request.session.get('cart', {})
    if(str(book_id) in cart):
        if action=='increase':
            cart[str(book_id)]+=1
        elif action == 'decrease':
            cart[str(book_id)]-=1
            if cart[str(book_id)]<=0:
                del cart[str(book_id)]
    request.session['cart']=cart
    return redirect('books:view_cart')

def clear_cart(request):
    if request.method == 'POST':
        request.session['cart'] = {}
    return redirect('books:view_cart')

