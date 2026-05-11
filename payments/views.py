import stripe
from django.conf import settings
from store.models import Book
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from order.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
class PaymentView(LoginRequiredMixin,View):
    def get(self,request):

        cart = request.session.get('cart', {})

        if not cart:
            return redirect('store')

        book_ids = cart.keys()

        books = Book.objects.filter(id__in=book_ids)

        cart_items= []
        total = 0


        for book in books:
            quantity= cart[str(book.id)]['quantity']
            subtotal = book.discount_price * quantity if book.discount_price is not None else book.price * quantity
            total += subtotal
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'subtotal': subtotal
            })


        intent = stripe.PaymentIntent.create(
                amount=int(total*100),
                currency='usd',
                metadata = {'user_id': request.user.id}
        )


        return render(request, 'payment.html', {
                'cart_items': cart_items,
                'total': total,
                'client_secret': intent.client_secret,
                'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })



class ConfirmOrderView(LoginRequiredMixin,View):
    def post(self,request):
        import json
        data= json.loads(request.body)

        payment_intent_id = data.get('payment_intent_id')
        address= data.get('address')

        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if intent.status != 'succeeded':
            return JsonResponse({'error': 'Payment not verified'}, status=400)

        cart = request.session.get('cart', {})
        books = Book.objects.filter(id__in=cart.keys())
        

        total = sum(
            # book.discount_price * cart[str(book.id)]['quantity'] if book.discount_price is not None else book.price * cart[str(book.id)]['quantity']
            cart[str(book.id)]['quantity'] * (book.discount_price  if book.discount_price is not None else book.price)
            for book in books
        )

        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_intent_id=payment_intent_id,
            total_price=total,
        )

        for book in books:
            quantity = cart[str(book.id)]['quantity']
            OrderItem.objects.create(
                order=order,
                product= book,
                quantity=quantity,
            )

        request.session['cart'] = {}

        return JsonResponse({'order_id': order.id})



class OrderSuccessView(View):
    def get(self,request,order_id):
        order = Order.objects.get(id=order_id)
        return render(request, 'order_success.html', {'order': order})
