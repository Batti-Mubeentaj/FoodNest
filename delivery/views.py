from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
import razorpay
from .models import Customer, Restaurant, Item, Cart

# Create your views here.
def index(request):
    return render(request, 'delivery/index.html')

def open_signup(request):
    return render(request, 'delivery/signup.html')

def open_login(request):
    return render(request, 'delivery/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        try:
            Customer.objects.get(username = username)
            return HttpResponse("Duplicate username!")
        except:
            Customer.objects.create(
                username = username,
                password = password,
                email = email,
                mobile = mobile,
                address = address,
            )
    return render(request, 'delivery/login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        request.session['username'] = username

        try:
            Customer.objects.get(
                username=username,
                password=password
            )

            if username == 'admin':
                return render(request, 'delivery/admin_home.html')
            else:
                restaurantList = Restaurant.objects.all()

                return render(
                    request,
                    'delivery/customer_home.html',
                    {
                        "restaurantList": restaurantList,
                        "username": username,
                        "search": ""
                    }   
                )

        except Customer.DoesNotExist:
            return HttpResponse("Registration Failed")

    return render(request, 'delivery/login.html')
    
    
def logout(request):
    request.session.flush()
    return redirect('index')    
    
def open_customer_home(request, username):

    search = request.GET.get('search', '').strip()

    if search:
        restaurantList = Restaurant.objects.filter(
            name__icontains=search
        )
    else:
        restaurantList = Restaurant.objects.all()

    return render(
        request,
        'delivery/customer_home.html',
        {
            "restaurantList": restaurantList,
            "username": username,
            "search": search
        }
    ) 
def open_add_restaurant(request):
    return render(request, 'delivery/add_restaurant.html')  

def open_admin_home(request):
    return render(request, 'delivery/admin_home.html')

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        location = request.POST.get('location')

        try:
            Restaurant.objects.get(name=name)
            return HttpResponse("Duplicate restaurant!")

        except:
            Restaurant.objects.create(
                name=name,
                picture=picture,
                cuisine=cuisine,
                rating=rating,
                location=location,
            )

    return render(request, 'delivery/admin_home.html')
  
def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html',{"restaurantList" : restaurantList})

def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'delivery/update_restaurant.html', {"restaurant" : restaurant})

def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        location = request.POST.get('location')

        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating
        restaurant.location = location

        restaurant.save()

    restaurantList = Restaurant.objects.all()

    return render(
        request,
        'delivery/show_restaurants.html',
        {"restaurantList": restaurantList}
    )
def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html',{"restaurantList" : restaurantList})

def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'delivery/update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})

def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    return render(request, 'delivery/admin_home.html')

def delete_menu_item(request, item_id, restaurant_id):
    item = Item.objects.get(id=item_id)
    item.delete()

    return redirect('open_update_menu', restaurant_id=restaurant_id)

def view_menu(request, restaurant_id, username):

    restaurant = Restaurant.objects.get(id=restaurant_id)

    search = request.GET.get('search', '').strip()

    if search:
        itemList = restaurant.items.filter(
            name__icontains=search
        )
    else:
        itemList = restaurant.items.all()

    return render(
        request,
        'delivery/customer_menu.html',
        {
            "itemList": itemList,
            "restaurant": restaurant,
            "username": username,
            "search": search
        }
    )
def add_to_cart(request, item_id, username):

    # Get the selected food item
    item = Item.objects.get(id=item_id)

    # Get the customer
    customer = Customer.objects.get(username=username)

    # Get existing cart or create a new cart
    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    # Add the item to the cart
    cart.items.add(item)

    # Send response back to JavaScript
    return HttpResponse("added to cart")

def show_cart(request, username):
    customer = Customer.objects.get(username=username)

    cart = Cart.objects.filter(customer=customer).first()

    items = cart.items.all() if cart else []

    total_price = cart.total_price() if cart else 0

    restaurant_id = items.first().restaurant.id if items else None

    return render(
        request,
        'delivery/cart.html',
        {
            "itemList": items,
            "total_price": total_price,
            "username": username,
            "restaurant_id": restaurant_id
        }
    )
    
# Checkout View
def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)

    # Pass the order details to the frontend
    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })


# Orders Page
def orders(request, username):

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    # Get cart details before clearing
    cart_items = list(cart.items.all()) if cart else []
    total_price = cart.total_price() if cart else 0

    # Clear cart
    if cart:
        cart.items.clear()

    return render(
        request,
        'delivery/orders.html',
        {
            'username': username,
            'customer': customer,
            'cart_items': cart_items,
            'total_price': total_price,
        }
    )