from django.db import models

# ---------- CUSTOMER REGISTRATION MODELS ----------
class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(unique=True)
    customer_number = models.CharField(max_length=15)
    password =  models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

# ---------- WAITER REGISTRATION MODELS ----------
class Waiter(models.Model):
    waiter_id = models.AutoField(primary_key=True)
    waiter_name = models.CharField(max_length=100)
    waiter_number = models.CharField(max_length=15)
    waiter_email = models.EmailField(unique=True)
    waiter_shift = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning Shift'),
            ('evening', 'Evening Shift'),
            ('night', 'Night Shift'),
        ]
    )
    password = models.CharField(max_length=255)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.waiter_name
    
    # ---------- MENU ITEMS UPLOAD MODELS ----------
class SubCategory(models.Model):
    name = models.CharField(max_length=120) 
    slug = models.SlugField(unique=True)      
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

def upload_to_menu(instance, filename):
    return f"menu_items/{instance.subcategory.slug}/{filename}"

class MenuItem(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to=upload_to_menu, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.subcategory.slug})"
    

   # ---------- TABLE RESERVATION  MODELS ----------
class Reservation(models.Model):
    res_id = models.AutoField(primary_key=True)
    cus_name = models.CharField(max_length=100)
    cus_email = models.EmailField()
    res_date = models.DateField()
    res_time = models.TimeField()
    num_people = models.PositiveIntegerField()
    
    def __str__(self):
        return self.cus_name



   # ---------- FEEDBACK MODELS ----------

RATING_CHOICES = [
    (5, "★★★★★ Excellent"),
    (4, "★★★★ Very Good"),
    (3, "★★★ Good"),
    (2, "★★ Average"),
    (1, "★ Poor"),
]

class Feedback(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    order = models.CharField(max_length=255, blank=True)
    food_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    service_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    ambience_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.date()}"


    # ---------- CONTACT MODELS ----------

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
