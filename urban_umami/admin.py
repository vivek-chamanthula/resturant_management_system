from django.contrib import admin
from .models import MenuItem,Feedback,Contact

admin.site.register(MenuItem)
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'food_rating',
        'service_rating',
        'ambience_rating',
        'created_at',
    )
    search_fields = ('name', 'email')
    list_filter = ('food_rating', 'service_rating', 'ambience_rating')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
