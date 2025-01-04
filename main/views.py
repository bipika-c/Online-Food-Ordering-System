
from django.shortcuts import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import re
from .forms import CheckoutForm

# Create your views here.
def home(request):
    
    return render(request, "home.html", {})


# homepage
def index(request):
    queryset= Food_items.objects.all()
    
    search = request.GET.get("search")
    if search:
        queryset = queryset.filter(itemname__icontains=search)
        
        
    context={'page':"Home","all_products":queryset, }
    return render(request, "index.html", context)



def items_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Food_items.objects.filter(category=category)
    data = Category.objects.all()  # Pass all categories for the navbar
    
    context = {
        
        'all_products': items,
        'data': data,
        'selected_category': category
    }
    return render(request, "index.html", context)

def log_out(request):
    logout(request)
    return redirect('/login/')


User= get_user_model()

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        
        #Validations
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,"Username already exists.")
            return redirect("/signup/")
        
        if not len(password)>=6:
            messages.error(request, "Password must be greater than 6 ")
            return redirect("/signup/")
        
        if not re.match(r'^(98|97)\d{8}$',phone):
            messages.error(request, "Phone number must start with 98 or 97 and be 10 digits long.")
            return redirect("/signup/")
        
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_address=address,
            user_phone=phone
            
        )
        
        messages.info(request,"You will be able to login after Admin Approval.")
        return redirect( "/signup/")
    
    queryset=User.objects.all()
    context={"register":queryset}
    return render(request,"signup.html",context)
    

def log_in(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user=authenticate(username=username, password=password)
    
        if user is None:
            messages.error(request,"Cannot Login Please Try Again !")
            return redirect("/login/")
    
        else:
            login(request, user)
            if user.is_superuser:
                return redirect("/admin/")
            else:
                return redirect("/index")
              
    return render(request, "login.html", {})





def menu(request):
    data = Category.objects.all()
    context={"data": data}
    return render(request,"menu.html",context)

def contact(request):
    return render(request,"contact.html",{})

def about(request):
    return render(request,"about.html",{})


def add_items(request):
    if request.method=="POST":
        itemname=request.POST.get('itemname')
        food_image=request.FILES.get('food_image')
        itemprice=request.POST.get('itemprice')
        discount=request.POST.get('discount')
        food_description=request.POST.get('food_description')
        
        Food_items.objects.create(
            itemname=itemname,
            food_image=food_image,
            itemprice=itemprice,   
            discount=discount,
            food_description=food_description
        )
         
        return redirect("/add_items/")
    
    queryset= Food_items.objects.all()
    context={"add_items":queryset}
    return render(request,"add_items.html",{})


#------------------------CART--------------------------------
#Add to cart
@login_required
def add_to_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Food_items, id=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item, user=request.user)
        if not created:
            messages.warning(request, "View cart to update quantity")
        
        else:
            messages.info(request, "Item added to Cart")
        
    return redirect('/index/')


#view cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.quantity * item.item.itemprice for item in cart_items)
    
    for item in cart_items:
        item.item_quantity = item.item.item_quantity
    
    
    context = {
        'cart_items': cart_items, 'total_price': total_price
    }
    return render(request, 'view_cart.html', context)

#update cart
@login_required
def update_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id)
        new_quantity = int(request.POST.get('quantity'))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
    return redirect('view_cart')


#remove from cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('/cart/')

#----------------------check out----------------------------------------
@login_required
def calculate_total_price(cart_items):
    total_price = sum(item.quantity * item.product.product_price for item in cart_items)
    return total_price

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderDetail

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderDetail

@login_required
def checkout(request):
    user = request.user  # Retrieve the current user from the request

    if request.method == 'POST':
        form = CheckoutForm(request.POST)  # Bind the form data
        if form.is_valid():
            # Retrieve form data
            receiver_name = form.cleaned_data['receiver_name']
            receiver_phone = form.cleaned_data['receiver_phone']
            receiver_address = form.cleaned_data['receiver_address']
            payment_method= form.cleaned_data['payment_method']

            # Retrieve cart items and total price
            cart_items = CartItem.objects.filter(cart__user=user)
            total_price = sum(item.quantity * item.item.itemprice for item in cart_items)

            # Create the order
            order = Order.objects.create(
                user=user,
                total_price=total_price,
                receiver_name=receiver_name,
                receiver_phone=receiver_phone,
                receiver_address=receiver_address,
                payment_method= payment_method
            )

            # Create order details for each cart item
            for cart_item in cart_items:
                OrderDetail.objects.create(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=cart_item.item.itemprice
                )
                order.items.add(cart_item)

            # Clear the user's cart
            cart_items.delete()

            messages.success(request, "Order placed successfully!")
            return redirect('thankyou')
    else:
        form = CheckoutForm()  # Create an empty form instance

    # Prepare context data
    address = user.user_address
    phone_number = user.user_phone
    cart_items = CartItem.objects.filter(cart__user=user)
    total_price = sum(item.quantity * item.item.itemprice for item in cart_items)

    context = {
        'form': form,
        'address': address,
        'phone_number': phone_number,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)

def thankyou(request):
    return render(request, "thankyou.html", {})

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    order_details = []
    for order in orders:
        items = order.details.all()  # Use the related_name 'details'
        item_details = [{'name': item.item.itemname, 'quantity': item.quantity, 'status': order.status} for item in items]
        order_details.append({'order': order, 'item_details': item_details})
    return render(request, 'view_orders.html', {'order_details': order_details})


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, "Order status updated successfully!")
        return redirect('order_detail', order_id=order_id)

    return render(request, 'update_order_status.html', {'order': order})

@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_details = order.details.all()
    context = {
        'order': order,
        'order_details': order_details,
    }
    return render(request, 'order_detail.html', context)