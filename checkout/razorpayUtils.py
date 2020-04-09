from django.shortcuts import get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
import razorpay
from razorpay import client
import datetime

from checkout.models import OrderLineItem
from products.models import BaseProduct



def save_order_items(userid, order, cart,order_id):
    for id, quantity in cart.items():
        print(userid)
        print(f"Typeis: {type(userid)}")
        product = get_object_or_404(BaseProduct, pk=id)
        shopper = get_object_or_404(User, pk=userid)
        order_line_item = OrderLineItem(
            order=order,
            product=product,
            quantity=quantity,
            shopper=shopper,
            orderId = order_id
        )
        order_line_item.save()


def create_order(total):
    order_id = None
    total_in_cent = int(total * 100)
    order_amount = total_in_cent
    order_currency = 'INR'
    order_receipt = 'order_rcptid_'+datetime.datetime.now().strftime('/d/m/yyyy hh:mm:ss')
    try:
        order_id = client.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture='0')
    except Exception as e:
        raise Exception(str(e))
    return order_id



def send_confirmation_email(email, username, items_and_total):
    context = {
        'site_name': "Blah Blah dot com",
        'user': username,
    }
    context.update(items_and_total)
    message = render_to_string('checkout/text_confirmation_email.html', context)
    html_message = render_to_string('checkout/html_confirmation_email.html', context)

    subject = 'Thanks for buying our stuff!'
    message = message
    from_email = settings.SYSTEM_EMAIL
    to_email = [email]

    send_mail(subject, message, from_email, to_email, fail_silently=True, html_message=html_message)