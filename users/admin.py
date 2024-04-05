from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import MyUser, Profile, MatricNumber



class CustomAdmin(UserAdmin):
    model = MyUser
    
    search_fields = ('email', 'first_name', 'other_name', 'last_name')
    list_filter = ('email', 'first_name', 'other_name', 'username', 'last_name', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'first_name', 'other_name', 'last_name', 'username', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'other_name', 'username', 'last_name')}),
        ('permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),
        ('personal', {'fields': ()}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'other_name', 'last_name', 'username', 'is_active', 'is_staff', 'is_admin', 'password1', 'password2')},
        ),
    )



    
    

admin.site.register(Profile)
admin.site.register(MatricNumber)
admin.site.register(MyUser, CustomAdmin)