from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserModelAdmin(UserAdmin):
    model=User
    list_display=["id","email","name","city","is_active","is_staff","is_superuser","is_recruiter","is_applicant"]
    list_filter=["is_superuser"]
    fieldsets=[
       ( "User Credentials",{"fields":["email","password"] }),
       ( "Personal Information",{"fields":["name","city"] }),
       ( "Permissions",{"fields":["is_active","is_staff","is_applicant","is_recruiter"] }),

    ]

    add_fieldsets=[
        (
            None,
            {
                "classes":["wide"],
                "fields":["email","password1","password2"],
            },
        ),
    ]
    search_fields=["email"]
    ordering=["email","id"]
    filter_horizontal=[]

admin.site.register(User,UserModelAdmin)