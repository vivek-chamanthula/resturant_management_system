from django import forms

from .models import Customer,Waiter,MenuItem, SubCategory,Reservation,Feedback,Contact
     
# ---------- CUSTOMER FORM----------
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'customer-control', 'placeholder': 'Enter your Name'}),
            'customer_email': forms.EmailInput(attrs={'class': 'customer-control', 'placeholder': 'Enter your Email'}),
            'customer_number': forms.TextInput(attrs={'class': 'customer-control', 'placeholder': 'Enter your phone number'}),
            'password': forms.PasswordInput(attrs={'class': 'customer-control', 'placeholder': 'Create your password'}),
        }


# ---------- WAITER FORM----------
class WaiterForm(forms.ModelForm):
    class Meta :
        model = Waiter   
        fields = "__all__" 

        widgets = {
            'waiter_name': forms.TextInput(attrs={'class': 'waiter-control', 'placeholder': 'Enter your Name'}),
            'waiter_number': forms.TextInput(attrs={'class': 'waiter-control', 'placeholder': 'Enter Phone number'}),
            'waiter_email': forms.EmailInput(attrs={'class': 'waiter-control', 'placeholder': 'Enter your Email'}),
            'password': forms.PasswordInput(attrs={'class': 'waiter-control','placeholder':'Enter your password'}),
        }


# ---------- MENU UPLOADING FORM----------
class MenuItemForm(forms.ModelForm):
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.order_by('id'),
        empty_label="(e.g. appetizers)",
        label="Choose Tab"
    )

    class Meta:
        model = MenuItem
        fields = ['subcategory', 'name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Item name',
                'class': 'input'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Item description',
                'class': 'textarea'
            }),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Price',
                'class': 'input'
            }),
        }

# ---------- RESERVATION FORM----------
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        
        widgets = {
             'cus_name': forms.TextInput(
                attrs={'class': 'reserve_content', 'placeholder': 'Customer Name'}
            ),
            'cus_email': forms.EmailInput(
                attrs={'class': 'reserve_content', 'placeholder': 'Email'}
            ),
            'res_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'reserve_content'}
            ),
            'res_time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'reserve_content'}
            ),
            'num_people': forms.NumberInput(
                attrs={'class': 'reserve_content', 'min': 1}
            ),
        }

# ---------- FEED BACK FORM----------

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"

# ---------- CONTACT FORM----------

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"