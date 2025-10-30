from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Contact,Ticket,Reply
from django.urls import reverse
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django import forms

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active","date_joined")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password", "username")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions","photo","about")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_active","photo","about")}
        ),
    )
    search_fields = ("email",)
    ordering = ("date_joined","email",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user','subject','message','created_at','is_closed','reply_link']
    list_editable = ['is_closed']

    def reply_link(self,obj):
        if obj.is_closed:
            return format_html('<span style="color: gray;">🔒 تیکت بسته شده</span>')
        url = f'{reverse('admin:accounts_reply_add')}?ticket={obj.id}'
        return format_html('<a class="button" href="{}">➕ افزودن پاسخ</a>',url)
    
    reply_link.short_description = 'افزودن پاسخ'

class ReplyAdminForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        ticket = cleaned_data.get('ticket')

        if ticket.is_closed:
            raise ValidationError("❌ این تیکت بسته شده است و نمی‌توانید پاسخ جدیدی اضافه کنید.")
        
        return cleaned_data

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    form = ReplyAdminForm
    list_display = ['ticket','user','message','date_sent']