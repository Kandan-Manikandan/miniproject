from django.conf import settings
from django.shortcuts import render, reverse, redirect
from environ import Env
from miniapplication.models import payment_details_cus
import stripe

stripe.api_key = settings.STR_SECRET_KEY

# Create your views here.
def homepage(req):
    mobile_product_id = 'prod_SlG5NXmAKkYnVD'
    product = stripe.Product.retrieve(mobile_product_id)
    prices = stripe.Price.list(product=mobile_product_id)
    price = prices.data[0]
    final_price = price.unit_amount / 100.00
    # print(product,final_price)
    if req.method == "POST":
        pro_id = req.POST.get('product_id')
        price_id = req.POST.get('price_id')
        quantity = req.POST.get('quan')
        email = req.POST.get('email', 'user@exmple.com')
        print(pro_id, price_id, quantity)
        Checkout_Session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': quantity,
                },
            ],
            payment_method_types=['card'],
            mode='payment',
            customer_creation='always',
            billing_address_collection='required',
            success_url=f'{settings.BASE_URL}{reverse("success")}?session_id={{CHECKOUT_SESSION_ID}}'
        )
        return redirect(Checkout_Session.url, code=303)
    return render(req, 'home.html', {'Product_detail': product, 'Price_amt': final_price})


def productpage(req):
    mobile_product_id = 'prod_SlG5NXmAKkYnVD'
    product = stripe.Product.retrieve(mobile_product_id)
    prices = stripe.Price.list(product=mobile_product_id)
    price = prices.data[0]
    final_price = price.unit_amount/100.00
    #print(product,final_price)
    if req.method == "POST":
        pro_id = req.POST.get('product_id')
        price_id = req.POST.get('price_id')
        quantity = req.POST.get('quan')
        email=req.POST.get('email','user@exmple.com')
        print(pro_id,price_id,quantity)
        Checkout_Session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': quantity,
                },
            ],
        payment_method_types=['card'],
        mode='payment',
        customer_creation='always',
        billing_address_collection='required',
        success_url=f'{settings.BASE_URL}{reverse("success")}?session_id={{CHECKOUT_SESSION_ID}}'
        )
        return redirect(Checkout_Session.url, code=303)
    return render(req, 'product.html',{'Product_detail':product,'Price_amt':final_price})

def successpage(req):
    checkout_session_id=req.GET.get('session_id',None)
    if checkout_session_id:
        session=stripe.checkout.Session.retrieve(checkout_session_id)
        customer_id=session.customer
        customer=stripe.Customer.retrieve(customer_id)
        line_items=stripe.checkout.Session.list_line_items(checkout_session_id).data[0]
        cus_name=customer.name
        print('SESSION DETAILS:',session,'CUSTOMER_DETAILS:',customer,'LINE_ITEMS',line_items,'NAME',cus_name)
        user1=payment_details_cus(
            customer_name=cus_name,
            customer_id=customer_id,
            product_price=line_items.price.unit_amount/100.00,
            product_id=line_items.price.product,
            checkout_id=checkout_session_id,
            amount_paid=True,
            quantity=line_items.quantity,

        )
        print('data save in database')
        user1.save()
        return redirect('/success')
    return render(req,'success.html')
    return render(req,'success.html')