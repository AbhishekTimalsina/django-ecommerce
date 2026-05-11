from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from store.models import Book
# Create your models here.

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart',{})

        book_ids = cart.keys()

        books = Book.objects.filter(id__in=book_ids)

        cart_item = []

        for book in books:
            quantity = cart[str(book.id)]['quantity']

            cart_item.append({
                'book': book,
                'quantity': quantity,
                'subtotal': book.discount_price * quantity if book.discount_price is not None else book.price * quantity
            })

        total = sum(item['subtotal'] for item in cart_item)

        return render(request,"cart.html",{'cart_item':cart_item, 'total':total})


class addToCart(View):
    def post(self,request,pk):
        cart = request.session.get('cart', {})
        str_pk = str(pk)

        if str_pk in cart:
            cart[str_pk]["quantity"] += 1
        else:
            cart[str_pk] = {"quantity": 1}

        request.session['cart'] = cart
        count = sum(item["quantity"] for item in cart.values())

        return JsonResponse({"status": "success", "count": count})
                

    def get(self,request):
        cart= request.session.get('cart', {})
        count = sum(item["quantity"] for item in cart.values())
        return JsonResponse({"count": count})