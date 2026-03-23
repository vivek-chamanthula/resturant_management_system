from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password
from .forms import CustomerForm, WaiterForm,MenuItemForm,ReservationForm,FeedbackForm,ContactForm
from .models import Customer,Waiter,SubCategory, MenuItem,Reservation
from django.views.decorators.http import require_POST
from datetime import datetime
from django.contrib import messages

# ---------- INDEX PAGE VIEWS ----------
def IndexView(request):
    return render(request,"urban_umami/index.html")



# ---------- NAV BAR VIEWS----------
def AboutView(request):
    return render(request,"urban_umami/nav/about.html")

def MenuView(request):
    return render(request,"urban_umami/nav/menu.html")



# ---------- FOOTER VIEWS ----------

def TermsView(request):
    return render(request,"urban_umami/footer/terms.html")

def PrivacyView(request):
    return render(request,"urban_umami/footer/privacy.html")



# ---------- WAITER & CUSTOMER REGISTRATION----------
def waiter_register(request):
    if request.method == "POST":
        form = WaiterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("waiter_login")
    else:
        form = WaiterForm()
    return render(request, "urban_umami/registration/register_waiter.html", {
        "form": form
    })

def customer_register(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("customer_login")
    else:
        form = CustomerForm()
    return render(request, "urban_umami/registration/register_customer.html", {
        "form": form
    })

# ---------- WAITER & CUSTOMER REGISTRATION DETAILS STORAGE ----------
def waiter_register_info(request):
    waiters = Waiter.objects.all()
    return render(request, "urban_umami/registration/waiter_register_info.html", {
        "waiters": waiters
    })

def customer_register_info(request):
    customers = Customer.objects.all()
    return render(request, "urban_umami/registration/customer_register_info.html", {
        "customers": customers
    })

# ---------- WAITER & CUSTOMER LOGINS ----------
def WaiterLogin(request):
    error = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            waiter = Waiter.objects.get(waiter_email=email, password=password)

            request.session['logged_in'] = True
            request.session['role'] = 'waiter'
            request.session['user_email'] = waiter.waiter_email

            return redirect("index")
        except Waiter.DoesNotExist:
            error = "Invalid Email or Password!"

    return render(request, "urban_umami/registration/waiter_login.html", {
        "error": error
    })

def CustomerLogin(request):
    error = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            customer = Customer.objects.get(customer_email=email, password=password)

            
            request.session['logged_in'] = True
            request.session['role'] = 'customer'
            request.session['user_email'] = customer.customer_email

            return redirect("index")
        except Customer.DoesNotExist:
            error = "Invalid Email or Password!"

    return render(request, "urban_umami/registration/customer_login.html", {
        "error": error
    })

# ---------- LOGOUT VIEWS ----------
def logout_view(request):
    request.session.flush()
    return redirect('index')  

# ---------- MENU PAGE VIEWS ----------

def menu_view(request):
    subcategories = SubCategory.objects.all()
    items_by_slug = {}
    for sc in subcategories:
        items_by_slug[sc.slug] = MenuItem.objects.filter(subcategory=sc)

    return render(request, "urban_umami/nav/menu.html", {
        "subcategories": subcategories,
        "items_by_slug": items_by_slug
    })


@login_required
def add_menu_item(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to access this page")

    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("menu")
    else:
        form = MenuItemForm()

    return render(request, "urban_umami/add_item.html", {"form": form})


# ---------- CART PAGE VIEWS ----------
def add_to_cart(request, item_id):
    if request.session.get('role') == 'customer':
        return HttpResponseForbidden("Customers are not allowed to add items to cart")

    if request.method == "POST":
        item = get_object_or_404(MenuItem, id=item_id)

        cart = request.session.get("cart", {})

        if str(item_id) in cart:
            cart[str(item_id)]["quantity"] += 1
        else:
            cart[str(item_id)] = {
                "name": item.name,
                "price": float(item.price),
                "image": item.image.url if item.image else "",
                "quantity": 1,
            }

        request.session["cart"] = cart

        return JsonResponse({
            "success": True,
            "cart_count": sum(i["quantity"] for i in cart.values())
        })
    return redirect("menu")
    
def cart_view(request):
    if request.session.get('role') == 'customer':
        return HttpResponseForbidden("Customers are not allowed to access cart")

    cart = request.session.get("cart", {})
    total = sum(item["price"] * item["quantity"] for item in cart.values())

    return render(request, "urban_umami/card.html", {
        "cart": cart,
        "total": total
    })

def update_qty(request, item_id, action):
    cart = request.session.get("cart", {})

    if str(item_id) in cart:
        if action == "inc":
            cart[str(item_id)]["quantity"] += 1
        elif action == "dec":
            if cart[str(item_id)]["quantity"] > 1:
                cart[str(item_id)]["quantity"] -= 1
            else:
                del cart[str(item_id)]

    request.session["cart"] = cart
    return JsonResponse({"success": True})


# ---------- ORDER PAGE VIEWS ----------

def order_view(request):
    if request.session.get('role') == 'customer':
        return HttpResponseForbidden("Customers are not allowed to place orders")

    cart = request.session.get("cart", {})
    order_items = []

    for item in cart.values():
        for _ in range(item["quantity"]):
            order_items.append({
                "image":item['image'],
                "name": item["name"],
                "price": item["price"]
            })

    request.session["cart"] = {}

    return render(request, "urban_umami/nav/orders.html", {
        "order_items": order_items
    })



# ---------- BILL GENARATATION ----------
def generate_bill(request):
    if request.method == "POST":

        bill_data = {
            "customer": request.POST.get("customer"),
            "phone": request.POST.get("phone"),
            "table": request.POST.get("table"),
            "date": request.POST.get("date"),
            "time": request.POST.get("time"),
            "items": request.POST.get("items"),
            "total": request.POST.get("total"),
        }
        generated_bills = request.session.get("generated_bills", [])
        generated_bills.append(bill_data)
        request.session["generated_bills"] = generated_bills
        order_list = request.session.get("order_list", [])
        order_list.append(bill_data)
        request.session["order_list"] = order_list
        return redirect("generated_bill")

    return redirect("order")


# ---------- BILL STORING DETAILS ----------
def generated_bill_view(request):
    bills = request.session.get("generated_bills", [])
    return render(request, "urban_umami/generatedbill.html", {
        "bills": bills
    })


# ---------- ORDER STORING DETAILS ----------
def order_list_view(request):
    order_list = request.session.get("order_list", [])
    return render(request, "urban_umami/orderdetail.html", {
        "order_list": order_list
    })



# ---------- RESERVATION DETAILS ----------
def reserve(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid():
            res_date = form.cleaned_data['res_date']
            res_time = form.cleaned_data['res_time']
            count = Reservation.objects.filter(
                res_date=res_date,
                res_time=res_time
            ).count()

            if count >= 12:
                messages.error(
                    request,
                    "All tables are booked. Please wait or choose another date/time."
                )
            else:
                form.save()
                messages.success(request, "Reservation added successfully!")
                return redirect('reserve')
    else:
        form = ReservationForm()

    reservations = Reservation.objects.all().order_by('-res_date')

    return render(request, 'urban_umami/nav/reserve.html', {
        'form': form,
        'reservations': reservations
    })


# ---------- RESERVATION UPDATE ----------
def update_reservation(request, id):
    if request.session.get('role') == 'customer':
        return HttpResponseForbidden("Customers are not allowed to update reservations")
    reservation = get_object_or_404(Reservation, res_id=id)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)

        if form.is_valid():
            res_date = form.cleaned_data['res_date']
            res_time = form.cleaned_data['res_time']

            count = Reservation.objects.filter(
                res_date=res_date,
                res_time=res_time
            ).exclude(res_id=id).count()

            if count >= 12:
                messages.error(
                    request,
                    "All tables are booked for this time. Choose another slot."
                )
            else:
                form.save()
                messages.success(request, "Reservation updated successfully!")
                return redirect('reserve')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'urban_umami/reserve_update.html', {'form': form})


# ----------  RESERVATION DELETE ----------
def delete_reservation(request, id):
    if request.session.get('role') == 'customer':
        return HttpResponseForbidden("Customers are not allowed to update reservations")
    reservation = get_object_or_404(Reservation, res_id=id)
    reservation.delete()
    messages.success(request, "Reservation deleted successfully!")
    return redirect('reserve')

# ----------  FEED BACK VIEW ----------
def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your valuable feedback!")
            return redirect('feedback')
        else:
            messages.error(request, "Please fill all required fields correctly.")
    else:
        form = FeedbackForm()

    return render(request, "urban_umami/footer/feedback.html", {"form": form})

# ----------  CONTACT VIEW ----------
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please fill the form correctly.")
    else:
        form = ContactForm()

    return render(request, "urban_umami/footer/contact.html", {'form': form})




