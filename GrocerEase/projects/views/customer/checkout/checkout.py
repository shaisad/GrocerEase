from projects.imports import *
from decimal import Decimal
from django.http import JsonResponse

def checkout(request, customer_id=None):
    if customer_id is None:
        customer_id = request.session.get('customer_id')

    items = []
    order = {}
    cartItems = 0
    customer = None

    if customer_id is not None:
        customer = Customer.objects.get(pk=customer_id)
        data = cartData(request, customer_id)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        amount_in_smallest_unit = order.get_cart_total * 100
        updated_amount = order.payment * 100


    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'customer': customer,
        'amount_in_cents': amount_in_smallest_unit,
        'updated_amount': updated_amount }

    if request.method == 'POST':
        shipping_name = request.POST.get('name')
        shipping_email = request.POST.get('email')
        shipping_address = request.POST.get('address')
        shipping_phone = request.POST.get('phone')

        order.shipping_name = shipping_name
        order.shipping_email = shipping_email
        order.shipping_address = shipping_address
        order.shipping_phone = shipping_phone
        order.status = 'Processing'  

        try:
            token = request.POST['stripeToken']

            print(f"Order object: {order}")
            if order:
                order.is_cart = False
                order.save()

                send_mail(
                    'GrocerEase Order Confirmation', 
                     f'Dear valued customer,\n\n'
                     f'Welcome to GrocerEase! '
                     'Your order is placed successfully.\n\n'
                     f'Your payable amount BDT { order.payment } for order ID: { order.id } is successful.\n\n'
                     f'Thank you for trusting GrocerEase.\n\n'
                     f'Best regards,\n'
                     f'The GrocerEase Team',
                    'grocereasedp1@gmail.com',
                    [order.shipping_email],
                    fail_silently=False,
                )

            messages.success(request, 'Order placed successfully!')
            return redirect('homecustomer', customer_id=customer_id)

        except Exception as e:
            messages.error(request, str(e))

    if 'HTTP_X_REQUESTED_WITH' in request.headers and request.headers['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        vouchercode = request.POST.get('vouchercode', '')
        print(vouchercode)

        if vouchercode:
            try:
                voucher = VoucherCode.objects.get(vouchercode=vouchercode)
                updated_payment_amount = Decimal(order.get_cart_total * (1 - voucher.voucher_percentage / 100))
                order.payment = updated_payment_amount
                order.save()

                return JsonResponse({
                    'valid': True,
                    'voucher_percentage': voucher.voucher_percentage,
                    'final_amount': float(updated_payment_amount)
                })

            except VoucherCode.DoesNotExist:
                return JsonResponse({'valid': False, 'error_message': 'Invalid voucher code.'})

    return render(request, 'customer/checkout.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')  
class SaveUpdatedPriceView(View):
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        updated_price = request.POST.get('updated_price')
        
        try:
            order = Order.objects.get(id=order_id)

            updated_price_decimal = Decimal(updated_price) if updated_price else Decimal('0.00')
            print(updated_price_decimal)

            if updated_price_decimal > order.payment:
                order.payment = updated_price_decimal
                order.save()
                print(updated_price_decimal)
                print(order.payment)
            elif updated_price_decimal == order.payment:
                order.payment = updated_price_decimal
                order.save()
                print(updated_price_decimal)
                print(order.payment)
            else:
                order.payment = updated_price_decimal
                order.save()
                print(order.payment)
                
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Order not found'})
