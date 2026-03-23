"""
URL configuration for resturant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from urban_umami import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout'),


    # --- INDEX URL -----
    path('',views.IndexView, name="index"),


    # --- NAV BAR URL -----
    path('about/',views.AboutView, name="about"),
    path('menu/', views.menu_view, name='menu'),
    path("order/", views.order_view, name="order"),
    path('reserve/', views.reserve, name='reserve'),


    # --- FOOTER URL -----
    path('contact/',views.contact, name='contact'),
    path('terms/',views.TermsView, name="terms"),
    path('privacy/',views.PrivacyView, name="privacy"),
    path('feedback/',views.feedback_view, name='feedback'),



    # --- REGISTRATION AND LOGINS URL -----
    path("customer/register/", views.customer_register, name="customer_register"),
    path("waiter/register/", views.waiter_register, name="waiter_register"),
    path("customer/login/", views.CustomerLogin, name="customer_login"),
    path("waiter/login/", views.WaiterLogin, name="waiter_login"),
    path("customer-info/",views.customer_register_info, name="customer_info"),
    path("waiter-info/",views.waiter_register_info, name="waiter_info"),


    # --- ADD CART URLS-----
    path('add-item/', views.add_menu_item, name='add_item'),
    path("add-to-cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("update-qty/<int:item_id>/<str:action>/", views.update_qty, name="update_qty"),


    # --- ORDER URLS-----
    path("generate-bill/", views.generate_bill, name="generate_bill"),
    path("generated-bill/", views.generated_bill_view, name="generated_bill"),
    path("order-detail/", views.order_list_view, name="orderdetail"),


    # --- RESERVATION URLS-----
    path('update/<int:id>/', views.update_reservation, name='update_reservation'),
    path('delete/<int:id>/', views.delete_reservation, name='delete_reservation'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
