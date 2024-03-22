from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header="Healthcare"
admin.site.site_title="Health"
admin.site.index_title="Welcome to Healthcare"

class PatientAdmin(admin.ModelAdmin):
    list_display=('get_user_email','name','age')
    search_fields=('name','user__email')
    list_editable=('name',)

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = 'User Email'
    get_user_email.admin_order_field = 'user__email'


admin.site.register(Patient,PatientAdmin)